# Benchmark pyperplan - Practice 1 Part 1 Exercise 1.3

- Generated at: `2026-03-16T02:41:09`
- Args: `{'min_size': 2, 'max_size': 10, 'step': 1, 'timeout': 80, 'domain': 'dronedomain.pddl', 'generator': 'generate-problem.py', 'results_dir': 'results', 'allow_basic_plots': False, 'problem_files': None}`

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
| 2 | problems/drone_problem_d1_r0_l2_p2_c2_g2_ct2.pddl | ok | 0.1594 |  |
| 3 | problems/drone_problem_d1_r0_l3_p3_c3_g3_ct2.pddl | ok | 0.1300 |  |
| 4 | problems/drone_problem_d1_r0_l4_p4_c4_g4_ct2.pddl | ok | 0.1287 |  |
| 5 | problems/drone_problem_d1_r0_l5_p5_c5_g5_ct2.pddl | ok | 0.1793 |  |
| 6 | problems/drone_problem_d1_r0_l6_p6_c6_g6_ct2.pddl | ok | 0.1839 |  |
| 7 | problems/drone_problem_d1_r0_l7_p7_c7_g7_ct2.pddl | ok | 0.1544 |  |
| 8 | problems/drone_problem_d1_r0_l8_p8_c8_g8_ct2.pddl | ok | 0.2655 |  |
| 9 | problems/drone_problem_d1_r0_l9_p9_c9_g9_ct2.pddl | ok | 0.1325 |  |
| 10 | problems/drone_problem_d1_r0_l10_p10_c10_g10_ct2.pddl | ok | 0.1724 |  |

## [RAW_ROWS]

