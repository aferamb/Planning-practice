# Benchmark pyperplan - Practice 1 Part 1 Exercise 1.3

- Generated at: `2026-03-16T00:35:33`
- Args: `{'min_size': 2, 'max_size': 6, 'step': 2, 'timeout': 10, 'domain': 'dronedomain.pddl', 'generator': 'generate-problem.py', 'results_dir': 'results', 'problem_files': None}`

## [ALIASES]

| alias | value |
| --- | --- |
| search.BFS | bfs |
| search.IDS | ids |
| search.ASTAR | astar |
| search.GBFS | gbf |
| search.EHC | ehs |
| heuristic.HMAX | hmax |
| heuristic.HADD | hadd |
| heuristic.HFF | hff |
| heuristic.LANDMARK | landmark |
| heuristic.LMCUT | lmcut |

## [GENERATION]

| size | problem_file | status | wall_time_s | error_excerpt |
| --- | --- | --- | --- | --- |
| 2 | problems/drone_problem_d1_r0_l2_p2_c2_g2_ct2.pddl | ok | 0.0501 |  |
| 4 | problems/drone_problem_d1_r0_l4_p4_c4_g4_ct2.pddl | ok | 0.0540 |  |
| 6 | problems/drone_problem_d1_r0_l6_p6_c6_g6_ct2.pddl | ok | 0.0551 |  |

## [RAW_ROWS]

| section | algorithm | search | heuristic | size | status | solved | search_time_s | wall_time_s | plan_length | optimal | problem_file | error_excerpt |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1.3.1 | BFS | bfs |  | 2 | solved | yes | 0.0008 | 1.3304 | 6 | yes | problems/drone_problem_d1_r0_l2_p2_c2_g2_ct2.pddl |  |
| 1.3.1 | IDS | ids |  | 2 | solved | yes | 0.0014 | 1.3682 | 6 | yes | problems/drone_problem_d1_r0_l2_p2_c2_g2_ct2.pddl |  |
| 1.3.1 | A*+hMAX | astar | hmax | 2 | solved | yes | 0.0019 | 1.3444 | 6 | yes | problems/drone_problem_d1_r0_l2_p2_c2_g2_ct2.pddl |  |
| 1.3.1 | GBFS+hMAX | gbf | hmax | 2 | solved | yes | 0.0015 | 1.3068 | 6 | no | problems/drone_problem_d1_r0_l2_p2_c2_g2_ct2.pddl |  |
| 1.3.1 | BFS | bfs |  | 4 | solved | yes | 0.0370 | 1.3735 | 12 | yes | problems/drone_problem_d1_r0_l4_p4_c4_g4_ct2.pddl |  |
| 1.3.1 | IDS | ids |  | 4 | timeout | no |  | 10.0100 |  | yes | problems/drone_problem_d1_r0_l4_p4_c4_g4_ct2.pddl |  |
| 1.3.1 | A*+hMAX | astar | hmax | 4 | solved | yes | 0.6300 | 1.9618 | 12 | yes | problems/drone_problem_d1_r0_l4_p4_c4_g4_ct2.pddl |  |
| 1.3.1 | GBFS+hMAX | gbf | hmax | 4 | solved | yes | 0.0990 | 1.4628 | 14 | no | problems/drone_problem_d1_r0_l4_p4_c4_g4_ct2.pddl |  |
| 1.3.1 | BFS | bfs |  | 6 | solved | yes | 3.6000 | 5.0840 | 18 | yes | problems/drone_problem_d1_r0_l6_p6_c6_g6_ct2.pddl |  |
| 1.3.1 | IDS | ids |  | 6 | timeout | no |  | 10.0116 |  | yes | problems/drone_problem_d1_r0_l6_p6_c6_g6_ct2.pddl |  |
| 1.3.1 | A*+hMAX | astar | hmax | 6 | timeout | no |  | 10.0062 |  | yes | problems/drone_problem_d1_r0_l6_p6_c6_g6_ct2.pddl |  |
| 1.3.1 | GBFS+hMAX | gbf | hmax | 6 | timeout | no |  | 10.0084 |  | no | problems/drone_problem_d1_r0_l6_p6_c6_g6_ct2.pddl |  |
| 1.3.2 | GBFS | gbf | hmax | 4 | solved | yes | 0.1300 | 1.7619 | 14 | no | problems/drone_problem_d1_r0_l4_p4_c4_g4_ct2.pddl |  |
| 1.3.2 | GBFS | gbf | hadd | 4 | solved | yes | 0.0130 | 1.6760 | 15 | no | problems/drone_problem_d1_r0_l4_p4_c4_g4_ct2.pddl |  |
| 1.3.2 | GBFS | gbf | hff | 4 | solved | yes | 0.0110 | 1.6026 | 12 | no | problems/drone_problem_d1_r0_l4_p4_c4_g4_ct2.pddl |  |
| 1.3.2 | GBFS | gbf | landmark | 4 | solved | yes | 0.0024 | 1.5977 | 16 | no | problems/drone_problem_d1_r0_l4_p4_c4_g4_ct2.pddl |  |
| 1.3.2 | EHC | ehs | hmax | 4 | solved | yes | 0.9600 | 2.6416 | 14 | no | problems/drone_problem_d1_r0_l4_p4_c4_g4_ct2.pddl |  |
| 1.3.2 | EHC | ehs | hadd | 4 | solved | yes | 0.0092 | 1.5966 | 16 | no | problems/drone_problem_d1_r0_l4_p4_c4_g4_ct2.pddl |  |
| 1.3.2 | EHC | ehs | hff | 4 | solved | yes | 0.0069 | 1.5989 | 13 | no | problems/drone_problem_d1_r0_l4_p4_c4_g4_ct2.pddl |  |
| 1.3.2 | EHC | ehs | landmark | 4 | solved | yes | 0.0071 | 1.6478 | 19 | no | problems/drone_problem_d1_r0_l4_p4_c4_g4_ct2.pddl |  |
| 1.3.3 | BFS | bfs |  | 4 | solved | yes | 0.0450 | 1.7599 | 12 | yes | problems/drone_problem_d1_r0_l4_p4_c4_g4_ct2.pddl |  |
| 1.3.3 | IDS | ids |  | 4 | timeout | no |  | 10.0135 |  | yes | problems/drone_problem_d1_r0_l4_p4_c4_g4_ct2.pddl |  |
| 1.3.3 | A*+hMAX | astar | hmax | 4 | solved | yes | 0.7500 | 2.4713 | 12 | yes | problems/drone_problem_d1_r0_l4_p4_c4_g4_ct2.pddl |  |
| 1.3.3 | A*+lmcut | astar | lmcut | 4 | solved | yes | 1.6000 | 3.3622 | 12 | yes | problems/drone_problem_d1_r0_l4_p4_c4_g4_ct2.pddl |  |

