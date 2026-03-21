#!/usr/bin/env python3
"""Benchmark Optic for Practice 1 Part 3 (V2).

Behavior:
- Sweep drones (default 1..5) with carriers=drones.
- For each drones/carriers pair, search max solved size within timeout (default 60s).
- Optic is anytime: extract first and last solution produced in the run window.
- Export CSV + TXT + MD + PNG under results/.
"""

from __future__ import annotations

import argparse
import csv
import datetime as dt
import re
import shlex
import shutil
import subprocess
import sys
import tempfile
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
PLAN_LINE_RE = re.compile(
    r"^\s*([0-9]+(?:\.[0-9]+)?)\s*:\s*\(.+\)\s*\[\s*([0-9]+(?:\.[0-9]+)?)\s*\]\s*$",
    re.IGNORECASE,
)
UNSOLVED_RE = re.compile(r"(unsolvable|no solution|search failed|goal can be simplified to false)", re.IGNORECASE)
UNSUPPORTED_RE = re.compile(
    r"(command not found|no such file or directory|invalid option|unknown option|module not found)",
    re.IGNORECASE,
)
# OPTIC prints the planning time as "; Time X.XXX" after each solution found.
# We collect all such occurrences and take the last one (most recent solution).
PROCESSING_PATTERNS = [
    re.compile(r";\s*Time\s+([0-9]+(?:\.[0-9]+)?)"),           # OPTIC: ; Time 1.234
    re.compile(r"total\s+time\s*[:=]\s*([0-9]+(?:\.[0-9]+)?)", re.IGNORECASE),
    re.compile(r"cpu\s*time\s*[:=]\s*([0-9]+(?:\.[0-9]+)?)", re.IGNORECASE),
    re.compile(r"processing\s*time\s*[:=]\s*([0-9]+(?:\.[0-9]+)?)", re.IGNORECASE),
    re.compile(r"b;\s*Total\s+time:\s*([0-9]+(?:\.[0-9]+)?)", re.IGNORECASE),  # FD style
    re.compile(r"time\s*[:=]\s*([0-9]+(?:\.[0-9]+)?)\s*(?:s|sec|seconds)", re.IGNORECASE),
]


@dataclass
class SweepRow:
    drones: int
    carriers: int
    size: int
    status: str
    processing_time_s: float | None
    first_plan_steps: int | None
    first_makespan: float | None
    last_plan_steps: int | None
    last_makespan: float | None
    wall_time_s: float
    problem_file: str
    error_excerpt: str


@dataclass
class SummaryRow:
    drones: int
    carriers: int
    max_solved_size: int | None
    status_at_max: str
    processing_time_s_at_max: float | None
    first_plan_steps: int | None
    first_makespan: float | None
    last_plan_steps: int | None
    last_makespan: float | None
    delta_steps: int | None
    delta_makespan: float | None
    problem_file: str


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Benchmark Optic for Part 3 V2 (anytime first vs last)")
    parser.add_argument("--min-drones", type=int, default=1, help="minimum drones")
    parser.add_argument("--max-drones", type=int, default=5, help="maximum drones")

    parser.add_argument("--min-size", type=int, default=2, help="minimum size for l=p=c=g")
    parser.add_argument("--max-size", type=int, default=40, help="maximum size for l=p=c=g")
    parser.add_argument("--step", type=int, default=1, help="size increment")

    parser.add_argument("--timeout", type=int, default=60, help="timeout per run in seconds")
    parser.add_argument("--stop-after-fails", type=int, default=3, help="stop after N consecutive non-solved runs")

    parser.add_argument("--domain", default="dronedomain.pddl", help="temporal domain path")
    parser.add_argument("--generator", default="generate-problem.py", help="problem generator path")
    parser.add_argument("--results-dir", default="results", help="output folder")

    parser.add_argument("--carrier-capacity", type=int, default=4, help="carrier capacity")
    parser.add_argument(
        "--seed",
        type=int,
        default=None,
        help="optional generator seed (used only if generator supports --seed)",
    )

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