| section | algorithm | search | heuristic | size | status | solved | search_time_s | wall_time_s | plan_length | optimal | problem_file | error_excerpt |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1.3.1 | BFS | bfs |  | 2 | solved | yes | 0.0007 | 2.0212 | 6 | yes | problems/drone_problem_d1_r0_l2_p2_c2_g2_ct2.pddl |  |
| 1.3.1 | IDS | ids |  | 2 | solved | yes | 0.0014 | 2.1636 | 6 | yes | problems/drone_problem_d1_r0_l2_p2_c2_g2_ct2.pddl |  |
| 1.3.1 | A*+hMAX | astar | hmax | 2 | solved | yes | 0.0038 | 2.3835 | 6 | yes | problems/drone_problem_d1_r0_l2_p2_c2_g2_ct2.pddl |  |
| 1.3.1 | GBFS+hMAX | gbf | hmax | 2 | solved | yes | 0.0014 | 1.9310 | 6 | no | problems/drone_problem_d1_r0_l2_p2_c2_g2_ct2.pddl |  |
| 1.3.1 | BFS | bfs |  | 3 | solved | yes | 0.0087 | 2.0516 | 10 | yes | problems/drone_problem_d1_r0_l3_p3_c3_g3_ct2.pddl |  |
| 1.3.1 | IDS | ids |  | 3 | solved | yes | 0.5500 | 3.0325 | 10 | yes | problems/drone_problem_d1_r0_l3_p3_c3_g3_ct2.pddl |  |
| 1.3.1 | A*+hMAX | astar | hmax | 3 | solved | yes | 0.1300 | 2.6435 | 10 | yes | problems/drone_problem_d1_r0_l3_p3_c3_g3_ct2.pddl |  |
| 1.3.1 | GBFS+hMAX | gbf | hmax | 3 | solved | yes | 0.0140 | 2.1928 | 10 | no | problems/drone_problem_d1_r0_l3_p3_c3_g3_ct2.pddl |  |
| 1.3.1 | BFS | bfs |  | 4 | solved | yes | 0.0820 | 2.1135 | 13 | yes | problems/drone_problem_d1_r0_l4_p4_c4_g4_ct2.pddl |  |
| 1.3.1 | IDS | ids |  | 4 | timeout | no |  | 80.0986 |  | yes | problems/drone_problem_d1_r0_l4_p4_c4_g4_ct2.pddl |  |
| 1.3.1 | A*+hMAX | astar | hmax | 4 | solved | yes | 1.1000 | 3.7449 | 13 | yes | problems/drone_problem_d1_r0_l4_p4_c4_g4_ct2.pddl |  |
| 1.3.1 | GBFS+hMAX | gbf | hmax | 4 | solved | yes | 0.1600 | 2.4445 | 14 | no | problems/drone_problem_d1_r0_l4_p4_c4_g4_ct2.pddl |  |
| 1.3.1 | BFS | bfs |  | 5 | solved | yes | 0.7200 | 3.3724 | 16 | yes | problems/drone_problem_d1_r0_l5_p5_c5_g5_ct2.pddl |  |
| 1.3.1 | IDS | ids |  | 5 | timeout | no |  | 80.0970 |  | yes | problems/drone_problem_d1_r0_l5_p5_c5_g5_ct2.pddl |  |
| 1.3.1 | A*+hMAX | astar | hmax | 5 | solved | yes | 1.3000 | 22.7399 | 16 | yes | problems/drone_problem_d1_r0_l5_p5_c5_g5_ct2.pddl |  |
| 1.3.1 | GBFS+hMAX | gbf | hmax | 5 | solved | yes | 0.3100 | 2.5139 | 19 | no | problems/drone_problem_d1_r0_l5_p5_c5_g5_ct2.pddl |  |
| 1.3.1 | BFS | bfs |  | 6 | solved | yes | 4.9000 | 9.6629 | 19 | yes | problems/drone_problem_d1_r0_l6_p6_c6_g6_ct2.pddl |  |
| 1.3.1 | IDS | ids |  | 6 | timeout | no |  | 80.0847 |  | yes | problems/drone_problem_d1_r0_l6_p6_c6_g6_ct2.pddl |  |
| 1.3.1 | A*+hMAX | astar | hmax | 6 | timeout | no |  | 80.0976 |  | yes | problems/drone_problem_d1_r0_l6_p6_c6_g6_ct2.pddl |  |
| 1.3.1 | GBFS+hMAX | gbf | hmax | 6 | solved | yes | 2.4000 | 5.7029 | 22 | no | problems/drone_problem_d1_r0_l6_p6_c6_g6_ct2.pddl |  |
| 1.3.1 | BFS | bfs |  | 7 | solved | yes | 3.9000 | 66.7620 | 23 | yes | problems/drone_problem_d1_r0_l7_p7_c7_g7_ct2.pddl |  |
| 1.3.1 | IDS | ids |  | 7 | timeout | no |  | 80.0831 |  | yes | problems/drone_problem_d1_r0_l7_p7_c7_g7_ct2.pddl |  |
| 1.3.1 | A*+hMAX | astar | hmax | 7 | timeout | no |  | 80.1051 |  | yes | problems/drone_problem_d1_r0_l7_p7_c7_g7_ct2.pddl |  |
| 1.3.1 | GBFS+hMAX | gbf | hmax | 7 | solved | yes | 2.9000 | 51.6372 | 26 | no | problems/drone_problem_d1_r0_l7_p7_c7_g7_ct2.pddl |  |
| 1.3.1 | BFS | bfs |  | 8 | timeout | no |  | 80.1090 |  | yes | problems/drone_problem_d1_r0_l8_p8_c8_g8_ct2.pddl |  |
| 1.3.1 | IDS | ids |  | 8 | timeout | no |  | 80.0844 |  | yes | problems/drone_problem_d1_r0_l8_p8_c8_g8_ct2.pddl |  |
| 1.3.1 | A*+hMAX | astar | hmax | 8 | timeout | no |  | 80.0902 |  | yes | problems/drone_problem_d1_r0_l8_p8_c8_g8_ct2.pddl |  |
| 1.3.1 | GBFS+hMAX | gbf | hmax | 8 | timeout | no |  | 80.0974 |  | no | problems/drone_problem_d1_r0_l8_p8_c8_g8_ct2.pddl |  |
| 1.3.1 | BFS | bfs |  | 9 | timeout | no |  | 80.0992 |  | yes | problems/drone_problem_d1_r0_l9_p9_c9_g9_ct2.pddl |  |
| 1.3.1 | IDS | ids |  | 9 | timeout | no |  | 80.1272 |  | yes | problems/drone_problem_d1_r0_l9_p9_c9_g9_ct2.pddl |  |
| 1.3.1 | A*+hMAX | astar | hmax | 9 | timeout | no |  | 80.0927 |  | yes | problems/drone_problem_d1_r0_l9_p9_c9_g9_ct2.pddl |  |
| 1.3.1 | GBFS+hMAX | gbf | hmax | 9 | timeout | no |  | 80.0940 |  | no | problems/drone_problem_d1_r0_l9_p9_c9_g9_ct2.pddl |  |
| 1.3.1 | BFS | bfs |  | 10 | timeout | no |  | 80.1076 |  | yes | problems/drone_problem_d1_r0_l10_p10_c10_g10_ct2.pddl |  |
| 1.3.1 | IDS | ids |  | 10 | timeout | no |  | 80.1053 |  | yes | problems/drone_problem_d1_r0_l10_p10_c10_g10_ct2.pddl |  |
| 1.3.1 | A*+hMAX | astar | hmax | 10 | timeout | no |  | 80.0949 |  | yes | problems/drone_problem_d1_r0_l10_p10_c10_g10_ct2.pddl |  |
| 1.3.1 | GBFS+hMAX | gbf | hmax | 10 | timeout | no |  | 80.0942 |  | no | problems/drone_problem_d1_r0_l10_p10_c10_g10_ct2.pddl |  |
| 1.3.2 | GBFS | gbf | hmax | 7 | solved | yes | 2.9000 | 64.0971 | 26 | no | problems/drone_problem_d1_r0_l7_p7_c7_g7_ct2.pddl |  |
| 1.3.2 | GBFS | gbf | hadd | 7 | solved | yes | 0.1300 | 3.6991 | 27 | no | problems/drone_problem_d1_r0_l7_p7_c7_g7_ct2.pddl |  |
| 1.3.2 | GBFS | gbf | hff | 7 | solved | yes | 0.2100 | 3.2099 | 23 | no | problems/drone_problem_d1_r0_l7_p7_c7_g7_ct2.pddl |  |
| 1.3.2 | GBFS | gbf | landmark | 7 | solved | yes | 0.0220 | 2.8640 | 28 | no | problems/drone_problem_d1_r0_l7_p7_c7_g7_ct2.pddl |  |
| 1.3.2 | EHC | ehs | hmax | 7 | timeout | no |  | 80.0943 |  | no | problems/drone_problem_d1_r0_l7_p7_c7_g7_ct2.pddl |  |
| 1.3.2 | EHC | ehs | hadd | 7 | solved | yes | 0.4400 | 4.0822 | 27 | no | problems/drone_problem_d1_r0_l7_p7_c7_g7_ct2.pddl |  |
| 1.3.2 | EHC | ehs | hff | 7 | solved | yes | 0.1600 | 3.6990 | 25 | no | problems/drone_problem_d1_r0_l7_p7_c7_g7_ct2.pddl |  |
| 1.3.2 | EHC | ehs | landmark | 7 | solved | yes | 0.1200 | 2.9761 | 34 | no | problems/drone_problem_d1_r0_l7_p7_c7_g7_ct2.pddl |  |
| 1.3.3 | BFS | bfs |  | 5 | solved | yes | 0.7300 | 4.5104 | 16 | yes | problems/drone_problem_d1_r0_l5_p5_c5_g5_ct2.pddl |  |
| 1.3.3 | IDS | ids |  | 5 | timeout | no |  | 80.1010 |  | yes | problems/drone_problem_d1_r0_l5_p5_c5_g5_ct2.pddl |  |
| 1.3.3 | A*+hMAX | astar | hmax | 5 | solved | yes | 1.4000 | 34.0961 | 16 | yes | problems/drone_problem_d1_r0_l5_p5_c5_g5_ct2.pddl |  |
| 1.3.3 | A*+lmcut | astar | lmcut | 5 | timeout | no |  | 80.1165 |  | yes | problems/drone_problem_d1_r0_l5_p5_c5_g5_ct2.pddl |  |

