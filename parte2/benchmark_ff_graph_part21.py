#!/usr/bin/env python3
"""Benchmark FF for Practice 1 Part 2 Exercise 2.1.

Main behavior:
- Generates instances with l=p=c=g over a size range (exercise=1 domain).
- Runs FF with per-instance timeout.
- Exports CSV + TXT + MD + PNG under results/.
"""

from __future__ import annotations

import argparse
import csv
import datetime as dt
import re
import shlex
import shutil
import struct
import subprocess
import sys
import time
import zlib
from dataclasses import dataclass
from pathlib import Path

try:
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    HAVE_MATPLOTLIB = True
except Exception:
    HAVE_MATPLOTLIB = False


FF_TIME_RE = re.compile(r"([0-9]+(?:\.[0-9]+)?)\s+seconds total time")
PLAN_LINE_RE = re.compile(r"^\s*(?:step\s+\d+:|\d+:)", re.MULTILINE)
SOLVED_RE = re.compile(r"found legal plan as follows", re.IGNORECASE)
UNSOLVABLE_RE = re.compile(r"problem proven unsolvable|goal can be simplified to false", re.IGNORECASE)
SIZE_RE = re.compile(r"_l([0-9]+)_")


@dataclass
class BenchmarkRow:
    size: int
    status: str
    solved: bool
    ff_time_s: float | None
    wall_time_s: float
    plan_steps: int | None
    problem_file: str
    solver_backend: str
    error_excerpt: str


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run FF benchmark for exercise 2.1")
    parser.add_argument("--min-size", type=int, default=2, help="minimum complexity value")
    parser.add_argument("--max-size", type=int, default=60, help="maximum complexity value")
    parser.add_argument("--step", type=int, default=1, help="increment between complexity values")
    parser.add_argument("--sizes", default=None, help="comma-separated list of sizes")

    parser.add_argument("--timeout", type=int, default=60, help="timeout per instance in seconds")
    parser.add_argument("--domain", default="dronedomain.pddl", help="path to domain file")
    parser.add_argument("--generator", default="generate-problem.py", help="problem generator script")
    parser.add_argument("--results-dir", default="results", help="output folder")

    parser.add_argument("--drones", type=int, default=1, help="number of drones for generated problems")
    parser.add_argument("--carriers", type=int, default=1, help="number of carriers for generated problems")
    parser.add_argument("--carrier-capacity", type=int, default=4, help="carrier capacity for generated problems")
    parser.add_argument("--exercise", type=int, default=1, choices=[1], help="generator exercise mode")
    parser.add_argument("--seed", type=int, default=None, help="optional generator seed")

    parser.add_argument("--csv-out", default=None, help="custom CSV output name/path")
    parser.add_argument("--txt-out", default=None, help="custom TXT output name/path")
    parser.add_argument("--md-out", default=None, help="custom MD output name/path")
    parser.add_argument("--png-out", default=None, help="custom PNG output name/path")
    parser.add_argument(
        "--allow-basic-plots",
        action="store_true",
        help="allow basic PNG plot without labels when matplotlib is unavailable",
    )

    parser.add_argument(
        "--problem-files",
        nargs="*",
        default=None,
        help="optional existing problem files; if set, generation is skipped",
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


def parse_sizes_csv(raw_sizes: str) -> list[int]:
    values: list[int] = []
    for token in raw_sizes.split(","):
        token = token.strip()
        if not token:
            continue
        values.append(int(token))
    if not values:
        raise ValueError("--sizes was provided but no valid integers were found")
    return values


def problem_file_name(size: int, exercise: int, drones: int, carriers: int, carrier_capacity: int, seed: int | None) -> str:
    name = (
        f"drone_problem_ex{exercise}"
        f"_d{drones}_r{carriers}_l{size}_p{size}_c{size}_g{size}_a{carrier_capacity}"
    )
    if seed is not None:
        name += f"_s{seed}"
    return f"{name}.pddl"


def extract_size_from_name(name: str) -> int:
    match = SIZE_RE.search(name)
    if match is None:
        return -1
    return int(match.group(1))


def run_command(cmd: list[str], cwd: Path | None = None, timeout_s: int | None = None) -> tuple[int, str, bool]:
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
        return proc.returncode, proc.stdout, False
    except subprocess.TimeoutExpired as exc:
        out = exc.stdout or ""
        if isinstance(out, bytes):
            out = out.decode(errors="replace")
        return 124, out, True
    except FileNotFoundError:
        return 127, f"command not found: {cmd[0]}", False


def make_error_excerpt(text: str, max_lines: int = 6) -> str:
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    if not lines:
        return ""
    return " | ".join(lines[:max_lines])[:500]


def generate_problem(
    size: int,
    generator_path: Path,
    problems_dir: Path,
    drones: int,
    carriers: int,
    carrier_capacity: int,
    exercise: int,
    seed: int | None,
) -> tuple[bool, Path, str]:
    output_path = problems_dir / problem_file_name(size, exercise, drones, carriers, carrier_capacity, seed)

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
        str(carrier_capacity),
        "--exercise",
        str(exercise),
    ]
    if seed is not None:
        cmd += ["--seed", str(seed)]

    code, out, timed_out = run_command(cmd, cwd=problems_dir)
    ok = (not timed_out) and code == 0 and output_path.exists()
    return ok, output_path, out


