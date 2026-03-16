# Benchmark pyperplan - Practice 1 Part 2 Exercise 2.1

- Generated at: `2026-03-16T04:43:37`
- Args: `{'min_size': 2, 'max_size': 10, 'step': 2, 'timeout': 60, 'domain': 'dronedomain.pddl', 'generator': 'generate-problem.py', 'results_dir': 'results', 'drones': 1, 'carriers': 1, 'carrier_capacity': 4, 'exercise': 1, 'seed': None, 'allow_basic_plots': False, 'problem_files': None}`

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
| 2 | problems/drone_problem_ex1_d1_r1_l2_p2_c2_g2_a4.pddl | ok | 0.1713 |  |
| 4 | problems/drone_problem_ex1_d1_r1_l4_p4_c4_g4_a4.pddl | ok | 0.1619 |  |
| 6 | problems/drone_problem_ex1_d1_r1_l6_p6_c6_g6_a4.pddl | ok | 0.1794 |  |
| 8 | problems/drone_problem_ex1_d1_r1_l8_p8_c8_g8_a4.pddl | ok | 0.2361 |  |
| 10 | problems/drone_problem_ex1_d1_r1_l10_p10_c10_g10_a4.pddl | ok | 0.1394 |  |

## [RAW_ROWS]

| section | algorithm | search | heuristic | size | status | solved | search_time_s | wall_time_s | plan_length | optimal | problem_file | error_excerpt |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2.1.1 | BFS | bfs |  | 2 | solved | yes | 0.0021 | 2.8863 | 7 | yes | problems/drone_problem_ex1_d1_r1_l2_p2_c2_g2_a4.pddl |  |
| 2.1.1 | IDS | ids |  | 2 | solved | yes | 0.0056 | 2.5916 | 7 | yes | problems/drone_problem_ex1_d1_r1_l2_p2_c2_g2_a4.pddl |  |
| 2.1.1 | A*+hMAX | astar | hmax | 2 | solved | yes | 0.0280 | 3.1249 | 7 | yes | problems/drone_problem_ex1_d1_r1_l2_p2_c2_g2_a4.pddl |  |
| 2.1.1 | GBFS+hMAX | gbf | hmax | 2 | solved | yes | 0.0220 | 2.8880 | 7 | no | problems/drone_problem_ex1_d1_r1_l2_p2_c2_g2_a4.pddl |  |
| 2.1.1 | BFS | bfs |  | 4 | solved | yes | 0.8500 | 4.5368 | 15 | yes | problems/drone_problem_ex1_d1_r1_l4_p4_c4_g4_a4.pddl |  |
| 2.1.1 | IDS | ids |  | 4 | timeout | no |  | 60.0758 |  | yes | problems/drone_problem_ex1_d1_r1_l4_p4_c4_g4_a4.pddl |  |
| 2.1.1 | A*+hMAX | astar | hmax | 4 | solved | yes | 2.2000 | 46.7299 | 15 | yes | problems/drone_problem_ex1_d1_r1_l4_p4_c4_g4_a4.pddl |  |
| 2.1.1 | GBFS+hMAX | gbf | hmax | 4 | solved | yes | 2.9000 | 10.0656 | 18 | no | problems/drone_problem_ex1_d1_r1_l4_p4_c4_g4_a4.pddl |  |
| 2.1.1 | BFS | bfs |  | 6 | timeout | no |  | 60.0704 |  | yes | problems/drone_problem_ex1_d1_r1_l6_p6_c6_g6_a4.pddl |  |
| 2.1.1 | IDS | ids |  | 6 | timeout | no |  | 60.0938 |  | yes | problems/drone_problem_ex1_d1_r1_l6_p6_c6_g6_a4.pddl |  |
| 2.1.1 | A*+hMAX | astar | hmax | 6 | timeout | no |  | 60.0740 |  | yes | problems/drone_problem_ex1_d1_r1_l6_p6_c6_g6_a4.pddl |  |
| 2.1.1 | GBFS+hMAX | gbf | hmax | 6 | timeout | no |  | 60.0897 |  | no | problems/drone_problem_ex1_d1_r1_l6_p6_c6_g6_a4.pddl |  |
| 2.1.1 | BFS | bfs |  | 8 | timeout | no |  | 60.2388 |  | yes | problems/drone_problem_ex1_d1_r1_l8_p8_c8_g8_a4.pddl |  |
| 2.1.1 | IDS | ids |  | 8 | timeout | no |  | 60.0968 |  | yes | problems/drone_problem_ex1_d1_r1_l8_p8_c8_g8_a4.pddl |  |
| 2.1.1 | A*+hMAX | astar | hmax | 8 | timeout | no |  | 60.0619 |  | yes | problems/drone_problem_ex1_d1_r1_l8_p8_c8_g8_a4.pddl |  |
| 2.1.1 | GBFS+hMAX | gbf | hmax | 8 | timeout | no |  | 60.0854 |  | no | problems/drone_problem_ex1_d1_r1_l8_p8_c8_g8_a4.pddl |  |
| 2.1.1 | BFS | bfs |  | 10 | timeout | no |  | 60.0787 |  | yes | problems/drone_problem_ex1_d1_r1_l10_p10_c10_g10_a4.pddl |  |
| 2.1.1 | IDS | ids |  | 10 | timeout | no |  | 60.0818 |  | yes | problems/drone_problem_ex1_d1_r1_l10_p10_c10_g10_a4.pddl |  |
| 2.1.1 | A*+hMAX | astar | hmax | 10 | timeout | no |  | 60.1043 |  | yes | problems/drone_problem_ex1_d1_r1_l10_p10_c10_g10_a4.pddl |  |
| 2.1.1 | GBFS+hMAX | gbf | hmax | 10 | timeout | no |  | 60.0675 |  | no | problems/drone_problem_ex1_d1_r1_l10_p10_c10_g10_a4.pddl |  |
| 2.1.2 | GBFS | gbf | hmax | 4 | solved | yes | 2.7000 | 10.6595 | 18 | no | problems/drone_problem_ex1_d1_r1_l4_p4_c4_g4_a4.pddl |  |
| 2.1.2 | GBFS | gbf | hadd | 4 | solved | yes | 0.0600 | 3.7483 | 15 | no | problems/drone_problem_ex1_d1_r1_l4_p4_c4_g4_a4.pddl |  |
| 2.1.2 | GBFS | gbf | hff | 4 | solved | yes | 0.0540 | 3.6123 | 15 | no | problems/drone_problem_ex1_d1_r1_l4_p4_c4_g4_a4.pddl |  |
| 2.1.2 | GBFS | gbf | landmark | 4 | solved | yes | 0.0056 | 3.5641 | 17 | no | problems/drone_problem_ex1_d1_r1_l4_p4_c4_g4_a4.pddl |  |
| 2.1.2 | EHC | ehs | hmax | 4 | solved | yes | 1.7000 | 48.3078 | 15 | no | problems/drone_problem_ex1_d1_r1_l4_p4_c4_g4_a4.pddl |  |
| 2.1.2 | EHC | ehs | hadd | 4 | solved | yes | 0.1400 | 3.9511 | 15 | no | problems/drone_problem_ex1_d1_r1_l4_p4_c4_g4_a4.pddl |  |
| 2.1.2 | EHC | ehs | hff | 4 | solved | yes | 0.1000 | 3.6007 | 15 | no | problems/drone_problem_ex1_d1_r1_l4_p4_c4_g4_a4.pddl |  |
| 2.1.2 | EHC | ehs | landmark | 4 | solved | yes | 0.0066 | 3.0821 | 18 | no | problems/drone_problem_ex1_d1_r1_l4_p4_c4_g4_a4.pddl |  |
| 2.1.3 | BFS | bfs |  | 4 | solved | yes | 0.9800 | 5.5718 | 15 | yes | problems/drone_problem_ex1_d1_r1_l4_p4_c4_g4_a4.pddl |  |
| 2.1.3 | IDS | ids |  | 4 | timeout | no |  | 60.1030 |  | yes | problems/drone_problem_ex1_d1_r1_l4_p4_c4_g4_a4.pddl |  |
| 2.1.3 | A*+hMAX | astar | hmax | 4 | timeout | no |  | 60.0763 |  | yes | problems/drone_problem_ex1_d1_r1_l4_p4_c4_g4_a4.pddl |  |
| 2.1.3 | A*+lmcut | astar | lmcut | 4 | timeout | no |  | 60.0834 |  | yes | problems/drone_problem_ex1_d1_r1_l4_p4_c4_g4_a4.pddl |  |

