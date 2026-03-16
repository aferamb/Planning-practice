# Benchmark cost planners - Practice 1 Part 2 Exercise 2.2

- Generated at: `2026-03-16T12:58:13`
- Args: `{'min_size': 2, 'max_size': 12, 'step': 1, 'sizes': None, 'timeout': 60, 'domain': 'dronedomain2.pddl', 'generator': 'generate-problem.py', 'results_dir': 'results', 'drones': 1, 'carriers': 1, 'carrier_capacity': 4, 'exercise': 2, 'seed': None, 'problem_files': None}`

## [GENERATION]

| size | problem_file | status | wall_time_s | error_excerpt |
| --- | --- | --- | --- | --- |
| 2 | problems/drone_problem_ex2_d1_r1_l2_p2_c2_g2_a4.pddl | ok | 0.0396 |  |
| 3 | problems/drone_problem_ex2_d1_r1_l3_p3_c3_g3_a4.pddl | ok | 0.0388 |  |
| 4 | problems/drone_problem_ex2_d1_r1_l4_p4_c4_g4_a4.pddl | ok | 0.0398 |  |
| 5 | problems/drone_problem_ex2_d1_r1_l5_p5_c5_g5_a4.pddl | ok | 0.0473 |  |
| 6 | problems/drone_problem_ex2_d1_r1_l6_p6_c6_g6_a4.pddl | ok | 0.0401 |  |
| 7 | problems/drone_problem_ex2_d1_r1_l7_p7_c7_g7_a4.pddl | ok | 0.0395 |  |
| 8 | problems/drone_problem_ex2_d1_r1_l8_p8_c8_g8_a4.pddl | ok | 0.0385 |  |
| 9 | problems/drone_problem_ex2_d1_r1_l9_p9_c9_g9_a4.pddl | ok | 0.0387 |  |
| 10 | problems/drone_problem_ex2_d1_r1_l10_p10_c10_g10_a4.pddl | ok | 0.0392 |  |
| 11 | problems/drone_problem_ex2_d1_r1_l11_p11_c11_g11_a4.pddl | ok | 0.0405 |  |
| 12 | problems/drone_problem_ex2_d1_r1_l12_p12_c12_g12_a4.pddl | ok | 0.0429 |  |

## [RAW_ROWS]

