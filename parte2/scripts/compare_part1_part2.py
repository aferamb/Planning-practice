#!/usr/bin/env python3
"""Compare Part 1 and Part 2 pyperplan benchmark CSVs.

Compares:
- Part 1: 1.3.2 and 1.3.3
- Part 2: 2.1.2 and 2.1.3

Outputs:
- CSV with row-level differences
- Technical Markdown report with time and plan length variations by combination
"""

from __future__ import annotations

import argparse
import csv
import datetime as dt
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Tuple

REQUIRED_COLUMNS = {
    "section",
    "algorithm",
    "search",
    "heuristic",
    "size",
    "status",
    "solved",
    "search_time_s",
    "plan_length",
    "problem_file",
}


@dataclass(frozen=True)
class ComboKey:
    group: str
    algorithm: str
    search: str
    heuristic: str


@dataclass
class BenchRow:
    section: str
    algorithm: str
    search: str
    heuristic: str
    size: Optional[int]
    status: str
    solved: bool
    search_time_s: Optional[float]
    plan_length: Optional[int]
    problem_file: str


@dataclass
class DiffRow:
    key: ComboKey
    part1: Optional[BenchRow]
    part2: Optional[BenchRow]
    delta_search_time_s: Optional[float]
    delta_search_time_pct: Optional[float]
    delta_plan_length: Optional[int]
    note: str


def default_paths() -> Dict[str, Path]:
    repo_root = Path(__file__).resolve().parents[2]
    return {
        "part1_132": repo_root / "parte1" / "results" / "benchmark_pyperplan_part13_132.csv",
        "part1_133": repo_root / "parte1" / "results" / "benchmark_pyperplan_part13_133.csv",
        "part2_212": repo_root / "parte2" / "results" / "benchmark_pyperplan_part21_212.csv",
        "part2_213": repo_root / "parte2" / "results" / "benchmark_pyperplan_part21_213.csv",
        "out_csv": repo_root / "parte2" / "results" / "compare_part1_part2_diffs.csv",
        "out_md": repo_root / "parte2" / "results" / "compare_part1_part2_report.md",
    }


def parse_args() -> argparse.Namespace:
    paths = default_paths()
    parser = argparse.ArgumentParser(
        description="Compare Part 1 (1.3.2/1.3.3) vs Part 2 (2.1.2/2.1.3) benchmark CSVs"
    )
    parser.add_argument("--part1-132", type=Path, default=paths["part1_132"], help="CSV from part1 section 1.3.2")
    parser.add_argument("--part1-133", type=Path, default=paths["part1_133"], help="CSV from part1 section 1.3.3")
    parser.add_argument("--part2-212", type=Path, default=paths["part2_212"], help="CSV from part2 section 2.1.2")
    parser.add_argument("--part2-213", type=Path, default=paths["part2_213"], help="CSV from part2 section 2.1.3")
    parser.add_argument("--out-csv", type=Path, default=paths["out_csv"], help="Output CSV path")
    parser.add_argument("--out-md", type=Path, default=paths["out_md"], help="Output Markdown path")
    return parser.parse_args()


def _normalize_heuristic(value: str) -> str:
    clean = (value or "").strip()
    return clean if clean else "-"


def _parse_int(value: str) -> Optional[int]:
    clean = (value or "").strip()
    if not clean:
        return None
    return int(clean)


def _parse_float(value: str) -> Optional[float]:
    clean = (value or "").strip()
    if not clean:
        return None
    return float(clean)


def _parse_solved(value: str) -> bool:
    clean = (value or "").strip().lower()
    return clean in {"yes", "true", "1", "solved"}


def validate_csv(path: Path) -> None:
    if not path.exists():
        raise FileNotFoundError(f"CSV not found: {path}")
    with path.open("r", encoding="utf-8", newline="") as fh:
        reader = csv.DictReader(fh)
        fieldnames = set(reader.fieldnames or [])
    missing = REQUIRED_COLUMNS - fieldnames
    if missing:
        needed = ", ".join(sorted(missing))
        raise ValueError(f"CSV {path} is missing required columns: {needed}")


def load_benchmark_csv(path: Path, group: str) -> Dict[ComboKey, BenchRow]:
    rows: Dict[ComboKey, BenchRow] = {}
    with path.open("r", encoding="utf-8", newline="") as fh:
        reader = csv.DictReader(fh)
        for idx, raw in enumerate(reader, start=2):
            key = ComboKey(
                group=group,
                algorithm=(raw.get("algorithm") or "").strip(),
                search=(raw.get("search") or "").strip(),
                heuristic=_normalize_heuristic(raw.get("heuristic") or ""),
            )
            row = BenchRow(
                section=(raw.get("section") or "").strip(),
                algorithm=key.algorithm,
                search=key.search,
                heuristic=key.heuristic,
                size=_parse_int(raw.get("size") or ""),
                status=(raw.get("status") or "").strip(),
                solved=_parse_solved(raw.get("solved") or ""),
                search_time_s=_parse_float(raw.get("search_time_s") or ""),
                plan_length=_parse_int(raw.get("plan_length") or ""),
                problem_file=(raw.get("problem_file") or "").strip(),
            )
            if key in rows:
                print(
                    f"Warning: duplicate combination at {path}:{idx} for key={key}; keeping first row.",
                    file=sys.stderr,
                )
                continue
            rows[key] = row
    return rows