def parse_ff_output(text: str) -> tuple[bool, float | None, int | None]:
    solved = SOLVED_RE.search(text) is not None

    ff_time = None
    time_match = FF_TIME_RE.search(text)
    if time_match:
        ff_time = float(time_match.group(1))

    plan_steps = None
    if solved:
        plan_steps = len(PLAN_LINE_RE.findall(text))

    return solved, ff_time, plan_steps


def run_ff(domain_file: Path, problem_file: Path, timeout_s: int) -> BenchmarkRow:
    planner_cwd = problem_file.parent
    domain_local = planner_cwd / "__benchmark_domain__.pddl"
    try:
        if domain_local.is_symlink() or domain_local.exists():
            domain_local.unlink()
        domain_local.symlink_to(domain_file.resolve())
    except OSError:
        shutil.copyfile(domain_file.resolve(), domain_local)

    domain_arg = domain_local.name
    problem_arg = problem_file.name

    attempts: list[tuple[str, list[str]]] = [
        ("planutils", ["planutils", "run", "ff", "--", domain_arg, problem_arg]),
        ("ff", ["ff", domain_arg, problem_arg]),
    ]

    size = extract_size_from_name(problem_file.name)
    start = time.perf_counter()

    for backend_name, cmd in attempts:
        code, out, timed_out = run_command(cmd, cwd=planner_cwd, timeout_s=timeout_s)
        wall_time = time.perf_counter() - start

        if timed_out:
            return BenchmarkRow(
                size=size,
                status="timeout",
                solved=False,
                ff_time_s=None,
                wall_time_s=wall_time,
                plan_steps=None,
                problem_file=str(problem_file),
                solver_backend=backend_name,
                error_excerpt="",
            )

        solved, ff_time_s, plan_steps = parse_ff_output(out)

        if solved:
            return BenchmarkRow(
                size=size,
                status="solved",
                solved=True,
                ff_time_s=ff_time_s,
                wall_time_s=wall_time,
                plan_steps=plan_steps,
                problem_file=str(problem_file),
                solver_backend=backend_name,
                error_excerpt="",
            )

        if UNSOLVABLE_RE.search(out):
            return BenchmarkRow(
                size=size,
                status="unsolved",
                solved=False,
                ff_time_s=ff_time_s,
                wall_time_s=wall_time,
                plan_steps=plan_steps,
                problem_file=str(problem_file),
                solver_backend=backend_name,
                error_excerpt="",
            )

        if backend_name == "planutils" and code != 0:
            continue

        return BenchmarkRow(
            size=size,
            status="error",
            solved=False,
            ff_time_s=ff_time_s,
            wall_time_s=wall_time,
            plan_steps=plan_steps,
            problem_file=str(problem_file),
            solver_backend=backend_name,
            error_excerpt=make_error_excerpt(out),
        )

    wall_time = time.perf_counter() - start
    return BenchmarkRow(
        size=size,
        status="error",
        solved=False,
        ff_time_s=None,
        wall_time_s=wall_time,
        plan_steps=None,
        problem_file=str(problem_file),
        solver_backend="none",
        error_excerpt="FF not available via planutils or ff binary",
    )