| planner | family | status | size | planner_time_s | wall_time_s | plan_cost | plan_length | error_excerpt | problem_file |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| metric-ff | sat | solved | 2 | 0.0000 | 1.0777 | 453.0000 | 7 |  | problems/drone_problem_ex2_d1_r1_l2_p2_c2_g2_a4.pddl |
| metric-ff | sat | solved | 3 | 0.0000 | 1.1123 | 1276.0000 | 11 |  | problems/drone_problem_ex2_d1_r1_l3_p3_c3_g3_a4.pddl |
| metric-ff | sat | solved | 4 | 0.0000 | 1.0674 | 1128.0000 | 15 |  | problems/drone_problem_ex2_d1_r1_l4_p4_c4_g4_a4.pddl |
| metric-ff | sat | solved | 5 | 0.0000 | 1.0827 | 1115.0000 | 19 |  | problems/drone_problem_ex2_d1_r1_l5_p5_c5_g5_a4.pddl |
| metric-ff | sat | solved | 6 | 0.0000 | 1.0667 | 1947.0000 | 23 |  | problems/drone_problem_ex2_d1_r1_l6_p6_c6_g6_a4.pddl |
| metric-ff | sat | solved | 7 | 0.0000 | 1.0835 | 1949.0000 | 28 |  | problems/drone_problem_ex2_d1_r1_l7_p7_c7_g7_a4.pddl |
| metric-ff | sat | solved | 8 | 0.0100 | 1.0744 | 2933.0000 | 32 |  | problems/drone_problem_ex2_d1_r1_l8_p8_c8_g8_a4.pddl |
| metric-ff | sat | solved | 9 | 0.0100 | 1.0621 | 2978.0000 | 35 |  | problems/drone_problem_ex2_d1_r1_l9_p9_c9_g9_a4.pddl |
| metric-ff | sat | solved | 10 | 0.0200 | 1.1699 | 3416.0000 | 39 |  | problems/drone_problem_ex2_d1_r1_l10_p10_c10_g10_a4.pddl |
| metric-ff | sat | error | 11 |  | 1.0640 |  |  | ff: parsing domain file \| domain 'UBERMEDICS-CARRIERS-COSTS' defined \| ... done. \| ff: parsing problem file \| problem... (E001) | problems/drone_problem_ex2_d1_r1_l11_p11_c11_g11_a4.pddl |
| metric-ff | sat | error | 12 |  | 1.0847 |  |  | ff: parsing domain file \| domain 'UBERMEDICS-CARRIERS-COSTS' defined \| ... done. \| ff: parsing problem file \| problem... (E002) | problems/drone_problem_ex2_d1_r1_l12_p12_c12_g12_a4.pddl |
| downward:lama-first | sat | solved | 2 | 0.0042 | 1.5877 | 453.0000 | 7 |  | problems/drone_problem_ex2_d1_r1_l2_p2_c2_g2_a4.pddl |
| downward:lama-first | sat | solved | 3 | 0.0037 | 1.4652 | 1278.0000 | 13 |  | problems/drone_problem_ex2_d1_r1_l3_p3_c3_g3_a4.pddl |
| downward:lama-first | sat | solved | 4 | 0.0050 | 1.4987 | 1128.0000 | 15 |  | problems/drone_problem_ex2_d1_r1_l4_p4_c4_g4_a4.pddl |
| downward:lama-first | sat | solved | 5 | 0.0051 | 1.4596 | 1119.0000 | 20 |  | problems/drone_problem_ex2_d1_r1_l5_p5_c5_g5_a4.pddl |
| downward:lama-first | sat | solved | 6 | 0.0092 | 1.4831 | 2027.0000 | 24 |  | problems/drone_problem_ex2_d1_r1_l6_p6_c6_g6_a4.pddl |
| downward:lama-first | sat | solved | 7 | 0.0058 | 1.5110 | 2087.0000 | 30 |  | problems/drone_problem_ex2_d1_r1_l7_p7_c7_g7_a4.pddl |
| downward:lama-first | sat | solved | 8 | 0.0128 | 1.4941 | 3465.0000 | 35 |  | problems/drone_problem_ex2_d1_r1_l8_p8_c8_g8_a4.pddl |
| downward:lama-first | sat | solved | 9 | 0.0113 | 1.4890 | 3571.0000 | 39 |  | problems/drone_problem_ex2_d1_r1_l9_p9_c9_g9_a4.pddl |
| downward:lama-first | sat | solved | 10 | 0.0193 | 1.5479 | 3926.0000 | 43 |  | problems/drone_problem_ex2_d1_r1_l10_p10_c10_g10_a4.pddl |
| downward:lama-first | sat | solved | 11 | 0.0172 | 1.5240 | 3043.0000 | 47 |  | problems/drone_problem_ex2_d1_r1_l11_p11_c11_g11_a4.pddl |
| downward:lama-first | sat | solved | 12 | 0.0180 | 1.5500 | 3963.0000 | 47 |  | problems/drone_problem_ex2_d1_r1_l12_p12_c12_g12_a4.pddl |
| downward:seq-sat-fdss-2 | sat | solved | 2 | 0.0061 | 1.4509 | 296.0000 | 7 |  | problems/drone_problem_ex2_d1_r1_l2_p2_c2_g2_a4.pddl |
| downward:seq-sat-fdss-2 | sat | solved | 3 | 0.0020 | 1.4113 | 266.0000 | 11 |  | problems/drone_problem_ex2_d1_r1_l3_p3_c3_g3_a4.pddl |
| downward:seq-sat-fdss-2 | sat | solved | 4 | 0.0991 | 1.5052 | 362.0000 | 15 |  | problems/drone_problem_ex2_d1_r1_l4_p4_c4_g4_a4.pddl |
| downward:seq-sat-fdss-2 | sat | solved | 5 | 1.2338 | 2.6192 | 413.0000 | 19 |  | problems/drone_problem_ex2_d1_r1_l5_p5_c5_g5_a4.pddl |
| downward:seq-sat-fdss-2 | sat | solved | 6 | 24.8261 | 25.3063 | 573.0000 | 23 |  | problems/drone_problem_ex2_d1_r1_l6_p6_c6_g6_a4.pddl |
| downward:seq-sat-fdss-2 | sat | solved | 7 | 0.0085 | 59.4789 | 447.0000 | 27 |  | problems/drone_problem_ex2_d1_r1_l7_p7_c7_g7_a4.pddl |
| downward:seq-sat-fdss-2 | sat | solved | 8 | 0.0106 | 59.5425 | 979.0000 | 31 |  | problems/drone_problem_ex2_d1_r1_l8_p8_c8_g8_a4.pddl |
| downward:seq-sat-fdss-2 | sat | solved | 9 | 0.0123 | 59.5427 | 1531.0000 | 35 |  | problems/drone_problem_ex2_d1_r1_l9_p9_c9_g9_a4.pddl |
| downward:seq-sat-fdss-2 | sat | solved | 10 | 0.0251 | 59.6431 | 1765.0000 | 39 |  | problems/drone_problem_ex2_d1_r1_l10_p10_c10_g10_a4.pddl |
| downward:seq-sat-fdss-2 | sat | solved | 11 | 0.0379 | 59.5861 | 1263.0000 | 43 |  | problems/drone_problem_ex2_d1_r1_l11_p11_c11_g11_a4.pddl |
| downward:seq-sat-fdss-2 | sat | solved | 12 | 0.0629 | 59.7602 | 1969.0000 | 47 |  | problems/drone_problem_ex2_d1_r1_l12_p12_c12_g12_a4.pddl |
| downward:seq-sat-fd-autotune-2 | sat | solved | 2 | 0.0185 | 1.4687 | 296.0000 | 9 |  | problems/drone_problem_ex2_d1_r1_l2_p2_c2_g2_a4.pddl |
| downward:seq-sat-fd-autotune-2 | sat | solved | 3 | 0.0969 | 1.5192 | 266.0000 | 11 |  | problems/drone_problem_ex2_d1_r1_l3_p3_c3_g3_a4.pddl |
| downward:seq-sat-fd-autotune-2 | sat | solved | 4 | 2.5146 | 3.8257 | 464.0000 | 19 |  | problems/drone_problem_ex2_d1_r1_l4_p4_c4_g4_a4.pddl |
| downward:seq-sat-fd-autotune-2 | sat | solved | 5 | 26.3869 | 26.4508 | 539.0000 | 23 |  | problems/drone_problem_ex2_d1_r1_l5_p5_c5_g5_a4.pddl |
| downward:seq-sat-fd-autotune-2 | sat | timeout | 6 | 2.2682 | 60.0062 | 1157.0000 | 27 |  | problems/drone_problem_ex2_d1_r1_l6_p6_c6_g6_a4.pddl |
| downward:seq-sat-fd-autotune-2 | sat | timeout | 7 | 18.2839 | 60.0136 | 917.0000 | 27 |  | problems/drone_problem_ex2_d1_r1_l7_p7_c7_g7_a4.pddl |
| downward:seq-sat-fd-autotune-2 | sat | timeout | 8 | 0.0943 | 60.0527 | 2721.0000 | 34 |  | problems/drone_problem_ex2_d1_r1_l8_p8_c8_g8_a4.pddl |
| downward:seq-sat-fd-autotune-2 | sat | timeout | 9 | 7.0583 | 60.0044 | 2328.0000 | 38 |  | problems/drone_problem_ex2_d1_r1_l9_p9_c9_g9_a4.pddl |
| downward:seq-sat-fd-autotune-2 | sat | timeout | 10 | 1.7855 | 60.0051 | 3274.0000 | 48 |  | problems/drone_problem_ex2_d1_r1_l10_p10_c10_g10_a4.pddl |
| downward:seq-sat-fd-autotune-2 | sat | timeout | 11 | 3.0463 | 60.0083 | 2536.0000 | 45 |  | problems/drone_problem_ex2_d1_r1_l11_p11_c11_g11_a4.pddl |
| downward:seq-sat-fd-autotune-2 | sat | timeout | 12 | 1.6703 | 60.0129 | 3963.0000 | 56 |  | problems/drone_problem_ex2_d1_r1_l12_p12_c12_g12_a4.pddl |
| downward:seq-opt-lmcut | opt | solved | 2 | 0.0027 | 1.2286 | 296.0000 | 10 |  | problems/drone_problem_ex2_d1_r1_l2_p2_c2_g2_a4.pddl |
| downward:seq-opt-lmcut | opt | solved | 3 | 0.0029 | 1.1896 | 266.0000 | 13 |  | problems/drone_problem_ex2_d1_r1_l3_p3_c3_g3_a4.pddl |
| downward:seq-opt-lmcut | opt | solved | 4 | 0.0181 | 1.1642 | 362.0000 | 19 |  | problems/drone_problem_ex2_d1_r1_l4_p4_c4_g4_a4.pddl |
| downward:seq-opt-lmcut | opt | solved | 5 | 0.8907 | 2.0287 | 409.0000 | 24 |  | problems/drone_problem_ex2_d1_r1_l5_p5_c5_g5_a4.pddl |
| downward:seq-opt-lmcut | opt | solved | 6 | 24.3928 | 24.4249 | 573.0000 | 29 |  | problems/drone_problem_ex2_d1_r1_l6_p6_c6_g6_a4.pddl |
| downward:seq-opt-lmcut | opt | timeout | 7 |  | 60.0015 |  |  |  | problems/drone_problem_ex2_d1_r1_l7_p7_c7_g7_a4.pddl |
| downward:seq-opt-lmcut | opt | timeout | 8 |  | 60.0025 |  |  |  | problems/drone_problem_ex2_d1_r1_l8_p8_c8_g8_a4.pddl |
| downward:seq-opt-lmcut | opt | timeout | 9 |  | 60.0072 |  |  |  | problems/drone_problem_ex2_d1_r1_l9_p9_c9_g9_a4.pddl |
| downward:seq-opt-lmcut | opt | timeout | 10 |  | 60.0213 |  |  |  | problems/drone_problem_ex2_d1_r1_l10_p10_c10_g10_a4.pddl |
| downward:seq-opt-lmcut | opt | timeout | 11 |  | 60.0381 |  |  |  | problems/drone_problem_ex2_d1_r1_l11_p11_c11_g11_a4.pddl |
| downward:seq-opt-lmcut | opt | timeout | 12 |  | 60.0194 |  |  |  | problems/drone_problem_ex2_d1_r1_l12_p12_c12_g12_a4.pddl |
| downward:seq-opt-bjolp | opt | solved | 2 | 0.0034 | 1.8145 | 296.0000 | 10 |  | problems/drone_problem_ex2_d1_r1_l2_p2_c2_g2_a4.pddl |
| downward:seq-opt-bjolp | opt | solved | 3 | 0.0033 | 1.7657 | 266.0000 | 13 |  | problems/drone_problem_ex2_d1_r1_l3_p3_c3_g3_a4.pddl |
| downward:seq-opt-bjolp | opt | solved | 4 | 0.0130 | 1.8222 | 362.0000 | 19 |  | problems/drone_problem_ex2_d1_r1_l4_p4_c4_g4_a4.pddl |
| downward:seq-opt-bjolp | opt | solved | 5 | 0.2945 | 1.8454 | 409.0000 | 24 |  | problems/drone_problem_ex2_d1_r1_l5_p5_c5_g5_a4.pddl |
| downward:seq-opt-bjolp | opt | solved | 6 | 4.2013 | 5.6343 | 573.0000 | 29 |  | problems/drone_problem_ex2_d1_r1_l6_p6_c6_g6_a4.pddl |
| downward:seq-opt-bjolp | opt | solved | 7 | 19.6647 | 35.9969 | 447.0000 | 33 |  | problems/drone_problem_ex2_d1_r1_l7_p7_c7_g7_a4.pddl |
| downward:seq-opt-bjolp | opt | timeout | 8 |  | 60.0062 |  |  |  | problems/drone_problem_ex2_d1_r1_l8_p8_c8_g8_a4.pddl |
| downward:seq-opt-bjolp | opt | timeout | 9 |  | 60.0037 |  |  |  | problems/drone_problem_ex2_d1_r1_l9_p9_c9_g9_a4.pddl |
| downward:seq-opt-bjolp | opt | timeout | 10 |  | 60.0036 |  |  |  | problems/drone_problem_ex2_d1_r1_l10_p10_c10_g10_a4.pddl |
| downward:seq-opt-bjolp | opt | timeout | 11 |  | 60.0022 |  |  |  | problems/drone_problem_ex2_d1_r1_l11_p11_c11_g11_a4.pddl |
| downward:seq-opt-bjolp | opt | timeout | 12 |  | 60.0045 |  |  |  | problems/drone_problem_ex2_d1_r1_l12_p12_c12_g12_a4.pddl |
| downward:seq-opt-fdss-2 | opt | solved | 2 | 0.0056 | 1.2037 | 296.0000 | 10 |  | problems/drone_problem_ex2_d1_r1_l2_p2_c2_g2_a4.pddl |
| downward:seq-opt-fdss-2 | opt | solved | 3 | 0.0049 | 1.1962 | 266.0000 | 13 |  | problems/drone_problem_ex2_d1_r1_l3_p3_c3_g3_a4.pddl |
| downward:seq-opt-fdss-2 | opt | solved | 4 | 0.0310 | 1.1719 | 362.0000 | 19 |  | problems/drone_problem_ex2_d1_r1_l4_p4_c4_g4_a4.pddl |
| downward:seq-opt-fdss-2 | opt | solved | 5 | 0.2035 | 1.4118 | 409.0000 | 24 |  | problems/drone_problem_ex2_d1_r1_l5_p5_c5_g5_a4.pddl |
| downward:seq-opt-fdss-2 | opt | solved | 6 | 2.4481 | 3.5587 | 573.0000 | 29 |  | problems/drone_problem_ex2_d1_r1_l6_p6_c6_g6_a4.pddl |
| downward:seq-opt-fdss-2 | opt | solved | 7 | 5.9565 | 17.7855 | 447.0000 | 33 |  | problems/drone_problem_ex2_d1_r1_l7_p7_c7_g7_a4.pddl |
| downward:seq-opt-fdss-2 | opt | error | 8 | 59.1000 | 57.2324 |  |  | INFO     planner time limit: 60s \| INFO     planner memory limit: None \| INFO     Running translator. \| INFO     tran... (E003) | problems/drone_problem_ex2_d1_r1_l8_p8_c8_g8_a4.pddl |
| downward:seq-opt-fdss-2 | opt | error | 9 | 59.4700 | 57.2716 |  |  | INFO     planner time limit: 60s \| INFO     planner memory limit: None \| INFO     Running translator. \| INFO     tran... (E003) | problems/drone_problem_ex2_d1_r1_l9_p9_c9_g9_a4.pddl |
| downward:seq-opt-fdss-2 | opt | error | 10 | 59.4300 | 57.2815 |  |  | INFO     planner time limit: 60s \| INFO     planner memory limit: None \| INFO     Running translator. \| INFO     tran... (E003) | problems/drone_problem_ex2_d1_r1_l10_p10_c10_g10_a4.pddl |
| downward:seq-opt-fdss-2 | opt | error | 11 | 59.3600 | 57.2957 |  |  | INFO     planner time limit: 60s \| INFO     planner memory limit: None \| INFO     Running translator. \| INFO     tran... (E003) | problems/drone_problem_ex2_d1_r1_l11_p11_c11_g11_a4.pddl |
| downward:seq-opt-fdss-2 | opt | error | 12 | 59.1000 | 57.3462 |  |  | INFO     planner time limit: 60s \| INFO     planner memory limit: None \| INFO     Running translator. \| INFO     tran... (E003) | problems/drone_problem_ex2_d1_r1_l12_p12_c12_g12_a4.pddl |

