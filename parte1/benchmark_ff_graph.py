#!/usr/bin/env python3
"""Benchmark FF on increasing problem sizes and create a detailed SVG plot.

Main behavior:
- Generates instances with l=p=c=g from min-size to max-size.
- Solves each instance with FF (timeout per instance).
- Saves all outputs under a `results/` folder by default.
- Writes CSV + SVG.
- Tries to display the SVG after finishing.
"""

from __future__ import annotations

import argparse
import csv
import os
import re
import shlex
import shutil
import subprocess
import sys
import time
import webbrowser
from dataclasses import dataclass
from pathlib import Path


# Regular expression to parse FF total time from planner output.
FF_TIME_RE = re.compile(r"([0-9]+(?:\.[0-9]+)?)\s+seconds total time")

# Regular expression to count plan steps in FF output.
PLAN_LINE_RE = re.compile(r"^\s*(?:step\s+\d+:|\d+:)", re.MULTILINE)

# Robust solve/unsolve markers across FF wrappers and versions.
SOLVED_RE = re.compile(r"found legal plan as follows", re.IGNORECASE)
UNSOLVABLE_RE = re.compile(r"problem proven unsolvable|goal can be simplified to false", re.IGNORECASE)


@dataclass
class BenchmarkRow:
    """One row of benchmark data for one complexity value."""

    size: int
    status: str
    solved: bool
    ff_time_s: float | None
    wall_time_s: float
    plan_steps: int | None
    problem_file: str
    solver_backend: str
    error_excerpt: str | None


def parse_args() -> argparse.Namespace:
    """Read command-line options."""
    parser = argparse.ArgumentParser(description="Run FF benchmark and plot results")

    # Complexity range: by default the script runs up to complexity 60.
    parser.add_argument("--min-size", type=int, default=2, help="minimum complexity value")
    parser.add_argument("--max-size", type=int, default=60, help="maximum complexity value")
    parser.add_argument("--step", type=int, default=1, help="increment between complexity values")
    parser.add_argument(
        "--sizes",
        default=None,
        help="legacy mode: comma-separated list of sizes, e.g. 2,3,5,7,10,15",
    )

    # Planner and generator settings.
    parser.add_argument("--timeout", type=int, default=60, help="timeout per instance in seconds")
    parser.add_argument("--domain", default="dronedomain.pddl", help="path to domain file")
    parser.add_argument("--generator", default="generate-problem.py", help="problem generator script")

    # Output layout: everything is saved under results/ by default.
    parser.add_argument("--results-dir", default="results", help="folder where outputs are saved")
    parser.add_argument(
        "--csv-out",
        default=None,
        help="legacy/custom CSV filename (relative paths are saved inside results-dir)",
    )
    parser.add_argument(
        "--svg-out",
        default=None,
        help="legacy/custom SVG filename (relative paths are saved inside results-dir)",
    )

    # Plot display behavior.
    parser.add_argument(
        "--no-show",
        action="store_true",
        help="do not try to open the SVG after generation",
    )

    # Optional fixed seed. We derive per-size seed by adding complexity value.
    parser.add_argument("--seed-base", type=int, default=0, help="base seed (use -1 to disable)")

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
    """Create a list of complexities to benchmark."""
    if min_size < 1:
        raise ValueError("--min-size must be >= 1")
    if max_size < min_size:
        raise ValueError("--max-size must be >= --min-size")
    if step < 1:
        raise ValueError("--step must be >= 1")

    return list(range(min_size, max_size + 1, step))


def parse_sizes_csv(raw_sizes: str) -> list[int]:
    """Parse --sizes list, e.g. '2,3,5,7'."""
    values: list[int] = []
    for token in raw_sizes.split(","):
        token = token.strip()
        if not token:
            continue
        values.append(int(token))
    if not values:
        raise ValueError("--sizes was provided but no valid integers were found")
    return values


def run_command(
    cmd: list[str], cwd: Path | None = None, timeout_s: int | None = None
) -> tuple[int, str, bool]:
    """Run a subprocess and capture all output.

    Returns:
    - return code
    - combined stdout/stderr text
    - timed_out flag
    """
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
        # If the runtime returns bytes, decode safely.
        if isinstance(out, bytes):
            out = out.decode(errors="replace")
        return 124, out, True
    except FileNotFoundError:
        return 127, f"command not found: {cmd[0]}", False