def load_existing_problems(problem_files: list[str]) -> list[Path]:
    problems: list[Path] = []
    for raw in problem_files:
        path = Path(raw).resolve()
        if not path.exists():
            raise FileNotFoundError(f"Problem file not found: {path}")
        problems.append(path)
    problems.sort(key=lambda p: extract_size_from_name(p.name))
    return problems


def run_benchmark(
    sizes: list[int],
    domain_file: Path,
    generator_path: Path,
    problems_dir: Path,
    timeout_s: int,
    drones: int,
    carriers: int,
    carrier_capacity: int,
    exercise: int,
    seed: int | None,
) -> list[BenchmarkRow]:
    rows: list[BenchmarkRow] = []

    for size in sizes:
        ok, problem_path, output = generate_problem(
            size=size,
            generator_path=generator_path,
            problems_dir=problems_dir,
            drones=drones,
            carriers=carriers,
            carrier_capacity=carrier_capacity,
            exercise=exercise,
            seed=seed,
        )
        if not ok:
            rows.append(
                BenchmarkRow(
                    size=size,
                    status="gen_error",
                    solved=False,
                    ff_time_s=None,
                    wall_time_s=0.0,
                    plan_steps=None,
                    problem_file=str(problem_path),
                    solver_backend="generator",
                    error_excerpt=make_error_excerpt(output),
                )
            )
            print(f"[size={size}] generation error")
            continue

        row = run_ff(domain_file, problem_path, timeout_s)
        rows.append(row)

        time_label = "-" if row.ff_time_s is None else f"{row.ff_time_s:.2f}s"
        print(f"[size={size}] status={row.status} ff_time={time_label} steps={row.plan_steps}")

    return rows


def run_benchmark_existing(domain_file: Path, problem_files: list[Path], timeout_s: int) -> list[BenchmarkRow]:
    rows: list[BenchmarkRow] = []
    for problem_file in problem_files:
        row = run_ff(domain_file, problem_file, timeout_s)
        rows.append(row)
        time_label = "-" if row.ff_time_s is None else f"{row.ff_time_s:.2f}s"
        print(f"[size={row.size}] status={row.status} ff_time={time_label} steps={row.plan_steps}")
    return rows


def write_csv(rows: list[BenchmarkRow], csv_path: Path) -> None:
    with csv_path.open("w", newline="", encoding="utf-8") as file_handle:
        writer = csv.writer(file_handle)
        writer.writerow(
            [
                "size",
                "status",
                "solved",
                "ff_time_s",
                "wall_time_s",
                "plan_steps",
                "solver_backend",
                "error_excerpt",
                "problem_file",
            ]
        )
        for row in rows:
            writer.writerow(
                [
                    row.size,
                    row.status,
                    "yes" if row.solved else "no",
                    "" if row.ff_time_s is None else f"{row.ff_time_s:.2f}",
                    f"{row.wall_time_s:.4f}",
                    "" if row.plan_steps is None else row.plan_steps,
                    row.solver_backend,
                    row.error_excerpt,
                    row.problem_file,
                ]
            )


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


def rows_as_lists(rows: list[BenchmarkRow]) -> list[list[str]]:
    return [
        [
            str(row.size),
            row.status,
            "yes" if row.solved else "no",
            "" if row.ff_time_s is None else f"{row.ff_time_s:.2f}",
            f"{row.wall_time_s:.4f}",
            "" if row.plan_steps is None else str(row.plan_steps),
            row.solver_backend,
            row.error_excerpt,
            row.problem_file,
        ]
        for row in rows
    ]


