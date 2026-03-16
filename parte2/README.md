# Parte 2 - Guía de ejecución y debugging

Este README documenta **todos los scripts Python de `parte2`** para que cualquier desarrollador pueda:
- ejecutarlos con comandos reproducibles,
- entender su flujo interno,
- localizar fallos rápidamente.

## 1) Scripts disponibles

| Script | Objetivo principal | Salidas principales |
|---|---|---|
| `generate-problem.py` | Generar instancias PDDL de ejercicio 2.1/2.2 | `drone_problem_*.pddl` |
| `benchmark_pyperplan_part21.py` | Benchmark pyperplan para ejercicio 2.1 (tablas 2.1.1, 2.1.2, 2.1.3) | CSV + TXT + MD + PNG |
| `benchmark_ff_graph_part21.py` | Benchmark FF para ejercicio 2.1 | CSV + TXT + MD + PNG |
| `benchmark_cost_planners_part22.py` | Benchmark de planificadores con coste para ejercicio 2.2 | CSV global/familias + resúmenes + TXT + MD + PNG |

## 2) Requisitos

- Python 3.10+
- `matplotlib` para imágenes (`pip install matplotlib`)
- Herramientas de planificación en PATH (según script):
  - `pyperplan` (vía planutils o binario)
  - `ff` / `metric-ff`
  - `downward` / `fast-downward.py`

## 3) Preparación rápida

```bash
cd Planning-practice/parte2
python3 generate-problem.py --help
python3 benchmark_pyperplan_part21.py --help
python3 benchmark_ff_graph_part21.py --help
python3 benchmark_cost_planners_part22.py --help
```

## 4) `generate-problem.py`

### Qué hace

Genera problemas PDDL del dominio de parte 2:
- `--exercise 1`: versión transportadores sin coste total.
- `--exercise 2`: versión con costes (`total-cost`, `fly-cost`, métrica de minimización).

### Cómo lo hace (para debugging)

1. Valida límites (`goals <= crates`, etc.).
2. Genera coordenadas aleatorias de localizaciones.
3. Construye necesidades de personas y cajas.
4. Escribe objetos/init/goal y, en ejercicio 2, funciones de coste y métrica.

Si una instancia no se genera, suele deberse a parámetros inválidos.

### Comandos útiles

```bash
# Ejercicio 2.1 (sin costes)
python3 generate-problem.py -d 1 -r 1 -l 4 -p 4 -c 4 -g 4 -a 4 --exercise 1

# Ejercicio 2.2 (con costes)
python3 generate-problem.py -d 1 -r 1 -l 6 -p 6 -c 6 -g 6 -a 4 --exercise 2

# Ejercicio 2.2 reproducible con semilla
python3 generate-problem.py -d 1 -r 1 -l 8 -p 8 -c 8 -g 8 -a 4 --exercise 2 --seed 42
```

## 5) `benchmark_pyperplan_part21.py`

### Qué hace

Automatiza el benchmark de la parte 2.1 en tres bloques:
- 2.1.1: comparación de algoritmos base por tamaño.
- 2.1.2: combinaciones search/heuristic en un tamaño ancla.
- 2.1.3: comparativa de combinaciones óptimas en tamaño ancla.

Genera:
- `results/benchmark_pyperplan_part21_all.csv`
- `results/benchmark_pyperplan_part21_211.csv`
- `results/benchmark_pyperplan_part21_212.csv`
- `results/benchmark_pyperplan_part21_213.csv`
- `results/benchmark_pyperplan_part21.txt`
- `results/benchmark_pyperplan_part21.md`
- `results/part21_1_runtime_vs_size.png`
- `results/part21_2_runtime_by_combo.png`
- `results/part21_3_optimal_runtime.png`

### Cómo lo hace (para debugging)

1. Genera instancias o usa `--problem-files`.
2. Resuelve aliases de pyperplan consultando `--help`.
3. Ejecuta cada configuración con timeout.
4. Parsea tiempo y longitud de plan de la salida.
5. Clasifica estado: `solved`, `unsolved`, `timeout`, `unsupported`, `error`.
6. Exporta tablas y gráficos.

### Comandos útiles

```bash
# Ejecución estándar
python3 benchmark_pyperplan_part21.py --timeout 60

# Barrido corto para test rápido
python3 benchmark_pyperplan_part21.py --min-size 2 --max-size 8 --step 2 --timeout 30

# Usar problemas ya existentes (sin generar)
python3 benchmark_pyperplan_part21.py \
  --problem-files results/problems/drone_problem_ex1_d1_r1_l2_p2_c2_g2_a4.pddl \
                  results/problems/drone_problem_ex1_d1_r1_l4_p4_c4_g4_a4.pddl
```

