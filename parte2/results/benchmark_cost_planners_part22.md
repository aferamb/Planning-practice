# Benchmark cost planners - Practice 1 Part 2 Exercise 2.2

- Generated at: `2026-03-22T06:42:42`
- Args: `{'min_size': 2, 'max_size': 12, 'step': 1, 'sizes': None, 'timeout': 100, 'domain': 'dronedomain2.pddl', 'generator': 'generate-problem.py', 'results_dir': 'results', 'drones': 1, 'carriers': 1, 'carrier_capacity': 4, 'exercise': 2, 'seed': None, 'problem_files': None}`

## [GENERATION]

| size | problem_file | status | wall_time_s | error_excerpt |
| --- | --- | --- | --- | --- |
| 2 | problems/drone_problem_ex2_d1_r1_l2_p2_c2_g2_a4.pddl | ok | 0.2569 |  |
| 3 | problems/drone_problem_ex2_d1_r1_l3_p3_c3_g3_a4.pddl | ok | 0.1987 |  |
| 4 | problems/drone_problem_ex2_d1_r1_l4_p4_c4_g4_a4.pddl | ok | 0.3692 |  |
| 5 | problems/drone_problem_ex2_d1_r1_l5_p5_c5_g5_a4.pddl | ok | 0.1703 |  |
| 6 | problems/drone_problem_ex2_d1_r1_l6_p6_c6_g6_a4.pddl | ok | 0.2329 |  |
| 7 | problems/drone_problem_ex2_d1_r1_l7_p7_c7_g7_a4.pddl | ok | 0.1666 |  |
| 8 | problems/drone_problem_ex2_d1_r1_l8_p8_c8_g8_a4.pddl | ok | 0.1165 |  |
| 9 | problems/drone_problem_ex2_d1_r1_l9_p9_c9_g9_a4.pddl | ok | 0.1628 |  |
| 10 | problems/drone_problem_ex2_d1_r1_l10_p10_c10_g10_a4.pddl | ok | 0.3644 |  |
| 11 | problems/drone_problem_ex2_d1_r1_l11_p11_c11_g11_a4.pddl | ok | 0.4260 |  |
| 12 | problems/drone_problem_ex2_d1_r1_l12_p12_c12_g12_a4.pddl | ok | 0.2950 |  |

## [RAW_ROWS]

