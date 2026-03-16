#!/usr/bin/env python3
"""Benchmark cost planners for Practice 1 Part 2 Exercise 2.2.

Supported planners:
- metric-ff
- downward aliases: lama-first, seq-sat-fdss-2, seq-sat-fd-autotune-2,
  seq-opt-lmcut, seq-opt-bjolp, seq-opt-fdss-2

Outputs under results/:
- CSV global + CSV by family (sat/opt)
- compact CSV summaries
- TXT + Markdown report
- PNG charts with title/axes/legend
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
FF_STEP_RE = re.compile(r"^\s*(?:step\s+\d+:|\d+:)", re.IGNORECASE | re.MULTILINE)
PLAN_LENGTH_PATTERNS = [
    re.compile(r"plan length:\s*([0-9]+)", re.IGNORECASE),
    re.compile(r"plan length\s*=\s*([0-9]+)", re.IGNORECASE),
]
PLAN_COST_PATTERNS = [
    re.compile(r"plan cost:\s*([0-9]+(?:\.[0-9]+)?)", re.IGNORECASE),
    re.compile(r"cost of plan:\s*([0-9]+(?:\.[0-9]+)?)", re.IGNORECASE),
    re.compile(r"metric value:\s*([0-9]+(?:\.[0-9]+)?)", re.IGNORECASE),
    re.compile(r";\s*cost\s*=\s*([0-9]+(?:\.[0-9]+)?)", re.IGNORECASE),
]
SOLVED_RE = re.compile(
    r"(found legal plan as follows|solution found!?|plan length:|cost of plan:|plan cost:)",
    re.IGNORECASE,
)
UNSOLVED_RE = re.compile(
    r"(no solution|unsolvable|goal can be simplified to false|problem proven unsolvable|search stopped without finding a solution)",
    re.IGNORECASE,
)
UNSUPPORTED_RE = re.compile(
    r"(invalid alias|unknown alias|unrecognized arguments|command not found|not found|module not found|no such file or directory)",
    re.IGNORECASE,
)
PACKAGE_NOT_INSTALLED_RE = re.compile(r"package\s+\S+\s+is not installed", re.IGNORECASE)
USAGE_RE = re.compile(r"(^|\n)\s*usage:\s", re.IGNORECASE)

ERROR_EXCERPT_MD_MAX_LEN = 120

RAW_HEADERS = [
    "planner",
    "family",
    "status",
    "size",
    "wall_time_s",
    "plan_cost",
    "plan_length",
    "error_excerpt",
    "problem_file",
]


@dataclass
class PlannerSpec:
    planner_id: str
    family: str  # sat | opt
    tool: str  # metric-ff | downward
    alias: str | None = None


@dataclass
class GenerationRow:
    size: int
    problem_file: str
    status: str
    wall_time_s: float
    error_excerpt: str


@dataclass
class RunRow:
    planner: str
    family: str
    status: str
    size: int
    wall_time_s: float
    plan_cost: float | None
    plan_length: int | None
    error_excerpt: str
    problem_file: str


PLANNERS: list[PlannerSpec] = [
    PlannerSpec("metric-ff", "sat", "metric-ff"),
    PlannerSpec("downward:lama-first", "sat", "downward", "lama-first"),
    PlannerSpec("downward:seq-sat-fdss-2", "sat", "downward", "seq-sat-fdss-2"),
    PlannerSpec("downward:seq-sat-fd-autotune-2", "sat", "downward", "seq-sat-fd-autotune-2"),
    PlannerSpec("downward:seq-opt-lmcut", "opt", "downward", "seq-opt-lmcut"),
    PlannerSpec("downward:seq-opt-bjolp", "opt", "downward", "seq-opt-bjolp"),
    PlannerSpec("downward:seq-opt-fdss-2", "opt", "downward", "seq-opt-fdss-2"),
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Benchmark cost planners for exercise 2.2")
    parser.add_argument("--min-size", type=int, default=2, help="minimum size for l=p=c=g")
    parser.add_argument("--max-size", type=int, default=20, help="maximum size for l=p=c=g")
    parser.add_argument("--step", type=int, default=2, help="size increment")
    parser.add_argument("--sizes", default=None, help="comma-separated size list (overrides min/max/step)")

    parser.add_argument("--timeout", type=int, default=60, help="timeout per planner/instance (seconds)")
    parser.add_argument("--domain", default="dronedomain2.pddl", help="cost domain path")
    parser.add_argument("--generator", default="generate-problem.py", help="problem generator path")
    parser.add_argument("--results-dir", default="results", help="output folder")

    parser.add_argument("--drones", type=int, default=1, help="number of drones")
    parser.add_argument("--carriers", type=int, default=1, help="number of carriers")
    parser.add_argument("--carrier-capacity", type=int, default=4, help="carrier capacity")
    parser.add_argument("--exercise", type=int, default=2, choices=[2], help="generator exercise mode (fixed to 2)")
    parser.add_argument("--seed", type=int, default=None, help="optional generator seed")

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
    return sorted(set(values))


def problem_file_name(
    size: int,
    exercise: int,
    drones: int,
    carriers: int,
    carrier_capacity: int,
    seed: int | None,
) -> str:
    name = (
        f"drone_problem_ex{exercise}"
        f"_d{drones}_r{carriers}_l{size}_p{size}_c{size}_g{size}_a{carrier_capacity}"
    )
    if seed is not None:
        name += f"_s{seed}"
    return f"{name}.pddl"


def extract_size(path: Path, fallback: int) -> int:
    match = SIZE_RE.search(path.name)
    if match is None:
        return fallback
    return int(match.group(1))


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


def parse_plan_cost(output: str) -> float | None:
    for pattern in PLAN_COST_PATTERNS:
        matches = pattern.findall(output)
        if matches:
            return float(matches[-1])
    return None


def parse_plan_length(output: str) -> int | None:
    for pattern in PLAN_LENGTH_PATTERNS:
        match = pattern.search(output)
        if match:
            return int(match.group(1))
    ff_steps = FF_STEP_RE.findall(output)
    if ff_steps:
        return len(ff_steps)
    return None


def parse_downward_plan_file(plan_file: Path) -> tuple[float | None, int | None]:
    if not plan_file.exists():
        return None, None
    try:
        content = plan_file.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return None, None

    plan_cost = None
    cost_match = re.search(r";\s*cost\s*=\s*([0-9]+(?:\.[0-9]+)?)", content, re.IGNORECASE)
    if cost_match:
        plan_cost = float(cost_match.group(1))

    plan_actions = [
        line
        for line in content.splitlines()
        if line.strip() and not line.lstrip().startswith(";")
    ]
    plan_length = len(plan_actions) if plan_actions else None
    return plan_cost, plan_length


def infer_status(code: int, output: str, timed_out: bool, plan_cost: float | None, plan_length: int | None) -> str:
    if timed_out:
        return "timeout"
    if code == 127:
        return "unsupported"
    if PACKAGE_NOT_INSTALLED_RE.search(output):
        return "unsupported"
    if UNSUPPORTED_RE.search(output):
        return "unsupported"
    if USAGE_RE.search(output) and plan_cost is None and plan_length is None:
        return "error"

    solved_by_values = (plan_cost is not None) or (plan_length is not None)
    solved_by_text = SOLVED_RE.search(output) is not None and code == 0
    if solved_by_values or solved_by_text:
        return "solved"

    if UNSOLVED_RE.search(output) is not None:
        return "unsolved"

    if code == 0:
        return "error"
    return "error"


def metric_ff_attempts(domain_file: Path, problem_file: Path) -> list[tuple[str, list[str]]]:
    d = str(domain_file)
    p = str(problem_file)
    return [
        ("planutils", ["planutils", "run", "metric-ff", "--", d, p]),
        ("metric-ff", ["metric-ff", d, p]),
        ("metric-ff", ["metric-ff", "-o", d, "-f", p]),
    ]


def alias_variants(alias: str) -> list[str]:
    variants = [alias]
    if alias == "seq-opt-fdss-2":
        variants.append("seq-opt-fdss2")
    elif alias == "seq-opt-fdss2":
        variants.append("seq-opt-fdss-2")
    return variants


def downward_attempts(
    domain_file: Path, problem_file: Path, alias: str, timeout_s: int, plan_file: Path
) -> list[tuple[str, list[str]]]:
    d = str(domain_file)
    p = str(problem_file)
    attempts: list[tuple[str, list[str]]] = []
    for alias_name in alias_variants(alias):
        attempts.extend(
            [
                (
                    "planutils",
                    [
                        "planutils",
                        "run",
                        "downward",
                        "--",
                        "--alias",
                        alias_name,
                        "--overall-time-limit",
                        str(timeout_s),
                        "--plan-file",
                        str(plan_file),
                        d,
                        p,
                    ],
                ),
                (
                    "downward",
                    [
                        "downward",
                        "--alias",
                        alias_name,
                        "--overall-time-limit",
                        str(timeout_s),
                        "--plan-file",
                        str(plan_file),
                        d,
                        p,
                    ],
                ),
                (
                    "fast-downward.py",
                    [
                        "fast-downward.py",
                        "--alias",
                        alias_name,
                        "--overall-time-limit",
                        str(timeout_s),
                        "--plan-file",
                        str(plan_file),
                        d,
                        p,
                    ],
                ),
                (
                    "fast-downward",
                    [
                        "fast-downward",
                        "--alias",
                        alias_name,
                        "--overall-time-limit",
                        str(timeout_s),
                        "--plan-file",
                        str(plan_file),
                        d,
                        p,
                    ],
                ),
            ]
        )
    return attempts


def run_planner_once(
    spec: PlannerSpec,
    size: int,
    domain_file: Path,
    problem_file: Path,
    timeout_s: int,
    logs_dir: Path,
    planner_artifacts_dir: Path,
) -> RunRow:
    planner_slug = spec.planner_id.replace(":", "__")
    planner_log_dir = logs_dir / planner_slug
    planner_log_dir.mkdir(parents=True, exist_ok=True)
    planner_artifact_dir = planner_artifacts_dir / planner_slug
    planner_artifact_dir.mkdir(parents=True, exist_ok=True)

    plan_file = planner_artifact_dir / f"size_{size}.plan"
    if plan_file.exists():
        plan_file.unlink()

    attempts = metric_ff_attempts(domain_file, problem_file)
    if spec.tool == "downward":
        if spec.alias is None:
            raise ValueError(f"Planner {spec.planner_id} needs alias")
        attempts = downward_attempts(
            domain_file, problem_file, spec.alias, timeout_s=timeout_s, plan_file=plan_file
        )

    last_row: RunRow | None = None
    last_out = ""

    for idx, (backend_name, cmd) in enumerate(attempts, start=1):
        code, out, timed_out, wall = run_command(cmd, cwd=problem_file.parent, timeout_s=timeout_s)
        last_out = out

        plan_cost = parse_plan_cost(out)
        plan_length = parse_plan_length(out)
        if spec.tool == "downward":
            file_cost, file_length = parse_downward_plan_file(plan_file)
            if plan_cost is None:
                plan_cost = file_cost
            if plan_length is None:
                plan_length = file_length

        status = infer_status(code, out, timed_out, plan_cost, plan_length)
        log_file = planner_log_dir / f"size_{size}_attempt_{idx}_{backend_name}.log"
        log_file.write_text(out, encoding="utf-8")

        keep_excerpt = status in {"error", "unsupported"} or (
            status == "unsolved" and plan_cost is None and plan_length is None
        )
        row = RunRow(
            planner=spec.planner_id,
            family=spec.family,
            status=status,
            size=size,
            wall_time_s=wall,
            plan_cost=plan_cost,
            plan_length=plan_length,
            error_excerpt=make_error_excerpt(out) if keep_excerpt else "",
            problem_file=str(problem_file),
        )
        last_row = row

        if status == "solved":
            return row

        if status == "timeout":
            return row

        # If this backend failed due to launcher availability, try next backend.
        launcher_missing = code in {127} or "No such file or directory" in out or "command not found" in out
        if launcher_missing:
            continue

        # For unsupported alias/tool, do not keep trying variants that won't help.
        if status == "unsupported":
            return row

        # Any deterministic non-launcher result becomes final for this planner run.
        if status in {"unsolved", "error"}:
            return row

    if last_row is not None:
        return last_row

    return RunRow(
        planner=spec.planner_id,
        family=spec.family,
        status="unsupported",
        size=size,
        wall_time_s=0.0,
        plan_cost=None,
        plan_length=None,
        error_excerpt=make_error_excerpt(last_out) or "planner backend not available",
        problem_file=str(problem_file),
    )


def generate_problems(
    sizes: list[int],
    generator_path: Path,
    output_dir: Path,
    timeout_s: int,
    drones: int,
    carriers: int,
    carrier_capacity: int,
    exercise: int,
    seed: int | None,
) -> tuple[list[tuple[int, Path]], list[GenerationRow]]:
    output_dir.mkdir(parents=True, exist_ok=True)
    ok_problems: list[tuple[int, Path]] = []
    gen_rows: list[GenerationRow] = []

    for size in sizes:
        problem_path = output_dir / problem_file_name(
            size=size,
            exercise=exercise,
            drones=drones,
            carriers=carriers,
            carrier_capacity=carrier_capacity,
            seed=seed,
        )
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

        code, out, timed_out, wall = run_command(cmd, cwd=output_dir, timeout_s=timeout_s)
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
            abs_problem = problem_path.resolve()
            ok_problems.append((size, abs_problem))
            gen_rows.append(
                GenerationRow(
                    size=size,
                    problem_file=str(abs_problem),
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


def run_benchmark(
    specs: list[PlannerSpec],
    problems: list[tuple[int, Path]],
    domain_file: Path,
    timeout_s: int,
    logs_dir: Path,
    planner_artifacts_dir: Path,
) -> list[RunRow]:
    rows: list[RunRow] = []

    planner_disabled_reason: dict[str, str] = {}

    for spec in specs:
        for size, problem_path in problems:
            disabled_reason = planner_disabled_reason.get(spec.planner_id)
            if disabled_reason is not None:
                rows.append(
                    RunRow(
                        planner=spec.planner_id,
                        family=spec.family,
                        status="unsupported",
                        size=size,
                        wall_time_s=0.0,
                        plan_cost=None,
                        plan_length=None,
                        error_excerpt=disabled_reason,
                        problem_file=str(problem_path),
                    )
                )
                print(f"[{spec.planner_id} size={size}] status=unsupported (cached)")
                continue

            row = run_planner_once(
                spec=spec,
                size=size,
                domain_file=domain_file,
                problem_file=problem_path,
                timeout_s=timeout_s,
                logs_dir=logs_dir,
                planner_artifacts_dir=planner_artifacts_dir,
            )
            rows.append(row)

            cost_text = "-" if row.plan_cost is None else f"{row.plan_cost:.2f}"
            length_text = "-" if row.plan_length is None else str(row.plan_length)
            print(
                f"[{spec.planner_id} size={size}] status={row.status} "
                f"wall={row.wall_time_s:.2f}s cost={cost_text} len={length_text}"
            )

            # If planner itself is unavailable, skip all subsequent sizes for that planner.
            if row.status == "unsupported":
                reason = row.error_excerpt or "planner unavailable or alias unsupported"
                planner_disabled_reason[spec.planner_id] = reason

    return rows


def run_row_values(row: RunRow) -> list[str]:
    return [
        row.planner,
        row.family,
        row.status,
        str(row.size),
        f"{row.wall_time_s:.4f}",
        "" if row.plan_cost is None else f"{row.plan_cost:.4f}",
        "" if row.plan_length is None else str(row.plan_length),
        row.error_excerpt,
        row.problem_file,
    ]


def write_csv_table(path: Path, headers: list[str], rows: list[list[str]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.writer(fh)
        writer.writerow(headers)
        writer.writerows(rows)


def export_csvs(results_dir: Path, rows: list[RunRow]) -> tuple[Path, Path, Path]:
    all_path = results_dir / "benchmark_cost_planners_part22_all.csv"
    sat_path = results_dir / "benchmark_cost_planners_part22_sat.csv"
    opt_path = results_dir / "benchmark_cost_planners_part22_opt.csv"

    all_rows = [run_row_values(r) for r in rows]
    sat_rows = [run_row_values(r) for r in rows if r.family == "sat"]
    opt_rows = [run_row_values(r) for r in rows if r.family == "opt"]

    write_csv_table(all_path, RAW_HEADERS, all_rows)
    write_csv_table(sat_path, RAW_HEADERS, sat_rows)
    write_csv_table(opt_path, RAW_HEADERS, opt_rows)
    return all_path, sat_path, opt_path


def best_row_for_planner(rows: list[RunRow], planner: str) -> RunRow | None:
    solved = [r for r in rows if r.planner == planner and r.status == "solved"]
    if not solved:
        return None

    max_size = max(r.size for r in solved)
    tied = [r for r in solved if r.size == max_size]

    def tie_key(row: RunRow) -> tuple[float, float]:
        cost = row.plan_cost if row.plan_cost is not None else float("inf")
        return (row.wall_time_s, cost)

    tied.sort(key=tie_key)
    return tied[0]


def status_counts(rows: list[RunRow], planner: str) -> dict[str, int]:
    values = [r for r in rows if r.planner == planner]
    return {
        "solved": sum(1 for r in values if r.status == "solved"),
        "timeout": sum(1 for r in values if r.status == "timeout"),
        "unsolved": sum(1 for r in values if r.status == "unsolved"),
        "unsupported": sum(1 for r in values if r.status == "unsupported"),
        "error": sum(1 for r in values if r.status == "error"),
    }


def compact_summary_rows(rows: list[RunRow], specs: list[PlannerSpec]) -> tuple[list[list[str]], list[list[str]], list[list[str]]]:
    sat_summary: list[list[str]] = []
    opt_summary: list[list[str]] = []
    global_summary: list[list[str]] = []

    for spec in specs:
        best = best_row_for_planner(rows, spec.planner_id)
        counts = status_counts(rows, spec.planner_id)
        if best is None:
            row = [
                spec.planner_id,
                spec.family,
                "-",
                "-",
                "-",
                "-",
                str(counts["solved"]),
                str(counts["timeout"]),
                str(counts["unsolved"]),
                str(counts["unsupported"]),
                str(counts["error"]),
            ]
        else:
            row = [
                spec.planner_id,
                spec.family,
                str(best.size),
                "" if best.plan_cost is None else f"{best.plan_cost:.4f}",
                "" if best.plan_length is None else str(best.plan_length),
                f"{best.wall_time_s:.4f}",
                str(counts["solved"]),
                str(counts["timeout"]),
                str(counts["unsolved"]),
                str(counts["unsupported"]),
                str(counts["error"]),
            ]

        global_summary.append(row)
        if spec.family == "sat":
            sat_summary.append(row)
        else:
            opt_summary.append(row)

    return sat_summary, opt_summary, global_summary


def write_summary_csvs(results_dir: Path, sat: list[list[str]], opt: list[list[str]], global_rows: list[list[str]]) -> tuple[Path, Path, Path]:
    headers = [
        "planner",
        "family",
        "max_solved_size",
        "plan_cost_at_max_size",
        "plan_length_at_max_size",
        "wall_time_s_at_max_size",
        "count_solved",
        "count_timeout",
        "count_unsolved",
        "count_unsupported",
        "count_error",
    ]

    sat_path = results_dir / "benchmark_cost_planners_part22_summary_sat.csv"
    opt_path = results_dir / "benchmark_cost_planners_part22_summary_opt.csv"
    global_path = results_dir / "benchmark_cost_planners_part22_summary_global.csv"

    write_csv_table(sat_path, headers, sat)
    write_csv_table(opt_path, headers, opt)
    write_csv_table(global_path, headers, global_rows)
    return sat_path, opt_path, global_path


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


def compact_problem_path(problem_file: str, results_dir: Path) -> str:
    path = Path(problem_file)
    abs_path = path.resolve()
    for base in (results_dir.resolve(), Path.cwd().resolve()):
        try:
            return abs_path.relative_to(base).as_posix()
        except ValueError:
            continue
    return path.name or problem_file


def markdown_error_cell(error_excerpt: str, error_id_by_text: dict[str, str], error_details: list[tuple[str, str]]) -> str:
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


def write_txt_report(
    output_path: Path,
    args: argparse.Namespace,
    generation_rows: list[GenerationRow],
    rows: list[RunRow],
    sat_summary: list[list[str]],
    opt_summary: list[list[str]],
    global_summary: list[list[str]],
) -> None:
    lines: list[str] = []
    lines.append("Benchmark cost planners - Practice 1 Part 2 Exercise 2.2")
    lines.append(f"Generated at: {dt.datetime.now().isoformat(timespec='seconds')}")
    lines.append(f"Args: {vars(args)}")
    lines.append("")

    if generation_rows:
        add_table_txt(
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

    add_table_txt(lines, "[RAW_ROWS]", RAW_HEADERS, [run_row_values(row) for row in rows])

    summary_headers = [
        "planner",
        "family",
        "max_solved_size",
        "plan_cost_at_max_size",
        "plan_length_at_max_size",
        "wall_time_s_at_max_size",
        "count_solved",
        "count_timeout",
        "count_unsolved",
        "count_unsupported",
        "count_error",
    ]

    add_table_txt(lines, "[TABLE_2.2_SAT_SUMMARY]", summary_headers, sat_summary)
    add_table_txt(lines, "[TABLE_2.2_OPT_SUMMARY]", summary_headers, opt_summary)
    add_table_txt(lines, "[TABLE_2.2_GLOBAL_SUMMARY]", summary_headers, global_summary)

    output_path.write_text("\n".join(lines), encoding="utf-8")


def write_md_report(
    output_path: Path,
    args: argparse.Namespace,
    generation_rows: list[GenerationRow],
    rows: list[RunRow],
    sat_summary: list[list[str]],
    opt_summary: list[list[str]],
    global_summary: list[list[str]],
    results_dir: Path,
    image_paths: list[Path],
) -> None:
    lines: list[str] = []
    lines.append("# Benchmark cost planners - Practice 1 Part 2 Exercise 2.2")
    lines.append("")
    lines.append(f"- Generated at: `{dt.datetime.now().isoformat(timespec='seconds')}`")
    lines.append(f"- Args: `{vars(args)}`")
    lines.append("")

    error_id_by_text: dict[str, str] = {}
    error_details: list[tuple[str, str]] = []

    if generation_rows:
        add_table_md(
            lines,
            "[GENERATION]",
            ["size", "problem_file", "status", "wall_time_s", "error_excerpt"],
            [
                [
                    str(r.size),
                    compact_problem_path(r.problem_file, results_dir),
                    r.status,
                    f"{r.wall_time_s:.4f}",
                    markdown_error_cell(r.error_excerpt, error_id_by_text, error_details),
                ]
                for r in generation_rows
            ],
        )

    raw_rows_for_md: list[list[str]] = []
    for row in rows:
        values = run_row_values(row)
        values[-1] = compact_problem_path(values[-1], results_dir)
        values[-2] = markdown_error_cell(values[-2], error_id_by_text, error_details)
        raw_rows_for_md.append(values)

    add_table_md(lines, "[RAW_ROWS]", RAW_HEADERS, raw_rows_for_md)

    summary_headers = [
        "planner",
        "family",
        "max_solved_size",
        "plan_cost_at_max_size",
        "plan_length_at_max_size",
        "wall_time_s_at_max_size",
        "count_solved",
        "count_timeout",
        "count_unsolved",
        "count_unsupported",
        "count_error",
    ]
    add_table_md(lines, "[TABLE_2.2_SAT_SUMMARY]", summary_headers, sat_summary)
    add_table_md(lines, "[TABLE_2.2_OPT_SUMMARY]", summary_headers, opt_summary)
    add_table_md(lines, "[TABLE_2.2_GLOBAL_SUMMARY]", summary_headers, global_summary)

    lines.append("## [PLOTS]")
    lines.append("")
    for img in image_paths:
        rel = img.name
        lines.append(f"![{img.stem}]({rel})")
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


def parse_summary_cost(summary_row: list[str]) -> float | None:
    value = summary_row[3].strip()
    if value in {"", "-"}:
        return None
    return float(value)


def parse_summary_size(summary_row: list[str]) -> int | None:
    value = summary_row[2].strip()
    if value in {"", "-"}:
        return None
    return int(value)


def make_plots(results_dir: Path, summary_rows: list[list[str]], all_rows: list[RunRow]) -> list[Path]:
    if not HAVE_MATPLOTLIB:
        raise RuntimeError(
            "matplotlib is required to generate PNG charts with title/axes/legend. "
            "Install it (e.g. `pip install matplotlib`)."
        )

    out1 = results_dir / "part22_max_solved_size_by_planner.png"
    out2 = results_dir / "part22_cost_at_max_solved_size_by_planner.png"
    out3 = results_dir / "part22_time_vs_cost_scatter.png"

    planners = [row[0] for row in summary_rows]
    families = [row[1] for row in summary_rows]
    max_sizes = [parse_summary_size(row) or 0 for row in summary_rows]
    costs = [parse_summary_cost(row) for row in summary_rows]

    family_colors = {"sat": "#1f77b4", "opt": "#ff7f0e"}
    bar_colors = [family_colors.get(f, "#7f7f7f") for f in families]

    plt.figure(figsize=(12, 6))
    bars = plt.bar(planners, max_sizes, color=bar_colors)
    plt.title("2.2 - Maximum solved size by planner")
    plt.xlabel("Planner")
    plt.ylabel("Max solved size")
    plt.xticks(rotation=25, ha="right")
    plt.grid(True, axis="y", alpha=0.3)
    for bar, value in zip(bars, max_sizes):
        plt.text(bar.get_x() + bar.get_width() / 2.0, value + 0.1, str(value), ha="center", va="bottom", fontsize=9)
    legend_handles = [
        plt.Rectangle((0, 0), 1, 1, color=family_colors["sat"], label="satisficing"),
        plt.Rectangle((0, 0), 1, 1, color=family_colors["opt"], label="optimal"),
    ]
    plt.legend(handles=legend_handles)
    plt.tight_layout()
    plt.savefig(out1, dpi=140)
    plt.close()

    plot_cost_values = [0.0 if c is None else c for c in costs]
    missing_cost = [c is None for c in costs]

    plt.figure(figsize=(12, 6))
    bars = plt.bar(planners, plot_cost_values, color=bar_colors)
    for bar, miss in zip(bars, missing_cost):
        if miss:
            bar.set_hatch("//")
            bar.set_alpha(0.4)
    plt.title("2.2 - Solution cost at max solved size")
    plt.xlabel("Planner")
    plt.ylabel("Plan cost")
    plt.xticks(rotation=25, ha="right")
    plt.grid(True, axis="y", alpha=0.3)
    for bar, cost, miss in zip(bars, costs, missing_cost):
        label = "N/A" if miss else f"{cost:.1f}"
        y = bar.get_height()
        plt.text(bar.get_x() + bar.get_width() / 2.0, y + max(0.1, y * 0.01), label, ha="center", va="bottom", fontsize=9)
    plt.legend(handles=legend_handles + [plt.Rectangle((0, 0), 1, 1, facecolor="#cccccc", hatch="//", label="cost not parseable")])
    plt.tight_layout()
    plt.savefig(out2, dpi=140)
    plt.close()

    planner_colors = {
        spec.planner_id: color
        for spec, color in zip(
            PLANNERS,
            ["#1f77b4", "#17becf", "#2ca02c", "#9467bd", "#ff7f0e", "#d62728", "#8c564b"],
        )
    }
    family_markers = {"sat": "o", "opt": "s"}

    from matplotlib.lines import Line2D

    plt.figure(figsize=(12, 7))
    plotted_any = False
    for spec in PLANNERS:
        solved_rows = [
            r
            for r in all_rows
            if r.planner == spec.planner_id and r.status == "solved" and r.plan_cost is not None and r.wall_time_s > 0
        ]
        if not solved_rows:
            continue
        xs = [r.plan_cost for r in solved_rows if r.plan_cost is not None]
        ys = [r.wall_time_s for r in solved_rows]
        sizes = [32 + (r.size * 3) for r in solved_rows]
        plt.scatter(
            xs,
            ys,
            s=sizes,
            marker=family_markers.get(spec.family, "o"),
            color=planner_colors.get(spec.planner_id, "#333333"),
            alpha=0.75,
            label=spec.planner_id,
        )
        plotted_any = True

    plt.title("2.2 - Time vs cost (solved runs)")
    plt.xlabel("Plan cost")
    plt.ylabel("Wall time (s)")
    plt.grid(True, alpha=0.3)
    family_handles = [
        Line2D([0], [0], marker="o", linestyle="", color="black", label="satisficing", markersize=7),
        Line2D([0], [0], marker="s", linestyle="", color="black", label="optimal", markersize=7),
    ]
    if plotted_any:
        planner_handles, planner_labels = plt.gca().get_legend_handles_labels()
        plt.legend(handles=planner_handles + family_handles, loc="best", fontsize=8)
    else:
        plt.legend(handles=family_handles, loc="best", fontsize=8)
        plt.text(
            0.5,
            0.5,
            "No solved runs with parseable cost/time.",
            transform=plt.gca().transAxes,
            ha="center",
            va="center",
            fontsize=10,
            color="#555555",
        )
    plt.tight_layout()
    plt.savefig(out3, dpi=140)
    plt.close()

    return [out1, out2, out3]


def main() -> None:
    args = parse_args()

    domain_file = Path(args.domain).resolve()
    generator_file = Path(args.generator).resolve()
    results_dir = Path(args.results_dir).resolve()
    problems_dir = results_dir / "problems"
    logs_dir = results_dir / "raw_logs"
    planner_artifacts_dir = results_dir / "planner_artifacts"

    if not domain_file.exists():
        raise FileNotFoundError(f"Domain file not found: {domain_file}")
    if args.problem_files is None and not generator_file.exists():
        raise FileNotFoundError(f"Generator file not found: {generator_file}")

    if args.sizes:
        sizes = parse_sizes_csv(args.sizes)
    else:
        sizes = make_sizes(args.min_size, args.max_size, args.step)

    results_dir.mkdir(parents=True, exist_ok=True)
    problems_dir.mkdir(parents=True, exist_ok=True)
    logs_dir.mkdir(parents=True, exist_ok=True)
    planner_artifacts_dir.mkdir(parents=True, exist_ok=True)

    if args.problem_files:
        problems = load_existing_problems(args.problem_files)
        generation_rows: list[GenerationRow] = []
    else:
        problems, generation_rows = generate_problems(
            sizes=sizes,
            generator_path=generator_file,
            output_dir=problems_dir,
            timeout_s=args.timeout,
            drones=args.drones,
            carriers=args.carriers,
            carrier_capacity=args.carrier_capacity,
            exercise=args.exercise,
            seed=args.seed,
        )

    if not problems:
        raise RuntimeError("No problems available for benchmark.")

    rows = run_benchmark(
        specs=PLANNERS,
        problems=problems,
        domain_file=domain_file,
        timeout_s=args.timeout,
        logs_dir=logs_dir,
        planner_artifacts_dir=planner_artifacts_dir,
    )

    all_csv, sat_csv, opt_csv = export_csvs(results_dir, rows)
    sat_summary, opt_summary, global_summary = compact_summary_rows(rows, PLANNERS)
    sum_sat_csv, sum_opt_csv, sum_global_csv = write_summary_csvs(results_dir, sat_summary, opt_summary, global_summary)

    txt_path = results_dir / "benchmark_cost_planners_part22.txt"
    md_path = results_dir / "benchmark_cost_planners_part22.md"

    image_paths = make_plots(results_dir, global_summary, rows)

    write_txt_report(
        output_path=txt_path,
        args=args,
        generation_rows=generation_rows,
        rows=rows,
        sat_summary=sat_summary,
        opt_summary=opt_summary,
        global_summary=global_summary,
    )
    write_md_report(
        output_path=md_path,
        args=args,
        generation_rows=generation_rows,
        rows=rows,
        sat_summary=sat_summary,
        opt_summary=opt_summary,
        global_summary=global_summary,
        results_dir=results_dir,
        image_paths=image_paths,
    )

    print("\nDone.")
    print(f"CSV: {all_csv}")
    print(f"CSV: {sat_csv}")
    print(f"CSV: {opt_csv}")
    print(f"CSV: {sum_sat_csv}")
    print(f"CSV: {sum_opt_csv}")
    print(f"CSV: {sum_global_csv}")
    print(f"TXT: {txt_path}")
    print(f"MD:  {md_path}")
    for img in image_paths:
        print(f"IMG: {img}")


if __name__ == "__main__":
    main()