### Fallos típicos y diagnóstico

- `unsupported`: alias no disponible en la instalación actual.
- `timeout`: subir `--timeout` o bajar rango.
- `matplotlib` ausente: instala dependencia o usa `--allow-basic-plots`.
- `error_excerpt` en CSV/MD/TXT contiene la pista principal del fallo.

## 6) `benchmark_ff_graph_part21.py`

### Qué hace

Benchmark de FF para 2.1 y generación de informe técnico.

Genera por defecto (según rango):
- `benchmark_ff_part21_<min>_to_<max>.csv`
- `benchmark_ff_part21_<min>_to_<max>.txt`
- `benchmark_ff_part21_<min>_to_<max>.md`
- `benchmark_ff_part21_<min>_to_<max>.png`

### Cómo lo hace (para debugging)

1. Genera instancias o usa `--problem-files`.
2. Ejecuta FF por `planutils run ff` y fallback `ff` binario.
3. Parsea tiempo de FF y pasos de plan.
4. Clasifica estados y exporta tablas/gráficas.

### Comandos útiles

```bash
# Ejecución estándar
python3 benchmark_ff_graph_part21.py --timeout 60

# Tamaños explícitos
python3 benchmark_ff_graph_part21.py --sizes 2,4,6,8,10 --timeout 45

# Forzar nombres de salida
python3 benchmark_ff_graph_part21.py \
  --min-size 2 --max-size 10 --step 2 \
  --csv-out ff_custom.csv --txt-out ff_custom.txt --md-out ff_custom.md --png-out ff_custom.png
```

### Fallos típicos y diagnóstico

- `solver_backend=none`: ni `planutils ff` ni `ff` están disponibles.
- `gen_error`: revisar parámetros de generación.
- Si hay PNG sin render adecuado, comprobar `matplotlib`.

## 7) `benchmark_cost_planners_part22.py`

### Qué hace

Benchmark de ejercicio 2.2 con planners de coste:
- `metric-ff`
- `downward` satisficing (`lama-first`, `seq-sat-fdss-2`, `seq-sat-fd-autotune-2`)
- `downward` óptimos (`seq-opt-lmcut`, `seq-opt-bjolp`, `seq-opt-fdss-2`)

Genera:
- `benchmark_cost_planners_part22_all.csv`
- `benchmark_cost_planners_part22_sat.csv`
- `benchmark_cost_planners_part22_opt.csv`
- `benchmark_cost_planners_part22_summary_sat.csv`
- `benchmark_cost_planners_part22_summary_opt.csv`
- `benchmark_cost_planners_part22_summary_global.csv`
- `benchmark_cost_planners_part22.txt`
- `benchmark_cost_planners_part22.md`
- `part22_max_solved_size_by_planner.png`
- `part22_cost_at_max_solved_size_by_planner.png`
- `part22_time_vs_cost_scatter.png`

### Cómo lo hace (para debugging)

1. Genera problemas de ejercicio 2 o usa `--problem-files`.
2. Ejecuta cada planner por tamaño.
3. En `downward` pasa `--overall-time-limit` (importante para FDSS).
4. Parsea `plan_cost` y `plan_length` cuando sea posible.
5. Crea resúmenes por familia y globales.

### Comandos útiles

```bash
# Ejecución estándar parte 2.2
python3 benchmark_cost_planners_part22.py --timeout 60

# Barrido controlado
python3 benchmark_cost_planners_part22.py --min-size 2 --max-size 12 --step 2 --timeout 60

# Tamaños explícitos y dominio/generador custom
python3 benchmark_cost_planners_part22.py \
  --sizes 2,4,6,8 \
  --domain dronedomain2.pddl \
  --generator generate-problem.py \
  --timeout 60
```

### Fallos típicos y diagnóstico

- `unsupported`: planner/alias no instalado.
- FDSS sin límite de tiempo puede fallar; aquí ya se fuerza `--overall-time-limit`.
- `plan_cost`/`plan_length` vacíos: salida no parseable para ese backend.
- Revisar `error_excerpt` en CSV y sección `[ERROR_DETAILS]` del MD.

## 8) Checklist de debugging rápido

```bash
# 1) Ver si scripts cargan
python3 benchmark_cost_planners_part22.py --help

# 2) Test corto
python3 benchmark_cost_planners_part22.py --sizes 2 --timeout 10

# 3) Revisar estados
cat results/benchmark_cost_planners_part22_all.csv

# 4) Revisar detalles de error
cat results/benchmark_cost_planners_part22.md
```