def threshold_summary(rows: list[BenchmarkRow], threshold_s: int) -> tuple[str, str, str]:
    solved_rows = [r for r in rows if r.solved and r.ff_time_s is not None]
    within = [r for r in solved_rows if r.ff_time_s <= float(threshold_s)]

    max_within = "none"
    if within:
        best = max(within, key=lambda r: r.size)
        max_within = f"size={best.size}, ff_time_s={best.ff_time_s:.2f}, plan_steps={best.plan_steps}"

    first_over = "none"
    over = [r for r in solved_rows if r.ff_time_s > float(threshold_s)]
    if over:
        first = min(over, key=lambda r: r.size)
        first_over = f"size={first.size}, ff_time_s={first.ff_time_s:.2f}, plan_steps={first.plan_steps}"

    counts = {
        "solved": sum(1 for r in rows if r.status == "solved"),
        "timeout": sum(1 for r in rows if r.status == "timeout"),
        "unsolved": sum(1 for r in rows if r.status == "unsolved"),
        "error": sum(1 for r in rows if r.status in {"error", "gen_error"}),
    }
    count_text = (
        f"solved={counts['solved']}, timeout={counts['timeout']}, "
        f"unsolved={counts['unsolved']}, error={counts['error']}"
    )
    return max_within, first_over, count_text


def write_txt_report(path: Path, rows: list[BenchmarkRow], args: argparse.Namespace) -> None:
    lines: list[str] = []
    lines.append("Benchmark FF - Practice 1 Part 2 Exercise 2.1")
    lines.append(f"Generated at: {dt.datetime.now().isoformat(timespec='seconds')}")
    lines.append(f"Args: {vars(args)}")
    lines.append("")

    headers = [
        "size",
        "status",
        "solved",
        "ff_time_s",
        "wall_time_s",
        "plan_steps",
        "solver_backend",
        "error_excerpt",
        "problem_file",
    ]
    add_table_txt(lines, "[RAW_ROWS]", headers, rows_as_lists(rows))

    max_within, first_over, count_text = threshold_summary(rows, args.timeout)
    lines.append("[SUMMARY_THRESHOLD]")
    lines.append(f"threshold_s\t{args.timeout}")
    lines.append(f"max_size_within_threshold\t{max_within}")
    lines.append(f"first_size_over_threshold\t{first_over}")
    lines.append(f"status_counts\t{count_text}")
    lines.append("")

    path.write_text("\n".join(lines), encoding="utf-8")


def write_md_report(path: Path, rows: list[BenchmarkRow], args: argparse.Namespace) -> None:
    lines: list[str] = []
    lines.append("# Benchmark FF - Practice 1 Part 2 Exercise 2.1")
    lines.append("")
    lines.append(f"- Generated at: `{dt.datetime.now().isoformat(timespec='seconds')}`")
    lines.append(f"- Args: `{vars(args)}`")
    lines.append("")

    headers = [
        "size",
        "status",
        "solved",
        "ff_time_s",
        "wall_time_s",
        "plan_steps",
        "solver_backend",
        "error_excerpt",
        "problem_file",
    ]
    add_table_md(lines, "[RAW_ROWS]", headers, rows_as_lists(rows))

    max_within, first_over, count_text = threshold_summary(rows, args.timeout)
    add_table_md(
        lines,
        "[SUMMARY_THRESHOLD]",
        ["threshold_s", "max_size_within_threshold", "first_size_over_threshold", "status_counts"],
        [[str(args.timeout), max_within, first_over, count_text]],
    )

    path.write_text("\n".join(lines), encoding="utf-8")


