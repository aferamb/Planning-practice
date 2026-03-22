# Parte 3 - Guía de ejecución y debugging

Este README documenta **todos los scripts Python de `parte3`** para operación y depuración.

Incluye:
- ejecución por terminal con diferentes parámetros,
- explicación funcional y técnica de cada script,
- pautas para detectar comportamientos incorrectos.

## 1) Scripts disponibles

| Script | Objetivo principal | Salidas principales |
|---|---|---|
| `generate-problem.py` | Generar instancias temporales del dominio con `durative-actions` | `drone_problem_*.pddl` |
| `benchmark_lpgtd_part3.py` | Benchmark legacy con LPG-TD (`quality` vs `speed`) | CSV + TXT + MD + PNG |
| `benchmark_optic_part3.py` | Benchmark V2 con Optic (anytime: primera vs última solución) | CSV + TXT + MD + PNG |

## 2) Requisitos

- Python 3.10+
- `matplotlib` para gráficos (`pip install matplotlib`)
- Planificadores en PATH según script:
  - LPG-TD (`lpg-td`) para script legacy
  - Optic (`optic`) para script V2

## 3) Preparación rápida

```bash
cd Planning-practice/parte3
python3 generate-problem.py --help
python3 benchmark_lpgtd_part3.py --help
python3 benchmark_optic_part3.py --help
```

## 4) `generate-problem.py`

### Qué hace

Genera problemas temporales para el dominio `ubermedics-carriers-temporal`.

### Cómo lo hace (para debugging)

1. Valida parámetros (`goals`, `crates`, etc.).
2. Genera localizaciones y costes de vuelo (`fly-cost`) aleatorios.
3. Escribe estado inicial con drones, carriers y numeración de carga.
4. Escribe meta en función de necesidades de personas.

### Comandos útiles

```bash
# Caso mínimo válido temporal
python3 generate-problem.py -d 1 -r 1 -l 2 -p 2 -c 2 -g 2 -a 4

# Caso medio
python3 generate-problem.py -d 3 -r 3 -l 6 -p 6 -c 6 -g 6 -a 4

# Estrés controlado
python3 generate-problem.py -d 5 -r 5 -l 8 -p 8 -c 8 -g 8 -a 4
```

### Fallos típicos y diagnóstico

- `Cannot have more goals than crates`: baja `-g` o sube `-c`.
- `Too many goals ...`: revisa combinación `persons`, `goals`, tipos de contenido.

## 5) `benchmark_lpgtd_part3.py` (legacy)

### Qué hace

Benchmark histórico con LPG-TD:
- busca máximo tamaño resuelto en `quality` por nº de drones/carriers,
- relanza el caso máximo en `speed`,
- compara tiempo, pasos y makespan.

Salidas por defecto en `results/`:
- `benchmark_lpgtd_part3_quality_sweep.csv`
- `benchmark_lpgtd_part3_comparison.csv`
- `benchmark_lpgtd_part3_summary.csv`
- `benchmark_lpgtd_part3.txt`
- `benchmark_lpgtd_part3.md`
- `part3_max_quality_size_by_drones.png`
- `part3_quality_vs_speed_processing_time.png`
- `part3_quality_vs_speed_plan_steps.png`
- `part3_quality_vs_speed_makespan.png`

### Cómo lo hace (para debugging)

1. Genera problemas por tamaño (`l=p=c=g`).
2. Ejecuta LPG-TD por timeout configurado.
3. Intenta parsear planes desde salida y ficheros `.SOL`.
4. Clasifica estado (`solved`, `timeout`, `unsupported`, `error`, ...).
5. Exporta resumen comparativo quality/speed.

### Comandos útiles

```bash
# Ejecución estándar
python3 benchmark_lpgtd_part3.py --timeout 60

# Rango reducido para test rápido
python3 benchmark_lpgtd_part3.py --min-drones 1 --max-drones 3 --min-size 2 --max-size 6 --timeout 30

# Ajuste de semilla LPG y criterio de parada
python3 benchmark_lpgtd_part3.py \
  --lpg-seed 42 \
  --stop-after-fails 2 \
  --timeout 60
```

### Fallos típicos y diagnóstico

- `unsupported`: `lpg-td` no disponible.
- Salida vacía de plan: revisar parseo de `.SOL` y el contenido en `results/plans`.
- Si no hay gráficos: revisar instalación de `matplotlib`.

