#!/usr/bin/env python3
"""Export manual command inventories for benchmark scripts (default settings).

This generates one TXT file per benchmark script under parte1/parte2/parte3.
Each file includes:
- precheck commands
- real default command sequence
- fallback potential commands
- runtime placeholder rules when behavior is data-dependent
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class CommandBlock:
    title: str
    commands: list[str]


def write_inventory(path: Path, script: str, defaults: dict[str, str], cwd: str, blocks: list[CommandBlock], rules: list[str]) -> None:
    lines: list[str] = []
    lines.append(f"[SCRIPT]\t{script}")
    lines.append(f"[CWD]\t{cwd}")
    lines.append("[DEFAULTS]")
    for key, value in defaults.items():
        lines.append(f"{key}\t{value}")
    lines.append("")

    for block in blocks:
        lines.append(f"[{block.title}]")
        if not block.commands:
            lines.append("(none)")
        else:
            for idx, cmd in enumerate(block.commands, start=1):
                lines.append(f"{idx:04d}\t{cmd}")
        lines.append("")

    lines.append("[RUNTIME_RULES_FOR_PLACEHOLDERS]")
    if not rules:
        lines.append("(none)")
    else:
        for idx, rule in enumerate(rules, start=1):
            lines.append(f"{idx}. {rule}")

    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def sizes(min_size: int, max_size: int, step: int) -> list[int]:
    return list(range(min_size, max_size + 1, step))


def p1_problem_name(size_value: int) -> str:
    return f"drone_problem_d1_r0_l{size_value}_p{size_value}_c{size_value}_g{size_value}_ct2.pddl"


def p2_problem_name_ex1(size_value: int) -> str:
    return f"drone_problem_ex1_d1_r1_l{size_value}_p{size_value}_c{size_value}_g{size_value}_a4.pddl"


def p2_problem_name_ex2(size_value: int) -> str:
    return f"drone_problem_ex2_d1_r1_l{size_value}_p{size_value}_c{size_value}_g{size_value}_a4.pddl"


def p3_problem_name(drones: int, size_value: int) -> str:
    carriers = drones
    return f"drone_problem_d{drones}_r{carriers}_l{size_value}_p{size_value}_c{size_value}_g{size_value}_a4.pddl"


def export_parte1_ff(repo: Path) -> None:
    part = repo / "parte1"
    out = part / "comandos_benchmark_ff_graph_default.txt"
    default_sizes = sizes(2, 60, 1)

    real: list[str] = []
    fallback: list[str] = []

    for s in default_sizes:
        p = p1_problem_name(s)
        real.append(
            f"python3 generate-problem.py -d 1 -r 0 -l {s} -p {s} -c {s} -g {s}"
        )
        real.append(
            f"planutils run ff -- __benchmark_domain__.pddl {p}"
        )
        fallback.append(
            f"ff __benchmark_domain__.pddl {p}"
        )

    write_inventory(
        path=out,
        script="benchmark_ff_graph.py",
        defaults={
            "min_size": "2",
            "max_size": "60",
            "step": "1",
            "timeout": "60",
            "domain": "dronedomain.pddl",
            "generator": "generate-problem.py",
            "results_dir": "results",
            "seed_base": "0",
        },
        cwd="Planning-practice/parte1 (FF commands run from results/problems internally)",
        blocks=[
            CommandBlock("PRECHECK_COMMANDS", []),
            CommandBlock("REAL_DEFAULT_COMMANDS", real),
            CommandBlock("FALLBACK_POTENTIAL_COMMANDS", fallback),
        ],
        rules=[],
    )


def export_parte1_pyperplan(repo: Path) -> None:
    part = repo / "parte1"
    out = part / "comandos_benchmark_pyperplan_part13_default.txt"
    default_sizes = sizes(2, 40, 2)

    pre = ["planutils run pyperplan -- --help"]
    real: list[str] = []

    for s in default_sizes:
        p = p1_problem_name(s)
        rel = f"results/problems/{p}"
        real.append(f"python3 generate-problem.py -d 1 -r 0 -l {s} -p {s} -c {s} -g {s}")
        real.append(f"planutils run pyperplan -- -s bfs dronedomain.pddl {rel}")
        real.append(f"planutils run pyperplan -- -s ids dronedomain.pddl {rel}")
        real.append(f"planutils run pyperplan -- -s astar -H hmax dronedomain.pddl {rel}")
        real.append(f"planutils run pyperplan -- -s gbfs -H hmax dronedomain.pddl {rel}")

    real.append("planutils run pyperplan -- -s gbfs -H hmax dronedomain.pddl results/problems/drone_problem_d1_r0_l<ANCHOR_132_SIZE>_p<ANCHOR_132_SIZE>_c<ANCHOR_132_SIZE>_g<ANCHOR_132_SIZE>_ct2.pddl")
    real.append("planutils run pyperplan -- -s gbfs -H hadd dronedomain.pddl results/problems/drone_problem_d1_r0_l<ANCHOR_132_SIZE>_p<ANCHOR_132_SIZE>_c<ANCHOR_132_SIZE>_g<ANCHOR_132_SIZE>_ct2.pddl")
    real.append("planutils run pyperplan -- -s gbfs -H hff dronedomain.pddl results/problems/drone_problem_d1_r0_l<ANCHOR_132_SIZE>_p<ANCHOR_132_SIZE>_c<ANCHOR_132_SIZE>_g<ANCHOR_132_SIZE>_ct2.pddl")
    real.append("planutils run pyperplan -- -s gbfs -H landmark dronedomain.pddl results/problems/drone_problem_d1_r0_l<ANCHOR_132_SIZE>_p<ANCHOR_132_SIZE>_c<ANCHOR_132_SIZE>_g<ANCHOR_132_SIZE>_ct2.pddl")
    real.append("planutils run pyperplan -- -s ehc -H hmax dronedomain.pddl results/problems/drone_problem_d1_r0_l<ANCHOR_132_SIZE>_p<ANCHOR_132_SIZE>_c<ANCHOR_132_SIZE>_g<ANCHOR_132_SIZE>_ct2.pddl")
    real.append("planutils run pyperplan -- -s ehc -H hadd dronedomain.pddl results/problems/drone_problem_d1_r0_l<ANCHOR_132_SIZE>_p<ANCHOR_132_SIZE>_c<ANCHOR_132_SIZE>_g<ANCHOR_132_SIZE>_ct2.pddl")
    real.append("planutils run pyperplan -- -s ehc -H hff dronedomain.pddl results/problems/drone_problem_d1_r0_l<ANCHOR_132_SIZE>_p<ANCHOR_132_SIZE>_c<ANCHOR_132_SIZE>_g<ANCHOR_132_SIZE>_ct2.pddl")
    real.append("planutils run pyperplan -- -s ehc -H landmark dronedomain.pddl results/problems/drone_problem_d1_r0_l<ANCHOR_132_SIZE>_p<ANCHOR_132_SIZE>_c<ANCHOR_132_SIZE>_g<ANCHOR_132_SIZE>_ct2.pddl")

    real.append("planutils run pyperplan -- -s bfs dronedomain.pddl results/problems/drone_problem_d1_r0_l<ANCHOR_133_SIZE>_p<ANCHOR_133_SIZE>_c<ANCHOR_133_SIZE>_g<ANCHOR_133_SIZE>_ct2.pddl")
    real.append("planutils run pyperplan -- -s ids dronedomain.pddl results/problems/drone_problem_d1_r0_l<ANCHOR_133_SIZE>_p<ANCHOR_133_SIZE>_c<ANCHOR_133_SIZE>_g<ANCHOR_133_SIZE>_ct2.pddl")
    real.append("planutils run pyperplan -- -s astar -H hmax dronedomain.pddl results/problems/drone_problem_d1_r0_l<ANCHOR_133_SIZE>_p<ANCHOR_133_SIZE>_c<ANCHOR_133_SIZE>_g<ANCHOR_133_SIZE>_ct2.pddl")
    real.append("planutils run pyperplan -- -s astar -H lmcut dronedomain.pddl results/problems/drone_problem_d1_r0_l<ANCHOR_133_SIZE>_p<ANCHOR_133_SIZE>_c<ANCHOR_133_SIZE>_g<ANCHOR_133_SIZE>_ct2.pddl")

    write_inventory(
        path=out,
        script="benchmark_pyperplan_part13.py",
        defaults={
            "min_size": "2",
            "max_size": "40",
            "step": "2",
            "timeout": "60",
            "domain": "dronedomain.pddl",
            "generator": "generate-problem.py",
            "results_dir": "results",
        },
        cwd="Planning-practice/parte1",
        blocks=[
            CommandBlock("PRECHECK_COMMANDS", pre),
            CommandBlock("REAL_DEFAULT_COMMANDS", real),
            CommandBlock("FALLBACK_POTENTIAL_COMMANDS", []),
        ],
        rules=[
            "ANCHOR_132_SIZE = mayor size con status=solved en seccion 1.3.1 para algoritmo GBFS+hMAX.",
            "ANCHOR_133_SIZE = mayor size con status=solved en seccion 1.3.1 para algoritmo A*+hMAX.",
            "Si un anchor no existe, ese bloque (1.3.2 o 1.3.3) ejecuta 0 comandos.",
        ],
    )


def export_parte2_ff(repo: Path) -> None:
    part = repo / "parte2"
    out = part / "comandos_benchmark_ff_graph_part21_default.txt"
    default_sizes = sizes(2, 80, 2)

    real: list[str] = []
    fallback: list[str] = []

    for s in default_sizes:
        p = p2_problem_name_ex1(s)
        real.append(
            f"python3 generate-problem.py -d 1 -r 1 -l {s} -p {s} -c {s} -g {s} -a 4 --exercise 1"
        )
        real.append(f"planutils run ff -- __benchmark_domain__.pddl {p}")
        fallback.append(f"ff __benchmark_domain__.pddl {p}")

    write_inventory(
        path=out,
        script="benchmark_ff_graph_part21.py",
        defaults={
            "min_size": "2",
            "max_size": "80",
            "step": "2",
            "timeout": "60",
            "domain": "dronedomain.pddl",
            "generator": "generate-problem.py",
            "results_dir": "results",
            "drones": "1",
            "carriers": "1",
            "carrier_capacity": "4",
            "exercise": "1",
            "seed": "None",
        },
        cwd="Planning-practice/parte2 (FF commands run from results/problems internally)",
        blocks=[
            CommandBlock("PRECHECK_COMMANDS", []),
            CommandBlock("REAL_DEFAULT_COMMANDS", real),
            CommandBlock("FALLBACK_POTENTIAL_COMMANDS", fallback),
        ],
        rules=[],
    )


def export_parte2_pyperplan(repo: Path) -> None:
    part = repo / "parte2"
    out = part / "comandos_benchmark_pyperplan_part21_default.txt"
    default_sizes = sizes(2, 40, 2)

    pre = ["planutils run pyperplan -- --help"]
    real: list[str] = []

    for s in default_sizes:
        p = p2_problem_name_ex1(s)
        rel = f"results/problems/{p}"
        real.append(f"python3 generate-problem.py -d 1 -r 1 -l {s} -p {s} -c {s} -g {s} -a 4 --exercise 1")
        real.append(f"planutils run pyperplan -- -s bfs dronedomain.pddl {rel}")
        real.append(f"planutils run pyperplan -- -s ids dronedomain.pddl {rel}")
        real.append(f"planutils run pyperplan -- -s astar -H hmax dronedomain.pddl {rel}")
        real.append(f"planutils run pyperplan -- -s gbfs -H hmax dronedomain.pddl {rel}")

    real.append("planutils run pyperplan -- -s gbfs -H hmax dronedomain.pddl results/problems/drone_problem_ex1_d1_r1_l<ANCHOR_212_SIZE>_p<ANCHOR_212_SIZE>_c<ANCHOR_212_SIZE>_g<ANCHOR_212_SIZE>_a4.pddl")
    real.append("planutils run pyperplan -- -s gbfs -H hadd dronedomain.pddl results/problems/drone_problem_ex1_d1_r1_l<ANCHOR_212_SIZE>_p<ANCHOR_212_SIZE>_c<ANCHOR_212_SIZE>_g<ANCHOR_212_SIZE>_a4.pddl")
    real.append("planutils run pyperplan -- -s gbfs -H hff dronedomain.pddl results/problems/drone_problem_ex1_d1_r1_l<ANCHOR_212_SIZE>_p<ANCHOR_212_SIZE>_c<ANCHOR_212_SIZE>_g<ANCHOR_212_SIZE>_a4.pddl")
    real.append("planutils run pyperplan -- -s gbfs -H landmark dronedomain.pddl results/problems/drone_problem_ex1_d1_r1_l<ANCHOR_212_SIZE>_p<ANCHOR_212_SIZE>_c<ANCHOR_212_SIZE>_g<ANCHOR_212_SIZE>_a4.pddl")
    real.append("planutils run pyperplan -- -s ehc -H hmax dronedomain.pddl results/problems/drone_problem_ex1_d1_r1_l<ANCHOR_212_SIZE>_p<ANCHOR_212_SIZE>_c<ANCHOR_212_SIZE>_g<ANCHOR_212_SIZE>_a4.pddl")
    real.append("planutils run pyperplan -- -s ehc -H hadd dronedomain.pddl results/problems/drone_problem_ex1_d1_r1_l<ANCHOR_212_SIZE>_p<ANCHOR_212_SIZE>_c<ANCHOR_212_SIZE>_g<ANCHOR_212_SIZE>_a4.pddl")
    real.append("planutils run pyperplan -- -s ehc -H hff dronedomain.pddl results/problems/drone_problem_ex1_d1_r1_l<ANCHOR_212_SIZE>_p<ANCHOR_212_SIZE>_c<ANCHOR_212_SIZE>_g<ANCHOR_212_SIZE>_a4.pddl")
    real.append("planutils run pyperplan -- -s ehc -H landmark dronedomain.pddl results/problems/drone_problem_ex1_d1_r1_l<ANCHOR_212_SIZE>_p<ANCHOR_212_SIZE>_c<ANCHOR_212_SIZE>_g<ANCHOR_212_SIZE>_a4.pddl")

    real.append("planutils run pyperplan -- -s bfs dronedomain.pddl results/problems/drone_problem_ex1_d1_r1_l<ANCHOR_213_SIZE>_p<ANCHOR_213_SIZE>_c<ANCHOR_213_SIZE>_g<ANCHOR_213_SIZE>_a4.pddl")
    real.append("planutils run pyperplan -- -s ids dronedomain.pddl results/problems/drone_problem_ex1_d1_r1_l<ANCHOR_213_SIZE>_p<ANCHOR_213_SIZE>_c<ANCHOR_213_SIZE>_g<ANCHOR_213_SIZE>_a4.pddl")
    real.append("planutils run pyperplan -- -s astar -H hmax dronedomain.pddl results/problems/drone_problem_ex1_d1_r1_l<ANCHOR_213_SIZE>_p<ANCHOR_213_SIZE>_c<ANCHOR_213_SIZE>_g<ANCHOR_213_SIZE>_a4.pddl")
    real.append("planutils run pyperplan -- -s astar -H lmcut dronedomain.pddl results/problems/drone_problem_ex1_d1_r1_l<ANCHOR_213_SIZE>_p<ANCHOR_213_SIZE>_c<ANCHOR_213_SIZE>_g<ANCHOR_213_SIZE>_a4.pddl")

    write_inventory(
        path=out,
        script="benchmark_pyperplan_part21.py",
        defaults={
            "min_size": "2",
            "max_size": "40",
            "step": "2",
            "timeout": "60",
            "domain": "dronedomain.pddl",
            "generator": "generate-problem.py",
            "results_dir": "results",
            "drones": "1",
            "carriers": "1",
            "carrier_capacity": "4",
            "exercise": "1",
            "seed": "None",
        },
        cwd="Planning-practice/parte2",
        blocks=[
            CommandBlock("PRECHECK_COMMANDS", pre),
            CommandBlock("REAL_DEFAULT_COMMANDS", real),
            CommandBlock("FALLBACK_POTENTIAL_COMMANDS", []),
        ],
        rules=[
            "ANCHOR_212_SIZE = mayor size con status=solved en seccion 2.1.1 para algoritmo GBFS+hMAX.",
            "ANCHOR_213_SIZE = mayor size con status=solved en seccion 2.1.1 para algoritmo A*+hMAX.",
            "Si un anchor no existe, ese bloque (2.1.2 o 2.1.3) ejecuta 0 comandos.",
        ],
    )


def export_parte2_cost(repo: Path) -> None:
    part = repo / "parte2"
    out = part / "comandos_benchmark_cost_planners_part22_default.txt"
    default_sizes = sizes(2, 20, 2)

    part_abs = part.resolve()
    domain_abs = part_abs / "dronedomain2.pddl"

    planner_specs = [
        ("metric-ff", "metric-ff", None),
        ("downward__lama-first", "downward", "lama-first"),
        ("downward__seq-sat-fdss-2", "downward", "seq-sat-fdss-2"),
        ("downward__seq-sat-fd-autotune-2", "downward", "seq-sat-fd-autotune-2"),
        ("downward__seq-opt-lmcut", "downward", "seq-opt-lmcut"),
        ("downward__seq-opt-bjolp", "downward", "seq-opt-bjolp"),
        ("downward__seq-opt-fdss-2", "downward", "seq-opt-fdss-2"),
    ]

    real: list[str] = []
    fallback: list[str] = []

    for s in default_sizes:
        real.append(
            f"python3 generate-problem.py -d 1 -r 1 -l {s} -p {s} -c {s} -g {s} -a 4 --exercise 2"
        )

    for slug, tool, alias in planner_specs:
        for s in default_sizes:
            problem_abs = part_abs / "results" / "problems" / p2_problem_name_ex2(s)
            plan_abs = part_abs / "results" / "planner_artifacts" / slug / f"size_{s}.plan"

            if tool == "metric-ff":
                real.append(f"planutils run metric-ff -- {domain_abs} {problem_abs}")
                fallback.append(f"metric-ff {domain_abs} {problem_abs}")
                fallback.append(f"metric-ff -o {domain_abs} -f {problem_abs}")
                continue

            real.append(
                "planutils run downward -- "
                f"--alias {alias} --overall-time-limit 60 --plan-file {plan_abs} {domain_abs} {problem_abs}"
            )
            fallback.append(
                f"downward --alias {alias} --overall-time-limit 60 --plan-file {plan_abs} {domain_abs} {problem_abs}"
            )
            fallback.append(
                f"fast-downward.py --alias {alias} --overall-time-limit 60 --plan-file {plan_abs} {domain_abs} {problem_abs}"
            )
            fallback.append(
                f"fast-downward --alias {alias} --overall-time-limit 60 --plan-file {plan_abs} {domain_abs} {problem_abs}"
            )

            if alias == "seq-opt-fdss-2":
                alias2 = "seq-opt-fdss2"
                fallback.append(
                    "planutils run downward -- "
                    f"--alias {alias2} --overall-time-limit 60 --plan-file {plan_abs} {domain_abs} {problem_abs}"
                )
                fallback.append(
                    f"downward --alias {alias2} --overall-time-limit 60 --plan-file {plan_abs} {domain_abs} {problem_abs}"
                )
                fallback.append(
                    f"fast-downward.py --alias {alias2} --overall-time-limit 60 --plan-file {plan_abs} {domain_abs} {problem_abs}"
                )
                fallback.append(
                    f"fast-downward --alias {alias2} --overall-time-limit 60 --plan-file {plan_abs} {domain_abs} {problem_abs}"
                )

    write_inventory(
        path=out,
        script="benchmark_cost_planners_part22.py",
        defaults={
            "min_size": "2",
            "max_size": "20",
            "step": "2",
            "timeout": "60",
            "domain": "dronedomain2.pddl",
            "generator": "generate-problem.py",
            "results_dir": "results",
            "drones": "1",
            "carriers": "1",
            "carrier_capacity": "4",
            "exercise": "2",
            "seed": "None",
        },
        cwd="Planning-practice/parte2",
        blocks=[
            CommandBlock("PRECHECK_COMMANDS", []),
            CommandBlock("REAL_DEFAULT_COMMANDS", real),
            CommandBlock("FALLBACK_POTENTIAL_COMMANDS", fallback),
        ],
        rules=[
            "Orden real del script: por planner (en orden fijo) y dentro por size ascendente.",
            "Si un planner queda unsupported en un size, el script marca unsupported cacheado para sizes siguientes.",
        ],
    )


def export_parte3_lpg(repo: Path) -> None:
    part = repo / "parte3"
    out = part / "comandos_benchmark_lpgtd_part3_default.txt"

    drones_values = list(range(1, 11))
    default_sizes = sizes(2, 30, 1)

    pre = ["python3 generate-problem.py --help"]
    real: list[str] = []
    fallback: list[str] = []

    for d in drones_values:
        for s in default_sizes:
            p = p3_problem_name(d, s)
            p_abs = (part / "results" / "problems" / p).resolve()
            plan_abs = (part / "results" / "plans" / f"lpgtd_quality_{Path(p).stem}.SOL").resolve()

            real.append(
                f"python3 generate-problem.py -d {d} -r {d} -l {s} -p {s} -c {s} -g {s} -a 4"
            )
            real.append(
                f"planutils run lpg-td -- -o {(part / 'dronedomain.pddl').resolve()} -f {p_abs} -quality -cputime 60 -out {plan_abs}"
            )
            fallback.append(
                f"lpg-td -o {(part / 'dronedomain.pddl').resolve()} -f {p_abs} -quality -cputime 60 -out {plan_abs}"
            )
            fallback.append(
                f"lpg -o {(part / 'dronedomain.pddl').resolve()} -f {p_abs} -quality -cputime 60 -out {plan_abs}"
            )

    for d in drones_values:
        p_abs = (part / "results" / "problems" / p3_problem_name(d, -1)).resolve()
        speed_plan_abs = (part / "results" / "plans" / f"lpgtd_speed_drone_problem_d{d}_r{d}_l<BEST_QUALITY_SIZE_D{d}>_p<BEST_QUALITY_SIZE_D{d}>_c<BEST_QUALITY_SIZE_D{d}>_g<BEST_QUALITY_SIZE_D{d}>_a4.SOL").resolve()
        real.append(
            "planutils run lpg-td -- "
            f"-o {(part / 'dronedomain.pddl').resolve()} "
            f"-f {str(p_abs).replace('_l-1_p-1_c-1_g-1_a4.pddl', '_l<BEST_QUALITY_SIZE_D'+str(d)+'>_p<BEST_QUALITY_SIZE_D'+str(d)+'>_c<BEST_QUALITY_SIZE_D'+str(d)+'>_g<BEST_QUALITY_SIZE_D'+str(d)+'>_a4.pddl')} "
            f"-speed -cputime 60 -out {speed_plan_abs}"
        )
        fallback.append(
            f"lpg-td -o {(part / 'dronedomain.pddl').resolve()} -f {str(p_abs).replace('_l-1_p-1_c-1_g-1_a4.pddl', '_l<BEST_QUALITY_SIZE_D'+str(d)+'>_p<BEST_QUALITY_SIZE_D'+str(d)+'>_c<BEST_QUALITY_SIZE_D'+str(d)+'>_g<BEST_QUALITY_SIZE_D'+str(d)+'>_a4.pddl')} -speed -cputime 60 -out {speed_plan_abs}"
        )
        fallback.append(
            f"lpg -o {(part / 'dronedomain.pddl').resolve()} -f {str(p_abs).replace('_l-1_p-1_c-1_g-1_a4.pddl', '_l<BEST_QUALITY_SIZE_D'+str(d)+'>_p<BEST_QUALITY_SIZE_D'+str(d)+'>_c<BEST_QUALITY_SIZE_D'+str(d)+'>_g<BEST_QUALITY_SIZE_D'+str(d)+'>_a4.pddl')} -speed -cputime 60 -out {speed_plan_abs}"
        )

    write_inventory(
        path=out,
        script="benchmark_lpgtd_part3.py",
        defaults={
            "min_drones": "1",
            "max_drones": "10",
            "min_size": "2",
            "max_size": "30",
            "step": "1",
            "timeout": "60",
            "stop_after_fails": "2",
            "domain": "dronedomain.pddl",
            "generator": "generate-problem.py",
            "results_dir": "results",
            "carrier_capacity": "4",
            "seed": "None",
            "lpg_seed": "None",
        },
        cwd="Planning-practice/parte3",
        blocks=[
            CommandBlock("PRECHECK_COMMANDS", pre),
            CommandBlock("REAL_DEFAULT_COMMANDS", real),
            CommandBlock("FALLBACK_POTENTIAL_COMMANDS", fallback),
        ],
        rules=[
            "Lista expandida en barrido completo (2..30 para cada dron), aunque el script puede cortar antes por stop-after-fails.",
            "BEST_QUALITY_SIZE_Dn = mayor size con status=solved en modo quality para ese dron n.",
            "Si no existe BEST_QUALITY_SIZE_Dn, el comando speed de ese dron no se ejecuta.",
        ],
    )


def export_parte3_optic(repo: Path) -> None:
    part = repo / "parte3"
    out = part / "comandos_benchmark_optic_part3_default.txt"

    drones_values = list(range(1, 6))
    default_sizes = sizes(2, 20, 1)

    pre = ["python3 generate-problem.py --help"]
    real: list[str] = []
    fallback: list[str] = []

    for d in drones_values:
        for s in default_sizes:
            p = p3_problem_name(d, s)
            p_abs = (part / "results" / "problems" / p).resolve()
            domain_abs = (part / "dronedomain.pddl").resolve()

            real.append(
                f"python3 generate-problem.py -d {d} -r {d} -l {s} -p {s} -c {s} -g {s} -a 4"
            )
            real.append(f"planutils run optic -- {domain_abs} {p_abs}")
            fallback.append(f"optic {domain_abs} {p_abs}")

    write_inventory(
        path=out,
        script="benchmark_optic_part3.py",
        defaults={
            "min_drones": "1",
            "max_drones": "5",
            "min_size": "2",
            "max_size": "20",
            "step": "1",
            "timeout": "60",
            "stop_after_fails": "2",
            "domain": "dronedomain.pddl",
            "generator": "generate-problem.py",
            "results_dir": "results",
            "carrier_capacity": "4",
            "seed": "None",
        },
        cwd="Planning-practice/parte3",
        blocks=[
            CommandBlock("PRECHECK_COMMANDS", pre),
            CommandBlock("REAL_DEFAULT_COMMANDS", real),
            CommandBlock("FALLBACK_POTENTIAL_COMMANDS", fallback),
        ],
        rules=[
            "Lista expandida en barrido completo (2..20 para cada dron), aunque el script puede cortar antes por stop-after-fails.",
        ],
    )


def main() -> None:
    repo = Path(__file__).resolve().parents[1]

    export_parte1_ff(repo)
    export_parte1_pyperplan(repo)
    export_parte2_ff(repo)
    export_parte2_pyperplan(repo)
    export_parte2_cost(repo)
    export_parte3_lpg(repo)
    export_parte3_optic(repo)

    print("Generated command inventories:")
    print("- parte1/comandos_benchmark_ff_graph_default.txt")
    print("- parte1/comandos_benchmark_pyperplan_part13_default.txt")
    print("- parte2/comandos_benchmark_ff_graph_part21_default.txt")
    print("- parte2/comandos_benchmark_pyperplan_part21_default.txt")
    print("- parte2/comandos_benchmark_cost_planners_part22_default.txt")
    print("- parte3/comandos_benchmark_lpgtd_part3_default.txt")
    print("- parte3/comandos_benchmark_optic_part3_default.txt")


if __name__ == "__main__":
    main()