def compute_note(part1: Optional[BenchRow], part2: Optional[BenchRow]) -> str:
    if part1 is None:
        return "missing_in_part1"
    if part2 is None:
        return "missing_in_part2"

    reasons: List[str] = []
    if part1.status.lower() != "solved" or not part1.solved:
        reasons.append(f"part1_status={part1.status or 'unknown'}")
    if part2.status.lower() != "solved" or not part2.solved:
        reasons.append(f"part2_status={part2.status or 'unknown'}")
    if part1.search_time_s is None or part2.search_time_s is None:
        reasons.append("time_not_comparable")
    if part1.plan_length is None or part2.plan_length is None:
        reasons.append("plan_not_comparable")

    return "ok" if not reasons else ";".join(reasons)


def compute_diffs(
    p1_rows: Dict[ComboKey, BenchRow],
    p2_rows: Dict[ComboKey, BenchRow],
) -> List[DiffRow]:
    keys = sorted(
        set(p1_rows.keys()) | set(p2_rows.keys()),
        key=lambda k: (k.group, k.algorithm, k.search, k.heuristic),
    )

    diffs: List[DiffRow] = []
    for key in keys:
        part1 = p1_rows.get(key)
        part2 = p2_rows.get(key)

        delta_t: Optional[float] = None
        delta_pct: Optional[float] = None
        delta_len: Optional[int] = None

        if part1 and part2 and part1.search_time_s is not None and part2.search_time_s is not None:
            delta_t = part2.search_time_s - part1.search_time_s
            if part1.search_time_s != 0:
                delta_pct = (delta_t / part1.search_time_s) * 100.0

        if part1 and part2 and part1.plan_length is not None and part2.plan_length is not None:
            delta_len = part2.plan_length - part1.plan_length

        diffs.append(
            DiffRow(
                key=key,
                part1=part1,
                part2=part2,
                delta_search_time_s=delta_t,
                delta_search_time_pct=delta_pct,
                delta_plan_length=delta_len,
                note=compute_note(part1, part2),
            )
        )
    return diffs


def _fmt_float(value: Optional[float], ndigits: int = 4) -> str:
    if value is None:
        return ""
    return f"{value:.{ndigits}f}"


def _fmt_int(value: Optional[int]) -> str:
    if value is None:
        return ""
    return str(value)


def _fmt_bool(value: bool) -> str:
    return "yes" if value else "no"


