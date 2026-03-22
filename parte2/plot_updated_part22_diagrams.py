#!/usr/bin/env python3
"""Regenerate updated Part 2.2 diagrams from existing CSV outputs.

This script does not rerun planners. It reads the original Part 2.2 CSV rows,
replaces the old `downward:lama-first` rows with the standalone benchmark rows,
and writes new PNG charts under a dedicated output directory.
"""

from __future__ import annotations

import argparse
import csv
from pathlib import Path

try:
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    HAVE_MATPLOTLIB = True
except Exception:
    HAVE_MATPLOTLIB = False

from benchmark_cost_planners_part22 import PLANNERS, RunRow, compact_summary_rows
from benchmark_downward_lama_first_part22 import save_lama_runtime_png

SCRIPT_DIR = Path(__file__).resolve().parent
REQUIRED_COLUMNS = [
    "planner",
    "family",
    "status",
    "size",
    "planner_time_s",
    "wall_time_s",
    "plan_cost",
    "plan_length",
    "error_excerpt",
    "problem_file",
]


def resolve_script_relative(path_value: str) -> Path:
    path = Path(path_value)
    if path.is_absolute():
        return path.resolve()
    return (SCRIPT_DIR / path).resolve()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Regenerate updated Part 2.2 charts from CSV outputs")
    parser.add_argument(
        "--main-all-csv",
        default="results/benchmark_cost_planners_part22_all.csv",
        help="main Part 2.2 all-rows CSV",
    )
    parser.add_argument(
        "--lama-all-csv",
        default="results/lama_first_part22/benchmark_downward_lama_first_part22_all.csv",
        help="standalone lama-first all-rows CSV",
    )
    parser.add_argument(
        "--output-dir",
        default="results/updated_diagrams_part22",
        help="directory where updated PNG charts will be written",
    )
    parser.add_argument(
        "--lama-timeout",
        type=int,
        default=70,
        help="timeout line used in the lama-first runtime-vs-size chart",
    )
    return parser.parse_args()


def parse_optional_float(value: str) -> float | None:
    raw = value.strip()
    if not raw:
        return None
    return float(raw)


def parse_optional_int(value: str) -> int | None:
    raw = value.strip()
    if not raw:
        return None
    return int(raw)


def load_run_rows(path: Path) -> list[RunRow]:
    with path.open(newline="", encoding="utf-8") as fh:
        reader = csv.DictReader(fh)
        if reader.fieldnames is None:
            raise RuntimeError(f"CSV has no header: {path}")
        missing = [col for col in REQUIRED_COLUMNS if col not in reader.fieldnames]
        if missing:
            raise RuntimeError(f"CSV missing required columns {missing}: {path}")

        rows: list[RunRow] = []
        for record in reader:
            rows.append(
                RunRow(
                    planner=record["planner"],
                    family=record["family"],
                    status=record["status"],
                    size=int(record["size"]),
                    planner_time_s=parse_optional_float(record["planner_time_s"]),
                    wall_time_s=float(record["wall_time_s"]),
                    plan_cost=parse_optional_float(record["plan_cost"]),
                    plan_length=parse_optional_int(record["plan_length"]),
                    error_excerpt=record["error_excerpt"],
                    problem_file=record["problem_file"],
                )
            )
    return rows


def merge_rows(main_rows: list[RunRow], lama_rows: list[RunRow]) -> list[RunRow]:
    kept = [row for row in main_rows if row.planner != "downward:lama-first"]
    return kept + lama_rows


def parse_summary_size(summary_row: list[str]) -> int | None:
    value = summary_row[2].strip()
    if value in {"", "-"}:
        return None
    return int(value)


def parse_summary_cost(summary_row: list[str]) -> float | None:
    value = summary_row[3].strip()
    if value in {"", "-"}:
        return None
    return float(value)


def make_updated_global_plots(output_dir: Path, summary_rows: list[list[str]], all_rows: list[RunRow]) -> list[Path]:
    if not HAVE_MATPLOTLIB:
        raise RuntimeError(
            "matplotlib is required to generate PNG charts with title/axes/legend. "
            "Install it (e.g. `pip install matplotlib`)."
        )

    out1 = output_dir / "part22_updated_max_solved_size_by_planner.png"
    out2 = output_dir / "part22_updated_cost_at_max_solved_size_by_planner.png"
    out3 = output_dir / "part22_updated_time_vs_cost_scatter.png"

    planners = [row[0] for row in summary_rows]
    families = [row[1] for row in summary_rows]
    max_sizes = [parse_summary_size(row) or 0 for row in summary_rows]
    costs = [parse_summary_cost(row) for row in summary_rows]

    family_colors = {"sat": "#1f77b4", "opt": "#ff7f0e"}
    bar_colors = [family_colors.get(f, "#7f7f7f") for f in families]

    plt.figure(figsize=(12, 6))
    bars = plt.bar(planners, max_sizes, color=bar_colors)
    plt.title("2.2 Updated - Maximum solved size by planner")
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
    plt.title("2.2 Updated - Solution cost at max solved size")
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
            row
            for row in all_rows
            if row.planner == spec.planner_id and row.status == "solved" and row.plan_cost is not None
        ]
        if not solved_rows:
            continue
        xs = [row.plan_cost for row in solved_rows if row.plan_cost is not None]
        ys = [row.planner_time_s if row.planner_time_s is not None else row.wall_time_s for row in solved_rows]
        sizes = [32 + (row.size * 3) for row in solved_rows]
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

    plt.title("2.2 Updated - Time vs cost (solved runs)")
    plt.xlabel("Plan cost")
    plt.ylabel("Planning time (s)")
    plt.grid(True, alpha=0.3)
    family_handles = [
        Line2D([0], [0], marker="o", linestyle="", color="black", label="satisficing", markersize=7),
        Line2D([0], [0], marker="s", linestyle="", color="black", label="optimal", markersize=7),
    ]
    if plotted_any:
        planner_handles, _ = plt.gca().get_legend_handles_labels()
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

    if not HAVE_MATPLOTLIB:
        raise RuntimeError(
            "matplotlib is required to generate updated Part 2.2 charts. "
            "Install it (e.g. `pip install matplotlib`)."
        )

    main_all_csv = resolve_script_relative(args.main_all_csv)
    lama_all_csv = resolve_script_relative(args.lama_all_csv)
    output_dir = resolve_script_relative(args.output_dir)

    if not main_all_csv.exists():
        raise FileNotFoundError(f"Main Part 2.2 CSV not found: {main_all_csv}")
    if not lama_all_csv.exists():
        raise FileNotFoundError(f"Standalone lama-first CSV not found: {lama_all_csv}")

    output_dir.mkdir(parents=True, exist_ok=True)

    main_rows = load_run_rows(main_all_csv)
    lama_rows = load_run_rows(lama_all_csv)
    merged_rows = merge_rows(main_rows, lama_rows)

    _, _, summary_rows = compact_summary_rows(merged_rows, PLANNERS)

    lama_plot = output_dir / "part22_lama_first_runtime_vs_size.png"
    save_lama_runtime_png(lama_rows, lama_plot, timeout_s=args.lama_timeout)
    other_plots = make_updated_global_plots(output_dir, summary_rows, merged_rows)

    print("\nDone.")
    print(f"IMG: {lama_plot}")
    for img in other_plots:
        print(f"IMG: {img}")


if __name__ == "__main__":
    main()