def save_png(rows: list[BenchmarkRow], output_path: Path, timeout_s: int, allow_basic_plots: bool) -> None:
    if timeout_s <= 0:
        timeout_s = 1

    if not HAVE_MATPLOTLIB:
        if not allow_basic_plots:
            raise RuntimeError(
                "matplotlib is required to generate readable PNG output. "
                "Install it with `pip install matplotlib` or use --allow-basic-plots."
            )
        save_png_basic(rows, output_path, timeout_s)
        return

    valid_rows = sorted((r for r in rows if r.size >= 0), key=lambda row: row.size)
    if not valid_rows:
        plt.figure(figsize=(16, 9), facecolor="#f8fafc")
        plt.title("FF Benchmark (Complexity vs Time)")
        plt.savefig(output_path, dpi=160)
        plt.close()
        return

    solved_rows = [row for row in valid_rows if row.solved and row.ff_time_s is not None]
    timeout_rows = [row for row in valid_rows if not row.solved or row.ff_time_s is None]
    plot_values = [row.ff_time_s if row.ff_time_s is not None else float(timeout_s) for row in valid_rows]
    x_values = [row.size for row in valid_rows]

    fig, ax = plt.subplots(figsize=(16, 9), facecolor="#f8fafc")
    ax.set_facecolor("#f8fafc")

    ax.plot(x_values, plot_values, color="#2563eb", linewidth=2.2, zorder=2)

    if solved_rows:
        ax.scatter(
            [row.size for row in solved_rows],
            [row.ff_time_s for row in solved_rows if row.ff_time_s is not None],
            s=42,
            color="#1d4ed8",
            label="solved",
            zorder=3,
        )
    if timeout_rows:
        ax.scatter(
            [row.size for row in timeout_rows],
            [float(timeout_s)] * len(timeout_rows),
            s=54,
            marker="x",
            linewidths=1.8,
            color="#b91c1c",
            label="not solved",
            zorder=4,
        )

    for row in valid_rows:
        y_value = row.ff_time_s if row.ff_time_s is not None else float(timeout_s)
        if row.solved and row.ff_time_s is not None:
            label = f"{row.ff_time_s:.2f}s"
            text_color = "#1e293b"
        else:
            label = "timeout"
            text_color = "#991b1b"
        ax.annotate(
            label,
            (row.size, y_value),
            textcoords="offset points",
            xytext=(0, 10),
            ha="center",
            va="bottom",
            fontsize=8,
            color=text_color,
            clip_on=False,
            zorder=5,
        )

    ax.axhline(
        float(timeout_s),
        color="#64748b",
        linestyle="--",
        linewidth=1.2,
        label=f"timeout={timeout_s}s",
        zorder=1,
    )

    x_min = min(x_values)
    x_max = max(x_values)
    if x_min == x_max:
        ax.set_xlim(x_min - 1, x_max + 1)
    else:
        ax.set_xlim(x_min - 0.6, x_max + 0.6)
    ax.set_ylim(0, float(timeout_s))
    ax.set_xticks(x_values)

    major_y_ticks = list(range(0, timeout_s + 1, 5)) if timeout_s >= 5 else list(range(0, timeout_s + 1))
    if timeout_s not in major_y_ticks:
        major_y_ticks.append(timeout_s)
    ax.set_yticks(sorted(set(major_y_ticks)))
    ax.set_yticks(list(range(0, timeout_s + 1)), minor=True)

    ax.grid(True, which="major", axis="y", color="#cbd5e1", linewidth=1.0)
    ax.grid(True, which="minor", axis="y", color="#e2e8f0", linewidth=0.6)
    ax.grid(True, which="major", axis="x", color="#e2e8f0", linewidth=0.6, alpha=0.7)

    for spine in ax.spines.values():
        spine.set_color("#334155")
        spine.set_linewidth(1.2)
    ax.tick_params(axis="x", colors="#334155", labelsize=9)
    ax.tick_params(axis="y", colors="#334155", labelsize=9)

    fig.suptitle("FF Benchmark (Complexity vs Time)", fontsize=20, color="#0f172a", x=0.08, ha="left")
    ax.set_title(
        "Complexity = l=p=c=g. Unsolved instances are shown at timeout line.",
        fontsize=11,
        color="#334155",
        loc="left",
        pad=18,
    )
    ax.set_xlabel("Complexity (l=p=c=g)", fontsize=12, color="#0f172a")
    ax.set_ylabel("Time (seconds)", fontsize=12, color="#0f172a")
    ax.legend(loc="upper left")

    fig.subplots_adjust(top=0.82, left=0.08, right=0.98, bottom=0.12)
    fig.savefig(output_path, dpi=160, facecolor=fig.get_facecolor())
    plt.close(fig)


def make_canvas(width: int, height: int, color: tuple[int, int, int] = (255, 255, 255)) -> bytearray:
    r, g, b = color
    return bytearray([r, g, b]) * (width * height)


def set_pixel(canvas: bytearray, width: int, height: int, x: int, y: int, color: tuple[int, int, int]) -> None:
    if x < 0 or y < 0 or x >= width or y >= height:
        return
    idx = (y * width + x) * 3
    canvas[idx] = color[0]
    canvas[idx + 1] = color[1]
    canvas[idx + 2] = color[2]