## [TABLE_2.1.1_ALL_RUNS]

| section | algorithm | search | heuristic | size | status | solved | search_time_s | wall_time_s | plan_length | optimal | problem_file | error_excerpt |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2.1.1 | BFS | bfs |  | 2 | solved | yes | 0.0021 | 2.8863 | 7 | yes | problems/drone_problem_ex1_d1_r1_l2_p2_c2_g2_a4.pddl |  |
| 2.1.1 | IDS | ids |  | 2 | solved | yes | 0.0056 | 2.5916 | 7 | yes | problems/drone_problem_ex1_d1_r1_l2_p2_c2_g2_a4.pddl |  |
| 2.1.1 | A*+hMAX | astar | hmax | 2 | solved | yes | 0.0280 | 3.1249 | 7 | yes | problems/drone_problem_ex1_d1_r1_l2_p2_c2_g2_a4.pddl |  |
| 2.1.1 | GBFS+hMAX | gbf | hmax | 2 | solved | yes | 0.0220 | 2.8880 | 7 | no | problems/drone_problem_ex1_d1_r1_l2_p2_c2_g2_a4.pddl |  |
| 2.1.1 | BFS | bfs |  | 4 | solved | yes | 0.8500 | 4.5368 | 15 | yes | problems/drone_problem_ex1_d1_r1_l4_p4_c4_g4_a4.pddl |  |
| 2.1.1 | IDS | ids |  | 4 | timeout | no |  | 60.0758 |  | yes | problems/drone_problem_ex1_d1_r1_l4_p4_c4_g4_a4.pddl |  |
| 2.1.1 | A*+hMAX | astar | hmax | 4 | solved | yes | 2.2000 | 46.7299 | 15 | yes | problems/drone_problem_ex1_d1_r1_l4_p4_c4_g4_a4.pddl |  |
| 2.1.1 | GBFS+hMAX | gbf | hmax | 4 | solved | yes | 2.9000 | 10.0656 | 18 | no | problems/drone_problem_ex1_d1_r1_l4_p4_c4_g4_a4.pddl |  |
| 2.1.1 | BFS | bfs |  | 6 | timeout | no |  | 60.0704 |  | yes | problems/drone_problem_ex1_d1_r1_l6_p6_c6_g6_a4.pddl |  |
| 2.1.1 | IDS | ids |  | 6 | timeout | no |  | 60.0938 |  | yes | problems/drone_problem_ex1_d1_r1_l6_p6_c6_g6_a4.pddl |  |
| 2.1.1 | A*+hMAX | astar | hmax | 6 | timeout | no |  | 60.0740 |  | yes | problems/drone_problem_ex1_d1_r1_l6_p6_c6_g6_a4.pddl |  |
| 2.1.1 | GBFS+hMAX | gbf | hmax | 6 | timeout | no |  | 60.0897 |  | no | problems/drone_problem_ex1_d1_r1_l6_p6_c6_g6_a4.pddl |  |
| 2.1.1 | BFS | bfs |  | 8 | timeout | no |  | 60.2388 |  | yes | problems/drone_problem_ex1_d1_r1_l8_p8_c8_g8_a4.pddl |  |
| 2.1.1 | IDS | ids |  | 8 | timeout | no |  | 60.0968 |  | yes | problems/drone_problem_ex1_d1_r1_l8_p8_c8_g8_a4.pddl |  |
| 2.1.1 | A*+hMAX | astar | hmax | 8 | timeout | no |  | 60.0619 |  | yes | problems/drone_problem_ex1_d1_r1_l8_p8_c8_g8_a4.pddl |  |
| 2.1.1 | GBFS+hMAX | gbf | hmax | 8 | timeout | no |  | 60.0854 |  | no | problems/drone_problem_ex1_d1_r1_l8_p8_c8_g8_a4.pddl |  |
| 2.1.1 | BFS | bfs |  | 10 | timeout | no |  | 60.0787 |  | yes | problems/drone_problem_ex1_d1_r1_l10_p10_c10_g10_a4.pddl |  |
| 2.1.1 | IDS | ids |  | 10 | timeout | no |  | 60.0818 |  | yes | problems/drone_problem_ex1_d1_r1_l10_p10_c10_g10_a4.pddl |  |
| 2.1.1 | A*+hMAX | astar | hmax | 10 | timeout | no |  | 60.1043 |  | yes | problems/drone_problem_ex1_d1_r1_l10_p10_c10_g10_a4.pddl |  |
| 2.1.1 | GBFS+hMAX | gbf | hmax | 10 | timeout | no |  | 60.0675 |  | no | problems/drone_problem_ex1_d1_r1_l10_p10_c10_g10_a4.pddl |  |

