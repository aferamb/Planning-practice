# Practice 1 - Part 1

Classic Planning with PDDL (Automated Planning, UAH 2025-26)

## 1. Folder Structure

```text
parte1/
|- dronedomain.pddl
|- droneproblem1.pddl
|- droneproblem2.pddl
|- domain.pddl                # alias copy of dronedomain.pddl
|- problem1.pddl              # alias copy of droneproblem1.pddl
|- problem2.pddl              # alias copy of droneproblem2.pddl
|- generator_core.py          # shared generation logic (simple, commented)
|- generate-problem.py        # generator entry point (assignment-style name)
|- generate_problem_little_inproved.py  # alternate entry point (same behavior)
|- benchmark_ff_graph.py      # benchmark + CSV + high-definition SVG plot
|- results/                   # generated benchmark outputs
`- README.md
```

## 2. Exercise 1.1 - Domain and Hand-Crafted Problems

### 2.1 Domain Overview

The domain models emergency logistics with:
- drones
- crates with content types (food/medicine)
- persons at locations
- two drone arms (left/right)

Main predicates used in this domain:
- `drone-at`
- `person-at`
- `crate-at`
- `crate-has`
- `person-has`
- `carrying-left`, `carrying-right`
- `arm-free-left`, `arm-free-right`

Main actions:
- `fly`
- `pick-up-left`, `pick-up-right`
- `deliver-left`, `deliver-right`

### 2.2 Hand-Crafted Problems

- `droneproblem1.pddl` / `problem1.pddl`
- `droneproblem2.pddl` / `problem2.pddl`

Both are compatible with `dronedomain.pddl` and can be solved with FF.

### 2.3 How to Test Exercise 1.1

```bash
cd parte1
planutils run ff -- dronedomain.pddl droneproblem1.pddl
planutils run ff -- dronedomain.pddl droneproblem2.pddl
```

Or using alias files:

```bash
planutils run ff -- domain.pddl problem1.pddl
planutils run ff -- domain.pddl problem2.pddl
```

## 3. Exercise 1.2 - Python Problem Generator and Benchmark

### 3.1 Simplified Python Codebase

All Python scripts were simplified and separated into clear parts:

- `generator_core.py`
  - validation
  - object creation
  - random crate-content distribution
  - random goal generation
  - PDDL writing

- `generate-problem.py`
  - small CLI wrapper around `generator_core.py`

- `generate_problem_little_inproved.py`
  - same simplified behavior as the previous script

- `benchmark_ff_graph.py`
  - run FF for increasing complexities
  - save CSV + high-definition SVG in `results/`
  - try to display the SVG after execution

### 3.2 Generate One Problem

```bash
cd parte1
python3 generate-problem.py -d 1 -r 0 -l 10 -p 10 -c 10 -g 10 --seed 10 --out-dir results/problems
```

### 3.3 Run the Benchmark (up to complexity 60)

Default behavior already runs from complexity 2 to 60:

```bash
cd parte1
python3 benchmark_ff_graph.py --domain dronedomain.pddl --generator generate-problem.py
```

Equivalent explicit command:

```bash
python3 benchmark_ff_graph.py \
  --min-size 2 \
  --max-size 60 \
  --step 1 \
  --timeout 60 \
  --domain dronedomain.pddl \
  --generator generate-problem.py \
  --results-dir results
```

Legacy compatible command style (still supported):

```bash
python3 benchmark_ff_graph.py \
  --sizes 2,3,5,7,10,15 \
  --timeout 60 \
  --domain dronedomain.pddl \
  --generator generate-problem.py \
  --csv-out ff_benchmark_results.csv \
  --svg-out ff_benchmark_plot.svg
```

Another example (range mode, stop at 60):

```bash
python3 benchmark_ff_graph.py \
  --min-size 2 \
  --max-size 60 \
  --step 2 \
  --timeout 60 \
  --domain dronedomain.pddl \
  --generator generate-problem.py \
  --results-dir results