def make_error_excerpt(text: str, max_lines: int = 6) -> str:
    """Create a short single-line error excerpt from command output."""
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    if not lines:
        return "no output"
    excerpt = " | ".join(lines[:max_lines])
    # Keep logs compact.
    return excerpt[:500]


def problem_file_name(size: int) -> str:
    """Build the expected generated problem filename for one size."""
    return f"drone_problem_d1_r0_l{size}_p{size}_c{size}_g{size}_ct2.pddl"


def generate_problem(
    size: int,
    generator_path: Path,
    problems_dir: Path,
    seed_base: int | None,
) -> tuple[bool, Path, str]:
    """Generate one problem file using the configured generator."""
    output_path = problems_dir / problem_file_name(size)

    cmd = [
        sys.executable,
        str(generator_path),
        "-d",
        "1",
        "-r",
        "0",
        "-l",
        str(size),
        "-p",
        str(size),
        "-c",
        str(size),
        "-g",
        str(size),
    ]

    # Use deterministic per-size seeds when requested.
    # NOTE: original `generate-problem.py` does not support --seed.
    if seed_base is not None and generator_path.name != "generate-problem.py":
        cmd += ["--seed", str(seed_base + size)]

    # The original generators write output in current working directory.
    # We run inside `problems_dir` so generated files are kept under results/.
    code, out, timed_out = run_command(cmd, cwd=problems_dir)
    ok = (not timed_out) and code == 0 and output_path.exists()
    return ok, output_path, out


def parse_ff_output(text: str) -> tuple[bool, float | None, int | None]:
    """Parse solved flag, planner time, and plan length from FF text output."""
    solved = SOLVED_RE.search(text) is not None

    ff_time = None
    time_match = FF_TIME_RE.search(text)
    if time_match:
        ff_time = float(time_match.group(1))

    plan_steps = None
    if solved:
        # Count each line that corresponds to one plan action.
        plan_steps = len(PLAN_LINE_RE.findall(text))

    return solved, ff_time, plan_steps


def run_ff(domain_file: Path, problem_file: Path, timeout_s: int) -> BenchmarkRow:
    """Run FF for one generated problem and return one benchmark row."""
    # Keep both PDDL files local to planner cwd to avoid wrapper/path quirks.
    planner_cwd = problem_file.parent
    domain_local = planner_cwd / "__benchmark_domain__.pddl"
    try:
        if domain_local.is_symlink() or domain_local.exists():
            domain_local.unlink()
        domain_local.symlink_to(domain_file.resolve())
    except OSError:
        # Fallback when symlinks are unavailable in the environment.
        shutil.copyfile(domain_file.resolve(), domain_local)

    domain_arg = domain_local.name
    problem_arg = problem_file.name

    # Try planutils first (portable when ff is installed through planutils).
    attempts: list[tuple[str, list[str]]] = [
        ("planutils", ["planutils", "run", "ff", "--", domain_arg, problem_arg]),
        # Fallback: direct ff binary, useful when planutils wrapper fails.
        ("ff", ["ff", domain_arg, problem_arg]),
    ]

    size = extract_size_from_name(problem_file.name)
    last_error_excerpt: str | None = None
    total_wall_time = 0.0

    for backend_name, cmd in attempts:
        start = time.perf_counter()
        code, out, timed_out = run_command(cmd, cwd=planner_cwd, timeout_s=timeout_s)
        attempt_wall_time = time.perf_counter() - start
        total_wall_time += attempt_wall_time

        solved, ff_time, plan_steps = parse_ff_output(out)
        unsolvable = UNSOLVABLE_RE.search(out) is not None

        # Some wrappers return code 0 but alter stdout formatting, so treat this as solved.
        if (not solved) and code == 0 and (ff_time is not None) and (not unsolvable):
            solved = True

        if timed_out:
            return BenchmarkRow(
                size=size,
                status="timeout",
                solved=False,
                ff_time_s=None,
                wall_time_s=attempt_wall_time,
                plan_steps=None,
                problem_file=str(problem_file),
                solver_backend=backend_name,
                error_excerpt=None,
            )

        if solved:
            return BenchmarkRow(
                size=size,
                status="solved",
                solved=True,
                ff_time_s=ff_time,
                wall_time_s=attempt_wall_time,
                plan_steps=plan_steps,
                problem_file=str(problem_file),
                solver_backend=backend_name,
                error_excerpt=None,
            )

        # Keep short output for user diagnosis if both backends fail.
        last_error_excerpt = make_error_excerpt(out)

        # If command executable is missing, subprocess returns 127-ish behavior inside shell,
        # but here we already captured it; continue to next backend.
        _ = code

    # Both attempts failed without timeout/solution.
    return BenchmarkRow(
        size=size,
        status="error(1)",
        solved=False,
        ff_time_s=None,
        wall_time_s=total_wall_time,
        plan_steps=None,
        problem_file=str(problem_file),
        solver_backend="none",
        error_excerpt=last_error_excerpt,
    )


