#!/usr/bin/env python3
"""Benchmark LPG-TD for Practice 1 Part 3 (temporal planning).

Features:
- Sweep drones=1..10 with carriers=drones.
- For each configuration, find max size solved in <= timeout using quality mode.
- Re-run that max-size case in speed mode.
- Export CSV + TXT + MD + PNG diagrams under results/.
"""

from __future__ import annotations

import argparse
import csv
import datetime as dt
import re
import shlex
import subprocess
import sys
import time
from dataclasses import dataclass
from pathlib import Path

try:
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    HAVE_MATPLOTLIB = True
except Exception:
    HAVE_MATPLOTLIB = False


SIZE_RE = re.compile(r"_l([0-9]+)_")
PLAN_LINE_RE = re.compile(r"^\s*([0-9]+(?:\.[0-9]+)?):\s*\(.+\)\s*\[([0-9]+(?:\.[0-9]+)?)\]", re.IGNORECASE)
SOLVED_RE = re.compile(r"(solution found|plan found|search successful|found plan)", re.IGNORECASE)
UNSOLVED_RE = re.compile(r"(unsolvable|no solution|search failed|can not find|cannot find)", re.IGNORECASE)
UNSUPPORTED_RE = re.compile(
    r"(command not found|no such file or directory|invalid option|unknown option|module not found)",
    re.IGNORECASE,
)

PROCESSING_PATTERNS = [
    re.compile(r"total\s+time\s*[:=]\s*([0-9]+(?:\.[0-9]+)?)", re.IGNORECASE),
    re.compile(r"cpu\s*time\s*[:=]\s*([0-9]+(?:\.[0-9]+)?)", re.IGNORECASE),
    re.compile(r"processing\s*time\s*[:=]\s*([0-9]+(?:\.[0-9]+)?)", re.IGNORECASE),
    re.compile(r"time\s*[:=]\s*([0-9]+(?:\.[0-9]+)?)\s*(?:s|sec|seconds)", re.IGNORECASE),
]


@dataclass
class QualityRow:
    drones: int
    carriers: int
    size: int
    status: str
    processing_time_s: float | None
    plan_steps: int | None
    makespan: float | None
    wall_time_s: float
    problem_file: str
    mode: str
    error_excerpt: str


@dataclass
class ComparisonRow:
    drones: int
    carriers: int
    max_quality_size: int | None
    quality_status: str
    quality_processing_time_s: float | None
    quality_plan_steps: int | None
    quality_makespan: float | None
    speed_status: str
    speed_processing_time_s: float | None
    speed_plan_steps: int | None
    speed_makespan: float | None
    delta_processing_time_s: float | None
    delta_plan_steps: int | None
    delta_makespan: float | None
    problem_file: str


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Benchmark LPG-TD for Part 3 (quality vs speed)")

    parser.add_argument("--min-drones", type=int, default=1, help="minimum drones")
    parser.add_argument("--max-drones", type=int, default=10, help="maximum drones")

    parser.add_argument("--min-size", type=int, default=2, help="minimum size for l=p=c=g")
    parser.add_argument("--max-size", type=int, default=30, help="maximum size for l=p=c=g")
    parser.add_argument("--step", type=int, default=1, help="size step")

    parser.add_argument("--timeout", type=int, default=60, help="timeout per run in seconds")
    parser.add_argument("--stop-after-fails", type=int, default=2, help="stop quality sweep after N consecutive non-solved")

    parser.add_argument("--domain", default="dronedomain.pddl", help="temporal domain path")
    parser.add_argument("--generator", default="generate-problem.py", help="problem generator script path")
    parser.add_argument("--results-dir", default="results", help="output folder")

    parser.add_argument("--carrier-capacity", type=int, default=4, help="carrier capacity")
    parser.add_argument("--seed", type=int, default=None, help="optional generator seed (used only if generator supports --seed)")
    parser.add_argument("--lpg-seed", type=int, default=None, help="optional LPG seed")

    if len(sys.argv) > 1:
        return parser.parse_args()

    print("No se han recibido parámetros por línea de comandos.")
    print("Modo interactivo: escribe argumentos como en CLI o pulsa Enter para usar valores por defecto.")
    try:
        raw_args = input("¿Qué parámetros quieres meter? ").strip()
    except EOFError:
        raw_args = ""

    if not raw_args:
        return parser.parse_args([])
    return parser.parse_args(shlex.split(raw_args))