def parse_processing_time(output: str) -> float | None:
    """Extract the planner's self-reported planning time from its output.

    Returns None if no timing information is found in the output, so the
    caller can distinguish 'no timing data' from 'zero seconds'.
    """
    for pattern in PROCESSING_PATTERNS:
        matches = pattern.findall(output)
        if matches:
            try:
                return float(matches[-1])
            except ValueError:
                continue
    return None


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
    timeout_s: int,
    seed: int | None,
    supports_seed: bool,
) -> tuple[bool, Path, str]:
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
        cmd += ["--seed", str(seed)]

    code, out, timed_out, _ = run_command(cmd, cwd=output_dir, timeout_s=timeout_s)
    ok = (not timed_out) and code == 0 and output_path.exists()
    return ok, output_path, out


def parse_plan_groups(text: str) -> list[tuple[int, float]]:
    groups: list[tuple[int, float]] = []
    current_steps = 0
    current_max_end: float | None = None

    for raw_line in text.splitlines():
        line = raw_line.strip()
        match = PLAN_LINE_RE.match(line)
        if match:
            start = float(match.group(1))
            dur = float(match.group(2))
            end = start + dur
            current_steps += 1
            current_max_end = end if current_max_end is None else max(current_max_end, end)
            continue

        if current_steps > 0:
            groups.append((current_steps, current_max_end if current_max_end is not None else 0.0))
            current_steps = 0
            current_max_end = None

    if current_steps > 0:
        groups.append((current_steps, current_max_end if current_max_end is not None else 0.0))

    return groups


def collect_anytime_solutions(stdout_text: str, run_dir: Path) -> list[tuple[int, float]]:
    groups = parse_plan_groups(stdout_text)

    # Some wrappers write plan data to files. Use mtime order as fallback/extension.
    file_patterns = ["*plan*", "*.soln", "*.SOL", "*.plan", "sas_plan*"]
    files: list[Path] = []
    for pattern in file_patterns:
        files.extend(run_dir.glob(pattern))
    files = sorted({path.resolve() for path in files if path.is_file()}, key=lambda p: p.stat().st_mtime)

    for path in files:
        try:
            text = path.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        file_groups = parse_plan_groups(text)
        groups.extend(file_groups)

    return groups


def infer_status(code: int, output: str, timed_out: bool, groups: list[tuple[int, float]]) -> str:
    # For anytime planners, if at least one plan was produced in the window, count as solved.
    if groups:
        return "solved"
    if timed_out:
        return "timeout"
    if code == 127:
        return "unsupported"
    if UNSUPPORTED_RE.search(output):
        return "unsupported"
    if UNSOLVED_RE.search(output):
        return "unsolved"
    if code == 0:
        return "unsolved"
    return "error"


def _is_optic_launcher_missing(code: int, out: str) -> bool:
    """True only when the optic/planutils binary itself is not found."""
    if code == 127:
        return True
    if "command not found" in out:
        return True
    # subprocess FileNotFoundError has the binary name (short, no slash) at end
    if re.search(r"\[Errno 2\] No such file or directory: '[^/]", out):
        return True
    return False


def _copy_to_tmp(src: Path, tmp_dir: str, name: str) -> Path:
    """Copy src to tmp_dir/name and return the destination Path."""
    dst = Path(tmp_dir) / name
    shutil.copy2(src, dst)
    return dst


def optic_attempts(domain_file: Path, problem_file: Path) -> list[list[str]]:
    d = str(domain_file)
    p = str(problem_file)
    return [
        ["planutils", "run", "optic", "--", d, p],
        ["optic", d, p],
    ]