def extract_size_from_name(name: str) -> int:
    """Extract complexity from filenames like ..._l40_p40_c40_g40_...."""
    marker = "_l"
    start = name.find(marker)
    if start == -1:
        return -1
    start += len(marker)
    end = name.find("_", start)
    if end == -1:
        return -1
    return int(name[start:end])


def save_csv(rows: list[BenchmarkRow], csv_path: Path) -> None:
    """Save all benchmark rows in CSV format."""
    with csv_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
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
                    "" if row.error_excerpt is None else row.error_excerpt,
                    row.problem_file,
                ]
            )


def scale(value: float, in_min: float, in_max: float, out_min: float, out_max: float) -> float:
    """Linear scaling helper used by the SVG plotting logic."""
    if in_max <= in_min:
        # Avoid division by zero when all values are equal.
        return (out_min + out_max) / 2.0
    return out_min + (value - in_min) * (out_max - out_min) / (in_max - in_min)


def save_svg(rows: list[BenchmarkRow], svg_path: Path, timeout_s: int) -> None:
    """Create a high-resolution SVG plot with dense ticks and per-point labels."""
    width, height = 2600, 1500  # high definition canvas
    left, right, top, bottom = 130, 80, 100, 160

    plot_w = width - left - right
    plot_h = height - top - bottom

    x0, y0 = left, top + plot_h
    x1, y1 = left + plot_w, top

    # X range is exactly the configured sizes present in rows.
    x_values = [row.size for row in rows]
    x_min = min(x_values) if x_values else 0
    x_max = max(x_values) if x_values else 1

    # Y range uses timeout as upper bound so timeout points are visible at top.
    y_min = 0.0
    y_max = float(timeout_s)

    # Build a single plotting value per row:
    # - solved -> FF reported time
    # - unsolved -> timeout value (for visibility)
    plot_points: list[tuple[float, float, BenchmarkRow]] = []
    for row in rows:
        y_value = row.ff_time_s if row.ff_time_s is not None else float(timeout_s)
        px = scale(float(row.size), float(x_min), float(x_max), float(left), float(left + plot_w))
        py = scale(y_value, y_min, y_max, float(top + plot_h), float(top))
        plot_points.append((px, py, row))

    lines: list[str] = []
    lines.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}">')
    lines.append('<rect x="0" y="0" width="100%" height="100%" fill="#f8fafc"/>')

    # Title and subtitle.
    lines.append(
        '<text x="130" y="52" font-family="Arial" font-size="34" fill="#0f172a">'
        'FF Benchmark (Complexity vs Time)</text>'
    )
    lines.append(
        '<text x="130" y="84" font-family="Arial" font-size="20" fill="#334155">'
        'Complexity = l=p=c=g. Unsolved instances are shown at timeout line.</text>'
    )

    # Axes.
    lines.append(f'<line x1="{x0}" y1="{y0}" x2="{x1}" y2="{y0}" stroke="#334155" stroke-width="3"/>')
    lines.append(f'<line x1="{x0}" y1="{y0}" x2="{x0}" y2="{y1}" stroke="#334155" stroke-width="3"/>')

    # X-axis ticks: one tick per complexity value (every point visible).
    for size in x_values:
        px = scale(float(size), float(x_min), float(x_max), float(left), float(left + plot_w))
        lines.append(f'<line x1="{px:.2f}" y1="{y0}" x2="{px:.2f}" y2="{y0 + 14}" stroke="#334155" stroke-width="2"/>')
        lines.append(
            f'<text x="{px:.2f}" y="{y0 + 42}" text-anchor="middle" '
            f'font-family="Arial" font-size="18" fill="#334155">{size}</text>'
        )

    # Y-axis ticks: one segment per second for maximum readability.
    for sec in range(0, timeout_s + 1):
        py = scale(float(sec), y_min, y_max, float(top + plot_h), float(top))

        # Longer tick every 5 seconds to improve visual grouping.
        tick_len = 12 if sec % 5 == 0 else 6
        grid_color = "#cbd5e1" if sec % 5 == 0 else "#e2e8f0"
        grid_width = 1.4 if sec % 5 == 0 else 0.8

        lines.append(f'<line x1="{x0 - tick_len}" y1="{py:.2f}" x2="{x0}" y2="{py:.2f}" stroke="#334155" stroke-width="1"/>')
        lines.append(f'<line x1="{x0}" y1="{py:.2f}" x2="{x1}" y2="{py:.2f}" stroke="{grid_color}" stroke-width="{grid_width}"/>')

        # Label only every 5s to avoid text clutter.
        if sec % 5 == 0:
            lines.append(
                f'<text x="{x0 - 18}" y="{py + 6:.2f}" text-anchor="end" '
                f'font-family="Arial" font-size="16" fill="#334155">{sec}</text>'
            )

    # Draw line through all points in complexity order.
    polyline = " ".join(f"{px:.2f},{py:.2f}" for px, py, _ in plot_points)
    lines.append(f'<polyline points="{polyline}" fill="none" stroke="#2563eb" stroke-width="3"/>')

    # Draw each point and add label.
    for px, py, row in plot_points:
        if row.solved:
            # Solved points in blue.
            lines.append(f'<circle cx="{px:.2f}" cy="{py:.2f}" r="6" fill="#1d4ed8"/>')
            label = f"{row.ff_time_s:.2f}s"
            label_color = "#1e293b"
        else:
            # Unsolved points shown as red cross at timeout level.
            lines.append(f'<line x1="{px - 7:.2f}" y1="{py - 7:.2f}" x2="{px + 7:.2f}" y2="{py + 7:.2f}" stroke="#b91c1c" stroke-width="3"/>')
            lines.append(f'<line x1="{px - 7:.2f}" y1="{py + 7:.2f}" x2="{px + 7:.2f}" y2="{py - 7:.2f}" stroke="#b91c1c" stroke-width="3"/>')
            label = "timeout"
            label_color = "#991b1b"

        lines.append(
            f'<text x="{px:.2f}" y="{py - 14:.2f}" text-anchor="middle" '
            f'font-family="Arial" font-size="14" fill="{label_color}">{label}</text>'
        )

    # Axis labels.
    lines.append(
        f'<text x="{(x0 + x1) / 2:.2f}" y="{height - 60}" text-anchor="middle" '
        'font-family="Arial" font-size="24" fill="#0f172a">Complexity (l=p=c=g)</text>'
    )
    lines.append(
        f'<text x="42" y="{(y0 + y1) / 2:.2f}" text-anchor="middle" '
        'font-family="Arial" font-size="24" fill="#0f172a" '
        f'transform="rotate(-90,42,{(y0 + y1) / 2:.2f})">Time (seconds)</text>'
    )

    lines.append("</svg>")
    svg_path.write_text("\n".join(lines), encoding="utf-8")