## [TABLE_2.2_SAT_SUMMARY]

| planner | family | max_solved_size | plan_cost_at_max_size | plan_length_at_max_size | wall_time_s_at_max_size | count_solved | count_timeout | count_unsolved | count_unsupported | count_error |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| metric-ff | sat | 10 | 3416.0000 | 39 | 1.1699 | 9 | 0 | 0 | 0 | 2 |
| downward:lama-first | sat | 12 | 3963.0000 | 47 | 1.5500 | 11 | 0 | 0 | 0 | 0 |
| downward:seq-sat-fdss-2 | sat | 12 | 1969.0000 | 47 | 59.7602 | 11 | 0 | 0 | 0 | 0 |
| downward:seq-sat-fd-autotune-2 | sat | 5 | 539.0000 | 23 | 26.4508 | 4 | 7 | 0 | 0 | 0 |

## [TABLE_2.2_OPT_SUMMARY]

| planner | family | max_solved_size | plan_cost_at_max_size | plan_length_at_max_size | wall_time_s_at_max_size | count_solved | count_timeout | count_unsolved | count_unsupported | count_error |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| downward:seq-opt-lmcut | opt | 6 | 573.0000 | 29 | 24.4249 | 5 | 6 | 0 | 0 | 0 |
| downward:seq-opt-bjolp | opt | 7 | 447.0000 | 33 | 35.9969 | 6 | 5 | 0 | 0 | 0 |
| downward:seq-opt-fdss-2 | opt | 7 | 447.0000 | 33 | 17.7855 | 6 | 0 | 0 | 0 | 5 |