| planner | family | status | size | planner_time_s | wall_time_s | plan_cost | plan_length | error_excerpt | problem_file |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| metric-ff | sat | solved | 2 | 0.0000 | 1.6709 | 154.0000 | 7 |  | problems/drone_problem_ex2_d1_r1_l2_p2_c2_g2_a4.pddl |
| metric-ff | sat | solved | 3 | 0.0100 | 1.9797 | 831.0000 | 11 |  | problems/drone_problem_ex2_d1_r1_l3_p3_c3_g3_a4.pddl |
| metric-ff | sat | solved | 4 | 0.0000 | 1.6291 | 1466.0000 | 15 |  | problems/drone_problem_ex2_d1_r1_l4_p4_c4_g4_a4.pddl |
| metric-ff | sat | solved | 5 | 0.0100 | 2.0162 | 1611.0000 | 19 |  | problems/drone_problem_ex2_d1_r1_l5_p5_c5_g5_a4.pddl |
| metric-ff | sat | solved | 6 | 0.0300 | 1.7858 | 2061.0000 | 23 |  | problems/drone_problem_ex2_d1_r1_l6_p6_c6_g6_a4.pddl |
| metric-ff | sat | solved | 7 | 0.0300 | 2.2965 | 1527.0000 | 29 |  | problems/drone_problem_ex2_d1_r1_l7_p7_c7_g7_a4.pddl |
| metric-ff | sat | solved | 8 | 0.0400 | 1.7787 | 2478.0000 | 31 |  | problems/drone_problem_ex2_d1_r1_l8_p8_c8_g8_a4.pddl |
| metric-ff | sat | solved | 9 | 0.0500 | 1.9477 | 3158.0000 | 37 |  | problems/drone_problem_ex2_d1_r1_l9_p9_c9_g9_a4.pddl |
| metric-ff | sat | solved | 10 | 0.0600 | 2.0460 | 3259.0000 | 39 |  | problems/drone_problem_ex2_d1_r1_l10_p10_c10_g10_a4.pddl |
| metric-ff | sat | error | 11 |  | 1.3299 |  |  | ff: parsing domain file \| domain 'UBERMEDICS-CARRIERS-COSTS' defined \| ... done. \| ff: parsing problem file \| problem... (E001) | problems/drone_problem_ex2_d1_r1_l11_p11_c11_g11_a4.pddl |
| metric-ff | sat | error | 12 |  | 1.3704 |  |  | ff: parsing domain file \| domain 'UBERMEDICS-CARRIERS-COSTS' defined \| ... done. \| ff: parsing problem file \| problem... (E002) | problems/drone_problem_ex2_d1_r1_l12_p12_c12_g12_a4.pddl |
| downward:lama-first | sat | solved | 2 | 0.5000 | 3.9852 | 154.0000 | 7 |  | problems/drone_problem_ex2_d1_r1_l2_p2_c2_g2_a4.pddl |
| downward:lama-first | sat | solved | 3 | 0.5600 | 3.6444 | 831.0000 | 11 |  | problems/drone_problem_ex2_d1_r1_l3_p3_c3_g3_a4.pddl |
| downward:lama-first | sat | solved | 4 | 0.4100 | 4.1341 | 1349.0000 | 15 |  | problems/drone_problem_ex2_d1_r1_l4_p4_c4_g4_a4.pddl |
| downward:lama-first | sat | solved | 5 | 0.4300 | 2.9387 | 1809.0000 | 20 |  | problems/drone_problem_ex2_d1_r1_l5_p5_c5_g5_a4.pddl |
| downward:lama-first | sat | solved | 6 | 0.4600 | 3.6711 | 2155.0000 | 24 |  | problems/drone_problem_ex2_d1_r1_l6_p6_c6_g6_a4.pddl |
| downward:lama-first | sat | solved | 7 | 0.5900 | 3.4721 | 1804.0000 | 30 |  | problems/drone_problem_ex2_d1_r1_l7_p7_c7_g7_a4.pddl |
| downward:lama-first | sat | solved | 8 | 0.5800 | 3.6615 | 2521.0000 | 32 |  | problems/drone_problem_ex2_d1_r1_l8_p8_c8_g8_a4.pddl |
| downward:lama-first | sat | solved | 9 | 0.5600 | 3.8044 | 3284.0000 | 39 |  | problems/drone_problem_ex2_d1_r1_l9_p9_c9_g9_a4.pddl |
| downward:lama-first | sat | solved | 10 | 0.6400 | 3.5802 | 3511.0000 | 43 |  | problems/drone_problem_ex2_d1_r1_l10_p10_c10_g10_a4.pddl |
| downward:lama-first | sat | solved | 11 | 0.6700 | 3.6566 | 3977.0000 | 48 |  | problems/drone_problem_ex2_d1_r1_l11_p11_c11_g11_a4.pddl |
| downward:lama-first | sat | solved | 12 | 0.8000 | 4.1125 | 3038.0000 | 51 |  | problems/drone_problem_ex2_d1_r1_l12_p12_c12_g12_a4.pddl |
| downward:seq-sat-fdss-2 | sat | solved | 2 | 0.4600 | 3.6828 | 58.0000 | 7 |  | problems/drone_problem_ex2_d1_r1_l2_p2_c2_g2_a4.pddl |
| downward:seq-sat-fdss-2 | sat | solved | 3 | 0.4800 | 3.3354 | 177.0000 | 11 |  | problems/drone_problem_ex2_d1_r1_l3_p3_c3_g3_a4.pddl |
| downward:seq-sat-fdss-2 | sat | solved | 4 | 0.8000 | 3.9204 | 267.0000 | 15 |  | problems/drone_problem_ex2_d1_r1_l4_p4_c4_g4_a4.pddl |
| downward:seq-sat-fdss-2 | sat | solved | 5 | 7.0900 | 15.3817 | 617.0000 | 19 |  | problems/drone_problem_ex2_d1_r1_l5_p5_c5_g5_a4.pddl |
| downward:seq-sat-fdss-2 | sat | timeout | 6 |  | 100.1293 | 709.0000 | 23 |  | problems/drone_problem_ex2_d1_r1_l6_p6_c6_g6_a4.pddl |
| downward:seq-sat-fdss-2 | sat | timeout | 7 |  | 100.0515 | 493.0000 | 27 |  | problems/drone_problem_ex2_d1_r1_l7_p7_c7_g7_a4.pddl |
| downward:seq-sat-fdss-2 | sat | timeout | 8 |  | 100.0932 | 814.0000 | 31 |  | problems/drone_problem_ex2_d1_r1_l8_p8_c8_g8_a4.pddl |
| downward:seq-sat-fdss-2 | sat | timeout | 9 |  | 100.0665 | 1219.0000 | 35 |  | problems/drone_problem_ex2_d1_r1_l9_p9_c9_g9_a4.pddl |
| downward:seq-sat-fdss-2 | sat | timeout | 10 |  | 100.1047 | 1819.0000 | 39 |  | problems/drone_problem_ex2_d1_r1_l10_p10_c10_g10_a4.pddl |
| downward:seq-sat-fdss-2 | sat | timeout | 11 |  | 100.0244 | 2059.0000 | 43 |  | problems/drone_problem_ex2_d1_r1_l11_p11_c11_g11_a4.pddl |
| downward:seq-sat-fdss-2 | sat | timeout | 12 |  | 100.0429 | 1391.0000 | 47 |  | problems/drone_problem_ex2_d1_r1_l12_p12_c12_g12_a4.pddl |
| downward:seq-sat-fd-autotune-2 | sat | solved | 2 | 0.5500 | 4.0091 | 58.0000 | 7 |  | problems/drone_problem_ex2_d1_r1_l2_p2_c2_g2_a4.pddl |
| downward:seq-sat-fd-autotune-2 | sat | solved | 3 | 0.7400 | 3.9289 | 505.0000 | 11 |  | problems/drone_problem_ex2_d1_r1_l3_p3_c3_g3_a4.pddl |
| downward:seq-sat-fd-autotune-2 | sat | solved | 4 | 6.5200 | 15.3050 | 384.0000 | 18 |  | problems/drone_problem_ex2_d1_r1_l4_p4_c4_g4_a4.pddl |
| downward:seq-sat-fd-autotune-2 | sat | timeout | 5 |  | 100.0368 | 701.0000 | 21 |  | problems/drone_problem_ex2_d1_r1_l5_p5_c5_g5_a4.pddl |
| downward:seq-sat-fd-autotune-2 | sat | timeout | 6 |  | 100.0534 | 1145.0000 | 30 |  | problems/drone_problem_ex2_d1_r1_l6_p6_c6_g6_a4.pddl |
| downward:seq-sat-fd-autotune-2 | sat | timeout | 7 |  | 100.0352 | 1121.0000 | 31 |  | problems/drone_problem_ex2_d1_r1_l7_p7_c7_g7_a4.pddl |
| downward:seq-sat-fd-autotune-2 | sat | timeout | 8 |  | 100.1137 | 2450.0000 | 32 |  | problems/drone_problem_ex2_d1_r1_l8_p8_c8_g8_a4.pddl |
| downward:seq-sat-fd-autotune-2 | sat | timeout | 9 |  | 100.1241 | 2907.0000 | 45 |  | problems/drone_problem_ex2_d1_r1_l9_p9_c9_g9_a4.pddl |
| downward:seq-sat-fd-autotune-2 | sat | timeout | 10 |  | 100.0282 | 3092.0000 | 48 |  | problems/drone_problem_ex2_d1_r1_l10_p10_c10_g10_a4.pddl |
| downward:seq-sat-fd-autotune-2 | sat | timeout | 11 |  | 100.0185 | 3193.0000 | 47 |  | problems/drone_problem_ex2_d1_r1_l11_p11_c11_g11_a4.pddl |
| downward:seq-sat-fd-autotune-2 | sat | timeout | 12 |  | 100.1071 | 2845.0000 | 67 |  | problems/drone_problem_ex2_d1_r1_l12_p12_c12_g12_a4.pddl |
| downward:seq-opt-lmcut | opt | solved | 2 | 0.3000 | 3.5197 | 58.0000 | 9 |  | problems/drone_problem_ex2_d1_r1_l2_p2_c2_g2_a4.pddl |
| downward:seq-opt-lmcut | opt | solved | 3 | 0.3300 | 2.8445 | 177.0000 | 13 |  | problems/drone_problem_ex2_d1_r1_l3_p3_c3_g3_a4.pddl |
| downward:seq-opt-lmcut | opt | solved | 4 | 0.5200 | 3.6412 | 267.0000 | 19 |  | problems/drone_problem_ex2_d1_r1_l4_p4_c4_g4_a4.pddl |
| downward:seq-opt-lmcut | opt | solved | 5 | 7.5900 | 17.9989 | 601.0000 | 22 |  | problems/drone_problem_ex2_d1_r1_l5_p5_c5_g5_a4.pddl |
| downward:seq-opt-lmcut | opt | solved | 6 | 48.4800 | 96.1500 | 680.0000 | 29 |  | problems/drone_problem_ex2_d1_r1_l6_p6_c6_g6_a4.pddl |
| downward:seq-opt-lmcut | opt | timeout | 7 |  | 100.0243 |  |  |  | problems/drone_problem_ex2_d1_r1_l7_p7_c7_g7_a4.pddl |
| downward:seq-opt-lmcut | opt | timeout | 8 |  | 100.0218 |  |  |  | problems/drone_problem_ex2_d1_r1_l8_p8_c8_g8_a4.pddl |
| downward:seq-opt-lmcut | opt | timeout | 9 |  | 100.0627 |  |  |  | problems/drone_problem_ex2_d1_r1_l9_p9_c9_g9_a4.pddl |
| downward:seq-opt-lmcut | opt | timeout | 10 |  | 100.0642 |  |  |  | problems/drone_problem_ex2_d1_r1_l10_p10_c10_g10_a4.pddl |
| downward:seq-opt-lmcut | opt | timeout | 11 |  | 100.0330 |  |  |  | problems/drone_problem_ex2_d1_r1_l11_p11_c11_g11_a4.pddl |
| downward:seq-opt-lmcut | opt | timeout | 12 |  | 100.0792 |  |  |  | problems/drone_problem_ex2_d1_r1_l12_p12_c12_g12_a4.pddl |
| downward:seq-opt-bjolp | opt | solved | 2 | 0.3600 | 2.9531 | 58.0000 | 9 |  | problems/drone_problem_ex2_d1_r1_l2_p2_c2_g2_a4.pddl |
| downward:seq-opt-bjolp | opt | solved | 3 | 0.3600 | 3.1243 | 177.0000 | 13 |  | problems/drone_problem_ex2_d1_r1_l3_p3_c3_g3_a4.pddl |
| downward:seq-opt-bjolp | opt | solved | 4 | 0.4200 | 3.4789 | 267.0000 | 19 |  | problems/drone_problem_ex2_d1_r1_l4_p4_c4_g4_a4.pddl |
| downward:seq-opt-bjolp | opt | solved | 5 | 1.4300 | 4.8475 | 601.0000 | 22 |  | problems/drone_problem_ex2_d1_r1_l5_p5_c5_g5_a4.pddl |
| downward:seq-opt-bjolp | opt | solved | 6 | 6.9100 | 14.8597 | 680.0000 | 29 |  | problems/drone_problem_ex2_d1_r1_l6_p6_c6_g6_a4.pddl |
| downward:seq-opt-bjolp | opt | solved | 7 | 24.0900 | 47.6772 | 452.0000 | 33 |  | problems/drone_problem_ex2_d1_r1_l7_p7_c7_g7_a4.pddl |
| downward:seq-opt-bjolp | opt | timeout | 8 |  | 100.0330 |  |  |  | problems/drone_problem_ex2_d1_r1_l8_p8_c8_g8_a4.pddl |
| downward:seq-opt-bjolp | opt | timeout | 9 |  | 100.0211 |  |  |  | problems/drone_problem_ex2_d1_r1_l9_p9_c9_g9_a4.pddl |
| downward:seq-opt-bjolp | opt | timeout | 10 |  | 100.0314 |  |  |  | problems/drone_problem_ex2_d1_r1_l10_p10_c10_g10_a4.pddl |
| downward:seq-opt-bjolp | opt | timeout | 11 |  | 100.0235 |  |  |  | problems/drone_problem_ex2_d1_r1_l11_p11_c11_g11_a4.pddl |
| downward:seq-opt-bjolp | opt | timeout | 12 |  | 100.0373 |  |  |  | problems/drone_problem_ex2_d1_r1_l12_p12_c12_g12_a4.pddl |
| downward:seq-opt-fdss-2 | opt | solved | 2 | 0.9400 | 5.4632 | 58.0000 | 9 |  | problems/drone_problem_ex2_d1_r1_l2_p2_c2_g2_a4.pddl |
| downward:seq-opt-fdss-2 | opt | solved | 3 | 0.7800 | 3.6786 | 177.0000 | 13 |  | problems/drone_problem_ex2_d1_r1_l3_p3_c3_g3_a4.pddl |
| downward:seq-opt-fdss-2 | opt | solved | 4 | 0.5500 | 3.7447 | 267.0000 | 19 |  | problems/drone_problem_ex2_d1_r1_l4_p4_c4_g4_a4.pddl |
| downward:seq-opt-fdss-2 | opt | solved | 5 | 1.3200 | 5.5351 | 601.0000 | 22 |  | problems/drone_problem_ex2_d1_r1_l5_p5_c5_g5_a4.pddl |
| downward:seq-opt-fdss-2 | opt | solved | 6 | 8.2700 | 16.1498 | 680.0000 | 29 |  | problems/drone_problem_ex2_d1_r1_l6_p6_c6_g6_a4.pddl |
| downward:seq-opt-fdss-2 | opt | solved | 7 | 28.9800 | 51.9132 | 452.0000 | 33 |  | problems/drone_problem_ex2_d1_r1_l7_p7_c7_g7_a4.pddl |
| downward:seq-opt-fdss-2 | opt | timeout | 8 |  | 100.0228 |  |  |  | problems/drone_problem_ex2_d1_r1_l8_p8_c8_g8_a4.pddl |
| downward:seq-opt-fdss-2 | opt | timeout | 9 |  | 100.0185 |  |  |  | problems/drone_problem_ex2_d1_r1_l9_p9_c9_g9_a4.pddl |
| downward:seq-opt-fdss-2 | opt | timeout | 10 |  | 100.0266 |  |  |  | problems/drone_problem_ex2_d1_r1_l10_p10_c10_g10_a4.pddl |
| downward:seq-opt-fdss-2 | opt | timeout | 11 |  | 100.0217 |  |  |  | problems/drone_problem_ex2_d1_r1_l11_p11_c11_g11_a4.pddl |
| downward:seq-opt-fdss-2 | opt | timeout | 12 |  | 100.0323 |  |  |  | problems/drone_problem_ex2_d1_r1_l12_p12_c12_g12_a4.pddl |

