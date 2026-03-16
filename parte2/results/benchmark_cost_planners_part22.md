# Benchmark cost planners - Practice 1 Part 2 Exercise 2.2

- Generated at: `2026-03-16T04:13:10`
- Args: `{'min_size': 2, 'max_size': 12, 'step': 1, 'sizes': None, 'timeout': 60, 'domain': 'dronedomain2.pddl', 'generator': 'generate-problem.py', 'results_dir': 'results', 'drones': 1, 'carriers': 1, 'carrier_capacity': 4, 'exercise': 2, 'seed': None, 'problem_files': None}`

## [GENERATION]

| size | problem_file | status | wall_time_s | error_excerpt |
| --- | --- | --- | --- | --- |
| 2 | problems/drone_problem_ex2_d1_r1_l2_p2_c2_g2_a4.pddl | ok | 0.3470 |  |
| 3 | problems/drone_problem_ex2_d1_r1_l3_p3_c3_g3_a4.pddl | ok | 0.2209 |  |
| 4 | problems/drone_problem_ex2_d1_r1_l4_p4_c4_g4_a4.pddl | ok | 0.3765 |  |
| 5 | problems/drone_problem_ex2_d1_r1_l5_p5_c5_g5_a4.pddl | ok | 0.2193 |  |
| 6 | problems/drone_problem_ex2_d1_r1_l6_p6_c6_g6_a4.pddl | ok | 0.1311 |  |
| 7 | problems/drone_problem_ex2_d1_r1_l7_p7_c7_g7_a4.pddl | ok | 0.1743 |  |
| 8 | problems/drone_problem_ex2_d1_r1_l8_p8_c8_g8_a4.pddl | ok | 0.1657 |  |
| 9 | problems/drone_problem_ex2_d1_r1_l9_p9_c9_g9_a4.pddl | ok | 0.2651 |  |
| 10 | problems/drone_problem_ex2_d1_r1_l10_p10_c10_g10_a4.pddl | ok | 0.2216 |  |
| 11 | problems/drone_problem_ex2_d1_r1_l11_p11_c11_g11_a4.pddl | ok | 0.3197 |  |
| 12 | problems/drone_problem_ex2_d1_r1_l12_p12_c12_g12_a4.pddl | ok | 0.1942 |  |

## [RAW_ROWS]