```

### 3.4 Benchmark Outputs

The benchmark stores everything inside `results/`:

- `results/problems/*.pddl` (generated instances)
- `results/benchmark_ff_<min>_to_<max>.csv`
- `results/benchmark_ff_<min>_to_<max>.svg`

The script attempts to open the SVG automatically when finished.
If auto-open is unavailable in your environment, it prints the file path.

### 3.5 Plot Quality / Readability

The SVG is high definition and includes:
- one X-axis tick per tested complexity value
- dense Y-axis segmentation (1 second granularity, emphasized each 5s)
- per-point labels (time or timeout)
- explicit timeout markers

This makes every complexity point and its runtime clearly visible.

### 3.6 Full Benchmark Arguments

`benchmark_ff_graph.py` supports these arguments:

| Argument | Type | Default | Description |
|---|---|---|---|
| `--min-size` | int | `2` | Minimum complexity (`l=p=c=g`) when using range mode. |
| `--max-size` | int | `60` | Maximum complexity (`l=p=c=g`) when using range mode. |
| `--step` | int | `1` | Step between complexities in range mode. |
| `--sizes` | csv string | `None` | Legacy mode list, e.g. `2,3,5,7,10,15`. Overrides range mode. |
| `--timeout` | int | `60` | Time limit (seconds) per FF run. |
| `--domain` | path | `dronedomain.pddl` | Domain PDDL file. |
| `--generator` | path | `generate-problem.py` | Generator script to produce problems. |
| `--results-dir` | path | `results` | Base output folder for CSV/SVG and generated problems. |
| `--csv-out` | path | `None` | Optional CSV output name/path. If relative, it is saved under `results-dir`. |
| `--svg-out` | path | `None` | Optional SVG output name/path. If relative, it is saved under `results-dir`. |
| `--seed-base` | int | `0` | Base seed. Use `-1` to disable deterministic seeds. |
| `--no-show` | flag | `False` | If set, do not auto-open SVG at the end. |

Notes:
- If you use `--sizes`, you can keep your old command style.
- With `--csv-out ff.csv` and `--svg-out plot.svg`, files are saved as `results/ff.csv` and `results/plot.svg`.

### 3.7 Troubleshooting `error(1)` in benchmark output

If you see lines like `status=error(1)`, run these checks:

```bash
# 1) Check FF wrapper availability
planutils run ff --

# 2) Generate one tiny problem manually
python3 generate-problem.py -d 1 -r 0 -l 2 -p 2 -c 2 -g 2

# 3) Solve it directly
planutils run ff -- dronedomain.pddl drone_problem_d1_r0_l2_p2_c2_g2_ct2.pddl
```

In the updated benchmark script, failed runs print an `error detail:` line with
the first relevant output lines from the solver command.

## 4. Exercise 1.3 - Search/Heuristic Comparison (pyperplan)

You can run pyperplan experiments with commands like:

```bash
python3 -m pyperplan -s bfs dronedomain.pddl droneproblem2.pddl
python3 -m pyperplan -s astar -H hmax dronedomain.pddl droneproblem2.pddl
python3 -m pyperplan -s gbfs -H hff dronedomain.pddl droneproblem2.pddl
```

To enforce 1-minute limits in Linux/WSL:

```bash
timeout 60 python3 -m pyperplan -s astar -H hmax dronedomain.pddl <problem.pddl>
```

## 5. Quick End-to-End Example

```bash
cd parte1

# 1) Generate one instance
python3 generate-problem.py -d 1 -r 0 -l 12 -p 12 -c 12 -g 12 --seed 12 --out-dir results/problems

# 2) Solve with FF
planutils run ff -- dronedomain.pddl results/problems/drone_problem_d1_r0_l12_p12_c12_g12_ct2.pddl

# 3) Run benchmark up to 60
python3 benchmark_ff_graph.py --domain dronedomain.pddl --generator generate-problem.py
```

## 6. Notes

- `.plan` files are ignored via `.gitignore` to keep the repository clean.
- If your system cannot auto-open SVG files, open the generated SVG manually from the printed path.