## [TABLE_2.2_SAT_SUMMARY]

| planner | family | max_solved_size | plan_cost_at_max_size | plan_length_at_max_size | wall_time_s_at_max_size | count_solved | count_timeout | count_unsolved | count_unsupported | count_error |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| metric-ff | sat | 10 | 3259.0000 | 39 | 2.0460 | 9 | 0 | 0 | 0 | 2 |
| downward:lama-first | sat | 12 | 3038.0000 | 51 | 4.1125 | 11 | 0 | 0 | 0 | 0 |
| downward:seq-sat-fdss-2 | sat | 5 | 617.0000 | 19 | 15.3817 | 4 | 7 | 0 | 0 | 0 |
| downward:seq-sat-fd-autotune-2 | sat | 4 | 384.0000 | 18 | 15.3050 | 3 | 8 | 0 | 0 | 0 |

## [TABLE_2.2_OPT_SUMMARY]

| planner | family | max_solved_size | plan_cost_at_max_size | plan_length_at_max_size | wall_time_s_at_max_size | count_solved | count_timeout | count_unsolved | count_unsupported | count_error |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| downward:seq-opt-lmcut | opt | 6 | 680.0000 | 29 | 96.1500 | 5 | 6 | 0 | 0 | 0 |
| downward:seq-opt-bjolp | opt | 7 | 452.0000 | 33 | 47.6772 | 6 | 5 | 0 | 0 | 0 |
| downward:seq-opt-fdss-2 | opt | 7 | 452.0000 | 33 | 51.9132 | 6 | 5 | 0 | 0 | 0 |