## [TABLE_2.1.2_ALL_RUNS]

| section | algorithm | search | heuristic | size | status | solved | search_time_s | wall_time_s | plan_length | optimal | problem_file | error_excerpt |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2.1.2 | GBFS | gbf | hmax | 4 | solved | yes | 2.7000 | 10.6595 | 18 | no | problems/drone_problem_ex1_d1_r1_l4_p4_c4_g4_a4.pddl |  |
| 2.1.2 | GBFS | gbf | hadd | 4 | solved | yes | 0.0600 | 3.7483 | 15 | no | problems/drone_problem_ex1_d1_r1_l4_p4_c4_g4_a4.pddl |  |
| 2.1.2 | GBFS | gbf | hff | 4 | solved | yes | 0.0540 | 3.6123 | 15 | no | problems/drone_problem_ex1_d1_r1_l4_p4_c4_g4_a4.pddl |  |
| 2.1.2 | GBFS | gbf | landmark | 4 | solved | yes | 0.0056 | 3.5641 | 17 | no | problems/drone_problem_ex1_d1_r1_l4_p4_c4_g4_a4.pddl |  |
| 2.1.2 | EHC | ehs | hmax | 4 | solved | yes | 1.7000 | 48.3078 | 15 | no | problems/drone_problem_ex1_d1_r1_l4_p4_c4_g4_a4.pddl |  |
| 2.1.2 | EHC | ehs | hadd | 4 | solved | yes | 0.1400 | 3.9511 | 15 | no | problems/drone_problem_ex1_d1_r1_l4_p4_c4_g4_a4.pddl |  |
| 2.1.2 | EHC | ehs | hff | 4 | solved | yes | 0.1000 | 3.6007 | 15 | no | problems/drone_problem_ex1_d1_r1_l4_p4_c4_g4_a4.pddl |  |
| 2.1.2 | EHC | ehs | landmark | 4 | solved | yes | 0.0066 | 3.0821 | 18 | no | problems/drone_problem_ex1_d1_r1_l4_p4_c4_g4_a4.pddl |  |