def make_sizes(min_size: int, max_size: int, step: int) -> list[int]:
    if min_size < 1:
        raise ValueError("--min-size must be >= 1")
    if max_size < min_size:
        raise ValueError("--max-size must be >= --min-size")
    if step < 1:
        raise ValueError("--step must be >= 1")
    return list(range(min_size, max_size + 1, step))


def make_drones(min_drones: int, max_drones: int) -> list[int]:
    if min_drones < 1:
        raise ValueError("--min-drones must be >= 1")
    if max_drones < min_drones:
        raise ValueError("--max-drones must be >= --min-drones")
    return list(range(min_drones, max_drones + 1))


def problem_file_name(drones: int, carriers: int, size: int, capacity: int) -> str:
    return f"drone_problem_d{drones}_r{carriers}_l{size}_p{size}_c{size}_g{size}_a{capacity}.pddl"


def extract_size(path: Path, fallback: int) -> int:
    match = SIZE_RE.search(path.name)
    if match:
        return int(match.group(1))
    return fallback


def run_command(cmd: list[str], cwd: Path | None = None, timeout_s: int | None = None) -> tuple[int, str, bool, float]:
    start = time.perf_counter()
    try:
        proc = subprocess.run(
            cmd,
            cwd=None if cwd is None else str(cwd),
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            timeout=timeout_s,
            check=False,
        )
        wall = time.perf_counter() - start
        return proc.returncode, proc.stdout, False, wall
    except subprocess.TimeoutExpired as exc:
        out = exc.stdout or ""
        if isinstance(out, bytes):
            out = out.decode(errors="replace")
        wall = time.perf_counter() - start
        return 124, out, True, wall
    except FileNotFoundError as exc:
        wall = time.perf_counter() - start
        return 127, str(exc), False, wall


def make_error_excerpt(text: str, max_lines: int = 6) -> str:
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    if not lines:
        return ""
    return " | ".join(lines[:max_lines])[:500]


def generator_supports_seed(generator_path: Path) -> bool:
    code, out, _, _ = run_command([sys.executable, str(generator_path), "--help"], cwd=generator_path.parent, timeout_s=10)
    if code != 0 and not out:
        return False
    return "--seed" in out or "-s" in out


def generate_problem(
    generator_path: Path,
    output_dir: Path,
    drones: int,
    carriers: int,
    size: int,
    capacity: int,
    seed: int | None,
    supports_seed: bool,
    timeout_s: int,
) -> tuple[bool, Path, float, str]:
    output_path = output_dir / problem_file_name(drones=drones, carriers=carriers, size=size, capacity=capacity)
    cmd = [
        sys.executable,
        str(generator_path),
        "-d",
        str(drones),
        "-r",
        str(carriers),
        "-l",
        str(size),
        "-p",
        str(size),
        "-c",
        str(size),
        "-g",
        str(size),
        "-a",
        str(capacity),
    ]

    if seed is not None and supports_seed:
        cmd.extend(["--seed", str(seed)])

    code, out, timed_out, wall = run_command(cmd, cwd=output_dir, timeout_s=timeout_s)
    ok = (not timed_out) and code == 0 and output_path.exists()
    return ok, output_path, wall, out


def parse_processing_time(output: str, wall_time: float) -> float:
    for pattern in PROCESSING_PATTERNS:
        all_matches = pattern.findall(output)
        if all_matches:
            try:
                return float(all_matches[-1])
            except ValueError:
                continue
    return wall_time


def parse_plan_from_text(text: str) -> tuple[int | None, float | None]:
    matches = PLAN_LINE_RE.findall(text)
    if not matches:
        return None, None
    steps = len(matches)
    end_times: list[float] = []
    for start_s, dur_s in matches:
        start = float(start_s)
        dur = float(dur_s)
        end_times.append(start + dur)
    return steps, (max(end_times) if end_times else None)


def parse_plan_from_file(path: Path) -> tuple[int | None, float | None]:
    if not path.exists():
        return None, None
    try:
        content = path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return None, None
    return parse_plan_from_text(content)