## [TABLE_1.3.1_ALL_RUNS]

| section | algorithm | search | heuristic | size | status | solved | search_time_s | wall_time_s | plan_length | optimal | problem_file | error_excerpt |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1.3.1 | BFS | bfs |  | 2 | solved | yes | 0.0008 | 1.3304 | 6 | yes | problems/drone_problem_d1_r0_l2_p2_c2_g2_ct2.pddl |  |
| 1.3.1 | IDS | ids |  | 2 | solved | yes | 0.0014 | 1.3682 | 6 | yes | problems/drone_problem_d1_r0_l2_p2_c2_g2_ct2.pddl |  |
| 1.3.1 | A*+hMAX | astar | hmax | 2 | solved | yes | 0.0019 | 1.3444 | 6 | yes | problems/drone_problem_d1_r0_l2_p2_c2_g2_ct2.pddl |  |
| 1.3.1 | GBFS+hMAX | gbf | hmax | 2 | solved | yes | 0.0015 | 1.3068 | 6 | no | problems/drone_problem_d1_r0_l2_p2_c2_g2_ct2.pddl |  |
| 1.3.1 | BFS | bfs |  | 4 | solved | yes | 0.0370 | 1.3735 | 12 | yes | problems/drone_problem_d1_r0_l4_p4_c4_g4_ct2.pddl |  |
| 1.3.1 | IDS | ids |  | 4 | timeout | no |  | 10.0100 |  | yes | problems/drone_problem_d1_r0_l4_p4_c4_g4_ct2.pddl |  |
| 1.3.1 | A*+hMAX | astar | hmax | 4 | solved | yes | 0.6300 | 1.9618 | 12 | yes | problems/drone_problem_d1_r0_l4_p4_c4_g4_ct2.pddl |  |
| 1.3.1 | GBFS+hMAX | gbf | hmax | 4 | solved | yes | 0.0990 | 1.4628 | 14 | no | problems/drone_problem_d1_r0_l4_p4_c4_g4_ct2.pddl |  |
| 1.3.1 | BFS | bfs |  | 6 | solved | yes | 3.6000 | 5.0840 | 18 | yes | problems/drone_problem_d1_r0_l6_p6_c6_g6_ct2.pddl |  |
| 1.3.1 | IDS | ids |  | 6 | timeout | no |  | 10.0116 |  | yes | problems/drone_problem_d1_r0_l6_p6_c6_g6_ct2.pddl |  |
| 1.3.1 | A*+hMAX | astar | hmax | 6 | timeout | no |  | 10.0062 |  | yes | problems/drone_problem_d1_r0_l6_p6_c6_g6_ct2.pddl |  |
| 1.3.1 | GBFS+hMAX | gbf | hmax | 6 | timeout | no |  | 10.0084 |  | no | problems/drone_problem_d1_r0_l6_p6_c6_g6_ct2.pddl |  |