## [TABLE_2.2_GLOBAL_SUMMARY]

| planner | family | max_solved_size | plan_cost_at_max_size | plan_length_at_max_size | wall_time_s_at_max_size | count_solved | count_timeout | count_unsolved | count_unsupported | count_error |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| metric-ff | sat | 10 | 3259.0000 | 39 | 2.0460 | 9 | 0 | 0 | 0 | 2 |
| downward:lama-first | sat | 12 | 3038.0000 | 51 | 4.1125 | 11 | 0 | 0 | 0 | 0 |
| downward:seq-sat-fdss-2 | sat | 5 | 617.0000 | 19 | 15.3817 | 4 | 7 | 0 | 0 | 0 |
| downward:seq-sat-fd-autotune-2 | sat | 4 | 384.0000 | 18 | 15.3050 | 3 | 8 | 0 | 0 | 0 |
| downward:seq-opt-lmcut | opt | 6 | 680.0000 | 29 | 96.1500 | 5 | 6 | 0 | 0 | 0 |
| downward:seq-opt-bjolp | opt | 7 | 452.0000 | 33 | 47.6772 | 6 | 5 | 0 | 0 | 0 |
| downward:seq-opt-fdss-2 | opt | 7 | 452.0000 | 33 | 51.9132 | 6 | 5 | 0 | 0 | 0 |

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