## [TABLE_1.3.1_ALL_RUNS]

| section | algorithm | search | heuristic | size | status | solved | search_time_s | wall_time_s | plan_length | optimal | problem_file | error_excerpt |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1.3.1 | BFS | bfs |  | 2 | solved | yes | 0.0007 | 2.0212 | 6 | yes | problems/drone_problem_d1_r0_l2_p2_c2_g2_ct2.pddl |  |
| 1.3.1 | IDS | ids |  | 2 | solved | yes | 0.0014 | 2.1636 | 6 | yes | problems/drone_problem_d1_r0_l2_p2_c2_g2_ct2.pddl |  |
| 1.3.1 | A*+hMAX | astar | hmax | 2 | solved | yes | 0.0038 | 2.3835 | 6 | yes | problems/drone_problem_d1_r0_l2_p2_c2_g2_ct2.pddl |  |
| 1.3.1 | GBFS+hMAX | gbf | hmax | 2 | solved | yes | 0.0014 | 1.9310 | 6 | no | problems/drone_problem_d1_r0_l2_p2_c2_g2_ct2.pddl |  |
| 1.3.1 | BFS | bfs |  | 3 | solved | yes | 0.0087 | 2.0516 | 10 | yes | problems/drone_problem_d1_r0_l3_p3_c3_g3_ct2.pddl |  |
| 1.3.1 | IDS | ids |  | 3 | solved | yes | 0.5500 | 3.0325 | 10 | yes | problems/drone_problem_d1_r0_l3_p3_c3_g3_ct2.pddl |  |
| 1.3.1 | A*+hMAX | astar | hmax | 3 | solved | yes | 0.1300 | 2.6435 | 10 | yes | problems/drone_problem_d1_r0_l3_p3_c3_g3_ct2.pddl |  |
| 1.3.1 | GBFS+hMAX | gbf | hmax | 3 | solved | yes | 0.0140 | 2.1928 | 10 | no | problems/drone_problem_d1_r0_l3_p3_c3_g3_ct2.pddl |  |
| 1.3.1 | BFS | bfs |  | 4 | solved | yes | 0.0820 | 2.1135 | 13 | yes | problems/drone_problem_d1_r0_l4_p4_c4_g4_ct2.pddl |  |
| 1.3.1 | IDS | ids |  | 4 | timeout | no |  | 80.0986 |  | yes | problems/drone_problem_d1_r0_l4_p4_c4_g4_ct2.pddl |  |
| 1.3.1 | A*+hMAX | astar | hmax | 4 | solved | yes | 1.1000 | 3.7449 | 13 | yes | problems/drone_problem_d1_r0_l4_p4_c4_g4_ct2.pddl |  |
| 1.3.1 | GBFS+hMAX | gbf | hmax | 4 | solved | yes | 0.1600 | 2.4445 | 14 | no | problems/drone_problem_d1_r0_l4_p4_c4_g4_ct2.pddl |  |
| 1.3.1 | BFS | bfs |  | 5 | solved | yes | 0.7200 | 3.3724 | 16 | yes | problems/drone_problem_d1_r0_l5_p5_c5_g5_ct2.pddl |  |
| 1.3.1 | IDS | ids |  | 5 | timeout | no |  | 80.0970 |  | yes | problems/drone_problem_d1_r0_l5_p5_c5_g5_ct2.pddl |  |
| 1.3.1 | A*+hMAX | astar | hmax | 5 | solved | yes | 1.3000 | 22.7399 | 16 | yes | problems/drone_problem_d1_r0_l5_p5_c5_g5_ct2.pddl |  |
| 1.3.1 | GBFS+hMAX | gbf | hmax | 5 | solved | yes | 0.3100 | 2.5139 | 19 | no | problems/drone_problem_d1_r0_l5_p5_c5_g5_ct2.pddl |  |
| 1.3.1 | BFS | bfs |  | 6 | solved | yes | 4.9000 | 9.6629 | 19 | yes | problems/drone_problem_d1_r0_l6_p6_c6_g6_ct2.pddl |  |
| 1.3.1 | IDS | ids |  | 6 | timeout | no |  | 80.0847 |  | yes | problems/drone_problem_d1_r0_l6_p6_c6_g6_ct2.pddl |  |
| 1.3.1 | A*+hMAX | astar | hmax | 6 | timeout | no |  | 80.0976 |  | yes | problems/drone_problem_d1_r0_l6_p6_c6_g6_ct2.pddl |  |
| 1.3.1 | GBFS+hMAX | gbf | hmax | 6 | solved | yes | 2.4000 | 5.7029 | 22 | no | problems/drone_problem_d1_r0_l6_p6_c6_g6_ct2.pddl |  |
| 1.3.1 | BFS | bfs |  | 7 | solved | yes | 3.9000 | 66.7620 | 23 | yes | problems/drone_problem_d1_r0_l7_p7_c7_g7_ct2.pddl |  |
| 1.3.1 | IDS | ids |  | 7 | timeout | no |  | 80.0831 |  | yes | problems/drone_problem_d1_r0_l7_p7_c7_g7_ct2.pddl |  |
| 1.3.1 | A*+hMAX | astar | hmax | 7 | timeout | no |  | 80.1051 |  | yes | problems/drone_problem_d1_r0_l7_p7_c7_g7_ct2.pddl |  |
| 1.3.1 | GBFS+hMAX | gbf | hmax | 7 | solved | yes | 2.9000 | 51.6372 | 26 | no | problems/drone_problem_d1_r0_l7_p7_c7_g7_ct2.pddl |  |
| 1.3.1 | BFS | bfs |  | 8 | timeout | no |  | 80.1090 |  | yes | problems/drone_problem_d1_r0_l8_p8_c8_g8_ct2.pddl |  |
| 1.3.1 | IDS | ids |  | 8 | timeout | no |  | 80.0844 |  | yes | problems/drone_problem_d1_r0_l8_p8_c8_g8_ct2.pddl |  |
| 1.3.1 | A*+hMAX | astar | hmax | 8 | timeout | no |  | 80.0902 |  | yes | problems/drone_problem_d1_r0_l8_p8_c8_g8_ct2.pddl |  |
| 1.3.1 | GBFS+hMAX | gbf | hmax | 8 | timeout | no |  | 80.0974 |  | no | problems/drone_problem_d1_r0_l8_p8_c8_g8_ct2.pddl |  |
| 1.3.1 | BFS | bfs |  | 9 | timeout | no |  | 80.0992 |  | yes | problems/drone_problem_d1_r0_l9_p9_c9_g9_ct2.pddl |  |
| 1.3.1 | IDS | ids |  | 9 | timeout | no |  | 80.1272 |  | yes | problems/drone_problem_d1_r0_l9_p9_c9_g9_ct2.pddl |  |
| 1.3.1 | A*+hMAX | astar | hmax | 9 | timeout | no |  | 80.0927 |  | yes | problems/drone_problem_d1_r0_l9_p9_c9_g9_ct2.pddl |  |
| 1.3.1 | GBFS+hMAX | gbf | hmax | 9 | timeout | no |  | 80.0940 |  | no | problems/drone_problem_d1_r0_l9_p9_c9_g9_ct2.pddl |  |
| 1.3.1 | BFS | bfs |  | 10 | timeout | no |  | 80.1076 |  | yes | problems/drone_problem_d1_r0_l10_p10_c10_g10_ct2.pddl |  |
| 1.3.1 | IDS | ids |  | 10 | timeout | no |  | 80.1053 |  | yes | problems/drone_problem_d1_r0_l10_p10_c10_g10_ct2.pddl |  |
| 1.3.1 | A*+hMAX | astar | hmax | 10 | timeout | no |  | 80.0949 |  | yes | problems/drone_problem_d1_r0_l10_p10_c10_g10_ct2.pddl |  |
| 1.3.1 | GBFS+hMAX | gbf | hmax | 10 | timeout | no |  | 80.0942 |  | no | problems/drone_problem_d1_r0_l10_p10_c10_g10_ct2.pddl |  |