## [TABLE_1.3.2_ALL_RUNS]

| section | algorithm | search | heuristic | size | status | solved | search_time_s | wall_time_s | plan_length | optimal | problem_file | error_excerpt |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1.3.2 | GBFS | gbf | hmax | 4 | solved | yes | 0.1300 | 1.7619 | 14 | no | problems/drone_problem_d1_r0_l4_p4_c4_g4_ct2.pddl |  |
| 1.3.2 | GBFS | gbf | hadd | 4 | solved | yes | 0.0130 | 1.6760 | 15 | no | problems/drone_problem_d1_r0_l4_p4_c4_g4_ct2.pddl |  |
| 1.3.2 | GBFS | gbf | hff | 4 | solved | yes | 0.0110 | 1.6026 | 12 | no | problems/drone_problem_d1_r0_l4_p4_c4_g4_ct2.pddl |  |
| 1.3.2 | GBFS | gbf | landmark | 4 | solved | yes | 0.0024 | 1.5977 | 16 | no | problems/drone_problem_d1_r0_l4_p4_c4_g4_ct2.pddl |  |
| 1.3.2 | EHC | ehs | hmax | 4 | solved | yes | 0.9600 | 2.6416 | 14 | no | problems/drone_problem_d1_r0_l4_p4_c4_g4_ct2.pddl |  |
| 1.3.2 | EHC | ehs | hadd | 4 | solved | yes | 0.0092 | 1.5966 | 16 | no | problems/drone_problem_d1_r0_l4_p4_c4_g4_ct2.pddl |  |
| 1.3.2 | EHC | ehs | hff | 4 | solved | yes | 0.0069 | 1.5989 | 13 | no | problems/drone_problem_d1_r0_l4_p4_c4_g4_ct2.pddl |  |
| 1.3.2 | EHC | ehs | landmark | 4 | solved | yes | 0.0071 | 1.6478 | 19 | no | problems/drone_problem_d1_r0_l4_p4_c4_g4_ct2.pddl |  |

## [TABLE_1.3.3_ALL_RUNS]

| section | algorithm | search | heuristic | size | status | solved | search_time_s | wall_time_s | plan_length | optimal | problem_file | error_excerpt |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1.3.3 | BFS | bfs |  | 4 | solved | yes | 0.0450 | 1.7599 | 12 | yes | problems/drone_problem_d1_r0_l4_p4_c4_g4_ct2.pddl |  |
| 1.3.3 | IDS | ids |  | 4 | timeout | no |  | 10.0135 |  | yes | problems/drone_problem_d1_r0_l4_p4_c4_g4_ct2.pddl |  |
| 1.3.3 | A*+hMAX | astar | hmax | 4 | solved | yes | 0.7500 | 2.4713 | 12 | yes | problems/drone_problem_d1_r0_l4_p4_c4_g4_ct2.pddl |  |
| 1.3.3 | A*+lmcut | astar | lmcut | 4 | solved | yes | 1.6000 | 3.3622 | 12 | yes | problems/drone_problem_d1_r0_l4_p4_c4_g4_ct2.pddl |  |

## [SUMMARY_1.3.1]

| algorithm | max_solved_size | time_s | plan_length | optimal |
| --- | --- | --- | --- | --- |
| BFS | 6 | 3.6000 | 18 | yes |
| IDS | 2 | 0.0014 | 6 | yes |
| A*+hMAX | 4 | 0.6300 | 12 | yes |
| GBFS+hMAX | 4 | 0.0990 | 14 | no |

## [SUMMARY_1.3.2]

| combo | status | time_s | plan_length | size |
| --- | --- | --- | --- | --- |
| GBFS/hmax | solved | 0.1300 | 14 | 4 |
| GBFS/hadd | solved | 0.0130 | 15 | 4 |
| GBFS/hff | solved | 0.0110 | 12 | 4 |
| GBFS/landmark | solved | 0.0024 | 16 | 4 |
| EHC/hmax | solved | 0.9600 | 14 | 4 |
| EHC/hadd | solved | 0.0092 | 16 | 4 |
| EHC/hff | solved | 0.0069 | 13 | 4 |
| EHC/landmark | solved | 0.0071 | 19 | 4 |

## [SUMMARY_1.3.3]

| combo | status | time_s | plan_length | size | optimal |
| --- | --- | --- | --- | --- | --- |
| BFS/- | solved | 0.0450 | 12 | 4 | yes |
| IDS/- | timeout |  |  | 4 | yes |
| A*+hMAX/hmax | solved | 0.7500 | 12 | 4 | yes |
| A*+lmcut/lmcut | solved | 1.6000 | 12 | 4 | yes |

## [BEST_OPTIMAL_1.3.3]

- `BFS/-`: `0.0450s`, plan_length=`12`