def infer_status(code: int, output: str, timed_out: bool, steps: int | None) -> str:
    if timed_out:
        return "timeout"
    if code == 127:
        return "unsupported"
    if UNSUPPORTED_RE.search(output):
        return "unsupported"
    if steps is not None:
        return "solved"
    if SOLVED_RE.search(output) and code == 0:
        return "solved"
    if UNSOLVED_RE.search(output):
        return "unsolved"
    if code == 0:
        return "unsolved"
    return "error"


def lpg_attempts(domain_file: Path, problem_file: Path, mode: str, timeout_s: int, out_plan: Path, lpg_seed: int | None) -> list[list[str]]:
    base = ["-o", str(domain_file), "-f", str(problem_file), f"-{mode}", "-cputime", str(timeout_s), "-out", str(out_plan)]
    if lpg_seed is not None:
        base += ["-seed", str(lpg_seed)]
    return [
        ["planutils", "run", "lpg-td", "--", *base],
        ["lpg-td", *base],
        ["lpg", *base],
    ]


def run_lpg(
    domain_file: Path,
    problem_file: Path,
    mode: str,
    timeout_s: int,
    plans_dir: Path,
    lpg_seed: int | None,
) -> QualityRow:
    size = extract_size(problem_file, -1)
    out_plan = plans_dir / f"lpgtd_{mode}_{problem_file.stem}.SOL"
    if out_plan.exists():
        out_plan.unlink()

    last_row: QualityRow | None = None

    for cmd in lpg_attempts(domain_file, problem_file, mode=mode, timeout_s=timeout_s, out_plan=out_plan, lpg_seed=lpg_seed):
        code, out, timed_out, wall = run_command(cmd, cwd=plans_dir, timeout_s=timeout_s + 5)

        steps_f, makespan_f = parse_plan_from_file(out_plan)
        steps_o, makespan_o = parse_plan_from_text(out)
        steps = steps_f if steps_f is not None else steps_o
        makespan = makespan_f if makespan_f is not None else makespan_o

        status = infer_status(code, out, timed_out, steps)
        processing_time = parse_processing_time(out, wall)
        row = QualityRow(
            drones=-1,
            carriers=-1,
            size=size,
            status=status,
            processing_time_s=processing_time,
            plan_steps=steps,
            makespan=makespan,
            wall_time_s=wall,
            problem_file=str(problem_file),
            mode=mode,
            error_excerpt="" if status in {"solved", "unsolved", "timeout"} else make_error_excerpt(out),
        )
        last_row = row

        if status in {"solved", "timeout", "unsolved", "unsupported"}:
            return row

        # Try next backend only if launcher is missing.
        launcher_missing = code == 127 or "No such file or directory" in out or "command not found" in out
        if not launcher_missing:
            return row

    if last_row is not None:
        return last_row

    return QualityRow(
        drones=-1,
        carriers=-1,
        size=size,
        status="unsupported",
        processing_time_s=None,
        plan_steps=None,
        makespan=None,
        wall_time_s=0.0,
        problem_file=str(problem_file),
        mode=mode,
        error_excerpt="lpg-td backend not available",
    )