## [TABLE_1.3.2_ALL_RUNS]

| section | algorithm | search | heuristic | size | status | solved | search_time_s | wall_time_s | plan_length | optimal | problem_file | error_excerpt |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1.3.2 | GBFS | gbf | hmax | 7 | solved | yes | 2.9000 | 64.0971 | 26 | no | problems/drone_problem_d1_r0_l7_p7_c7_g7_ct2.pddl |  |
| 1.3.2 | GBFS | gbf | hadd | 7 | solved | yes | 0.1300 | 3.6991 | 27 | no | problems/drone_problem_d1_r0_l7_p7_c7_g7_ct2.pddl |  |
| 1.3.2 | GBFS | gbf | hff | 7 | solved | yes | 0.2100 | 3.2099 | 23 | no | problems/drone_problem_d1_r0_l7_p7_c7_g7_ct2.pddl |  |
| 1.3.2 | GBFS | gbf | landmark | 7 | solved | yes | 0.0220 | 2.8640 | 28 | no | problems/drone_problem_d1_r0_l7_p7_c7_g7_ct2.pddl |  |
| 1.3.2 | EHC | ehs | hmax | 7 | timeout | no |  | 80.0943 |  | no | problems/drone_problem_d1_r0_l7_p7_c7_g7_ct2.pddl |  |
| 1.3.2 | EHC | ehs | hadd | 7 | solved | yes | 0.4400 | 4.0822 | 27 | no | problems/drone_problem_d1_r0_l7_p7_c7_g7_ct2.pddl |  |
| 1.3.2 | EHC | ehs | hff | 7 | solved | yes | 0.1600 | 3.6990 | 25 | no | problems/drone_problem_d1_r0_l7_p7_c7_g7_ct2.pddl |  |
| 1.3.2 | EHC | ehs | landmark | 7 | solved | yes | 0.1200 | 2.9761 | 34 | no | problems/drone_problem_d1_r0_l7_p7_c7_g7_ct2.pddl |  |

