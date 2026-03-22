#!/usr/bin/env python3
"""Minimal benchmark runner for Practice 1.3 using pyperplan via planutils.

This script is intended to run inside WSL where `planutils` is available.
It executes all sections from exercise 1.3, writes all data to one .txt file,
and exports three PNG plots.
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
    from matplotlib.lines import Line2D
    from matplotlib.patches import Patch

    HAVE_MATPLOTLIB = True
except Exception:
    HAVE_MATPLOTLIB = False


SEARCH_TIME_RE = re.compile(r"Search time:\s*([0-9]+(?:\.[0-9]+)?)", re.IGNORECASE)
TOTAL_TIME_RE = re.compile(r"Total time:\s*([0-9]+(?:\.[0-9]+)?)", re.IGNORECASE)
PLAN_LENGTH_RE = re.compile(r"Plan length:\s*([0-9]+)", re.IGNORECASE)
UNSOLVED_RE = re.compile(
    r"(no solution could be found|task unsolvable|problem unsolvable|goal not reachable)",
    re.IGNORECASE,
)
UNSUPPORTED_RE = re.compile(
    r"(invalid choice|unknown heuristic|unknown search|argument -s: invalid choice|argument -H: invalid choice)",
    re.IGNORECASE,
)
SIZE_RE = re.compile(r"_l([0-9]+)_")


@dataclass
class RunRow:
    section: str
    algorithm: str
    search: str
    heuristic: str
    size: int
    problem_file: str
    status: str
    solved: bool
    search_time_s: float | None
    wall_time_s: float
    plan_length: int | None
    optimal: str
    error_excerpt: str


@dataclass
class GenerationRow:
    size: int
    problem_file: str
    status: str
    wall_time_s: float
    error_excerpt: str


RUN_TABLE_HEADERS = [
    "section",
    "algorithm",
    "search",
    "heuristic",
    "size",
    "status",
    "solved",
    "search_time_s",
    "wall_time_s",
    "plan_length",
    "optimal",
    "problem_file",
    "error_excerpt",
]

RUN_COL_PROBLEM_FILE = RUN_TABLE_HEADERS.index("problem_file")
RUN_COL_ERROR_EXCERPT = RUN_TABLE_HEADERS.index("error_excerpt")
ERROR_EXCERPT_MD_MAX_LEN = 120
CERTIFIABLY_OPTIMAL_ALGORITHMS = {"BFS", "IDS", "A*+hMAX"}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Benchmark pyperplan for exercise 1.3")
    parser.add_argument("--min-size", type=int, default=2, help="minimum size for l=p=c=g")
    parser.add_argument("--max-size", type=int, default=40, help="maximum size for l=p=c=g")
    parser.add_argument("--step", type=int, default=2, help="size step")
    parser.add_argument("--timeout", type=int, default=60, help="timeout per run in seconds")
    parser.add_argument("--domain", default="dronedomain.pddl", help="path to domain file")
    parser.add_argument("--generator", default="generate-problem.py", help="path to generator script")
    parser.add_argument("--results-dir", default="results", help="output folder")
    parser.add_argument(
        "--allow-basic-plots",
        action="store_true",
        help="allow basic PNG plots without labels/legend when matplotlib is unavailable",
    )
    parser.add_argument(
        "--problem-files",
        nargs="*",
        default=None,
        help="optional existing problem .pddl files; if set, generation is skipped",
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


def problem_file_name(size: int) -> str:
    return f"drone_problem_d1_r0_l{size}_p{size}_c{size}_g{size}_ct2.pddl"


def extract_size(path: Path, fallback: int) -> int:
    match = SIZE_RE.search(path.name)
    if match is None:
        return fallback
    return int(match.group(1))


def run_command(
    cmd: list[str], timeout_s: int | None = None, cwd: Path | None = None
) -> tuple[int, str, bool, float]:
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
        wall_time = time.perf_counter() - start
        return proc.returncode, proc.stdout, False, wall_time
    except subprocess.TimeoutExpired as exc:
        out = exc.stdout or ""
        if isinstance(out, bytes):
            out = out.decode(errors="replace")
        wall_time = time.perf_counter() - start
        return 124, out, True, wall_time
    except FileNotFoundError as exc:
        wall_time = time.perf_counter() - start
        return 127, str(exc), False, wall_time


def make_error_excerpt(text: str, max_lines: int = 5) -> str:
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    if not lines:
        return ""
    return " | ".join(lines[:max_lines])[:500]


def parse_time(output: str) -> float | None:
    match = SEARCH_TIME_RE.search(output)
    if match:
        return float(match.group(1))
    match = TOTAL_TIME_RE.search(output)
    if match:
        return float(match.group(1))
    return None


def parse_plan_length(output: str) -> int | None:
    match = PLAN_LENGTH_RE.search(output)
    if match:
        return int(match.group(1))
    return None


def choose_alias(candidates: list[str], help_text: str, help_ok: bool) -> str | None:
    if not help_ok:
        return candidates[0]
    lowered = help_text.lower()
    for cand in candidates:
        if re.search(rf"\b{re.escape(cand.lower())}\b", lowered):
            return cand
    return None


def resolve_aliases(base_cmd: list[str]) -> tuple[dict[str, str | None], dict[str, str | None], str]:
    help_cmd = base_cmd + ["--help"]
    code, out, timed_out, _ = run_command(help_cmd, timeout_s=20)
    help_ok = (not timed_out) and code == 0 and bool(out.strip())

    search_candidates = {
        "BFS": ["bfs"],
        "IDS": ["ids"],
        "ASTAR": ["astar"],
        "GBFS": ["gbfs", "gbf"],
        "EHC": ["ehc", "ehs"],
    }
    heuristic_candidates = {
        "BLIND": ["blind"],
        "HMAX": ["hmax"],
        "HADD": ["hadd"],
        "HFF": ["hff"],
        "LANDMARK": ["landmark"],
        "LMCUT": ["lmcut"],
    }

    search_aliases = {key: choose_alias(vals, out, help_ok) for key, vals in search_candidates.items()}
    heuristic_aliases = {key: choose_alias(vals, out, help_ok) for key, vals in heuristic_candidates.items()}
    return search_aliases, heuristic_aliases, out


def generate_problems(
    sizes: list[int], generator_path: Path, output_dir: Path, timeout_s: int
) -> tuple[list[tuple[int, Path]], list[GenerationRow]]:
    output_dir.mkdir(parents=True, exist_ok=True)
    ok_problems: list[tuple[int, Path]] = []
    gen_rows: list[GenerationRow] = []

    for size in sizes:
        problem_path = output_dir / problem_file_name(size)
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
        code, out, timed_out, wall = run_command(cmd, timeout_s=timeout_s, cwd=output_dir)
        if timed_out:
            gen_rows.append(
                GenerationRow(
                    size=size,
                    problem_file=str(problem_path),
                    status="timeout",
                    wall_time_s=wall,
                    error_excerpt="",
                )
            )
            print(f"[generate size={size}] timeout")
            continue

        if code == 0 and problem_path.exists():
            ok_problems.append((size, problem_path.resolve()))
            gen_rows.append(
                GenerationRow(
                    size=size,
                    problem_file=str(problem_path.resolve()),
                    status="ok",
                    wall_time_s=wall,
                    error_excerpt="",
                )
            )
            print(f"[generate size={size}] ok")
        else:
            gen_rows.append(
                GenerationRow(
                    size=size,
                    problem_file=str(problem_path),
                    status="error",
                    wall_time_s=wall,
                    error_excerpt=make_error_excerpt(out),
                )
            )
            print(f"[generate size={size}] error")

    return ok_problems, gen_rows


def load_existing_problems(problem_files: list[str]) -> list[tuple[int, Path]]:
    problems: list[tuple[int, Path]] = []
    for idx, raw in enumerate(problem_files, start=1):
        path = Path(raw).resolve()
        if not path.exists():
            raise FileNotFoundError(f"Problem file not found: {path}")
        size = extract_size(path, idx)
        problems.append((size, path))
    problems.sort(key=lambda item: item[0])
    return problems


def run_pyperplan_case(
    section: str,
    algorithm: str,
    search: str,
    heuristic: str,
    size: int,
    domain_file: Path,
    problem_file: Path,
    timeout_s: int,
    base_cmd: list[str],
    optimal: str,
) -> RunRow:
    planner_cwd = domain_file.parent.resolve()
    domain_arg = domain_file.name

    try:
        problem_arg = str(problem_file.resolve().relative_to(planner_cwd))
    except ValueError:
        local_problem = planner_cwd / "__pyperplan_problem__.pddl"
        if local_problem.exists() or local_problem.is_symlink():
            local_problem.unlink()
        try:
            local_problem.symlink_to(problem_file.resolve())
        except OSError:
            shutil.copyfile(problem_file.resolve(), local_problem)
        problem_arg = local_problem.name

    cmd = base_cmd + ["-s", search]
    if heuristic:
        cmd += ["-H", heuristic]
    cmd += [domain_arg, problem_arg]

    code, out, timed_out, wall = run_command(cmd, timeout_s=timeout_s, cwd=planner_cwd)
    if timed_out:
        return RunRow(
            section=section,
            algorithm=algorithm,
            search=search,
            heuristic=heuristic,
            size=size,
            problem_file=str(problem_file),
            status="timeout",
            solved=False,
            search_time_s=None,
            wall_time_s=wall,
            plan_length=None,
            optimal=optimal,
            error_excerpt="",
        )

    parsed_time = parse_time(out)
    plan_length = parse_plan_length(out)
    unsolved = UNSOLVED_RE.search(out) is not None
    unsupported = UNSUPPORTED_RE.search(out) is not None

    if unsupported:
        status = "unsupported"
        solved = False
    elif plan_length is not None:
        status = "solved"
        solved = True
    elif unsolved:
        status = "unsolved"
        solved = False
    elif code == 0:
        status = "unsolved"
        solved = False
    else:
        status = "error"
        solved = False

    effective_time = parsed_time if parsed_time is not None else wall
    excerpt = make_error_excerpt(out) if status in {"error", "unsupported"} else ""
    return RunRow(
        section=section,
        algorithm=algorithm,
        search=search,
        heuristic=heuristic,
        size=size,
        problem_file=str(problem_file),
        status=status,
        solved=solved,
        search_time_s=effective_time,
        wall_time_s=wall,
        plan_length=plan_length,
        optimal=optimal,
        error_excerpt=excerpt,
    )


def run_section_131(
    problems: list[tuple[int, Path]],
    domain_file: Path,
    timeout_s: int,
    base_cmd: list[str],
    search_aliases: dict[str, str | None],
    heuristic_aliases: dict[str, str | None],
) -> list[RunRow]:
    rows: list[RunRow] = []
    configs = [
        ("BFS", "BFS", "", "yes"),
        ("IDS", "IDS", "", "yes"),
        ("A*+hMAX", "ASTAR", "HMAX", "yes"),
        ("GBFS+hMAX", "GBFS", "HMAX", "no"),
    ]

    for size, problem in problems:
        for algorithm, search_key, heuristic_key, optimal in configs:
            search_alias = search_aliases.get(search_key)
            heuristic_alias = "" if not heuristic_key else (heuristic_aliases.get(heuristic_key) or "")

            if search_alias is None or (heuristic_key and not heuristic_alias):
                row = RunRow(
                    section="1.3.1",
                    algorithm=algorithm,
                    search=search_alias or "",
                    heuristic=heuristic_alias,
                    size=size,
                    problem_file=str(problem),
                    status="unsupported",
                    solved=False,
                    search_time_s=None,
                    wall_time_s=0.0,
                    plan_length=None,
                    optimal=optimal,
                    error_excerpt="alias not found in pyperplan --help",
                )
            else:
                row = run_pyperplan_case(
                    section="1.3.1",
                    algorithm=algorithm,
                    search=search_alias,
                    heuristic=heuristic_alias,
                    size=size,
                    domain_file=domain_file,
                    problem_file=problem,
                    timeout_s=timeout_s,
                    base_cmd=base_cmd,
                    optimal=optimal,
                )

            rows.append(row)
            t = "-" if row.search_time_s is None else f"{row.search_time_s:.4f}"
            print(f"[1.3.1 size={size} {algorithm}] status={row.status} time={t}")
    return assign_proven_plan_optimality(rows)


def largest_solved(rows: list[RunRow], algorithm: str) -> RunRow | None:
    solved = [r for r in rows if r.algorithm == algorithm and r.status == "solved"]
    if not solved:
        return None
    return max(solved, key=lambda r: r.size)


def assign_proven_plan_optimality(rows: list[RunRow]) -> list[RunRow]:
    rows_by_problem: dict[str, list[RunRow]] = {}
    for row in rows:
        rows_by_problem.setdefault(row.problem_file, []).append(row)

    for group in rows_by_problem.values():
        certified_lengths = [
            row.plan_length
            for row in group
            if row.algorithm in CERTIFIABLY_OPTIMAL_ALGORITHMS
            and row.status == "solved"
            and row.plan_length is not None
        ]
        optimal_length = min(certified_lengths) if certified_lengths else None

        for row in group:
            if row.status != "solved" or row.plan_length is None or optimal_length is None:
                row.optimal = ""
            elif row.plan_length == optimal_length:
                row.optimal = "yes"
            else:
                row.optimal = "no"

    return rows


def run_section_132(
    anchor_row: RunRow | None,
    domain_file: Path,
    timeout_s: int,
    base_cmd: list[str],
    search_aliases: dict[str, str | None],
    heuristic_aliases: dict[str, str | None],
) -> list[RunRow]:
    if anchor_row is None:
        return []

    problem = Path(anchor_row.problem_file)
    size = anchor_row.size
    rows: list[RunRow] = []
    combos = [
        ("GBFS", "GBFS", "HMAX"),
        ("GBFS", "GBFS", "HADD"),
        ("GBFS", "GBFS", "HFF"),
        ("GBFS", "GBFS", "LANDMARK"),
        ("EHC", "EHC", "HMAX"),
        ("EHC", "EHC", "HADD"),
        ("EHC", "EHC", "HFF"),
        ("EHC", "EHC", "LANDMARK"),
    ]

    for algorithm, search_key, heuristic_key in combos:
        search_alias = search_aliases.get(search_key)
        heuristic_alias = heuristic_aliases.get(heuristic_key) or ""

        if search_alias is None or not heuristic_alias:
            row = RunRow(
                section="1.3.2",
                algorithm=algorithm,
                search=search_alias or "",
                heuristic=heuristic_alias,
                size=size,
                problem_file=str(problem),
                status="unsupported",
                solved=False,
                search_time_s=None,
                wall_time_s=0.0,
                plan_length=None,
                optimal="no",
                error_excerpt="alias not found in pyperplan --help",
            )
        else:
            row = run_pyperplan_case(
                section="1.3.2",
                algorithm=algorithm,
                search=search_alias,
                heuristic=heuristic_alias,
                size=size,
                domain_file=domain_file,
                problem_file=problem,
                timeout_s=timeout_s,
                base_cmd=base_cmd,
                optimal="no",
            )

        rows.append(row)
        t = "-" if row.search_time_s is None else f"{row.search_time_s:.4f}"
        print(f"[1.3.2 {algorithm}/{heuristic_key}] status={row.status} time={t}")
    return rows


def run_section_133(
    anchor_row: RunRow | None,
    domain_file: Path,
    timeout_s: int,
    base_cmd: list[str],
    search_aliases: dict[str, str | None],
    heuristic_aliases: dict[str, str | None],
) -> list[RunRow]:
    if anchor_row is None:
        return []

    problem = Path(anchor_row.problem_file)
    size = anchor_row.size
    rows: list[RunRow] = []
    configs = [
        ("BFS", "BFS", "", "yes"),
        ("IDS", "IDS", "", "yes"),
        ("A*+hMAX", "ASTAR", "HMAX", "yes"),
        ("A*+lmcut", "ASTAR", "LMCUT", "yes"),
        ("A*+blind", "ASTAR", "BLIND", "yes"),
        ("A*+landmark", "ASTAR", "LANDMARK", "yes"),
    ]

    for algorithm, search_key, heuristic_key, optimal in configs:
        search_alias = search_aliases.get(search_key)
        heuristic_alias = "" if not heuristic_key else (heuristic_aliases.get(heuristic_key) or "")

        if search_alias is None or (heuristic_key and not heuristic_alias):
            row = RunRow(
                section="1.3.3",
                algorithm=algorithm,
                search=search_alias or "",
                heuristic=heuristic_alias,
                size=size,
                problem_file=str(problem),
                status="unsupported",
                solved=False,
                search_time_s=None,
                wall_time_s=0.0,
                plan_length=None,
                optimal=optimal,
                error_excerpt="alias not found in pyperplan --help",
            )
        else:
            row = run_pyperplan_case(
                section="1.3.3",
                algorithm=algorithm,
                search=search_alias,
                heuristic=heuristic_alias,
                size=size,
                domain_file=domain_file,
                problem_file=problem,
                timeout_s=timeout_s,
                base_cmd=base_cmd,
                optimal=optimal,
            )

        rows.append(row)
        t = "-" if row.search_time_s is None else f"{row.search_time_s:.4f}"
        print(f"[1.3.3 {algorithm}] status={row.status} time={t}")
    return assign_proven_plan_optimality(rows)


def summarize_131(rows: list[RunRow]) -> list[dict[str, str]]:
    order = ["BFS", "IDS", "A*+hMAX", "GBFS+hMAX"]
    summary: list[dict[str, str]] = []
    for algorithm in order:
        best = largest_solved(rows, algorithm)
        if best is None:
            summary.append(
                {
                    "algorithm": algorithm,
                    "max_solved_size": "-",
                    "time_s": "-",
                    "plan_length": "-",
                    "optimal": "n/a",
                }
            )
            continue

        summary.append(
            {
                "algorithm": algorithm,
                "max_solved_size": str(best.size),
                "time_s": f"{best.search_time_s:.4f}" if best.search_time_s is not None else "-",
                "plan_length": str(best.plan_length) if best.plan_length is not None else "-",
                "optimal": best.optimal,
            }
        )
    return summary


def best_optimal_row(rows: list[RunRow]) -> RunRow | None:
    candidates = [r for r in rows if r.status == "solved" and r.optimal == "yes" and r.search_time_s is not None]
    if not candidates:
        return None
    return min(candidates, key=lambda r: r.search_time_s if r.search_time_s is not None else float("inf"))


def time_for_plot(row: RunRow, timeout_s: int) -> float:
    if row.search_time_s is not None:
        return row.search_time_s
    return float(timeout_s)


def clamp(value: float, low: float, high: float) -> float:
    return max(low, min(high, value))


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


def save_plot_131_basic(rows: list[RunRow], output_path: Path, timeout_s: int) -> None:
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

    if rows:
        sizes = [r.size for r in rows]
        min_size = min(sizes)
        max_size = max(sizes)
    else:
        min_size, max_size = 0, 1

    def x_of(size: int) -> int:
        if max_size <= min_size:
            return x0 + plot_w // 2
        return x0 + int(((size - min_size) / (max_size - min_size)) * plot_w)

    def y_of(value: float) -> int:
        v = clamp(value, 0.0, float(timeout_s))
        return y0 - int((v / float(timeout_s)) * plot_h)

    colors = {
        "BFS": (31, 119, 180),
        "IDS": (255, 127, 14),
        "A*+hMAX": (44, 160, 44),
        "GBFS+hMAX": (148, 103, 189),
    }
    order = ["BFS", "IDS", "A*+hMAX", "GBFS+hMAX"]
    for algorithm in order:
        alg_rows = sorted([r for r in rows if r.algorithm == algorithm], key=lambda r: r.size)
        if not alg_rows:
            continue
        color = colors[algorithm]
        points: list[tuple[int, int, RunRow]] = []
        for r in alg_rows:
            x = x_of(r.size)
            y = y_of(time_for_plot(r, timeout_s))
            points.append((x, y, r))

        for idx in range(1, len(points)):
            draw_line(
                canvas,
                width,
                height,
                points[idx - 1][0],
                points[idx - 1][1],
                points[idx][0],
                points[idx][1],
                color,
            )

        for x, y, row in points:
            fill_rect(canvas, width, height, x - 2, y - 2, 5, 5, color)
            if row.status != "solved":
                draw_cross(canvas, width, height, x, y, 5, (220, 38, 38))

    write_png(output_path, width, height, canvas)


def save_bar_plot_basic(rows: list[RunRow], output_path: Path, timeout_s: int) -> None:
    width = max(900, 140 * max(1, len(rows)) + 200)
    height = 650
    left, right, top, bottom = 80, 40, 40, 80
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

    if not rows:
        write_png(output_path, width, height, canvas)
        return

    step = plot_w / len(rows)
    bar_w = max(12, int(step * 0.6))
    for idx, row in enumerate(rows):
        center_x = int(x0 + (idx + 0.5) * step)
        bar_left = center_x - bar_w // 2
        value = time_for_plot(row, timeout_s)
        v = clamp(value, 0.0, float(timeout_s))
        bar_top = y0 - int((v / float(timeout_s)) * plot_h)
        color = (31, 119, 180) if row.status == "solved" else (214, 39, 40)
        fill_rect(canvas, width, height, bar_left, bar_top, bar_w, max(1, y0 - bar_top), color)
        if row.status != "solved":
            draw_cross(canvas, width, height, center_x, max(y1 + 5, bar_top - 6), 5, (214, 39, 40))

    write_png(output_path, width, height, canvas)


def save_plot_131(rows: list[RunRow], output_path: Path, timeout_s: int) -> None:
    if not HAVE_MATPLOTLIB:
        save_plot_131_basic(rows, output_path, timeout_s)
        return

    order = ["BFS", "IDS", "A*+hMAX", "GBFS+hMAX"]
    plt.figure(figsize=(11, 6))
    for algorithm in order:
        alg_rows = sorted([r for r in rows if r.algorithm == algorithm], key=lambda r: r.size)
        if not alg_rows:
            continue
        xs = [r.size for r in alg_rows]
        ys = [time_for_plot(r, timeout_s) for r in alg_rows]
        plt.plot(xs, ys, marker="o", label=algorithm)
        for r in alg_rows:
            if r.status != "solved":
                plt.scatter([r.size], [time_for_plot(r, timeout_s)], marker="x", color="red", zorder=5)
    plt.axhline(timeout_s, color="gray", linestyle="--", linewidth=1, label=f"timeout={timeout_s}s")
    plt.xlabel("Problem size (l=p=c=g)")
    plt.ylabel("Time (s)")
    plt.title("1.3.1 - Runtime vs Problem Size")
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.tight_layout()
    plt.savefig(output_path, dpi=140)
    plt.close()


def save_bar_plot(rows: list[RunRow], output_path: Path, title: str, timeout_s: int) -> None:
    if not HAVE_MATPLOTLIB:
        _ = title
        save_bar_plot_basic(rows, output_path, timeout_s)
        return

    plt.figure(figsize=(12, 6))
    labels = [f"{r.algorithm}/{r.heuristic or '-'}" for r in rows]
    values = [time_for_plot(r, timeout_s) for r in rows]
    colors = ["#1f77b4" if r.status == "solved" else "#d62728" for r in rows]
    plt.bar(labels, values, color=colors)
    plt.axhline(timeout_s, color="gray", linestyle="--", linewidth=1, label=f"timeout={timeout_s}s")
    legend_handles = [
        Patch(facecolor="#1f77b4", label="solved"),
        Patch(facecolor="#d62728", label="not solved (timeout/error/unsolved)"),
        Line2D([0], [0], color="gray", linestyle="--", linewidth=1, label=f"timeout={timeout_s}s"),
    ]
    plt.ylabel("Time (s)")
    plt.xlabel("Search / heuristic combination")
    plt.title(title)
    plt.xticks(rotation=25, ha="right")
    plt.grid(True, axis="y", alpha=0.3)
    plt.legend(handles=legend_handles)
    plt.tight_layout()
    plt.savefig(output_path, dpi=140)
    plt.close()


def add_table(lines: list[str], title: str, headers: list[str], rows: list[list[str]]) -> None:
    lines.append(title)
    lines.append("\t".join(headers))
    for row in rows:
        lines.append("\t".join(row))
    lines.append("")


def markdown_escape(value: str) -> str:
    return value.replace("|", r"\|").replace("\n", "<br>").replace("\r", "")


def add_markdown_table(lines: list[str], title: str, headers: list[str], rows: list[list[str]]) -> None:
    lines.append(f"## {title}")
    lines.append("")
    lines.append("| " + " | ".join(markdown_escape(header) for header in headers) + " |")
    lines.append("| " + " | ".join("---" for _ in headers) + " |")
    for row in rows:
        normalized = row[: len(headers)] + [""] * max(0, len(headers) - len(row))
        lines.append("| " + " | ".join(markdown_escape(cell) for cell in normalized) + " |")
    lines.append("")


def compact_problem_path(problem_file: str, results_dir: Path) -> str:
    path = Path(problem_file)
    abs_path = path.resolve()
    for base in (results_dir.resolve(), Path.cwd().resolve()):
        try:
            return abs_path.relative_to(base).as_posix()
        except ValueError:
            continue
    return path.name or problem_file


def run_row_as_list(row: RunRow) -> list[str]:
    return [
        row.section,
        row.algorithm,
        row.search,
        row.heuristic,
        str(row.size),
        row.status,
        "yes" if row.solved else "no",
        "" if row.search_time_s is None else f"{row.search_time_s:.4f}",
        f"{row.wall_time_s:.4f}",
        "" if row.plan_length is None else str(row.plan_length),
        row.optimal,
        row.problem_file,
        row.error_excerpt,
    ]


def write_csv_table(path: Path, headers: list[str], rows: list[list[str]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as file_handle:
        writer = csv.writer(file_handle)
        writer.writerow(headers)
        writer.writerows(rows)


def write_csv_exports(results_dir: Path, rows_131: list[RunRow], rows_132: list[RunRow], rows_133: list[RunRow]) -> None:
    rows_all = rows_131 + rows_132 + rows_133
    rows_all_values = [run_row_as_list(row) for row in rows_all]
    rows_131_values = [run_row_as_list(row) for row in rows_131]
    rows_132_values = [run_row_as_list(row) for row in rows_132]
    rows_133_values = [run_row_as_list(row) for row in rows_133]

    write_csv_table(results_dir / "benchmark_pyperplan_part13_all.csv", RUN_TABLE_HEADERS, rows_all_values)
    write_csv_table(results_dir / "benchmark_pyperplan_part13_131.csv", RUN_TABLE_HEADERS, rows_131_values)
    write_csv_table(results_dir / "benchmark_pyperplan_part13_132.csv", RUN_TABLE_HEADERS, rows_132_values)
    write_csv_table(results_dir / "benchmark_pyperplan_part13_133.csv", RUN_TABLE_HEADERS, rows_133_values)


def write_report(
    output_path: Path,
    args: argparse.Namespace,
    search_aliases: dict[str, str | None],
    heuristic_aliases: dict[str, str | None],
    generation_rows: list[GenerationRow],
    rows_131: list[RunRow],
    rows_132: list[RunRow],
    rows_133: list[RunRow],
) -> None:
    lines: list[str] = []
    lines.append("Benchmark pyperplan - Practice 1 Part 1 Exercise 1.3")
    lines.append(f"Generated at: {dt.datetime.now().isoformat(timespec='seconds')}")
    lines.append(f"Args: {vars(args)}")
    lines.append("")
    lines.append("[ALIASES]")
    for key, value in search_aliases.items():
        lines.append(f"search.{key}\t{value}")
    for key, value in heuristic_aliases.items():
        lines.append(f"heuristic.{key}\t{value}")
    lines.append("")

    if generation_rows:
        add_table(
            lines,
            "[GENERATION]",
            ["size", "problem_file", "status", "wall_time_s", "error_excerpt"],
            [
                [
                    str(r.size),
                    r.problem_file,
                    r.status,
                    f"{r.wall_time_s:.4f}",
                    r.error_excerpt,
                ]
                for r in generation_rows
            ],
        )

    all_rows = rows_131 + rows_132 + rows_133
    add_table(
        lines,
        "[RAW_ROWS]",
        RUN_TABLE_HEADERS,
        [run_row_as_list(row) for row in all_rows],
    )

    add_table(
        lines,
        "[TABLE_1.3.1_ALL_RUNS]",
        RUN_TABLE_HEADERS,
        [run_row_as_list(row) for row in rows_131],
    )

    add_table(
        lines,
        "[TABLE_1.3.2_ALL_RUNS]",
        RUN_TABLE_HEADERS,
        [run_row_as_list(row) for row in rows_132],
    )

    add_table(
        lines,
        "[TABLE_1.3.3_ALL_RUNS]",
        RUN_TABLE_HEADERS,
        [run_row_as_list(row) for row in rows_133],
    )

    summary_131 = summarize_131(rows_131)
    add_table(
        lines,
        "[SUMMARY_1.3.1]",
        ["algorithm", "max_solved_size", "time_s", "plan_length", "optimal"],
        [
            [row["algorithm"], row["max_solved_size"], row["time_s"], row["plan_length"], row["optimal"]]
            for row in summary_131
        ],
    )

    add_table(
        lines,
        "[SUMMARY_1.3.2]",
        ["combo", "status", "time_s", "plan_length", "size"],
        [
            [
                f"{r.algorithm}/{r.heuristic or '-'}",
                r.status,
                "" if r.search_time_s is None else f"{r.search_time_s:.4f}",
                "" if r.plan_length is None else str(r.plan_length),
                str(r.size),
            ]
            for r in rows_132
        ],
    )

    add_table(
        lines,
        "[SUMMARY_1.3.3]",
        ["combo", "status", "time_s", "plan_length", "size", "optimal"],
        [
            [
                f"{r.algorithm}/{r.heuristic or '-'}",
                r.status,
                "" if r.search_time_s is None else f"{r.search_time_s:.4f}",
                "" if r.plan_length is None else str(r.plan_length),
                str(r.size),
                r.optimal,
            ]
            for r in rows_133
        ],
    )

    best = best_optimal_row(rows_133)
    lines.append("[BEST_OPTIMAL_1.3.3]")
    if best is None:
        lines.append("none")
    else:
        lines.append(
            f"{best.algorithm}/{best.heuristic or '-'}\t{best.search_time_s:.4f}s\tplan_length={best.plan_length}"
        )
    lines.append("")

    output_path.write_text("\n".join(lines), encoding="utf-8")


def write_markdown_report(
    output_path: Path,
    args: argparse.Namespace,
    search_aliases: dict[str, str | None],
    heuristic_aliases: dict[str, str | None],
    generation_rows: list[GenerationRow],
    rows_131: list[RunRow],
    rows_132: list[RunRow],
    rows_133: list[RunRow],
    results_dir: Path,
) -> None:
    lines: list[str] = []
    lines.append("# Benchmark pyperplan - Practice 1 Part 1 Exercise 1.3")
    lines.append("")
    lines.append(f"- Generated at: `{dt.datetime.now().isoformat(timespec='seconds')}`")
    lines.append(f"- Args: `{vars(args)}`")
    lines.append("")

    alias_rows: list[list[str]] = []
    for key, value in search_aliases.items():
        alias_rows.append([f"search.{key}", "" if value is None else value])
    for key, value in heuristic_aliases.items():
        alias_rows.append([f"heuristic.{key}", "" if value is None else value])
    add_markdown_table(lines, "[ALIASES]", ["alias", "value"], alias_rows)

    error_id_by_text: dict[str, str] = {}
    error_details: list[tuple[str, str]] = []

    def markdown_error_cell(error_excerpt: str) -> str:
        clean = error_excerpt.strip()
        if not clean:
            return ""
        error_id = error_id_by_text.get(clean)
        if error_id is None:
            error_id = f"E{len(error_details) + 1:03d}"
            error_id_by_text[clean] = error_id
            error_details.append((error_id, clean))
        short = clean
        if len(short) > ERROR_EXCERPT_MD_MAX_LEN:
            short = short[: ERROR_EXCERPT_MD_MAX_LEN - 3].rstrip() + "..."
        return f"{short} ({error_id})"

    def run_row_as_markdown_list(row: RunRow) -> list[str]:
        values = run_row_as_list(row)
        values[RUN_COL_PROBLEM_FILE] = compact_problem_path(values[RUN_COL_PROBLEM_FILE], results_dir)
        values[RUN_COL_ERROR_EXCERPT] = markdown_error_cell(values[RUN_COL_ERROR_EXCERPT])
        return values

    if generation_rows:
        add_markdown_table(
            lines,
            "[GENERATION]",
            ["size", "problem_file", "status", "wall_time_s", "error_excerpt"],
            [
                [
                    str(r.size),
                    compact_problem_path(r.problem_file, results_dir),
                    r.status,
                    f"{r.wall_time_s:.4f}",
                    markdown_error_cell(r.error_excerpt),
                ]
                for r in generation_rows
            ],
        )

    all_rows = rows_131 + rows_132 + rows_133
    add_markdown_table(
        lines,
        "[RAW_ROWS]",
        RUN_TABLE_HEADERS,
        [run_row_as_markdown_list(row) for row in all_rows],
    )
    add_markdown_table(
        lines,
        "[TABLE_1.3.1_ALL_RUNS]",
        RUN_TABLE_HEADERS,
        [run_row_as_markdown_list(row) for row in rows_131],
    )
    add_markdown_table(
        lines,
        "[TABLE_1.3.2_ALL_RUNS]",
        RUN_TABLE_HEADERS,
        [run_row_as_markdown_list(row) for row in rows_132],
    )
    add_markdown_table(
        lines,
        "[TABLE_1.3.3_ALL_RUNS]",
        RUN_TABLE_HEADERS,
        [run_row_as_markdown_list(row) for row in rows_133],
    )

    summary_131 = summarize_131(rows_131)
    add_markdown_table(
        lines,
        "[SUMMARY_1.3.1]",
        ["algorithm", "max_solved_size", "time_s", "plan_length", "optimal"],
        [
            [row["algorithm"], row["max_solved_size"], row["time_s"], row["plan_length"], row["optimal"]]
            for row in summary_131
        ],
    )
    add_markdown_table(
        lines,
        "[SUMMARY_1.3.2]",
        ["combo", "status", "time_s", "plan_length", "size"],
        [
            [
                f"{r.algorithm}/{r.heuristic or '-'}",
                r.status,
                "" if r.search_time_s is None else f"{r.search_time_s:.4f}",
                "" if r.plan_length is None else str(r.plan_length),
                str(r.size),
            ]
            for r in rows_132
        ],
    )
    add_markdown_table(
        lines,
        "[SUMMARY_1.3.3]",
        ["combo", "status", "time_s", "plan_length", "size", "optimal"],
        [
            [
                f"{r.algorithm}/{r.heuristic or '-'}",
                r.status,
                "" if r.search_time_s is None else f"{r.search_time_s:.4f}",
                "" if r.plan_length is None else str(r.plan_length),
                str(r.size),
                r.optimal,
            ]
            for r in rows_133
        ],
    )

    best = best_optimal_row(rows_133)
    lines.append("## [BEST_OPTIMAL_1.3.3]")
    lines.append("")
    if best is None:
        lines.append("- none")
    else:
        lines.append(f"- `{best.algorithm}/{best.heuristic or '-'}`: `{best.search_time_s:.4f}s`, plan_length=`{best.plan_length}`")
    lines.append("")

    if error_details:
        lines.append("## [ERROR_DETAILS]")
        lines.append("")
        for error_id, full_text in error_details:
            lines.append(f"### {error_id}")
            lines.append("```text")
            lines.append(full_text)
            lines.append("```")
            lines.append("")

    output_path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    args = parse_args()

    domain_file = Path(args.domain).resolve()
    generator_file = Path(args.generator).resolve()
    results_dir = Path(args.results_dir).resolve()
    report_path = results_dir / "benchmark_pyperplan_part13.txt"
    report_md_path = results_dir / "benchmark_pyperplan_part13.md"
    png_131 = results_dir / "part13_1_runtime_vs_size.png"
    png_132 = results_dir / "part13_2_runtime_by_combo.png"
    png_133 = results_dir / "part13_3_optimal_runtime.png"

    if not domain_file.exists():
        raise FileNotFoundError(f"Domain file not found: {domain_file}")
    if args.problem_files is None and not generator_file.exists():
        raise FileNotFoundError(f"Generator file not found: {generator_file}")
    if not HAVE_MATPLOTLIB and not args.allow_basic_plots:
        raise RuntimeError(
            "matplotlib is required to generate readable PNG plots with title/axes/legend. "
            "Install it (e.g. `pip install matplotlib`) or use --allow-basic-plots."
        )

    results_dir.mkdir(parents=True, exist_ok=True)

    base_cmd = ["planutils", "run", "pyperplan", "--"]
    search_aliases, heuristic_aliases, _ = resolve_aliases(base_cmd)

    if args.problem_files:
        problems = load_existing_problems(args.problem_files)
        generation_rows: list[GenerationRow] = []
    else:
        sizes = make_sizes(args.min_size, args.max_size, args.step)
        problems_dir = results_dir / "problems"
        problems, generation_rows = generate_problems(
            sizes=sizes,
            generator_path=generator_file,
            output_dir=problems_dir,
            timeout_s=args.timeout,
        )

    if not problems:
        raise RuntimeError("No problems available for benchmark.")

    rows_131 = run_section_131(
        problems=problems,
        domain_file=domain_file,
        timeout_s=args.timeout,
        base_cmd=base_cmd,
        search_aliases=search_aliases,
        heuristic_aliases=heuristic_aliases,
    )

    anchor_132 = largest_solved(rows_131, "GBFS+hMAX")
    rows_132 = run_section_132(
        anchor_row=anchor_132,
        domain_file=domain_file,
        timeout_s=args.timeout,
        base_cmd=base_cmd,
        search_aliases=search_aliases,
        heuristic_aliases=heuristic_aliases,
    )

    anchor_133 = largest_solved(rows_131, "A*+hMAX")
    rows_133 = run_section_133(
        anchor_row=anchor_133,
        domain_file=domain_file,
        timeout_s=args.timeout,
        base_cmd=base_cmd,
        search_aliases=search_aliases,
        heuristic_aliases=heuristic_aliases,
    )

    write_report(
        output_path=report_path,
        args=args,
        search_aliases=search_aliases,
        heuristic_aliases=heuristic_aliases,
        generation_rows=generation_rows,
        rows_131=rows_131,
        rows_132=rows_132,
        rows_133=rows_133,
    )
    write_markdown_report(
        output_path=report_md_path,
        args=args,
        search_aliases=search_aliases,
        heuristic_aliases=heuristic_aliases,
        generation_rows=generation_rows,
        rows_131=rows_131,
        rows_132=rows_132,
        rows_133=rows_133,
        results_dir=results_dir,
    )
    write_csv_exports(results_dir=results_dir, rows_131=rows_131, rows_132=rows_132, rows_133=rows_133)

    save_plot_131(rows_131, png_131, timeout_s=args.timeout)
    save_bar_plot(rows_132, png_132, "1.3.2 - Runtime by search/heuristic combination", timeout_s=args.timeout)
    save_bar_plot(rows_133, png_133, "1.3.3 - Runtime for optimal planning combinations", timeout_s=args.timeout)

    print("\nDone.")
    print(f"TXT: {report_path}")
    print(f"MD: {report_md_path}")
    print(f"CSV: {results_dir / 'benchmark_pyperplan_part13_all.csv'}")
    print(f"CSV: {results_dir / 'benchmark_pyperplan_part13_131.csv'}")
    print(f"CSV: {results_dir / 'benchmark_pyperplan_part13_132.csv'}")
    print(f"CSV: {results_dir / 'benchmark_pyperplan_part13_133.csv'}")
    print(f"IMG: {png_131}")
    print(f"IMG: {png_132}")
    print(f"IMG: {png_133}")


if __name__ == "__main__":
    main()