def run_sweep_for_drones(
    drones: int,
    sizes: list[int],
    domain_file: Path,
    generator_file: Path,
    problems_dir: Path,
    plans_dir: Path,
    timeout_s: int,
    stop_after_fails: int,
    capacity: int,
    seed: int | None,
    supports_seed: bool,
    lpg_seed: int | None,
) -> tuple[list[QualityRow], ComparisonRow]:
    carriers = drones
    quality_rows: list[QualityRow] = []
    consecutive_fails = 0
    best_quality: QualityRow | None = None

    planner_unavailable = False

    for size in sizes:
        ok, problem_file, _, gen_out = generate_problem(
            generator_path=generator_file,
            output_dir=problems_dir,
            drones=drones,
            carriers=carriers,
            size=size,
            capacity=capacity,
            seed=seed,
            supports_seed=supports_seed,
            timeout_s=timeout_s,
        )
        if not ok:
            row = QualityRow(
                drones=drones,
                carriers=carriers,
                size=size,
                status="error",
                processing_time_s=None,
                plan_steps=None,
                makespan=None,
                wall_time_s=0.0,
                problem_file=str(problem_file),
                mode="quality",
                error_excerpt=f"generation failed: {make_error_excerpt(gen_out)}",
            )
            quality_rows.append(row)
            consecutive_fails += 1
            print(f"[d={drones} size={size} quality] generation error")
            if consecutive_fails >= stop_after_fails:
                break
            continue

        run = run_lpg(
            domain_file=domain_file,
            problem_file=problem_file,
            mode="quality",
            timeout_s=timeout_s,
            plans_dir=plans_dir,
            lpg_seed=lpg_seed,
        )
        run.drones = drones
        run.carriers = carriers
        quality_rows.append(run)

        pt = "-" if run.processing_time_s is None else f"{run.processing_time_s:.2f}"
        ms = "-" if run.makespan is None else f"{run.makespan:.2f}"
        print(f"[d={drones} size={size} quality] status={run.status} t={pt}s steps={run.plan_steps or '-'} makespan={ms}")

        if run.status == "unsupported":
            planner_unavailable = True
            break

        if run.status == "solved":
            best_quality = run
            consecutive_fails = 0
        else:
            consecutive_fails += 1
            if consecutive_fails >= stop_after_fails:
                break

    if best_quality is None:
        speed_status = "unsupported" if planner_unavailable else "skipped"
        comp = ComparisonRow(
            drones=drones,
            carriers=carriers,
            max_quality_size=None,
            quality_status="not_found",
            quality_processing_time_s=None,
            quality_plan_steps=None,
            quality_makespan=None,
            speed_status=speed_status,
            speed_processing_time_s=None,
            speed_plan_steps=None,
            speed_makespan=None,
            delta_processing_time_s=None,
            delta_plan_steps=None,
            delta_makespan=None,
            problem_file="",
        )
        return quality_rows, comp

    speed_run = run_lpg(
        domain_file=domain_file,
        problem_file=Path(best_quality.problem_file),
        mode="speed",
        timeout_s=timeout_s,
        plans_dir=plans_dir,
        lpg_seed=lpg_seed,
    )
    speed_run.drones = drones
    speed_run.carriers = carriers

    pt = "-" if speed_run.processing_time_s is None else f"{speed_run.processing_time_s:.2f}"
    ms = "-" if speed_run.makespan is None else f"{speed_run.makespan:.2f}"
    print(f"[d={drones} size={best_quality.size} speed] status={speed_run.status} t={pt}s steps={speed_run.plan_steps or '-'} makespan={ms}")

    delta_time = None
    if best_quality.processing_time_s is not None and speed_run.processing_time_s is not None:
        delta_time = best_quality.processing_time_s - speed_run.processing_time_s

    delta_steps = None
    if best_quality.plan_steps is not None and speed_run.plan_steps is not None:
        delta_steps = best_quality.plan_steps - speed_run.plan_steps

    delta_makespan = None
    if best_quality.makespan is not None and speed_run.makespan is not None:
        delta_makespan = best_quality.makespan - speed_run.makespan

    comp = ComparisonRow(
        drones=drones,
        carriers=carriers,
        max_quality_size=best_quality.size,
        quality_status=best_quality.status,
        quality_processing_time_s=best_quality.processing_time_s,
        quality_plan_steps=best_quality.plan_steps,
        quality_makespan=best_quality.makespan,
        speed_status=speed_run.status,
        speed_processing_time_s=speed_run.processing_time_s,
        speed_plan_steps=speed_run.plan_steps,
        speed_makespan=speed_run.makespan,
        delta_processing_time_s=delta_time,
        delta_plan_steps=delta_steps,
        delta_makespan=delta_makespan,
        problem_file=best_quality.problem_file,
    )
    return quality_rows, comp


def quality_row_values(row: QualityRow) -> list[str]:
    return [
        str(row.drones),
        str(row.carriers),
        row.mode,
        str(row.size),
        row.status,
        "" if row.processing_time_s is None else f"{row.processing_time_s:.4f}",
        "" if row.plan_steps is None else str(row.plan_steps),
        "" if row.makespan is None else f"{row.makespan:.4f}",
        f"{row.wall_time_s:.4f}",
        row.problem_file,
        row.error_excerpt,
    ]