def show_svg(svg_path: Path) -> None:
    """Try to display the SVG after execution.

    This tries browser opening first, then OS-specific open commands.
    """
    opened = webbrowser.open(svg_path.resolve().as_uri())
    if opened:
        return

    # Fallbacks for common operating systems.
    try:
        if sys.platform.startswith("linux"):
            subprocess.Popen(
                ["xdg-open", str(svg_path)],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
        elif sys.platform == "darwin":
            subprocess.Popen(
                ["open", str(svg_path)],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
        elif os.name == "nt":
            os.startfile(str(svg_path))  # type: ignore[attr-defined]
    except (FileNotFoundError, OSError):
        # If auto-open is not available in this environment, continue silently.
        print(f"Could not auto-open plot. Open it manually: {svg_path}")


def run_benchmark(
    sizes: list[int],
    domain_file: Path,
    generator_file: Path,
    problems_dir: Path,
    timeout_s: int,
    seed_base: int | None,
) -> list[BenchmarkRow]:
    """Run generation + FF for each complexity value."""
    rows: list[BenchmarkRow] = []

    for size in sizes:
        ok, problem_path, gen_out = generate_problem(size, generator_file, problems_dir, seed_base)

        if not ok:
            rows.append(
                BenchmarkRow(
                    size=size,
                    status="generator_error",
                    solved=False,
                    ff_time_s=None,
                    wall_time_s=0.0,
                    plan_steps=None,
                    problem_file=str(problem_path),
                    solver_backend="generator",
                    error_excerpt=make_error_excerpt(gen_out),
                )
            )
            print(f"[size={size}] generator error")
            continue

        row = run_ff(domain_file, problem_path, timeout_s)
        rows.append(row)

        ff_text = "-" if row.ff_time_s is None else f"{row.ff_time_s:.2f}"
        steps_text = "-" if row.plan_steps is None else str(row.plan_steps)
        print(
            f"[size={size}] status={row.status} "
            f"ff_time={ff_text} wall={row.wall_time_s:.4f}s steps={steps_text}"
        )
        if row.status.startswith("error") and row.error_excerpt:
            print(f"  error detail: {row.error_excerpt}")

    return rows


def print_summary(rows: list[BenchmarkRow]) -> None:
    """Print quick summary to terminal."""
    solved_rows = [r for r in rows if r.solved]

    print("\nSummary")
    print(f"- Total instances: {len(rows)}")
    print(f"- Solved instances: {len(solved_rows)}")

    if solved_rows:
        max_solved = max(r.size for r in solved_rows)
        slowest = max(solved_rows, key=lambda r: r.ff_time_s if r.ff_time_s is not None else r.wall_time_s)
        slowest_time = slowest.ff_time_s if slowest.ff_time_s is not None else slowest.wall_time_s

        print(f"- Largest solved complexity: {max_solved}")
        print(f"- Slowest solved run: size {slowest.size}, time {slowest_time:.2f}s")


def main() -> None:
    """Main script workflow."""
    args = parse_args()

    # Support both new range-based interface and legacy --sizes list.
    if args.sizes is not None:
        sizes = parse_sizes_csv(args.sizes)
        effective_min = min(sizes)
        effective_max = max(sizes)
    else:
        sizes = make_sizes(args.min_size, args.max_size, args.step)
        effective_min = args.min_size
        effective_max = args.max_size

    domain_file = Path(args.domain).resolve()
    generator_file = Path(args.generator).resolve()

    if not domain_file.exists():
        raise FileNotFoundError(f"Domain file not found: {domain_file}")
    if not generator_file.exists():
        raise FileNotFoundError(f"Generator file not found: {generator_file}")

    # Create results folders.
    results_dir = Path(args.results_dir).resolve()
    problems_dir = results_dir / "problems"
    results_dir.mkdir(parents=True, exist_ok=True)
    problems_dir.mkdir(parents=True, exist_ok=True)

    # Build output paths inside results/ by default.
    # If user passes legacy --csv-out / --svg-out:
    # - absolute paths are used as-is
    # - relative paths are stored inside results_dir
    if args.csv_out is None:
        csv_path = results_dir / f"benchmark_ff_{effective_min}_to_{effective_max}.csv"
    else:
        csv_candidate = Path(args.csv_out)
        csv_path = csv_candidate if csv_candidate.is_absolute() else results_dir / csv_candidate

    if args.svg_out is None:
        svg_path = results_dir / f"benchmark_ff_{effective_min}_to_{effective_max}.svg"
    else:
        svg_candidate = Path(args.svg_out)
        svg_path = svg_candidate if svg_candidate.is_absolute() else results_dir / svg_candidate

    # Disable deterministic seeds when seed-base is negative.
    seed_base = None if args.seed_base < 0 else args.seed_base

    rows = run_benchmark(
        sizes=sizes,
        domain_file=domain_file,
        generator_file=generator_file,
        problems_dir=problems_dir,
        timeout_s=args.timeout,
        seed_base=seed_base,
    )

    save_csv(rows, csv_path)
    save_svg(rows, svg_path, timeout_s=args.timeout)
    print_summary(rows)

    print(f"\nCSV saved to: {csv_path}")
    print(f"SVG saved to: {svg_path}")

    # Try to display the plot after execution unless user disabled it.
    if not args.no_show:
        show_svg(svg_path)


if __name__ == "__main__":
    main()
