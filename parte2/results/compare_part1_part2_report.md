# Part1 vs Part2 - Technical Comparison (1.3.2/1.3.3 vs 2.1.2/2.1.3)

- Generated at: `2026-03-21T20:08:06`
- Time metric compared: `search_time_s`
- Delta convention: `delta = part2 - part1` (negative means improvement in part2)

## Sources

- part1 1.3.2: `/mnt/c/Users/05jan/Desktop/Tareas/Uni/3_Curso/2_cuatri/Planificacion_automatica/Lab/PL1/Planning-practice/parte1/results/benchmark_pyperplan_part13_132.csv`
- part1 1.3.3: `/mnt/c/Users/05jan/Desktop/Tareas/Uni/3_Curso/2_cuatri/Planificacion_automatica/Lab/PL1/Planning-practice/parte1/results/benchmark_pyperplan_part13_133.csv`
- part2 2.1.2: `/mnt/c/Users/05jan/Desktop/Tareas/Uni/3_Curso/2_cuatri/Planificacion_automatica/Lab/PL1/Planning-practice/parte2/results/benchmark_pyperplan_part21_212.csv`
- part2 2.1.3: `/mnt/c/Users/05jan/Desktop/Tareas/Uni/3_Curso/2_cuatri/Planificacion_automatica/Lab/PL1/Planning-practice/parte2/results/benchmark_pyperplan_part21_213.csv`

## Global Summary

| total_combinations | comparable_time | comparable_plan_length |
| --- | --- | --- |
| 12 | 8 | 8 |

## 1.3.2_vs_2.1.2

- combinations: `8`
- comparable time rows: `7`
- comparable plan_length rows: `7`

| algorithm | search | heuristic | part1_status | part1_time_s | part1_plan_length | part2_status | part2_time_s | part2_plan_length | delta_time_s | delta_time_pct | delta_plan_length | note |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| EHC | ehs | hadd | solved | 0.4400 | 27 | solved | 0.1400 | 15 | -0.3000 | -68.1818 | -12 | ok |
| EHC | ehs | hff | solved | 0.1600 | 25 | solved | 0.1000 | 15 | -0.0600 | -37.5000 | -10 | ok |
| EHC | ehs | hmax | timeout |  |  | solved | 1.7000 | 15 |  |  |  | part1_status=timeout;time_not_comparable;plan_not_comparable |
| EHC | ehs | landmark | solved | 0.1200 | 34 | solved | 0.0066 | 18 | -0.1134 | -94.5000 | -16 | ok |
| GBFS | gbf | hadd | solved | 0.1300 | 27 | solved | 0.0600 | 15 | -0.0700 | -53.8462 | -12 | ok |
| GBFS | gbf | hff | solved | 0.2100 | 23 | solved | 0.0540 | 15 | -0.1560 | -74.2857 | -8 | ok |
| GBFS | gbf | hmax | solved | 2.9000 | 26 | solved | 2.7000 | 18 | -0.2000 | -6.8966 | -8 | ok |
| GBFS | gbf | landmark | solved | 0.0220 | 28 | solved | 0.0056 | 17 | -0.0164 | -74.5455 | -11 | ok |

## 1.3.3_vs_2.1.3

- combinations: `4`
- comparable time rows: `1`
- comparable plan_length rows: `1`

| algorithm | search | heuristic | part1_status | part1_time_s | part1_plan_length | part2_status | part2_time_s | part2_plan_length | delta_time_s | delta_time_pct | delta_plan_length | note |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| A*+hMAX | astar | hmax | solved | 1.4000 | 16 | timeout |  |  |  |  |  | part2_status=timeout;time_not_comparable;plan_not_comparable |
| A*+lmcut | astar | lmcut | timeout |  |  | timeout |  |  |  |  |  | part1_status=timeout;part2_status=timeout;time_not_comparable;plan_not_comparable |
| BFS | bfs | - | solved | 0.7300 | 16 | solved | 0.9800 | 15 | 0.2500 | 34.2466 | -1 | ok |
| IDS | ids | - | timeout |  |  | timeout |  |  |  |  |  | part1_status=timeout;part2_status=timeout;time_not_comparable;plan_not_comparable |