## [TABLE_2.2_GLOBAL_SUMMARY]

| planner | family | max_solved_size | plan_cost_at_max_size | plan_length_at_max_size | wall_time_s_at_max_size | count_solved | count_timeout | count_unsolved | count_unsupported | count_error |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| metric-ff | sat | 10 | 3416.0000 | 39 | 1.1699 | 9 | 0 | 0 | 0 | 2 |
| downward:lama-first | sat | 12 | 3963.0000 | 47 | 1.5500 | 11 | 0 | 0 | 0 | 0 |
| downward:seq-sat-fdss-2 | sat | 12 | 1969.0000 | 47 | 59.7602 | 11 | 0 | 0 | 0 | 0 |
| downward:seq-sat-fd-autotune-2 | sat | 5 | 539.0000 | 23 | 26.4508 | 4 | 7 | 0 | 0 | 0 |
| downward:seq-opt-lmcut | opt | 6 | 573.0000 | 29 | 24.4249 | 5 | 6 | 0 | 0 | 0 |
| downward:seq-opt-bjolp | opt | 7 | 447.0000 | 33 | 35.9969 | 6 | 5 | 0 | 0 | 0 |
| downward:seq-opt-fdss-2 | opt | 7 | 447.0000 | 33 | 17.7855 | 6 | 0 | 0 | 0 | 5 |

## [PLOTS]

![part22_max_solved_size_by_planner](part22_max_solved_size_by_planner.png)

![part22_cost_at_max_solved_size_by_planner](part22_cost_at_max_solved_size_by_planner.png)

![part22_time_vs_cost_scatter](part22_time_vs_cost_scatter.png)

## [ERROR_DETAILS]

### E001
```text
ff: parsing domain file | domain 'UBERMEDICS-CARRIERS-COSTS' defined | ... done. | ff: parsing problem file | problem 'DRONE_PROBLEM_EX2_D1_R1_L11_P11_C11_G11_A4' defined | ... done.
```

### E002
```text
ff: parsing domain file | domain 'UBERMEDICS-CARRIERS-COSTS' defined | ... done. | ff: parsing problem file | problem 'DRONE_PROBLEM_EX2_D1_R1_L12_P12_C12_G12_A4' defined | ... done.
```

### E003
```text
INFO     planner time limit: 60s | INFO     planner memory limit: None | INFO     Running translator. | INFO     translator stdin: None | INFO     translator time limit: 59s | INFO     translator memory limit: None
```
