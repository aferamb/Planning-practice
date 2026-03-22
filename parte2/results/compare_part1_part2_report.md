# Part1 vs Part2 - Technical Comparison (1.3.2/1.3.3 vs 2.1.2/2.1.3)

- Generated at: `2026-03-22T04:35:57`
- Time metric compared: `search_time_s`
- Delta convention: `delta = part2 - part1` (negative means improvement in part2)

## Sources

- part1 1.3.2: `C:\Users\05jan\Desktop\Tareas\Uni\3_Curso\2_cuatri\Planificacion_automatica\Lab\PL1\Planning-practice\parte1\results\benchmark_pyperplan_part13_132.csv`
- part1 1.3.3: `C:\Users\05jan\Desktop\Tareas\Uni\3_Curso\2_cuatri\Planificacion_automatica\Lab\PL1\Planning-practice\parte1\results\benchmark_pyperplan_part13_133.csv`
- part2 2.1.2: `C:\Users\05jan\Desktop\Tareas\Uni\3_Curso\2_cuatri\Planificacion_automatica\Lab\PL1\Planning-practice\parte2\results\benchmark_pyperplan_part21_212.csv`
- part2 2.1.3: `C:\Users\05jan\Desktop\Tareas\Uni\3_Curso\2_cuatri\Planificacion_automatica\Lab\PL1\Planning-practice\parte2\results\benchmark_pyperplan_part21_213.csv`

## Global Summary

| total_combinations | comparable_time | comparable_plan_length |
| --- | --- | --- |
| 14 | 10 | 10 |

## 1.3.2_vs_2.1.2

- combinations: `8`
- comparable time rows: `7`
- comparable plan_length rows: `7`

| algorithm | search | heuristic | part1_status | part1_time_s | part1_plan_length | part2_status | part2_time_s | part2_plan_length | delta_time_s | delta_time_pct | delta_plan_length | note |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| EHC | ehs | hadd | solved | 0.0980 | 22 | solved | 0.1400 | 21 | 0.0420 | 42.8571 | -1 | ok |
| EHC | ehs | hff | solved | 0.1700 | 22 | solved | 0.1800 | 19 | 0.0100 | 5.8824 | -3 | ok |
| EHC | ehs | hmax | timeout |  |  | timeout |  |  |  |  |  | part1_status=timeout;part2_status=timeout;time_not_comparable;plan_not_comparable |
| EHC | ehs | landmark | solved | 0.0350 | 27 | solved | 0.0250 | 23 | -0.0100 | -28.5714 | -4 | ok |
| GBFS | gbf | hadd | solved | 0.1100 | 23 | solved | 0.1100 | 19 | 0.0000 | 0.0000 | -4 | ok |
| GBFS | gbf | hff | solved | 0.1100 | 22 | solved | 0.1100 | 19 | 0.0000 | 0.0000 | -3 | ok |
| GBFS | gbf | hmax | solved | 4.8000 | 23 | solved | 2.7000 | 23 | -2.1000 | -43.7500 | 0 | ok |
| GBFS | gbf | landmark | solved | 0.0097 | 24 | solved | 0.0230 | 23 | 0.0133 | 137.1134 | -1 | ok |

## 1.3.3_vs_2.1.3

- combinations: `6`
- comparable time rows: `3`
- comparable plan_length rows: `3`

| algorithm | search | heuristic | part1_status | part1_time_s | part1_plan_length | part2_status | part2_time_s | part2_plan_length | delta_time_s | delta_time_pct | delta_plan_length | note |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| A*+blind | astar | blind | solved | 8.1000 | 18 | solved | 1.2000 | 15 | -6.9000 | -85.1852 | -3 | ok |
| A*+hMAX | astar | hmax | timeout |  |  | solved | 2.2000 | 15 |  |  |  | part1_status=timeout;time_not_comparable;plan_not_comparable |
| A*+landmark | astar | landmark | solved | 6.6000 | 18 | solved | 1.4000 | 15 | -5.2000 | -78.7879 | -3 | ok |
| A*+lmcut | astar | lmcut | timeout |  |  | timeout |  |  |  |  |  | part1_status=timeout;part2_status=timeout;time_not_comparable;plan_not_comparable |
| BFS | bfs | - | solved | 5.3000 | 18 | solved | 0.8200 | 15 | -4.4800 | -84.5283 | -3 | ok |
| IDS | ids | - | timeout |  |  | timeout |  |  |  |  |  | part1_status=timeout;part2_status=timeout;time_not_comparable;plan_not_comparable |