## 6) `benchmark_optic_part3.py` (V2 oficial)

### Qué hace

Benchmark de la versión V2 con Optic (anytime):
- barrido por drones/carriers,
- búsqueda del tamaño máximo resuelto en ventana de 60s,
- extracción de **primera** y **última** solución del run (pasos y makespan).

Salidas por defecto en `results/`:
- `benchmark_optic_part3_sweep.csv`
- `benchmark_optic_part3_summary.csv`
- `benchmark_optic_part3.txt`
- `benchmark_optic_part3.md`
- `part3_optic_max_solved_size_by_drones.png`
- `part3_optic_first_vs_last_steps.png`
- `part3_optic_first_vs_last_makespan.png`

### Cómo lo hace (para debugging)

1. Genera problemas por tamaño y drones.
2. Ejecuta Optic con timeout de proceso.
3. Parsea bloques temporales (`t: (action) [dur]`) de salida/ficheros auxiliares.
4. Toma el primer bloque como primera solución y el último como última solución.
5. Resume por drones el mayor tamaño resuelto.

### Comandos útiles

Sí. Si en tu entorno planutils run optic funciona normal, el comando simple es este, ejecutándolo desde Planning-practice/parte3:
```bash
cd /mnt/c/Users/05jan/Desktop/Tareas/Uni/3_Curso/2_cuatri/Planificacion_automatica/Lab/PL1/Planning-practice/parte3                                                                                                                                                          
planutils run optic -- dronedomain.pddl drone_problem_d1_r1_l2_p2_c2_g2_a2.pddl                                                                                                                                                                                              
```
Y para el segundo problema:                                                                                                                                                                                                                                                  
```bash
cd /mnt/c/Users/05jan/Desktop/Tareas/Uni/3_Curso/2_cuatri/Planificacion_automatica/Lab/PL1/Planning-practice/parte3                                                                                                                                                          
planutils run optic -- dronedomain.pddl drone_problem_d2_r2_l4_p4_c6_g4_a4.pddl                                                                                                                                                                                              
```
Si quieres guardar la salida en fichero:                                                                                                                                                                                                                                     
```bash
planutils run optic -- dronedomain.pddl drone_problem_d1_r1_l2_p2_c2_g2_a2.pddl > drone_problem_d1_r1_l2_p2_c2_g2_a2.optic.stdout.txt                                                                                                                                        
planutils run optic -- dronedomain.pddl drone_problem_d2_r2_l4_p4_c6_g4_a4.pddl > drone_problem_d2_r2_l4_p4_c6_g4_a4.optic.stdout.txt                                                                                                                                        
```
Y si quieres sacar solo el plan final, lo normal es copiar manualmente el último bloque de acciones temporales que imprime OPTIC.                                                                                                                                            


```bash
# Ejecución estándar V2
python3 benchmark_optic_part3.py --timeout 60

# Barrido corto de validación
python3 benchmark_optic_part3.py --min-drones 1 --max-drones 2 --min-size 2 --max-size 5 --timeout 20

# Control fino de rango y parada
python3 benchmark_optic_part3.py \
  --min-drones 1 --max-drones 5 \
  --min-size 2 --max-size 12 --step 1 \
  --stop-after-fails 2 \
  --timeout 60
```

### Fallos típicos y diagnóstico

- `unsupported`: `optic` no está instalado en el entorno.
- `unsolved` o `timeout` con tamaño alto: reduce `max-size` o sube timeout.
- Sin `first/last` parseado: inspeccionar `error_excerpt` y la salida de planner capturada.

## 7) Checklist de debugging rápido

```bash
# 1) Ayuda de scripts
python3 benchmark_optic_part3.py --help

# 2) Smoke test mínimo
python3 benchmark_optic_part3.py --min-drones 1 --max-drones 1 --min-size 2 --max-size 2 --timeout 10

# 3) Revisar resultados
cat results/benchmark_optic_part3_summary.csv
cat results/benchmark_optic_part3.md
```

## 8) Nota de convivencia entre scripts

- `benchmark_lpgtd_part3.py` se mantiene por compatibilidad y comparación histórica.
- `benchmark_optic_part3.py` es el flujo alineado con el enunciado V2.
- Ambos pueden coexistir en `parte3` sin interferencia, usando `--results-dir` distinto si quieres separar runs.