def run_optic(
    domain_file: Path,
    problem_file: Path,
    timeout_s: int,
    run_dir: Path,
) -> SweepRow:
    size = extract_size(problem_file, -1)

    # clean up previous possible plan artifacts in this run dir
    for old in run_dir.glob("*"):
        if old.is_file():
            try:
                old.unlink()
            except OSError:
                pass

    # The Apptainer container for OPTIC cannot access /mnt/c/... WSL paths.
    # Copy domain and problem to a native Linux /tmp directory.
    tmp_dir = tempfile.mkdtemp(prefix="optic_bench_")
    eff_domain = _copy_to_tmp(domain_file, tmp_dir, domain_file.name)
    eff_problem = _copy_to_tmp(problem_file, tmp_dir, problem_file.name)

    last_row: SweepRow | None = None
    attempt_idx = 0

    try:
        for cmd in optic_attempts(domain_file=eff_domain, problem_file=eff_problem):
            attempt_idx += 1
            # Run from the tmp dir so any output plan files land there
            code, out, timed_out, wall = run_command(cmd, cwd=Path(tmp_dir), timeout_s=timeout_s)

            # Save log for debugging
            log_file = run_dir / f"optic_attempt_{attempt_idx}.log"
            try:
                log_file.write_text(out, encoding="utf-8")
            except OSError:
                pass

            groups = collect_anytime_solutions(out, Path(tmp_dir))
            status = infer_status(code, out, timed_out, groups)
            processing = parse_processing_time(out)

            if groups:
                first_steps, first_makespan = groups[0]
                last_steps, last_makespan = groups[-1]
            else:
                first_steps = None
                first_makespan = None
                last_steps = None
                last_makespan = None

            row = SweepRow(
                drones=-1,
                carriers=-1,
                size=size,
                status=status,
                processing_time_s=processing,
                first_plan_steps=first_steps,
                first_makespan=first_makespan,
                last_plan_steps=last_steps,
                last_makespan=last_makespan,
                wall_time_s=wall,
                problem_file=str(problem_file),
                error_excerpt="" if status in {"solved", "unsolved", "timeout"} else make_error_excerpt(out),
            )
            last_row = row

            if status in {"solved", "timeout", "unsolved", "unsupported"}:
                return row

            if not _is_optic_launcher_missing(code, out):
                return row

        if last_row is not None:
            return last_row

        return SweepRow(
            drones=-1,
            carriers=-1,
            size=size,
            status="unsupported",
            processing_time_s=None,
            first_plan_steps=None,
            first_makespan=None,
            last_plan_steps=None,
            last_makespan=None,
            wall_time_s=0.0,
            problem_file=str(problem_file),
            error_excerpt="optic backend not available",
        )
    finally:
        shutil.rmtree(tmp_dir, ignore_errors=True)


def run_sweep_for_drones(
    drones: int,
    sizes: list[int],
    domain_file: Path,
    generator_file: Path,
    problems_dir: Path,
    runs_dir: Path,
    timeout_s: int,
    stop_after_fails: int,
    capacity: int,
    seed: int | None,
    supports_seed: bool,
) -> tuple[list[SweepRow], SummaryRow]:
    carriers = drones
    sweep_rows: list[SweepRow] = []

    consecutive_fails = 0
    best: SweepRow | None = None
    planner_unavailable = False

    for size in sizes:
        ok, problem_file, gen_out = generate_problem(
            generator_path=generator_file,
            output_dir=problems_dir,
            drones=drones,
            carriers=carriers,
            size=size,
            capacity=capacity,
            timeout_s=timeout_s,
            seed=seed,
            supports_seed=supports_seed,
        )
        if not ok:
            row = SweepRow(
                drones=drones,
                carriers=carriers,
                size=size,
                status="error",
                processing_time_s=None,
                first_plan_steps=None,
                first_makespan=None,
                last_plan_steps=None,
                last_makespan=None,
                wall_time_s=0.0,
                problem_file=str(problem_file),
                error_excerpt=f"generation failed: {make_error_excerpt(gen_out)}",
            )
            sweep_rows.append(row)
            consecutive_fails += 1
            print(f"[d={drones} size={size}] generation error")
            if consecutive_fails >= stop_after_fails:
                break
            continue

        run_dir = runs_dir / f"d{drones}_s{size}"
        run_dir.mkdir(parents=True, exist_ok=True)

        row = run_optic(domain_file=domain_file, problem_file=problem_file, timeout_s=timeout_s, run_dir=run_dir)
        row.drones = drones
        row.carriers = carriers
        sweep_rows.append(row)

        fsteps = "-" if row.first_plan_steps is None else str(row.first_plan_steps)
        lsteps = "-" if row.last_plan_steps is None else str(row.last_plan_steps)
        fm = "-" if row.first_makespan is None else f"{row.first_makespan:.2f}"
        lm = "-" if row.last_makespan is None else f"{row.last_makespan:.2f}"
        pt = "-" if row.processing_time_s is None else f"{row.processing_time_s:.2f}"
        print(
            f"[d={drones} size={size}] status={row.status} t={pt}s "
            f"first=({fsteps},{fm}) last=({lsteps},{lm})"
        )

        if row.status == "unsupported":
            planner_unavailable = True
            break

        if row.status == "solved":
            best = row
            consecutive_fails = 0
        else:
            consecutive_fails += 1
            if consecutive_fails >= stop_after_fails:
                break

    if best is None:
        status = "unsupported" if planner_unavailable else "not_found"
        summary = SummaryRow(
            drones=drones,
            carriers=carriers,
            max_solved_size=None,
            status_at_max=status,
            processing_time_s_at_max=None,
            first_plan_steps=None,
            first_makespan=None,
            last_plan_steps=None,
            last_makespan=None,
            delta_steps=None,
            delta_makespan=None,
            problem_file="",
        )
        return sweep_rows, summary

    delta_steps = None
    if best.first_plan_steps is not None and best.last_plan_steps is not None:
        delta_steps = best.last_plan_steps - best.first_plan_steps

    delta_makespan = None
    if best.first_makespan is not None and best.last_makespan is not None:
        delta_makespan = best.last_makespan - best.first_makespan

    summary = SummaryRow(
        drones=drones,
        carriers=carriers,
        max_solved_size=best.size,
        status_at_max=best.status,
        processing_time_s_at_max=best.processing_time_s,
        first_plan_steps=best.first_plan_steps,
        first_makespan=best.first_makespan,
        last_plan_steps=best.last_plan_steps,
        last_makespan=best.last_makespan,
        delta_steps=delta_steps,
        delta_makespan=delta_makespan,
        problem_file=best.problem_file,
    )
    return sweep_rows, summary