def write_diff_csv(path: Path, rows: Iterable[DiffRow]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.writer(fh)
        writer.writerow(
            [
                "comparison_group",
                "algorithm",
                "search",
                "heuristic",
                "part1_section",
                "part1_size",
                "part1_status",
                "part1_solved",
                "part1_search_time_s",
                "part1_plan_length",
                "part1_problem_file",
                "part2_section",
                "part2_size",
                "part2_status",
                "part2_solved",
                "part2_search_time_s",
                "part2_plan_length",
                "part2_problem_file",
                "delta_search_time_s",
                "delta_search_time_pct",
                "delta_plan_length",
                "comparison_note",
            ]
        )
        for row in rows:
            p1 = row.part1
            p2 = row.part2
            writer.writerow(
                [
                    row.key.group,
                    row.key.algorithm,
                    row.key.search,
                    row.key.heuristic,
                    "" if p1 is None else p1.section,
                    "" if p1 is None else _fmt_int(p1.size),
                    "" if p1 is None else p1.status,
                    "" if p1 is None else _fmt_bool(p1.solved),
                    "" if p1 is None else _fmt_float(p1.search_time_s),
                    "" if p1 is None else _fmt_int(p1.plan_length),
                    "" if p1 is None else p1.problem_file,
                    "" if p2 is None else p2.section,
                    "" if p2 is None else _fmt_int(p2.size),
                    "" if p2 is None else p2.status,
                    "" if p2 is None else _fmt_bool(p2.solved),
                    "" if p2 is None else _fmt_float(p2.search_time_s),
                    "" if p2 is None else _fmt_int(p2.plan_length),
                    "" if p2 is None else p2.problem_file,
                    _fmt_float(row.delta_search_time_s),
                    _fmt_float(row.delta_search_time_pct),
                    _fmt_int(row.delta_plan_length),
                    row.note,
                ]
            )


def _md_escape(text: str) -> str:
    return text.replace("|", r"\|").replace("\n", " ").replace("\r", " ")


def _group_summary(rows: List[DiffRow]) -> Tuple[int, int, int]:
    total = len(rows)
    comparable_time = sum(1 for r in rows if r.delta_search_time_s is not None)
    comparable_plan = sum(1 for r in rows if r.delta_plan_length is not None)
    return total, comparable_time, comparable_plan


def write_markdown_report(path: Path, rows: List[DiffRow], args: argparse.Namespace) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)

    by_group: Dict[str, List[DiffRow]] = {}
    for row in rows:
        by_group.setdefault(row.key.group, []).append(row)

    total, comparable_time, comparable_plan = _group_summary(rows)

    lines: List[str] = []
    lines.append("# Part1 vs Part2 - Technical Comparison (1.3.2/1.3.3 vs 2.1.2/2.1.3)")
    lines.append("")
    lines.append(f"- Generated at: `{dt.datetime.now().isoformat(timespec='seconds')}`")
    lines.append("- Time metric compared: `search_time_s`")
    lines.append("- Delta convention: `delta = part2 - part1` (negative means improvement in part2)")
    lines.append("")
    lines.append("## Sources")
    lines.append("")
    lines.append(f"- part1 1.3.2: `{args.part1_132}`")
    lines.append(f"- part1 1.3.3: `{args.part1_133}`")
    lines.append(f"- part2 2.1.2: `{args.part2_212}`")
    lines.append(f"- part2 2.1.3: `{args.part2_213}`")
    lines.append("")
    lines.append("## Global Summary")
    lines.append("")
    lines.append("| total_combinations | comparable_time | comparable_plan_length |")
    lines.append("| --- | --- | --- |")
    lines.append(f"| {total} | {comparable_time} | {comparable_plan} |")
    lines.append("")

    for group in sorted(by_group.keys()):
        group_rows = sorted(
            by_group[group],
            key=lambda r: (r.key.algorithm, r.key.search, r.key.heuristic),
        )
        g_total, g_time, g_plan = _group_summary(group_rows)
        lines.append(f"## {group}")
        lines.append("")
        lines.append(f"- combinations: `{g_total}`")
        lines.append(f"- comparable time rows: `{g_time}`")
        lines.append(f"- comparable plan_length rows: `{g_plan}`")
        lines.append("")
        lines.append(
            "| algorithm | search | heuristic | part1_status | part1_time_s | part1_plan_length | part2_status | part2_time_s | part2_plan_length | delta_time_s | delta_time_pct | delta_plan_length | note |"
        )
        lines.append("| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |")
        for row in group_rows:
            p1 = row.part1
            p2 = row.part2
            lines.append(
                "| "
                + " | ".join(
                    [
                        _md_escape(row.key.algorithm),
                        _md_escape(row.key.search),
                        _md_escape(row.key.heuristic),
                        _md_escape("" if p1 is None else p1.status),
                        _md_escape("" if p1 is None else _fmt_float(p1.search_time_s)),
                        _md_escape("" if p1 is None else _fmt_int(p1.plan_length)),
                        _md_escape("" if p2 is None else p2.status),
                        _md_escape("" if p2 is None else _fmt_float(p2.search_time_s)),
                        _md_escape("" if p2 is None else _fmt_int(p2.plan_length)),
                        _md_escape(_fmt_float(row.delta_search_time_s)),
                        _md_escape(_fmt_float(row.delta_search_time_pct)),
                        _md_escape(_fmt_int(row.delta_plan_length)),
                        _md_escape(row.note),
                    ]
                )
                + " |"
            )
        lines.append("")

    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    args = parse_args()

    for candidate in [args.part1_132, args.part1_133, args.part2_212, args.part2_213]:
        validate_csv(candidate)

    part1_132 = load_benchmark_csv(args.part1_132, "1.3.2_vs_2.1.2")
    part2_212 = load_benchmark_csv(args.part2_212, "1.3.2_vs_2.1.2")
    part1_133 = load_benchmark_csv(args.part1_133, "1.3.3_vs_2.1.3")
    part2_213 = load_benchmark_csv(args.part2_213, "1.3.3_vs_2.1.3")

    rows_132 = compute_diffs(part1_132, part2_212)
    rows_133 = compute_diffs(part1_133, part2_213)
    all_rows = rows_132 + rows_133

    write_diff_csv(args.out_csv, all_rows)
    write_markdown_report(args.out_md, all_rows, args)

    print(f"Done. CSV: {args.out_csv}")
    print(f"Done. MD:  {args.out_md}")


if __name__ == "__main__":
    main()