def comparison_row_values(row: ComparisonRow) -> list[str]:
    return [
        str(row.drones),
        str(row.carriers),
        "" if row.max_quality_size is None else str(row.max_quality_size),
        row.quality_status,
        "" if row.quality_processing_time_s is None else f"{row.quality_processing_time_s:.4f}",
        "" if row.quality_plan_steps is None else str(row.quality_plan_steps),
        "" if row.quality_makespan is None else f"{row.quality_makespan:.4f}",
        row.speed_status,
        "" if row.speed_processing_time_s is None else f"{row.speed_processing_time_s:.4f}",
        "" if row.speed_plan_steps is None else str(row.speed_plan_steps),
        "" if row.speed_makespan is None else f"{row.speed_makespan:.4f}",
        "" if row.delta_processing_time_s is None else f"{row.delta_processing_time_s:.4f}",
        "" if row.delta_plan_steps is None else str(row.delta_plan_steps),
        "" if row.delta_makespan is None else f"{row.delta_makespan:.4f}",
        row.problem_file,
    ]


def write_csv_table(path: Path, headers: list[str], rows: list[list[str]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.writer(fh)
        writer.writerow(headers)
        writer.writerows(rows)


def markdown_escape(value: str) -> str:
    return value.replace("|", r"\|").replace("\n", "<br>").replace("\r", "")


def add_table_md(lines: list[str], title: str, headers: list[str], rows: list[list[str]]) -> None:
    lines.append(f"## {title}")
    lines.append("")
    lines.append("| " + " | ".join(markdown_escape(h) for h in headers) + " |")
    lines.append("| " + " | ".join("---" for _ in headers) + " |")
    for row in rows:
        normalized = row[: len(headers)] + [""] * max(0, len(headers) - len(row))
        lines.append("| " + " | ".join(markdown_escape(v) for v in normalized) + " |")
    lines.append("")


def add_table_txt(lines: list[str], title: str, headers: list[str], rows: list[list[str]]) -> None:
    lines.append(title)
    lines.append("\t".join(headers))
    for row in rows:
        lines.append("\t".join(row))
    lines.append("")


def write_reports(
    txt_path: Path,
    md_path: Path,
    args: argparse.Namespace,
    quality_rows: list[QualityRow],
    comparison_rows: list[ComparisonRow],
    images: list[Path],
) -> None:
    q_headers = [
        "drones",
        "carriers",
        "mode",
        "size",
        "status",
        "processing_time_s",
        "plan_steps",
        "makespan",
        "wall_time_s",
        "problem_file",
        "error_excerpt",
    ]
    c_headers = [
        "drones",
        "carriers",
        "max_quality_size",
        "quality_status",
        "quality_processing_time_s",
        "quality_plan_steps",
        "quality_makespan",
        "speed_status",
        "speed_processing_time_s",
        "speed_plan_steps",
        "speed_makespan",
        "delta_processing_time_s",
        "delta_plan_steps",
        "delta_makespan",
        "problem_file",
    ]

    q_rows = [quality_row_values(r) for r in quality_rows]
    c_rows = [comparison_row_values(r) for r in comparison_rows]

    txt_lines: list[str] = []
    txt_lines.append("Benchmark LPG-TD - Practice 1 Part 3")
    txt_lines.append(f"Generated at: {dt.datetime.now().isoformat(timespec='seconds')}")
    txt_lines.append(f"Args: {vars(args)}")
    txt_lines.append("")
    add_table_txt(txt_lines, "[QUALITY_SWEEP]", q_headers, q_rows)
    add_table_txt(txt_lines, "[QUALITY_VS_SPEED]", c_headers, c_rows)
    txt_path.write_text("\n".join(txt_lines), encoding="utf-8")

    md_lines: list[str] = []
    md_lines.append("# Benchmark LPG-TD - Practice 1 Part 3")
    md_lines.append("")
    md_lines.append(f"- Generated at: `{dt.datetime.now().isoformat(timespec='seconds')}`")
    md_lines.append(f"- Args: `{vars(args)}`")
    md_lines.append("")
    add_table_md(md_lines, "Tabla por número de drones/carriers (quality vs speed)", c_headers, c_rows)
    add_table_md(md_lines, "Barrido quality por configuración", q_headers, q_rows)

    md_lines.append("## Diagramas")
    md_lines.append("")
    for image in images:
        md_lines.append(f"![{image.stem}]({image.name})")
        md_lines.append("")

    md_path.write_text("\n".join(md_lines), encoding="utf-8")


def as_float(value: float | None) -> float | None:
    return value if value is not None else None


def make_plots(results_dir: Path, comparison_rows: list[ComparisonRow]) -> list[Path]:
    if not HAVE_MATPLOTLIB:
        raise RuntimeError(
            "matplotlib is required to generate diagram images. Install it with `pip install matplotlib`."
        )

    img1 = results_dir / "part3_max_quality_size_by_drones.png"
    img2 = results_dir / "part3_quality_vs_speed_processing_time.png"
    img3 = results_dir / "part3_quality_vs_speed_plan_steps.png"
    img4 = results_dir / "part3_quality_vs_speed_makespan.png"

    rows = sorted(comparison_rows, key=lambda r: r.drones)
    drones = [r.drones for r in rows]

    max_sizes = [0 if r.max_quality_size is None else r.max_quality_size for r in rows]

    plt.figure(figsize=(10, 5.5))
    plt.plot(drones, max_sizes, marker="o", color="#1f77b4", label="max size solved (quality)")
    plt.title("Parte 3 - Tamaño máximo resuelto por nº drones/carriers")
    plt.xlabel("Drones (carriers=drones)")
    plt.ylabel("Max size (l=p=c=g)")
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.tight_layout()
    plt.savefig(img1, dpi=140)
    plt.close()

    q_t = [as_float(r.quality_processing_time_s) for r in rows]
    s_t = [as_float(r.speed_processing_time_s) for r in rows]
    q_steps = [r.quality_plan_steps for r in rows]
    s_steps = [r.speed_plan_steps for r in rows]
    q_m = [as_float(r.quality_makespan) for r in rows]
    s_m = [as_float(r.speed_makespan) for r in rows]

    def grouped_bar(image_path: Path, y1: list[float | int | None], y2: list[float | int | None], title: str, ylabel: str) -> None:
        x = list(range(len(drones)))
        width = 0.38

        def normalize(values: list[float | int | None]) -> list[float]:
            return [float(v) if v is not None else 0.0 for v in values]

        y1n = normalize(y1)
        y2n = normalize(y2)

        fig, ax = plt.subplots(figsize=(11, 5.5))
        x_left = [i - width / 2 for i in x]
        x_right = [i + width / 2 for i in x]
        b1 = ax.bar(x_left, y1n, width, label="quality", color="#1f77b4")
        b2 = ax.bar(x_right, y2n, width, label="speed", color="#ff7f0e")

        missing1 = [v is None for v in y1]
        missing2 = [v is None for v in y2]
        for bar, miss in zip(b1, missing1):
            if miss:
                bar.set_hatch("//")
                bar.set_alpha(0.4)
        for bar, miss in zip(b2, missing2):
            if miss:
                bar.set_hatch("//")
                bar.set_alpha(0.4)

        ax.set_title(title)
        ax.set_xlabel("Drones (carriers=drones)")
        ax.set_ylabel(ylabel)
        ax.set_xticks(x)
        ax.set_xticklabels([str(d) for d in drones])
        ax.grid(True, axis="y", alpha=0.3)
        ax.legend()
        fig.tight_layout()
        fig.savefig(image_path, dpi=140)
        plt.close(fig)

    grouped_bar(img2, q_t, s_t, "Parte 3 - Quality vs Speed: processing time", "Processing time (s)")
    grouped_bar(img3, q_steps, s_steps, "Parte 3 - Quality vs Speed: plan steps", "Plan steps")
    grouped_bar(img4, q_m, s_m, "Parte 3 - Quality vs Speed: makespan", "Makespan")

    return [img1, img2, img3, img4]


def write_summary_csv(path: Path, comparison_rows: list[ComparisonRow]) -> None:
    headers = [
        "drones",
        "carriers",
        "max_quality_size",
        "quality_processing_time_s",
        "quality_plan_steps",
        "quality_makespan",
        "speed_processing_time_s",
        "speed_plan_steps",
        "speed_makespan",
        "delta_processing_time_s",
        "delta_plan_steps",
        "delta_makespan",
        "quality_status",
        "speed_status",
    ]
    rows = [
        [
            str(r.drones),
            str(r.carriers),
            "" if r.max_quality_size is None else str(r.max_quality_size),
            "" if r.quality_processing_time_s is None else f"{r.quality_processing_time_s:.4f}",
            "" if r.quality_plan_steps is None else str(r.quality_plan_steps),
            "" if r.quality_makespan is None else f"{r.quality_makespan:.4f}",
            "" if r.speed_processing_time_s is None else f"{r.speed_processing_time_s:.4f}",
            "" if r.speed_plan_steps is None else str(r.speed_plan_steps),
            "" if r.speed_makespan is None else f"{r.speed_makespan:.4f}",
            "" if r.delta_processing_time_s is None else f"{r.delta_processing_time_s:.4f}",
            "" if r.delta_plan_steps is None else str(r.delta_plan_steps),
            "" if r.delta_makespan is None else f"{r.delta_makespan:.4f}",
            r.quality_status,
            r.speed_status,
        ]
        for r in comparison_rows
    ]
    write_csv_table(path, headers, rows)


def main() -> None:
    args = parse_args()

    domain_file = Path(args.domain).resolve()
    generator_file = Path(args.generator).resolve()
    results_dir = Path(args.results_dir).resolve()
    problems_dir = results_dir / "problems"
    plans_dir = results_dir / "plans"

    if not domain_file.exists():
        raise FileNotFoundError(f"Domain file not found: {domain_file}")
    if not generator_file.exists():
        raise FileNotFoundError(f"Generator file not found: {generator_file}")

    results_dir.mkdir(parents=True, exist_ok=True)
    problems_dir.mkdir(parents=True, exist_ok=True)
    plans_dir.mkdir(parents=True, exist_ok=True)

    sizes = make_sizes(args.min_size, args.max_size, args.step)
    drones_values = make_drones(args.min_drones, args.max_drones)

    supports_seed = generator_supports_seed(generator_file)
    if args.seed is not None and not supports_seed:
        print("Aviso: --seed indicado pero el generador no soporta --seed; se ignora.")

    all_quality_rows: list[QualityRow] = []
    all_comparison_rows: list[ComparisonRow] = []

    for drones in drones_values:
        q_rows, c_row = run_sweep_for_drones(
            drones=drones,
            sizes=sizes,
            domain_file=domain_file,
            generator_file=generator_file,
            problems_dir=problems_dir,
            plans_dir=plans_dir,
            timeout_s=args.timeout,
            stop_after_fails=args.stop_after_fails,
            capacity=args.carrier_capacity,
            seed=args.seed,
            supports_seed=supports_seed,
            lpg_seed=args.lpg_seed,
        )
        all_quality_rows.extend(q_rows)
        all_comparison_rows.append(c_row)

    quality_csv = results_dir / "benchmark_lpgtd_part3_quality_sweep.csv"
    compare_csv = results_dir / "benchmark_lpgtd_part3_comparison.csv"
    summary_csv = results_dir / "benchmark_lpgtd_part3_summary.csv"
    txt_path = results_dir / "benchmark_lpgtd_part3.txt"
    md_path = results_dir / "benchmark_lpgtd_part3.md"

    quality_headers = [
        "drones",
        "carriers",
        "mode",
        "size",
        "status",
        "processing_time_s",
        "plan_steps",
        "makespan",
        "wall_time_s",
        "problem_file",
        "error_excerpt",
    ]
    comparison_headers = [
        "drones",
        "carriers",
        "max_quality_size",
        "quality_status",
        "quality_processing_time_s",
        "quality_plan_steps",
        "quality_makespan",
        "speed_status",
        "speed_processing_time_s",
        "speed_plan_steps",
        "speed_makespan",
        "delta_processing_time_s",
        "delta_plan_steps",
        "delta_makespan",
        "problem_file",
    ]

    write_csv_table(quality_csv, quality_headers, [quality_row_values(r) for r in all_quality_rows])
    write_csv_table(compare_csv, comparison_headers, [comparison_row_values(r) for r in all_comparison_rows])
    write_summary_csv(summary_csv, all_comparison_rows)

    images = make_plots(results_dir, all_comparison_rows)
    write_reports(
        txt_path=txt_path,
        md_path=md_path,
        args=args,
        quality_rows=all_quality_rows,
        comparison_rows=all_comparison_rows,
        images=images,
    )

    print("\nDone.")
    print(f"CSV: {quality_csv}")
    print(f"CSV: {compare_csv}")
    print(f"CSV: {summary_csv}")
    print(f"TXT: {txt_path}")
    print(f"MD:  {md_path}")
    for image in images:
        print(f"IMG: {image}")


if __name__ == "__main__":
    main()
