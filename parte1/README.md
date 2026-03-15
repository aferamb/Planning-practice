# Practice 1 - Part 1

Classic Planning with PDDL (Automated Planning, UAH 2025-26)

## 1. Folder Structure

```text
parte1/
|- dronedomain.pddl
|- droneproblem1.pddl
|- droneproblem2.pddl
|- generate-problem.py
|- benchmark_ff_graph.py
|- benchmark_pyperplan_part13.py
|- problems/
|- results/
`- README.md
```

## 2. Requirements

- Python 3.10+ (or equivalent)
- `planutils` installed in your environment
- FF planner available through `planutils run ff`
- pyperplan available through `planutils run pyperplan`
- `matplotlib` for readable PNG plots in part 1.3 (titles, axes, legends)

Quick checks:

```bash
planutils run ff --
planutils run pyperplan -- --help
```

## 3. Exercise 1.1 - Domain and Hand-Crafted Problems

Run:

```bash
cd parte1
planutils run ff -- dronedomain.pddl droneproblem1.pddl
planutils run ff -- dronedomain.pddl droneproblem2.pddl
```

## 4. Exercise 1.2 - Generator + FF Benchmark

### 4.1 Generate One Problem

```bash
cd parte1
python3 generate-problem.py -d 1 -r 0 -l 10 -p 10 -c 10 -g 10
```

### 4.2 FF Benchmark Script

Script: `benchmark_ff_graph.py`

Main behavior:
- Generates instances with `l=p=c=g`
- Runs FF for each size
- Saves CSV + SVG under `results/`

### 4.3 Run FF Benchmark (Normal CLI)

```bash
cd parte1
python3 benchmark_ff_graph.py \
  --min-size 2 \
  --max-size 60 \
  --step 1 \
  --timeout 60 \
  --domain dronedomain.pddl \
  --generator generate-problem.py \
  --results-dir results
```

Legacy list mode:

```bash
python3 benchmark_ff_graph.py --sizes 2,3,5,7,10,15 --timeout 60
```

### 4.4 Run FF Benchmark (Interactive Mode)

If you run the script with no CLI arguments, it prompts:

```text
¿Qué parámetros quieres meter?
```

Use it like this:

```bash
python3 benchmark_ff_graph.py
```

Then type, for example:

```text
--min-size 2 --max-size 30 --step 2 --timeout 45 --results-dir results
```

Or press Enter to run with defaults.

### 4.5 FF Benchmark Outputs

- `results/problems/*.pddl`
- `results/benchmark_ff_<min>_to_<max>.csv`
- `results/benchmark_ff_<min>_to_<max>.svg`

## 5. Exercise 1.3 - pyperplan Benchmark (Part 1.3)

Script: `benchmark_pyperplan_part13.py`

Main behavior:
- Runs all benchmark blocks for exercise 1.3
- Uses `planutils run pyperplan -- ...`
- Produces one text report, multiple CSV files, and PNG charts

### 5.1 Run pyperplan Benchmark (Normal CLI)

```bash
cd parte1
python3 benchmark_pyperplan_part13.py \
  --min-size 2 \
  --max-size 40 \
  --step 2 \
  --timeout 60 \
  --domain dronedomain.pddl \
  --generator generate-problem.py \
  --results-dir results
```

### 5.2 Run pyperplan Benchmark Using Existing PDDL Files

```bash
python3 benchmark_pyperplan_part13.py \
  --timeout 60 \
  --domain dronedomain.pddl \
  --results-dir results \
  --problem-files \
  problems/drone_problem_d1_r0_l10_p10_c10_g10_ct2.pddl \
  problems/drone_problem_d1_r0_l20_p20_c20_g20_ct2.pddl
```

### 5.3 Run pyperplan Benchmark (Interactive Mode)

Run with no arguments:

```bash
python3 benchmark_pyperplan_part13.py
```

Then type a full argument line, for example:

```text
--min-size 2 --max-size 24 --step 2 --timeout 60 --results-dir results
```

Or press Enter to run with defaults.

### 5.4 pyperplan Benchmark Outputs

- `results/benchmark_pyperplan_part13.txt`
- `results/benchmark_pyperplan_part13.md` (human-readable Markdown report)
- `results/benchmark_pyperplan_part13_all.csv`
- `results/benchmark_pyperplan_part13_131.csv`
- `results/benchmark_pyperplan_part13_132.csv`
- `results/benchmark_pyperplan_part13_133.csv`
- `results/part13_1_runtime_vs_size.png`
- `results/part13_2_runtime_by_combo.png`
- `results/part13_3_optimal_runtime.png`

## 6. Argument Reference

### 6.1 `benchmark_ff_graph.py`

| Argument | Default | Description |
|---|---|---|
| `--min-size` | `2` | Minimum complexity (`l=p=c=g`) in range mode |
| `--max-size` | `60` | Maximum complexity in range mode |
| `--step` | `1` | Step in range mode |
| `--sizes` | `None` | Legacy CSV list, e.g. `2,3,5,7` |
| `--timeout` | `60` | Timeout per instance (seconds) |
| `--domain` | `dronedomain.pddl` | Domain PDDL path |
| `--generator` | `generate-problem.py` | Generator script path |
| `--results-dir` | `results` | Output directory |
| `--csv-out` | `None` | Optional CSV output path/name |
| `--svg-out` | `None` | Optional SVG output path/name |
| `--no-show` | `False` | Disable auto-open for SVG |
| `--seed-base` | `0` | Seed base (`-1` to disable deterministic seed mode) |

### 6.2 `benchmark_pyperplan_part13.py`

| Argument | Default | Description |
|---|---|---|
| `--min-size` | `2` | Minimum size (`l=p=c=g`) |
| `--max-size` | `40` | Maximum size (`l=p=c=g`) |
| `--step` | `2` | Size increment |
| `--timeout` | `60` | Timeout per run (seconds) |
| `--domain` | `dronedomain.pddl` | Domain PDDL path |
| `--generator` | `generate-problem.py` | Generator script path (used when `--problem-files` is not given) |
| `--results-dir` | `results` | Output directory |
| `--allow-basic-plots` | `False` | Allow unlabeled basic PNG fallback if matplotlib is unavailable |
| `--problem-files` | `None` | Existing PDDL files (skip generation) |

## 7. Quick Run Examples

```bash
cd parte1

# FF benchmark (interactive)
python3 benchmark_ff_graph.py

# pyperplan benchmark part 1.3 (interactive)
python3 benchmark_pyperplan_part13.py

# FF benchmark (explicit CLI)
python3 benchmark_ff_graph.py --min-size 2 --max-size 20 --step 2 --timeout 60

# pyperplan benchmark part 1.3 (explicit CLI)
python3 benchmark_pyperplan_part13.py --min-size 2 --max-size 20 --step 2 --timeout 60
```