## [TABLE_1.3.3_ALL_RUNS]

| section | algorithm | search | heuristic | size | status | solved | search_time_s | wall_time_s | plan_length | optimal | problem_file | error_excerpt |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1.3.3 | BFS | bfs |  | 5 | solved | yes | 0.7300 | 4.5104 | 16 | yes | problems/drone_problem_d1_r0_l5_p5_c5_g5_ct2.pddl |  |
| 1.3.3 | IDS | ids |  | 5 | timeout | no |  | 80.1010 |  | yes | problems/drone_problem_d1_r0_l5_p5_c5_g5_ct2.pddl |  |
| 1.3.3 | A*+hMAX | astar | hmax | 5 | solved | yes | 1.4000 | 34.0961 | 16 | yes | problems/drone_problem_d1_r0_l5_p5_c5_g5_ct2.pddl |  |
| 1.3.3 | A*+lmcut | astar | lmcut | 5 | timeout | no |  | 80.1165 |  | yes | problems/drone_problem_d1_r0_l5_p5_c5_g5_ct2.pddl |  |

## [SUMMARY_1.3.1]

| algorithm | max_solved_size | time_s | plan_length | optimal |
| --- | --- | --- | --- | --- |
| BFS | 7 | 3.9000 | 23 | yes |
| IDS | 3 | 0.5500 | 10 | yes |
| A*+hMAX | 5 | 1.3000 | 16 | yes |
| GBFS+hMAX | 7 | 2.9000 | 26 | no |

## [SUMMARY_1.3.2]

| combo | status | time_s | plan_length | size |
| --- | --- | --- | --- | --- |
| GBFS/hmax | solved | 2.9000 | 26 | 7 |
| GBFS/hadd | solved | 0.1300 | 27 | 7 |
| GBFS/hff | solved | 0.2100 | 23 | 7 |
| GBFS/landmark | solved | 0.0220 | 28 | 7 |
| EHC/hmax | timeout |  |  | 7 |
| EHC/hadd | solved | 0.4400 | 27 | 7 |
| EHC/hff | solved | 0.1600 | 25 | 7 |
| EHC/landmark | solved | 0.1200 | 34 | 7 |

## [SUMMARY_1.3.3]

| combo | status | time_s | plan_length | size | optimal |
| --- | --- | --- | --- | --- | --- |
| BFS/- | solved | 0.7300 | 16 | 5 | yes |
| IDS/- | timeout |  |  | 5 | yes |
| A*+hMAX/hmax | solved | 1.4000 | 16 | 5 | yes |
| A*+lmcut/lmcut | timeout |  |  | 5 | yes |

## [BEST_OPTIMAL_1.3.3]

- `BFS/-`: `0.7300s`, plan_length=`16`
