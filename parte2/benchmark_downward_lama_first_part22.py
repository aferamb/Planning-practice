#!/usr/bin/env python3
"""Standalone large-size benchmark for Fast Downward `lama-first` on Part 2.2.

This script reuses the execution/parsing infrastructure from
`benchmark_cost_planners_part22.py` but benchmarks only `downward:lama-first`
so larger instances can be explored without rerunning the full multi-planner
suite.

Outputs under the configured results directory:
- benchmark_downward_lama_first_part22_all.csv
- benchmark_downward_lama_first_part22_summary.csv
- benchmark_downward_lama_first_part22.txt
- benchmark_downward_lama_first_part22.md
- raw_logs/
- planner_artifacts/
- problems/
"""

from __future__ import annotations

import argparse
import datetime as dt
import shlex
import sys
from pathlib import Path

from benchmark_cost_planners_part22 import (
    RAW_HEADERS,
    GenerationRow,
    PlannerSpec,
    RunRow,
    add_table_md,
    add_table_txt,
    compact_problem_path,
    compact_summary_rows,
    generate_problems,
    load_existing_problems,
    make_sizes,
    markdown_error_cell,
    parse_sizes_csv,
    run_benchmark,
    run_row_values,
    write_csv_table,
)

SCRIPT_DIR = Path(__file__).resolve().parent
LAMA_SPEC = PlannerSpec("downward:lama-first", "sat", "downward", "lama-first")
SUMMARY_HEADERS = [
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


def resolve_script_relative(path_value: str) -> Path:
    path = Path(path_value)
    if path.is_absolute():
        return path.resolve()
    return (SCRIPT_DIR / path).resolve()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Benchmark only downward:lama-first for larger Part 2.2 instances"
    )
    parser.add_argument("--min-size", type=int, default=2, help="minimum size for l=p=c=g")
    parser.add_argument(
        "--hard-max-size",
        "--max-size",
        dest="hard_max_size",
        type=int,
        default=80,
        help="upper bound for the adaptive sweep when --sizes is not used",
    )
    parser.add_argument("--step", type=int, default=1, help="size increment for non-explicit sweeps")
    parser.add_argument(
        "--sizes",
        default=None,
        help="comma-separated size list; disables adaptive early stop and runs exactly those sizes",
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=70,
        help="timeout per planner/instance in seconds",
    )
    parser.add_argument(
        "--stop-after-consecutive-failures",
        type=int,
        default=3,
        help="for adaptive sweeps, stop after this many consecutive non-solved runs after the first solved size",
    )

    parser.add_argument("--domain", default="dronedomain2.pddl", help="cost domain path")
    parser.add_argument("--generator", default="generate-problem.py", help="problem generator path")
    parser.add_argument(
        "--results-dir",
        default="results/lama_first_part22",
        help="output folder for this standalone benchmark",
    )

    parser.add_argument("--drones", type=int, default=1, help="number of drones")
    parser.add_argument("--carriers", type=int, default=1, help="number of carriers")
    parser.add_argument("--carrier-capacity", type=int, default=4, help="carrier capacity")
    parser.add_argument(
        "--exercise",
        type=int,
        default=2,
        choices=[2],
        help="generator exercise mode (fixed to 2)",
    )
    parser.add_argument("--seed", type=int, default=None, help="optional generator seed")
    parser.add_argument(
        "--problem-files",
        nargs="*",
        default=None,
        help="optional existing problem files; if set, generation is skipped",
    )

    if len(sys.argv) > 1:
        args = parser.parse_args()
    else:
        print("No se han recibido parámetros por línea de comandos.")
        print("Modo interactivo: escribe argumentos como en CLI o pulsa Enter para usar valores por defecto.")
        try:
            raw_args = input("¿Qué parámetros quieres meter? ").strip()
        except EOFError:
            raw_args = ""
        args = parser.parse_args([] if not raw_args else shlex.split(raw_args))

    if args.stop_after_consecutive_failures < 1:
        parser.error("--stop-after-consecutive-failures must be >= 1")
    return args


def summary_rows(rows: list[RunRow]) -> list[list[str]]:
    _, _, global_rows = compact_summary_rows(rows, [LAMA_SPEC])
    return global_rows