def draw_line(
    canvas: bytearray,
    width: int,
    height: int,
    x0: int,
    y0: int,
    x1: int,
    y1: int,
    color: tuple[int, int, int],
) -> None:
    dx = abs(x1 - x0)
    dy = -abs(y1 - y0)
    sx = 1 if x0 < x1 else -1
    sy = 1 if y0 < y1 else -1
    err = dx + dy
    while True:
        set_pixel(canvas, width, height, x0, y0, color)
        if x0 == x1 and y0 == y1:
            break
        e2 = 2 * err
        if e2 >= dy:
            err += dy
            x0 += sx
        if e2 <= dx:
            err += dx
            y0 += sy


def fill_rect(
    canvas: bytearray,
    width: int,
    height: int,
    x: int,
    y: int,
    rect_w: int,
    rect_h: int,
    color: tuple[int, int, int],
) -> None:
    x_start = max(0, x)
    y_start = max(0, y)
    x_end = min(width, x + rect_w)
    y_end = min(height, y + rect_h)
    if x_start >= x_end or y_start >= y_end:
        return
    for py in range(y_start, y_end):
        base = (py * width) * 3
        for px in range(x_start, x_end):
            idx = base + px * 3
            canvas[idx] = color[0]
            canvas[idx + 1] = color[1]
            canvas[idx + 2] = color[2]


def draw_cross(
    canvas: bytearray,
    width: int,
    height: int,
    x: int,
    y: int,
    radius: int,
    color: tuple[int, int, int],
) -> None:
    draw_line(canvas, width, height, x - radius, y - radius, x + radius, y + radius, color)
    draw_line(canvas, width, height, x - radius, y + radius, x + radius, y - radius, color)


def draw_dashed_hline(
    canvas: bytearray,
    width: int,
    height: int,
    x0: int,
    x1: int,
    y: int,
    color: tuple[int, int, int],
    dash: int = 8,
) -> None:
    x = x0
    draw = True
    while x <= x1:
        if draw:
            segment_end = min(x + dash - 1, x1)
            draw_line(canvas, width, height, x, y, segment_end, y, color)
        x += dash
        draw = not draw


def png_chunk(tag: bytes, data: bytes) -> bytes:
    crc = zlib.crc32(tag + data) & 0xFFFFFFFF
    return struct.pack("!I", len(data)) + tag + data + struct.pack("!I", crc)


def write_png(path: Path, width: int, height: int, pixels_rgb: bytearray) -> None:
    raw = bytearray()
    stride = width * 3
    for y in range(height):
        raw.append(0)
        start = y * stride
        raw.extend(pixels_rgb[start : start + stride])

    ihdr = struct.pack("!IIBBBBB", width, height, 8, 2, 0, 0, 0)
    idat = zlib.compress(bytes(raw), level=9)
    data = b"".join(
        [
            b"\x89PNG\r\n\x1a\n",
            png_chunk(b"IHDR", ihdr),
            png_chunk(b"IDAT", idat),
            png_chunk(b"IEND", b""),
        ]
    )
    path.write_bytes(data)


def save_png_basic(rows: list[BenchmarkRow], output_path: Path, timeout_s: int) -> None:
    width, height = 1200, 700
    left, right, top, bottom = 90, 40, 40, 80
    x0, x1 = left, width - right
    y1, y0 = top, height - bottom
    plot_w = x1 - x0
    plot_h = y0 - y1

    canvas = make_canvas(width, height, (255, 255, 255))
    draw_line(canvas, width, height, x0, y0, x1, y0, (20, 20, 20))
    draw_line(canvas, width, height, x0, y0, x0, y1, (20, 20, 20))

    if timeout_s <= 0:
        timeout_s = 1

    timeout_y = y0 - int((timeout_s / timeout_s) * plot_h)
    draw_dashed_hline(canvas, width, height, x0, x1, timeout_y, (160, 160, 160))

    valid_rows = [row for row in rows if row.size >= 0]
    if valid_rows:
        min_size = min(row.size for row in valid_rows)
        max_size = max(row.size for row in valid_rows)
    else:
        min_size, max_size = 0, 1

    def x_of(size: int) -> int:
        if max_size <= min_size:
            return x0 + plot_w // 2
        return x0 + int(((size - min_size) / (max_size - min_size)) * plot_w)

    def y_of(value: float) -> int:
        value = max(0.0, min(float(timeout_s), value))
        return y0 - int((value / float(timeout_s)) * plot_h)

    for row in valid_rows:
        value = row.ff_time_s if row.ff_time_s is not None else float(timeout_s)
        x = x_of(row.size)
        y = y_of(value)
        color = (31, 119, 180) if row.status == "solved" else (214, 39, 40)
        fill_rect(canvas, width, height, x - 2, y - 2, 5, 5, color)
        if row.status != "solved":
            draw_cross(canvas, width, height, x, y, 5, (214, 39, 40))

    write_png(output_path, width, height, canvas)