| planner | family | status | size | wall_time_s | plan_cost | plan_length | error_excerpt | problem_file |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| metric-ff | sat | error | 2 | 2.3253 |  |  | /home/alex/.planutils/packages/metric-ff/run: line 44: $PROBLEM.plan: ambiguous redirect \| usage of ff: \| OPTIONS   D... (E001) | problems/drone_problem_ex2_d1_r1_l2_p2_c2_g2_a4.pddl |
| metric-ff | sat | error | 3 | 2.2963 |  |  | /home/alex/.planutils/packages/metric-ff/run: line 44: $PROBLEM.plan: ambiguous redirect \| usage of ff: \| OPTIONS   D... (E001) | problems/drone_problem_ex2_d1_r1_l3_p3_c3_g3_a4.pddl |
| metric-ff | sat | error | 4 | 2.5752 |  |  | /home/alex/.planutils/packages/metric-ff/run: line 44: $PROBLEM.plan: ambiguous redirect \| usage of ff: \| OPTIONS   D... (E001) | problems/drone_problem_ex2_d1_r1_l4_p4_c4_g4_a4.pddl |
| metric-ff | sat | error | 5 | 2.5399 |  |  | /home/alex/.planutils/packages/metric-ff/run: line 44: $PROBLEM.plan: ambiguous redirect \| usage of ff: \| OPTIONS   D... (E001) | problems/drone_problem_ex2_d1_r1_l5_p5_c5_g5_a4.pddl |
| metric-ff | sat | error | 6 | 2.1584 |  |  | /home/alex/.planutils/packages/metric-ff/run: line 44: $PROBLEM.plan: ambiguous redirect \| usage of ff: \| OPTIONS   D... (E001) | problems/drone_problem_ex2_d1_r1_l6_p6_c6_g6_a4.pddl |
| metric-ff | sat | error | 7 | 2.1827 |  |  | /home/alex/.planutils/packages/metric-ff/run: line 44: $PROBLEM.plan: ambiguous redirect \| usage of ff: \| OPTIONS   D... (E001) | problems/drone_problem_ex2_d1_r1_l7_p7_c7_g7_a4.pddl |
| metric-ff | sat | error | 8 | 2.1892 |  |  | /home/alex/.planutils/packages/metric-ff/run: line 44: $PROBLEM.plan: ambiguous redirect \| usage of ff: \| OPTIONS   D... (E001) | problems/drone_problem_ex2_d1_r1_l8_p8_c8_g8_a4.pddl |
| metric-ff | sat | error | 9 | 1.9894 |  |  | /home/alex/.planutils/packages/metric-ff/run: line 44: $PROBLEM.plan: ambiguous redirect \| usage of ff: \| OPTIONS   D... (E001) | problems/drone_problem_ex2_d1_r1_l9_p9_c9_g9_a4.pddl |
| metric-ff | sat | error | 10 | 4.6311 |  |  | /home/alex/.planutils/packages/metric-ff/run: line 44: $PROBLEM.plan: ambiguous redirect \| usage of ff: \| OPTIONS   D... (E001) | problems/drone_problem_ex2_d1_r1_l10_p10_c10_g10_a4.pddl |
| metric-ff | sat | error | 11 | 2.6367 |  |  | /home/alex/.planutils/packages/metric-ff/run: line 44: $PROBLEM.plan: ambiguous redirect \| usage of ff: \| OPTIONS   D... (E001) | problems/drone_problem_ex2_d1_r1_l11_p11_c11_g11_a4.pddl |
| metric-ff | sat | error | 12 | 2.3562 |  |  | /home/alex/.planutils/packages/metric-ff/run: line 44: $PROBLEM.plan: ambiguous redirect \| usage of ff: \| OPTIONS   D... (E001) | problems/drone_problem_ex2_d1_r1_l12_p12_c12_g12_a4.pddl |
| downward:lama-first | sat | error | 2 | 5.0611 |  |  | fast-downward.py: error: translator needs one or two PDDL input files \| usage: fast-downward.py [-h] [-v] [--show-ali... (E002) | problems/drone_problem_ex2_d1_r1_l2_p2_c2_g2_a4.pddl |
| downward:lama-first | sat | error | 3 | 4.4152 |  |  | fast-downward.py: error: translator needs one or two PDDL input files \| usage: fast-downward.py [-h] [-v] [--show-ali... (E002) | problems/drone_problem_ex2_d1_r1_l3_p3_c3_g3_a4.pddl |
| downward:lama-first | sat | error | 4 | 3.4191 |  |  | fast-downward.py: error: translator needs one or two PDDL input files \| usage: fast-downward.py [-h] [-v] [--show-ali... (E002) | problems/drone_problem_ex2_d1_r1_l4_p4_c4_g4_a4.pddl |
| downward:lama-first | sat | error | 5 | 4.9732 |  |  | fast-downward.py: error: translator needs one or two PDDL input files \| usage: fast-downward.py [-h] [-v] [--show-ali... (E002) | problems/drone_problem_ex2_d1_r1_l5_p5_c5_g5_a4.pddl |
| downward:lama-first | sat | error | 6 | 4.1370 |  |  | fast-downward.py: error: translator needs one or two PDDL input files \| usage: fast-downward.py [-h] [-v] [--show-ali... (E002) | problems/drone_problem_ex2_d1_r1_l6_p6_c6_g6_a4.pddl |
| downward:lama-first | sat | error | 7 | 3.5643 |  |  | fast-downward.py: error: translator needs one or two PDDL input files \| usage: fast-downward.py [-h] [-v] [--show-ali... (E002) | problems/drone_problem_ex2_d1_r1_l7_p7_c7_g7_a4.pddl |
| downward:lama-first | sat | error | 8 | 3.7112 |  |  | fast-downward.py: error: translator needs one or two PDDL input files \| usage: fast-downward.py [-h] [-v] [--show-ali... (E002) | problems/drone_problem_ex2_d1_r1_l8_p8_c8_g8_a4.pddl |
| downward:lama-first | sat | error | 9 | 3.3848 |  |  | fast-downward.py: error: translator needs one or two PDDL input files \| usage: fast-downward.py [-h] [-v] [--show-ali... (E002) | problems/drone_problem_ex2_d1_r1_l9_p9_c9_g9_a4.pddl |
| downward:lama-first | sat | error | 10 | 4.1396 |  |  | fast-downward.py: error: translator needs one or two PDDL input files \| usage: fast-downward.py [-h] [-v] [--show-ali... (E002) | problems/drone_problem_ex2_d1_r1_l10_p10_c10_g10_a4.pddl |
| downward:lama-first | sat | error | 11 | 4.1193 |  |  | fast-downward.py: error: translator needs one or two PDDL input files \| usage: fast-downward.py [-h] [-v] [--show-ali... (E002) | problems/drone_problem_ex2_d1_r1_l11_p11_c11_g11_a4.pddl |
| downward:lama-first | sat | error | 12 | 3.7970 |  |  | fast-downward.py: error: translator needs one or two PDDL input files \| usage: fast-downward.py [-h] [-v] [--show-ali... (E002) | problems/drone_problem_ex2_d1_r1_l12_p12_c12_g12_a4.pddl |
| downward:seq-sat-fdss-2 | sat | error | 2 | 3.8928 |  |  | fast-downward.py: error: translator needs one or two PDDL input files \| usage: fast-downward.py [-h] [-v] [--show-ali... (E002) | problems/drone_problem_ex2_d1_r1_l2_p2_c2_g2_a4.pddl |
| downward:seq-sat-fdss-2 | sat | error | 3 | 3.3999 |  |  | fast-downward.py: error: translator needs one or two PDDL input files \| usage: fast-downward.py [-h] [-v] [--show-ali... (E002) | problems/drone_problem_ex2_d1_r1_l3_p3_c3_g3_a4.pddl |
| downward:seq-sat-fdss-2 | sat | error | 4 | 4.1300 |  |  | fast-downward.py: error: translator needs one or two PDDL input files \| usage: fast-downward.py [-h] [-v] [--show-ali... (E002) | problems/drone_problem_ex2_d1_r1_l4_p4_c4_g4_a4.pddl |
| downward:seq-sat-fdss-2 | sat | error | 5 | 3.6304 |  |  | fast-downward.py: error: translator needs one or two PDDL input files \| usage: fast-downward.py [-h] [-v] [--show-ali... (E002) | problems/drone_problem_ex2_d1_r1_l5_p5_c5_g5_a4.pddl |
| downward:seq-sat-fdss-2 | sat | error | 6 | 3.5975 |  |  | fast-downward.py: error: translator needs one or two PDDL input files \| usage: fast-downward.py [-h] [-v] [--show-ali... (E002) | problems/drone_problem_ex2_d1_r1_l6_p6_c6_g6_a4.pddl |
| downward:seq-sat-fdss-2 | sat | error | 7 | 4.0635 |  |  | fast-downward.py: error: translator needs one or two PDDL input files \| usage: fast-downward.py [-h] [-v] [--show-ali... (E002) | problems/drone_problem_ex2_d1_r1_l7_p7_c7_g7_a4.pddl |
| downward:seq-sat-fdss-2 | sat | error | 8 | 4.5911 |  |  | fast-downward.py: error: translator needs one or two PDDL input files \| usage: fast-downward.py [-h] [-v] [--show-ali... (E002) | problems/drone_problem_ex2_d1_r1_l8_p8_c8_g8_a4.pddl |
| downward:seq-sat-fdss-2 | sat | error | 9 | 5.7649 |  |  | fast-downward.py: error: translator needs one or two PDDL input files \| usage: fast-downward.py [-h] [-v] [--show-ali... (E002) | problems/drone_problem_ex2_d1_r1_l9_p9_c9_g9_a4.pddl |
| downward:seq-sat-fdss-2 | sat | error | 10 | 14.5003 |  |  | fast-downward.py: error: translator needs one or two PDDL input files \| usage: fast-downward.py [-h] [-v] [--show-ali... (E002) | problems/drone_problem_ex2_d1_r1_l10_p10_c10_g10_a4.pddl |
| downward:seq-sat-fdss-2 | sat | error | 11 | 10.6054 |  |  | fast-downward.py: error: translator needs one or two PDDL input files \| usage: fast-downward.py [-h] [-v] [--show-ali... (E002) | problems/drone_problem_ex2_d1_r1_l11_p11_c11_g11_a4.pddl |
| downward:seq-sat-fdss-2 | sat | error | 12 | 3.7617 |  |  | fast-downward.py: error: translator needs one or two PDDL input files \| usage: fast-downward.py [-h] [-v] [--show-ali... (E002) | problems/drone_problem_ex2_d1_r1_l12_p12_c12_g12_a4.pddl |
| downward:seq-sat-fd-autotune-2 | sat | error | 2 | 3.5402 |  |  | fast-downward.py: error: translator needs one or two PDDL input files \| usage: fast-downward.py [-h] [-v] [--show-ali... (E002) | problems/drone_problem_ex2_d1_r1_l2_p2_c2_g2_a4.pddl |
| downward:seq-sat-fd-autotune-2 | sat | error | 3 | 3.5522 |  |  | fast-downward.py: error: translator needs one or two PDDL input files \| usage: fast-downward.py [-h] [-v] [--show-ali... (E002) | problems/drone_problem_ex2_d1_r1_l3_p3_c3_g3_a4.pddl |
| downward:seq-sat-fd-autotune-2 | sat | error | 4 | 3.9393 |  |  | fast-downward.py: error: translator needs one or two PDDL input files \| usage: fast-downward.py [-h] [-v] [--show-ali... (E002) | problems/drone_problem_ex2_d1_r1_l4_p4_c4_g4_a4.pddl |
| downward:seq-sat-fd-autotune-2 | sat | error | 5 | 3.2863 |  |  | fast-downward.py: error: translator needs one or two PDDL input files \| usage: fast-downward.py [-h] [-v] [--show-ali... (E002) | problems/drone_problem_ex2_d1_r1_l5_p5_c5_g5_a4.pddl |
| downward:seq-sat-fd-autotune-2 | sat | error | 6 | 3.2477 |  |  | fast-downward.py: error: translator needs one or two PDDL input files \| usage: fast-downward.py [-h] [-v] [--show-ali... (E002) | problems/drone_problem_ex2_d1_r1_l6_p6_c6_g6_a4.pddl |
| downward:seq-sat-fd-autotune-2 | sat | error | 7 | 3.6205 |  |  | fast-downward.py: error: translator needs one or two PDDL input files \| usage: fast-downward.py [-h] [-v] [--show-ali... (E002) | problems/drone_problem_ex2_d1_r1_l7_p7_c7_g7_a4.pddl |
| downward:seq-sat-fd-autotune-2 | sat | error | 8 | 3.4384 |  |  | fast-downward.py: error: translator needs one or two PDDL input files \| usage: fast-downward.py [-h] [-v] [--show-ali... (E002) | problems/drone_problem_ex2_d1_r1_l8_p8_c8_g8_a4.pddl |
| downward:seq-sat-fd-autotune-2 | sat | error | 9 | 4.4093 |  |  | fast-downward.py: error: translator needs one or two PDDL input files \| usage: fast-downward.py [-h] [-v] [--show-ali... (E002) | problems/drone_problem_ex2_d1_r1_l9_p9_c9_g9_a4.pddl |
| downward:seq-sat-fd-autotune-2 | sat | error | 10 | 3.3670 |  |  | fast-downward.py: error: translator needs one or two PDDL input files \| usage: fast-downward.py [-h] [-v] [--show-ali... (E002) | problems/drone_problem_ex2_d1_r1_l10_p10_c10_g10_a4.pddl |
| downward:seq-sat-fd-autotune-2 | sat | error | 11 | 3.3715 |  |  | fast-downward.py: error: translator needs one or two PDDL input files \| usage: fast-downward.py [-h] [-v] [--show-ali... (E002) | problems/drone_problem_ex2_d1_r1_l11_p11_c11_g11_a4.pddl |
| downward:seq-sat-fd-autotune-2 | sat | error | 12 | 3.6438 |  |  | fast-downward.py: error: translator needs one or two PDDL input files \| usage: fast-downward.py [-h] [-v] [--show-ali... (E002) | problems/drone_problem_ex2_d1_r1_l12_p12_c12_g12_a4.pddl |
| downward:seq-opt-lmcut | opt | error | 2 | 4.3982 |  |  | fast-downward.py: error: translator needs one or two PDDL input files \| usage: fast-downward.py [-h] [-v] [--show-ali... (E002) | problems/drone_problem_ex2_d1_r1_l2_p2_c2_g2_a4.pddl |
| downward:seq-opt-lmcut | opt | error | 3 | 3.7133 |  |  | fast-downward.py: error: translator needs one or two PDDL input files \| usage: fast-downward.py [-h] [-v] [--show-ali... (E002) | problems/drone_problem_ex2_d1_r1_l3_p3_c3_g3_a4.pddl |
| downward:seq-opt-lmcut | opt | error | 4 | 3.3949 |  |  | fast-downward.py: error: translator needs one or two PDDL input files \| usage: fast-downward.py [-h] [-v] [--show-ali... (E002) | problems/drone_problem_ex2_d1_r1_l4_p4_c4_g4_a4.pddl |
| downward:seq-opt-lmcut | opt | error | 5 | 3.3807 |  |  | fast-downward.py: error: translator needs one or two PDDL input files \| usage: fast-downward.py [-h] [-v] [--show-ali... (E002) | problems/drone_problem_ex2_d1_r1_l5_p5_c5_g5_a4.pddl |
| downward:seq-opt-lmcut | opt | error | 6 | 3.4388 |  |  | fast-downward.py: error: translator needs one or two PDDL input files \| usage: fast-downward.py [-h] [-v] [--show-ali... (E002) | problems/drone_problem_ex2_d1_r1_l6_p6_c6_g6_a4.pddl |
| downward:seq-opt-lmcut | opt | error | 7 | 3.4362 |  |  | fast-downward.py: error: translator needs one or two PDDL input files \| usage: fast-downward.py [-h] [-v] [--show-ali... (E002) | problems/drone_problem_ex2_d1_r1_l7_p7_c7_g7_a4.pddl |
| downward:seq-opt-lmcut | opt | error | 8 | 3.0829 |  |  | fast-downward.py: error: translator needs one or two PDDL input files \| usage: fast-downward.py [-h] [-v] [--show-ali... (E002) | problems/drone_problem_ex2_d1_r1_l8_p8_c8_g8_a4.pddl |
| downward:seq-opt-lmcut | opt | error | 9 | 3.7169 |  |  | fast-downward.py: error: translator needs one or two PDDL input files \| usage: fast-downward.py [-h] [-v] [--show-ali... (E002) | problems/drone_problem_ex2_d1_r1_l9_p9_c9_g9_a4.pddl |
| downward:seq-opt-lmcut | opt | error | 10 | 3.3645 |  |  | fast-downward.py: error: translator needs one or two PDDL input files \| usage: fast-downward.py [-h] [-v] [--show-ali... (E002) | problems/drone_problem_ex2_d1_r1_l10_p10_c10_g10_a4.pddl |
| downward:seq-opt-lmcut | opt | error | 11 | 3.5283 |  |  | fast-downward.py: error: translator needs one or two PDDL input files \| usage: fast-downward.py [-h] [-v] [--show-ali... (E002) | problems/drone_problem_ex2_d1_r1_l11_p11_c11_g11_a4.pddl |
| downward:seq-opt-lmcut | opt | error | 12 | 4.2609 |  |  | fast-downward.py: error: translator needs one or two PDDL input files \| usage: fast-downward.py [-h] [-v] [--show-ali... (E002) | problems/drone_problem_ex2_d1_r1_l12_p12_c12_g12_a4.pddl |
| downward:seq-opt-bjolp | opt | error | 2 | 4.2284 |  |  | fast-downward.py: error: translator needs one or two PDDL input files \| usage: fast-downward.py [-h] [-v] [--show-ali... (E002) | problems/drone_problem_ex2_d1_r1_l2_p2_c2_g2_a4.pddl |
| downward:seq-opt-bjolp | opt | error | 3 | 4.6283 |  |  | fast-downward.py: error: translator needs one or two PDDL input files \| usage: fast-downward.py [-h] [-v] [--show-ali... (E002) | problems/drone_problem_ex2_d1_r1_l3_p3_c3_g3_a4.pddl |
| downward:seq-opt-bjolp | opt | error | 4 | 4.9872 |  |  | fast-downward.py: error: translator needs one or two PDDL input files \| usage: fast-downward.py [-h] [-v] [--show-ali... (E002) | problems/drone_problem_ex2_d1_r1_l4_p4_c4_g4_a4.pddl |
| downward:seq-opt-bjolp | opt | error | 5 | 6.8554 |  |  | fast-downward.py: error: translator needs one or two PDDL input files \| usage: fast-downward.py [-h] [-v] [--show-ali... (E002) | problems/drone_problem_ex2_d1_r1_l5_p5_c5_g5_a4.pddl |
| downward:seq-opt-bjolp | opt | error | 6 | 6.2582 |  |  | fast-downward.py: error: translator needs one or two PDDL input files \| usage: fast-downward.py [-h] [-v] [--show-ali... (E002) | problems/drone_problem_ex2_d1_r1_l6_p6_c6_g6_a4.pddl |
| downward:seq-opt-bjolp | opt | error | 7 | 5.8179 |  |  | fast-downward.py: error: translator needs one or two PDDL input files \| usage: fast-downward.py [-h] [-v] [--show-ali... (E002) | problems/drone_problem_ex2_d1_r1_l7_p7_c7_g7_a4.pddl |
| downward:seq-opt-bjolp | opt | error | 8 | 6.7746 |  |  | fast-downward.py: error: translator needs one or two PDDL input files \| usage: fast-downward.py [-h] [-v] [--show-ali... (E002) | problems/drone_problem_ex2_d1_r1_l8_p8_c8_g8_a4.pddl |
| downward:seq-opt-bjolp | opt | error | 9 | 6.2757 |  |  | fast-downward.py: error: translator needs one or two PDDL input files \| usage: fast-downward.py [-h] [-v] [--show-ali... (E002) | problems/drone_problem_ex2_d1_r1_l9_p9_c9_g9_a4.pddl |
| downward:seq-opt-bjolp | opt | error | 10 | 7.1195 |  |  | fast-downward.py: error: translator needs one or two PDDL input files \| usage: fast-downward.py [-h] [-v] [--show-ali... (E002) | problems/drone_problem_ex2_d1_r1_l10_p10_c10_g10_a4.pddl |
| downward:seq-opt-bjolp | opt | error | 11 | 4.9534 |  |  | fast-downward.py: error: translator needs one or two PDDL input files \| usage: fast-downward.py [-h] [-v] [--show-ali... (E002) | problems/drone_problem_ex2_d1_r1_l11_p11_c11_g11_a4.pddl |
| downward:seq-opt-bjolp | opt | error | 12 | 4.9587 |  |  | fast-downward.py: error: translator needs one or two PDDL input files \| usage: fast-downward.py [-h] [-v] [--show-ali... (E002) | problems/drone_problem_ex2_d1_r1_l12_p12_c12_g12_a4.pddl |
| downward:seq-opt-fdss-2 | opt | error | 2 | 4.6580 |  |  | fast-downward.py: error: translator needs one or two PDDL input files \| usage: fast-downward.py [-h] [-v] [--show-ali... (E002) | problems/drone_problem_ex2_d1_r1_l2_p2_c2_g2_a4.pddl |
| downward:seq-opt-fdss-2 | opt | error | 3 | 5.7062 |  |  | fast-downward.py: error: translator needs one or two PDDL input files \| usage: fast-downward.py [-h] [-v] [--show-ali... (E002) | problems/drone_problem_ex2_d1_r1_l3_p3_c3_g3_a4.pddl |
| downward:seq-opt-fdss-2 | opt | error | 4 | 4.3836 |  |  | fast-downward.py: error: translator needs one or two PDDL input files \| usage: fast-downward.py [-h] [-v] [--show-ali... (E002) | problems/drone_problem_ex2_d1_r1_l4_p4_c4_g4_a4.pddl |
| downward:seq-opt-fdss-2 | opt | error | 5 | 4.8352 |  |  | fast-downward.py: error: translator needs one or two PDDL input files \| usage: fast-downward.py [-h] [-v] [--show-ali... (E002) | problems/drone_problem_ex2_d1_r1_l5_p5_c5_g5_a4.pddl |
| downward:seq-opt-fdss-2 | opt | error | 6 | 4.3678 |  |  | fast-downward.py: error: translator needs one or two PDDL input files \| usage: fast-downward.py [-h] [-v] [--show-ali... (E002) | problems/drone_problem_ex2_d1_r1_l6_p6_c6_g6_a4.pddl |
| downward:seq-opt-fdss-2 | opt | error | 7 | 5.7245 |  |  | fast-downward.py: error: translator needs one or two PDDL input files \| usage: fast-downward.py [-h] [-v] [--show-ali... (E002) | problems/drone_problem_ex2_d1_r1_l7_p7_c7_g7_a4.pddl |
| downward:seq-opt-fdss-2 | opt | error | 8 | 4.0705 |  |  | fast-downward.py: error: translator needs one or two PDDL input files \| usage: fast-downward.py [-h] [-v] [--show-ali... (E002) | problems/drone_problem_ex2_d1_r1_l8_p8_c8_g8_a4.pddl |
| downward:seq-opt-fdss-2 | opt | error | 9 | 4.8402 |  |  | fast-downward.py: error: translator needs one or two PDDL input files \| usage: fast-downward.py [-h] [-v] [--show-ali... (E002) | problems/drone_problem_ex2_d1_r1_l9_p9_c9_g9_a4.pddl |
| downward:seq-opt-fdss-2 | opt | error | 10 | 4.6872 |  |  | fast-downward.py: error: translator needs one or two PDDL input files \| usage: fast-downward.py [-h] [-v] [--show-ali... (E002) | problems/drone_problem_ex2_d1_r1_l10_p10_c10_g10_a4.pddl |
| downward:seq-opt-fdss-2 | opt | error | 11 | 3.7700 |  |  | fast-downward.py: error: translator needs one or two PDDL input files \| usage: fast-downward.py [-h] [-v] [--show-ali... (E002) | problems/drone_problem_ex2_d1_r1_l11_p11_c11_g11_a4.pddl |
| downward:seq-opt-fdss-2 | opt | error | 12 | 4.4058 |  |  | fast-downward.py: error: translator needs one or two PDDL input files \| usage: fast-downward.py [-h] [-v] [--show-ali... (E002) | problems/drone_problem_ex2_d1_r1_l12_p12_c12_g12_a4.pddl |

## [TABLE_2.2_SAT_SUMMARY]

| planner | family | max_solved_size | plan_cost_at_max_size | plan_length_at_max_size | wall_time_s_at_max_size | count_solved | count_timeout | count_unsolved | count_unsupported | count_error |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| metric-ff | sat | - | - | - | - | 0 | 0 | 0 | 0 | 11 |
| downward:lama-first | sat | - | - | - | - | 0 | 0 | 0 | 0 | 11 |
| downward:seq-sat-fdss-2 | sat | - | - | - | - | 0 | 0 | 0 | 0 | 11 |
| downward:seq-sat-fd-autotune-2 | sat | - | - | - | - | 0 | 0 | 0 | 0 | 11 |

## [TABLE_2.2_OPT_SUMMARY]

| planner | family | max_solved_size | plan_cost_at_max_size | plan_length_at_max_size | wall_time_s_at_max_size | count_solved | count_timeout | count_unsolved | count_unsupported | count_error |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| downward:seq-opt-lmcut | opt | - | - | - | - | 0 | 0 | 0 | 0 | 11 |
| downward:seq-opt-bjolp | opt | - | - | - | - | 0 | 0 | 0 | 0 | 11 |
| downward:seq-opt-fdss-2 | opt | - | - | - | - | 0 | 0 | 0 | 0 | 11 |

## [TABLE_2.2_GLOBAL_SUMMARY]

| planner | family | max_solved_size | plan_cost_at_max_size | plan_length_at_max_size | wall_time_s_at_max_size | count_solved | count_timeout | count_unsolved | count_unsupported | count_error |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| metric-ff | sat | - | - | - | - | 0 | 0 | 0 | 0 | 11 |
| downward:lama-first | sat | - | - | - | - | 0 | 0 | 0 | 0 | 11 |
| downward:seq-sat-fdss-2 | sat | - | - | - | - | 0 | 0 | 0 | 0 | 11 |
| downward:seq-sat-fd-autotune-2 | sat | - | - | - | - | 0 | 0 | 0 | 0 | 11 |
| downward:seq-opt-lmcut | opt | - | - | - | - | 0 | 0 | 0 | 0 | 11 |
| downward:seq-opt-bjolp | opt | - | - | - | - | 0 | 0 | 0 | 0 | 11 |
| downward:seq-opt-fdss-2 | opt | - | - | - | - | 0 | 0 | 0 | 0 | 11 |

## [PLOTS]

![part22_max_solved_size_by_planner](part22_max_solved_size_by_planner.png)

![part22_cost_at_max_solved_size_by_planner](part22_cost_at_max_solved_size_by_planner.png)

![part22_time_vs_cost_scatter](part22_time_vs_cost_scatter.png)

## [ERROR_DETAILS]

### E001
```text
/home/alex/.planutils/packages/metric-ff/run: line 44: $PROBLEM.plan: ambiguous redirect | usage of ff: | OPTIONS   DESCRIPTIONS | -p <str>    Path for operator and fact file | -o <str>    Operator file name | -f <str>    Fact file name
```

### E002
```text
fast-downward.py: error: translator needs one or two PDDL input files | usage: fast-downward.py [-h] [-v] [--show-aliases] [--run-all] [--translate] | [--search] | [--translate-time-limit TRANSLATE_TIME_LIMIT] | [--translate-memory-limit TRANSLATE_MEMORY_LIMIT] | [--search-time-limit SEARCH_TIME_LIMIT]
```