def write_summary_csv(path: Path, rows: list[list[str]]) -> None:
    write_csv_table(path, SUMMARY_HEADERS, rows)


def write_txt_report(
    output_path: Path,
    args: argparse.Namespace,
    generation_rows: list[GenerationRow],
    rows: list[RunRow],
    summary: list[list[str]],
    stop_reason: str | None,
) -> None:
    lines: list[str] = []
    lines.append("Benchmark downward:lama-first - Practice 1 Part 2 Exercise 2.2")
    lines.append(f"Generated at: {dt.datetime.now().isoformat(timespec='seconds')}")
    lines.append(f"Args: {vars(args)}")
    if stop_reason:
        lines.append(f"Stop reason: {stop_reason}")
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
    add_table_txt(lines, "[TABLE_LAMA_FIRST_SUMMARY]", SUMMARY_HEADERS, summary)
    output_path.write_text("\n".join(lines), encoding="utf-8")


def write_md_report(
    output_path: Path,
    args: argparse.Namespace,
    generation_rows: list[GenerationRow],
    rows: list[RunRow],
    summary: list[list[str]],
    results_dir: Path,
    stop_reason: str | None,
) -> None:
    lines: list[str] = []
    lines.append("# Benchmark downward:lama-first - Practice 1 Part 2 Exercise 2.2")
    lines.append("")
    lines.append(f"- Generated at: `{dt.datetime.now().isoformat(timespec='seconds')}`")
    lines.append(f"- Args: `{vars(args)}`")
    if stop_reason:
        lines.append(f"- Stop reason: `{stop_reason}`")
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
    add_table_md(lines, "[TABLE_LAMA_FIRST_SUMMARY]", SUMMARY_HEADERS, summary)

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


def run_explicit_problems(
    problems: list[tuple[int, Path]],
    domain_file: Path,
    timeout_s: int,
    logs_dir: Path,
    planner_artifacts_dir: Path,
) -> list[RunRow]:
    rows: list[RunRow] = []
    for size, problem_path in problems:
        batch = run_benchmark(
            specs=[LAMA_SPEC],
            problems=[(size, problem_path)],
            domain_file=domain_file,
            timeout_s=timeout_s,
            logs_dir=logs_dir,
            planner_artifacts_dir=planner_artifacts_dir,
        )
        rows.extend(batch)
        if batch and batch[-1].status == "unsupported":
            break
    return rows


def run_adaptive_generated_sweep(
    sizes: list[int],
    generator_file: Path,
    problems_dir: Path,
    domain_file: Path,
    timeout_s: int,
    logs_dir: Path,
    planner_artifacts_dir: Path,
    drones: int,
    carriers: int,
    carrier_capacity: int,
    exercise: int,
    seed: int | None,
    stop_after_failures: int,
) -> tuple[list[GenerationRow], list[RunRow], str | None]:
    generation_rows: list[GenerationRow] = []
    rows: list[RunRow] = []
    stop_reason: str | None = None
    had_solved = False
    consecutive_failures = 0

    for size in sizes:
        problems, new_generation_rows = generate_problems(
            sizes=[size],
            generator_path=generator_file,
            output_dir=problems_dir,
            timeout_s=timeout_s,
            drones=drones,
            carriers=carriers,
            carrier_capacity=carrier_capacity,
            exercise=exercise,
            seed=seed,
        )
        generation_rows.extend(new_generation_rows)
        if not problems:
            continue

        batch = run_benchmark(
            specs=[LAMA_SPEC],
            problems=problems,
            domain_file=domain_file,
            timeout_s=timeout_s,
            logs_dir=logs_dir,
            planner_artifacts_dir=planner_artifacts_dir,
        )
        rows.extend(batch)
        if not batch:
            continue

        status = batch[-1].status
        if status == "unsupported":
            stop_reason = f"planner became unsupported at size {size}"
            break

        if status == "solved":
            had_solved = True
            consecutive_failures = 0
            continue

        if had_solved:
            consecutive_failures += 1
            if consecutive_failures >= stop_after_failures:
                stop_reason = (
                    f"stopped after {consecutive_failures} consecutive non-solved runs "
                    f"starting at size {size - consecutive_failures + 1}"
                )
                break

    return generation_rows, rows, stop_reason