## [TABLE_2.1.3_ALL_RUNS]

| section | algorithm | search | heuristic | size | status | solved | search_time_s | wall_time_s | plan_length | optimal | problem_file | error_excerpt |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2.1.3 | BFS | bfs |  | 4 | solved | yes | 0.9800 | 5.5718 | 15 | yes | problems/drone_problem_ex1_d1_r1_l4_p4_c4_g4_a4.pddl |  |
| 2.1.3 | IDS | ids |  | 4 | timeout | no |  | 60.1030 |  | yes | problems/drone_problem_ex1_d1_r1_l4_p4_c4_g4_a4.pddl |  |
| 2.1.3 | A*+hMAX | astar | hmax | 4 | timeout | no |  | 60.0763 |  | yes | problems/drone_problem_ex1_d1_r1_l4_p4_c4_g4_a4.pddl |  |
| 2.1.3 | A*+lmcut | astar | lmcut | 4 | timeout | no |  | 60.0834 |  | yes | problems/drone_problem_ex1_d1_r1_l4_p4_c4_g4_a4.pddl |  |

## [SUMMARY_2.1.1]

| algorithm | max_solved_size | time_s | plan_length | optimal |
| --- | --- | --- | --- | --- |
| BFS | 4 | 0.8500 | 15 | yes |
| IDS | 2 | 0.0056 | 7 | yes |
| A*+hMAX | 4 | 2.2000 | 15 | yes |
| GBFS+hMAX | 4 | 2.9000 | 18 | no |

## [SUMMARY_2.1.2]

| combo | status | time_s | plan_length | size |
| --- | --- | --- | --- | --- |
| GBFS/hmax | solved | 2.7000 | 18 | 4 |
| GBFS/hadd | solved | 0.0600 | 15 | 4 |
| GBFS/hff | solved | 0.0540 | 15 | 4 |
| GBFS/landmark | solved | 0.0056 | 17 | 4 |
| EHC/hmax | solved | 1.7000 | 15 | 4 |
| EHC/hadd | solved | 0.1400 | 15 | 4 |
| EHC/hff | solved | 0.1000 | 15 | 4 |
| EHC/landmark | solved | 0.0066 | 18 | 4 |

## [SUMMARY_2.1.3]

| combo | status | time_s | plan_length | size | optimal |
| --- | --- | --- | --- | --- | --- |
| BFS/- | solved | 0.9800 | 15 | 4 | yes |
| IDS/- | timeout |  |  | 4 | yes |
| A*+hMAX/hmax | timeout |  |  | 4 | yes |
| A*+lmcut/lmcut | timeout |  |  | 4 | yes |

## [BEST_OPTIMAL_2.1.3]

- `BFS/-`: `0.9800s`, plan_length=`15`