def print_summary(rows: list[BenchmarkRow]) -> None:
    solved = sum(1 for r in rows if r.status == "solved")
    timeout = sum(1 for r in rows if r.status == "timeout")
    unsolved = sum(1 for r in rows if r.status == "unsolved")
    errors = sum(1 for r in rows if r.status in {"error", "gen_error"})
    print("\nSummary:")
    print(f"  solved:   {solved}")
    print(f"  timeout:  {timeout}")
    print(f"  unsolved: {unsolved}")
    print(f"  errors:   {errors}")


def output_path(results_dir: Path, explicit: str | None, default_name: str) -> Path:
    if explicit is None:
        return results_dir / default_name
    candidate = Path(explicit)
    return candidate if candidate.is_absolute() else results_dir / candidate


def main() -> None:
    args = parse_args()

    domain_file = Path(args.domain).resolve()
    generator_file = Path(args.generator).resolve()
    results_dir = Path(args.results_dir).resolve()
    problems_dir = results_dir / "problems"

    if not domain_file.exists():
        raise FileNotFoundError(f"Domain file not found: {domain_file}")
    if args.problem_files is None and not generator_file.exists():
        raise FileNotFoundError(f"Generator file not found: {generator_file}")

    if args.sizes:
        sizes = sorted(set(parse_sizes_csv(args.sizes)))
        effective_min, effective_max = min(sizes), max(sizes)
    else:
        sizes = make_sizes(args.min_size, args.max_size, args.step)
        effective_min, effective_max = args.min_size, args.max_size

    results_dir.mkdir(parents=True, exist_ok=True)
    problems_dir.mkdir(parents=True, exist_ok=True)

    csv_path = output_path(results_dir, args.csv_out, f"benchmark_ff_part21_{effective_min}_to_{effective_max}.csv")
    txt_path = output_path(results_dir, args.txt_out, f"benchmark_ff_part21_{effective_min}_to_{effective_max}.txt")
    md_path = output_path(results_dir, args.md_out, f"benchmark_ff_part21_{effective_min}_to_{effective_max}.md")
    png_path = output_path(results_dir, args.png_out, f"benchmark_ff_part21_{effective_min}_to_{effective_max}.png")

    if args.problem_files:
        problems = load_existing_problems(args.problem_files)
        rows = run_benchmark_existing(domain_file=domain_file, problem_files=problems, timeout_s=args.timeout)
    else:
        rows = run_benchmark(
            sizes=sizes,
            domain_file=domain_file,
            generator_path=generator_file,
            problems_dir=problems_dir,
            timeout_s=args.timeout,
            drones=args.drones,
            carriers=args.carriers,
            carrier_capacity=args.carrier_capacity,
            exercise=args.exercise,
            seed=args.seed,
        )

    write_csv(rows, csv_path)
    write_txt_report(txt_path, rows, args)
    write_md_report(md_path, rows, args)
    save_png(rows, png_path, timeout_s=args.timeout, allow_basic_plots=args.allow_basic_plots)

    print_summary(rows)
    print(f"\nCSV: {csv_path}")
    print(f"TXT: {txt_path}")
    print(f"MD:  {md_path}")
    print(f"PNG: {png_path}")


if __name__ == "__main__":
    main()