def main() -> None:
    args = parse_args()

    domain_file = resolve_script_relative(args.domain)
    generator_file = resolve_script_relative(args.generator)
    results_dir = resolve_script_relative(args.results_dir)
    problems_dir = results_dir / "problems"
    logs_dir = results_dir / "raw_logs"
    planner_artifacts_dir = results_dir / "planner_artifacts"

    if not domain_file.exists():
        raise FileNotFoundError(f"Domain file not found: {domain_file}")
    if args.problem_files is None and not generator_file.exists():
        raise FileNotFoundError(f"Generator file not found: {generator_file}")

    results_dir.mkdir(parents=True, exist_ok=True)
    problems_dir.mkdir(parents=True, exist_ok=True)
    logs_dir.mkdir(parents=True, exist_ok=True)
    planner_artifacts_dir.mkdir(parents=True, exist_ok=True)

    if args.problem_files:
        problems = load_existing_problems(args.problem_files)
        generation_rows: list[GenerationRow] = []
        rows = run_explicit_problems(
            problems=problems,
            domain_file=domain_file,
            timeout_s=args.timeout,
            logs_dir=logs_dir,
            planner_artifacts_dir=planner_artifacts_dir,
        )
        stop_reason = None
    else:
        sizes = parse_sizes_csv(args.sizes) if args.sizes else make_sizes(args.min_size, args.hard_max_size, args.step)
        if not sizes:
            raise RuntimeError("No sizes selected for the benchmark.")

        if args.sizes:
            generation_rows = []
            rows = []
            stop_reason = None
            for size in sizes:
                problems, new_generation_rows = generate_problems(
                    sizes=[size],
                    generator_path=generator_file,
                    output_dir=problems_dir,
                    timeout_s=args.timeout,
                    drones=args.drones,
                    carriers=args.carriers,
                    carrier_capacity=args.carrier_capacity,
                    exercise=args.exercise,
                    seed=args.seed,
                )
                generation_rows.extend(new_generation_rows)
                if not problems:
                    continue
                batch = run_benchmark(
                    specs=[LAMA_SPEC],
                    problems=problems,
                    domain_file=domain_file,
                    timeout_s=args.timeout,
                    logs_dir=logs_dir,
                    planner_artifacts_dir=planner_artifacts_dir,
                )
                rows.extend(batch)
                if batch and batch[-1].status == "unsupported":
                    stop_reason = f"planner became unsupported at size {size}"
                    break
        else:
            generation_rows, rows, stop_reason = run_adaptive_generated_sweep(
                sizes=sizes,
                generator_file=generator_file,
                problems_dir=problems_dir,
                domain_file=domain_file,
                timeout_s=args.timeout,
                logs_dir=logs_dir,
                planner_artifacts_dir=planner_artifacts_dir,
                drones=args.drones,
                carriers=args.carriers,
                carrier_capacity=args.carrier_capacity,
                exercise=args.exercise,
                seed=args.seed,
                stop_after_failures=args.stop_after_consecutive_failures,
            )

    if not generation_rows and not rows:
        raise RuntimeError("No problems available for benchmark.")

    summary = summary_rows(rows)

    all_csv = results_dir / "benchmark_downward_lama_first_part22_all.csv"
    summary_csv = results_dir / "benchmark_downward_lama_first_part22_summary.csv"
    txt_path = results_dir / "benchmark_downward_lama_first_part22.txt"
    md_path = results_dir / "benchmark_downward_lama_first_part22.md"

    write_csv_table(all_csv, RAW_HEADERS, [run_row_values(r) for r in rows])
    write_summary_csv(summary_csv, summary)
    write_txt_report(
        output_path=txt_path,
        args=args,
        generation_rows=generation_rows,
        rows=rows,
        summary=summary,
        stop_reason=stop_reason,
    )
    write_md_report(
        output_path=md_path,
        args=args,
        generation_rows=generation_rows,
        rows=rows,
        summary=summary,
        results_dir=results_dir,
        stop_reason=stop_reason,
    )

    print("\nDone.")
    print(f"CSV: {all_csv}")
    print(f"CSV: {summary_csv}")
    print(f"TXT: {txt_path}")
    print(f"MD:  {md_path}")
    if stop_reason:
        print(f"STOP: {stop_reason}")


if __name__ == "__main__":
    main()