def sweep_row_values(row: SweepRow) -> list[str]:
    return [
        str(row.drones),
        str(row.carriers),
        str(row.size),
        row.status,
        "" if row.processing_time_s is None else f"{row.processing_time_s:.4f}",
        "" if row.first_plan_steps is None else str(row.first_plan_steps),
        "" if row.first_makespan is None else f"{row.first_makespan:.4f}",
        "" if row.last_plan_steps is None else str(row.last_plan_steps),
        "" if row.last_makespan is None else f"{row.last_makespan:.4f}",
        f"{row.wall_time_s:.4f}",
        row.problem_file,
        row.error_excerpt,
    ]


def summary_row_values(row: SummaryRow) -> list[str]:
    return [
        str(row.drones),
        str(row.carriers),
        "" if row.max_solved_size is None else str(row.max_solved_size),
        row.status_at_max,
        "" if row.processing_time_s_at_max is None else f"{row.processing_time_s_at_max:.4f}",
        "" if row.first_plan_steps is None else str(row.first_plan_steps),
        "" if row.first_makespan is None else f"{row.first_makespan:.4f}",
        "" if row.last_plan_steps is None else str(row.last_plan_steps),
        "" if row.last_makespan is None else f"{row.last_makespan:.4f}",
        "" if row.delta_steps is None else str(row.delta_steps),
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


def add_table_txt(lines: list[str], title: str, headers: list[str], rows: list[list[str]]) -> None:
    lines.append(title)
    lines.append("\t".join(headers))
    for row in rows:
        lines.append("\t".join(row))
    lines.append("")


def add_table_md(lines: list[str], title: str, headers: list[str], rows: list[list[str]]) -> None:
    lines.append(f"## {title}")
    lines.append("")
    lines.append("| " + " | ".join(markdown_escape(h) for h in headers) + " |")
    lines.append("| " + " | ".join("---" for _ in headers) + " |")
    for row in rows:
        normalized = row[: len(headers)] + [""] * max(0, len(headers) - len(row))
        lines.append("| " + " | ".join(markdown_escape(v) for v in normalized) + " |")
    lines.append("")


def write_reports(
    txt_path: Path,
    md_path: Path,
    args: argparse.Namespace,
    sweep_rows: list[SweepRow],
    summary_rows: list[SummaryRow],
    images: list[Path],
) -> None:
    sweep_headers = [
        "drones",
        "carriers",
        "size",
        "status",
        "processing_time_s",
        "first_plan_steps",
        "first_makespan",
        "last_plan_steps",
        "last_makespan",
        "wall_time_s",
        "problem_file",
        "error_excerpt",
    ]
    summary_headers = [
        "drones",
        "carriers",
        "max_solved_size",
        "status_at_max",
        "processing_time_s_at_max",
        "first_plan_steps",
        "first_makespan",
        "last_plan_steps",
        "last_makespan",
        "delta_steps",
        "delta_makespan",
        "problem_file",
    ]

    sweep_values = [sweep_row_values(r) for r in sweep_rows]
    summary_values = [summary_row_values(r) for r in summary_rows]

    txt_lines: list[str] = []
    txt_lines.append("Benchmark Optic - Practice 1 Part 3 V2")
    txt_lines.append(f"Generated at: {dt.datetime.now().isoformat(timespec='seconds')}")
    txt_lines.append(f"Args: {vars(args)}")
    txt_lines.append("")
    add_table_txt(txt_lines, "[SUMMARY]", summary_headers, summary_values)
    add_table_txt(txt_lines, "[SWEEP]", sweep_headers, sweep_values)
    txt_path.write_text("\n".join(txt_lines), encoding="utf-8")

    md_lines: list[str] = []
    md_lines.append("# Benchmark Optic - Practice 1 Part 3 V2")
    md_lines.append("")
    md_lines.append(f"- Generated at: `{dt.datetime.now().isoformat(timespec='seconds')}`")
    md_lines.append(f"- Args: `{vars(args)}`")
    md_lines.append("")
    add_table_md(md_lines, "Tabla por número de drones/carriers", summary_headers, summary_values)
    add_table_md(md_lines, "Barrido de tamaños", sweep_headers, sweep_values)

    md_lines.append("## Diagramas")
    md_lines.append("")
    for image in images:
        md_lines.append(f"![{image.stem}]({image.name})")
        md_lines.append("")

    md_path.write_text("\n".join(md_lines), encoding="utf-8")


def make_plots(results_dir: Path, summary_rows: list[SummaryRow]) -> list[Path]:
    if not HAVE_MATPLOTLIB:
        raise RuntimeError(
            "matplotlib is required to generate diagram images. Install it with `pip install matplotlib`."
        )

    rows = sorted(summary_rows, key=lambda r: r.drones)
    drones = [r.drones for r in rows]

    img1 = results_dir / "part3_optic_max_solved_size_by_drones.png"
    img2 = results_dir / "part3_optic_first_vs_last_steps.png"
    img3 = results_dir / "part3_optic_first_vs_last_makespan.png"

    max_sizes = [0 if r.max_solved_size is None else r.max_solved_size for r in rows]
    plt.figure(figsize=(10, 5.5))
    plt.plot(drones, max_sizes, marker="o", color="#1f77b4", label="max solved size")
    plt.title("Parte 3 V2 (Optic) - Tamaño máximo resuelto por nº drones/carriers")
    plt.xlabel("Drones (carriers=drones)")
    plt.ylabel("Max size (l=p=c=g)")
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.tight_layout()
    plt.savefig(img1, dpi=140)
    plt.close()

    first_steps = [r.first_plan_steps for r in rows]
    last_steps = [r.last_plan_steps for r in rows]
    first_m = [r.first_makespan for r in rows]
    last_m = [r.last_makespan for r in rows]

    def grouped_bar(image_path: Path, y1: list[int | float | None], y2: list[int | float | None], title: str, ylabel: str) -> None:
        x = list(range(len(drones)))
        width = 0.38

        def norm(vals: list[int | float | None]) -> list[float]:
            return [0.0 if v is None else float(v) for v in vals]

        y1n = norm(y1)
        y2n = norm(y2)
        x_left = [i - width / 2 for i in x]
        x_right = [i + width / 2 for i in x]

        fig, ax = plt.subplots(figsize=(11, 5.5))
        b1 = ax.bar(x_left, y1n, width, label="first solution", color="#1f77b4")
        b2 = ax.bar(x_right, y2n, width, label="last solution", color="#ff7f0e")

        for bar, miss in zip(b1, [v is None for v in y1]):
            if miss:
                bar.set_hatch("//")
                bar.set_alpha(0.4)
        for bar, miss in zip(b2, [v is None for v in y2]):
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

    grouped_bar(
        img2,
        first_steps,
        last_steps,
        "Parte 3 V2 (Optic) - Comparación primera vs última solución (pasos)",
        "Plan steps",
    )
    grouped_bar(
        img3,
        first_m,
        last_m,
        "Parte 3 V2 (Optic) - Comparación primera vs última solución (makespan)",
        "Makespan",
    )

    return [img1, img2, img3]


def main() -> None:
    args = parse_args()

    domain_file = Path(args.domain).resolve()
    generator_file = Path(args.generator).resolve()
    results_dir = Path(args.results_dir).resolve()
    problems_dir = results_dir / "problems"
    runs_dir = results_dir / "optic_runs"

    if not domain_file.exists():
        raise FileNotFoundError(f"Domain file not found: {domain_file}")
    if not generator_file.exists():
        raise FileNotFoundError(f"Generator file not found: {generator_file}")

    sizes = make_sizes(args.min_size, args.max_size, args.step)
    drones_values = make_drones(args.min_drones, args.max_drones)

    results_dir.mkdir(parents=True, exist_ok=True)
    problems_dir.mkdir(parents=True, exist_ok=True)
    runs_dir.mkdir(parents=True, exist_ok=True)

    supports_seed = generator_supports_seed(generator_file)
    if args.seed is not None and not supports_seed:
        print("Aviso: --seed indicado pero el generador no soporta --seed; se ignora.")

    sweep_rows: list[SweepRow] = []
    summary_rows: list[SummaryRow] = []

    for drones in drones_values:
        s_rows, summary = run_sweep_for_drones(
            drones=drones,
            sizes=sizes,
            domain_file=domain_file,
            generator_file=generator_file,
            problems_dir=problems_dir,
            runs_dir=runs_dir,
            timeout_s=args.timeout,
            stop_after_fails=args.stop_after_fails,
            capacity=args.carrier_capacity,
            seed=args.seed,
            supports_seed=supports_seed,
        )
        sweep_rows.extend(s_rows)
        summary_rows.append(summary)

    sweep_csv = results_dir / "benchmark_optic_part3_sweep.csv"
    summary_csv = results_dir / "benchmark_optic_part3_summary.csv"
    txt_path = results_dir / "benchmark_optic_part3.txt"
    md_path = results_dir / "benchmark_optic_part3.md"

    sweep_headers = [
        "drones",
        "carriers",
        "size",
        "status",
        "processing_time_s",
        "first_plan_steps",
        "first_makespan",
        "last_plan_steps",
        "last_makespan",
        "wall_time_s",
        "problem_file",
        "error_excerpt",
    ]
    summary_headers = [
        "drones",
        "carriers",
        "max_solved_size",
        "status_at_max",
        "processing_time_s_at_max",
        "first_plan_steps",
        "first_makespan",
        "last_plan_steps",
        "last_makespan",
        "delta_steps",
        "delta_makespan",
        "problem_file",
    ]

    write_csv_table(sweep_csv, sweep_headers, [sweep_row_values(r) for r in sweep_rows])
    write_csv_table(summary_csv, summary_headers, [summary_row_values(r) for r in summary_rows])

    images = make_plots(results_dir, summary_rows)
    write_reports(
        txt_path=txt_path,
        md_path=md_path,
        args=args,
        sweep_rows=sweep_rows,
        summary_rows=summary_rows,
        images=images,
    )

    print("\nDone.")
    print(f"CSV: {sweep_csv}")
    print(f"CSV: {summary_csv}")
    print(f"TXT: {txt_path}")
    print(f"MD:  {md_path}")
    for image in images:
        print(f"IMG: {image}")


if __name__ == "__main__":
    main()
