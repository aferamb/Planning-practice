# Practica 1 Parte 1 — Planificación Clásica con PDDL

**Automated Planning — Universidad de Alcalá — Curso 2025-26**

---

## Índice

1. [Estructura de ficheros](#1-estructura-de-ficheros)
2. [Ejercicio 1.1 — Dominio PDDL y problemas manuales](#2-ejercicio-11--dominio-pddl-y-problemas-manuales)
3. [Ejercicio 1.2 — Generador de problemas en Python](#3-ejercicio-12--generador-de-problemas-en-python)
4. [Ejercicio 1.3 — Comparativa de algoritmos y heurísticas](#4-ejercicio-13--comparativa-de-algoritmos-y-heurísticas)
5. [Requisitos del entorno](#5-requisitos-del-entorno)
6. [Cómo ejecutarlo todo paso a paso](#6-cómo-ejecutarlo-todo-paso-a-paso)

---

## 1. Estructura de ficheros

```
parte1/
├── domain.pddl           # Dominio PDDL (STRIPS + :typing) — Ejercicio 1.1
├── problem1.pddl         # Problema pequeño: 1 persona, 1 caja — Ejercicio 1.1
├── problem2.pddl         # Problema mediano: 2 personas, 3 cajas — Ejercicio 1.1
├── generate-problem.py   # Generador de problemas en Python — Ejercicio 1.2
└── README.md             # Este fichero
```

---

## 2. Ejercicio 1.1 — Dominio PDDL y problemas manuales

### 2.1 Descripción del dominio

El dominio modela un sistema de atención de emergencias en el que un **dron** reparte **cajas** con suministros a **personas heridas** en distintas localizaciones.

#### Restricciones del enunciado respetadas

| Restricción | Solución adoptada |
|-------------|-------------------|
| No precondiciones negativas | `at-crate` se elimina al recoger → recoger sólo requiere que `at-crate` sea verdadero |
| No metas negativas | Todas las metas son conjunciones positivas de `has-content` y `at-drone` |
| `:typing` activado | Sí, usando `:requirements :strips :typing` |
| Sin comentarios en el PDDL | Los ficheros `.pddl` no contienen comentarios de `;` |
| Espacios alrededor de `-` en tipos | Comprobado: `?d - drone`, `?c - crate`, etc. |
| Contenido de cajas genérico | `food` y `medicine` son **objetos** del tipo `contents`, no predicados especiales |

#### Tipos declarados

```pddl
(:types drone location crate contents person)
```

- **`drone`** — El dron que reparte cajas.
- **`location`** — Cualquier localización, incluyendo el depósito.
- **`crate`** — Una caja con un contenido determinado.
- **`contents`** — El tipo de contenido de una caja (`food`, `medicine`, …). Definido como **objeto** del problema para que añadir nuevos tipos no requiera modificar el dominio.
- **`person`** — Una persona herida que puede necesitar cajas.

#### Predicados

| Predicado | Significado |
|-----------|-------------|
| `(at-drone ?d ?l)` | El dron `?d` está en la localización `?l` |
| `(at-crate ?c ?l)` | La caja `?c` está en la localización `?l` (en el suelo) |
| `(at-person ?p ?l)` | La persona `?p` está en la localización `?l` |
| `(arm1-free ?d)` | El brazo 1 del dron `?d` está libre |
| `(arm2-free ?d)` | El brazo 2 del dron `?d` está libre |
| `(holding-arm1 ?d ?c)` | El dron `?d` lleva la caja `?c` en el brazo 1 |
| `(holding-arm2 ?d ?c)` | El dron `?d` lleva la caja `?c` en el brazo 2 |
| `(crate-contents ?c ?ct)` | La caja `?c` contiene el tipo `?ct` |
| `(has-content ?p ?ct)` | La persona `?p` ya tiene el suministro de tipo `?ct` |

> **¿Por qué `arm1-free`/`arm2-free` en lugar de negaciones?**
> El enunciado prohíbe precondiciones negativas. Para saber si un brazo está ocupado
> usamos un predicado positivo `arm-free`. Cuando el dron recoge una caja, ese
> predicado se elimina (efecto negativo en acción, permitido). Cuando entrega la caja,
> el predicado se reinstala.

#### Acciones

##### `pick-up-arm1` / `pick-up-arm2`
Recoger una caja del suelo con el brazo 1 (o 2).

```
Precondiciones:
  at-drone en la misma localización que la caja
  at-crate de la caja en esa localización
  armX-free

Efectos:
  +holding-armX(dron, caja)
  -armX-free(dron)
  -at-crate(caja, localización)     ← la caja deja de estar en el suelo
```

Que `at-crate` se elimine al recoger es la clave para evitar precondiciones negativas:
el planificador no necesita comprobar `(not (holding ?c))` porque la presencia de
`at-crate` ya garantiza que la caja está en el suelo.

##### `fly`
Volar de una localización a otra.

```
Precondiciones:  at-drone en ?from
Efectos:         +at-drone en ?to,  -at-drone en ?from
```

No hay restricciones de rutas: el dron puede volar directamente entre cualquier par.

##### `deliver-arm1` / `deliver-arm2`
Entregar la caja de un brazo a una persona que esté en la misma localización.

```
Precondiciones:
  at-drone en la misma localización que la persona
  at-person de la persona en esa localización
  holding-armX(dron, caja)
  crate-contents(caja, tipo)

Efectos:
  +has-content(persona, tipo)
  +armX-free(dron)
  -holding-armX(dron, caja)
```

La caja desaparece (ya no está en ningún sitio, queda implícitamente consumida),
y la persona queda satisfecha para ese tipo de contenido.

---

### 2.2 Problema 1 — 1 persona, 1 caja

**Fichero:** `problem1.pddl`

| Elemento | Valor |
|----------|-------|
| Drones | `drone1` en `depot` |
| Personas | `person1` en `loc1` |
| Cajas | `crate1` (comida) en `depot` |
| Objetivo | `person1` tiene comida y `drone1` vuelve al depósito |

**Plan óptimo esperado (5 pasos):**
```
1. pick-up-arm1 drone1 crate1 depot
2. fly drone1 depot loc1
3. deliver-arm1 drone1 crate1 person1 loc1 food
4. fly drone1 loc1 depot
```

---

### 2.3 Problema 2 — 2 personas, 3 cajas

**Fichero:** `problem2.pddl`

| Elemento | Valor |
|----------|-------|
| Drones | `drone1` en `depot` |
| Personas | `person1` en `loc1`, `person2` en `loc2` |
| Cajas | `crate1`(comida), `crate2`(medicina), `crate3`(comida) — todas en `depot` |
| Objetivo | `person1` tiene comida, `person2` tiene medicina, `drone1` en `depot` |

**Plan eficiente esperado (aprovechando los dos brazos):**
```
1. pick-up-arm1 drone1 crate1 depot       ; coger comida en brazo 1
2. pick-up-arm2 drone1 crate2 depot       ; coger medicina en brazo 2
3. fly drone1 depot loc1
4. deliver-arm1 drone1 crate1 person1 loc1 food
5. fly drone1 loc1 loc2
6. deliver-arm2 drone1 crate2 person2 loc2 medicine
7. fly drone1 loc2 depot
```

---

## 3. Ejercicio 1.2 — Generador de problemas en Python

### 3.1 Qué hace el generador

El fichero `generate-problem.py` genera instancias de problema PDDL aleatoriamente a partir de parámetros dados por línea de comandos. El script:

1. Asigna cajas a tipos de contenido aleatoriamente (al menos una por tipo).
2. Coloca personas en localizaciones aleatorias (no en el depósito).
3. Genera aleatoriamente qué personas necesitan qué suministros.
4. Escribe el fichero `.pddl` completo con las secciones `:objects`, `:init` y `:goal`.

### 3.2 Cambios respecto al esqueleto original

El esqueleto tenía tres secciones marcadas como `TODO`:

#### TODO 1 — Tipos de objetos (`:objects`)
- Ya estaba casi completo. Se mantiene igual pero con nombres de tipo acordes al dominio.

#### TODO 2 — Estado inicial (`:init`)
Se añadió:
- `(at-drone drone1 depot)` — todos los drones parten del depósito.
- `(arm1-free droneX)` y `(arm2-free droneX)` — ambos brazos libres al inicio.
- `(at-crate crateX depot)` — todas las cajas parten del depósito.
- `(crate-contents crateX contentY)` — qué contiene cada caja.
- `(at-person personX locY)` — localización aleatoria de cada persona.

#### TODO 3 — Metas (`:goal`)
Se añadió:
- `(at-drone droneX depot)` — los drones deben regresar al depósito.
- `(has-content personX contentY)` — para cada par (persona, contenido) generado por `setup_person_needs`.

### 3.3 Cómo ejecutar el generador

```bash
# Desde la carpeta parte1/ (en WSL con el entorno virtual activado):
python generate-problem.py -d 1 -r 0 -l 3 -p 3 -c 3 -g 3
```

Parámetros:

| Parámetro | Descripción | Ejemplo |
|-----------|-------------|---------|
| `-d NUM` | Número de drones | `-d 1` |
| `-r NUM` | Número de carriers (ignorado en parte 1) | `-r 0` |
| `-l NUM` | Número de localizaciones (sin contar el depósito) | `-l 3` |
| `-p NUM` | Número de personas | `-p 3` |
| `-c NUM` | Número de cajas | `-c 3` |
| `-g NUM` | Número de objetivos de entrega | `-g 3` |

El fichero generado se llamará, por ejemplo:
`drone_problem_d1_r0_l3_p3_c3_g3_ct2.pddl`

### 3.4 Secuencia de problemas de complejidad creciente

Manteniendo `-d 1 -r 0` y haciendo crecer `l`, `p`, `c` y `g` a la vez:

```bash
python generate-problem.py -d 1 -r 0 -l 2  -p 2  -c 2  -g 2
python generate-problem.py -d 1 -r 0 -l 3  -p 3  -c 3  -g 3
python generate-problem.py -d 1 -r 0 -l 5  -p 5  -c 5  -g 5
python generate-problem.py -d 1 -r 0 -l 7  -p 7  -c 7  -g 7
python generate-problem.py -d 1 -r 0 -l 10 -p 10 -c 10 -g 10
python generate-problem.py -d 1 -r 0 -l 15 -p 15 -c 15 -g 15
```

Para resolver con FF:
```bash
planutils run ff -o domain.pddl -f drone_problem_d1_r0_lX_pX_cX_gX_ct2.pddl
```

### 3.5 Resultados — FF Planner (Ejercicio 1.2.2)

*(Completa esta tabla ejecutando los experimentos en WSL)*

| Tamaño (l=p=c=g) | Tiempo FF (s) | Plan encontrado |
|:-----------------:|:-------------:|:---------------:|
| 2 | — | — |
| 3 | — | — |
| 5 | — | — |
| 7 | — | — |
| 10 | — | — |
| 15 | — | — |

**¿Hasta qué tamaño puede FF resolver en 1 minuto?** — Rellenar tras experimentos.

---

## 4. Ejercicio 1.3 — Comparativa de algoritmos y heurísticas

### 4.1 Herramienta: pyperplan

```bash
# Instalación (una vez, en el entorno virtual):
pip install pyperplan

# Uso básico:
python -m pyperplan -s bfs domain.pddl problema.pddl
python -m pyperplan -s astar -H hmax domain.pddl problema.pddl
```

Opciones de algoritmo (`-s`): `bfs`, `ids`, `astar`, `wastar`, `gbfs`, `ehs`, `sat`  
Opciones de heurística (`-H`): `hadd`, `hsa`, `hmax`, `hff`, `landmark`, `lmcut`

### 4.2 Parte 1 — Búsqueda no informada vs. informada

Algoritmos probados: BFS, IDS, A\* (hMAX), GBFS (hMAX).  
Tiempo límite: **1 minuto** por ejecución.

```bash
# Ejemplo de comandos (adaptar el fichero de problema):
timeout 60 python -m pyperplan -s bfs   domain.pddl problema.pddl
timeout 60 python -m pyperplan -s ids   domain.pddl problema.pddl
timeout 60 python -m pyperplan -s astar -H hmax domain.pddl problema.pddl
timeout 60 python -m pyperplan -s gbfs  -H hmax domain.pddl problema.pddl
```

*(Completa la siguiente tabla con tus resultados)*

| Algoritmo | Tamaño máx. resuelto | Tiempo (s) | Nº pasos plan | ¿Óptimo? |
|-----------|:--------------------:|:----------:|:-------------:|:--------:|
| BFS | — | — | — | Sí |
| IDS | — | — | — | Sí |
| A\* (hMAX) | — | — | — | Sí |
| GBFS (hMAX) | — | — | — | No garantizado |

**Discusión:**
- BFS e IDS garantizan optimalidad pero el espacio de estados crece exponencialmente, por lo que resuelven problemas más pequeños.
- A\* con hMAX es admisible (no sobreestima) y garantiza optimalidad, siendo más eficiente que BFS/IDS gracias a la guía heurística.
- GBFS no garantiza optimalidad pero suele ser más rápido al no explorar sistemáticamente todos los estados.

### 4.3 Parte 2 — Satisficing: GBFS y EHC con distintas heurísticas

Usar el mayor problema que GBFS pudo resolver en 1 minuto (tamaño de la tabla anterior).

```bash
# GBFS + hMAX, hADD, hFF, Landmark
timeout 60 python -m pyperplan -s gbfs -H hmax     domain.pddl problema.pddl
timeout 60 python -m pyperplan -s gbfs -H hadd     domain.pddl problema.pddl
timeout 60 python -m pyperplan -s gbfs -H hff      domain.pddl problema.pddl
timeout 60 python -m pyperplan -s gbfs -H landmark domain.pddl problema.pddl

# EHC + hMAX, hADD, hFF, Landmark
timeout 60 python -m pyperplan -s ehs -H hmax     domain.pddl problema.pddl
timeout 60 python -m pyperplan -s ehs -H hadd     domain.pddl problema.pddl
timeout 60 python -m pyperplan -s ehs -H hff      domain.pddl problema.pddl
timeout 60 python -m pyperplan -s ehs -H landmark domain.pddl problema.pddl
```

*(Completa la tabla con tus resultados)*

| Algoritmo | Heurística | Tiempo (s) | Nº pasos plan |
|-----------|-----------|:----------:|:-------------:|
| GBFS | hMAX | — | — |
| GBFS | hADD | — | — |
| GBFS | hFF | — | — |
| GBFS | Landmark | — | — |
| EHC | hMAX | — | — |
| EHC | hADD | — | — |
| EHC | hFF | — | — |
| EHC | Landmark | — | — |

**Diferencia entre GBFS y EHC:**
- **GBFS** evalúa todos los nodos abiertos y expande el mejor según h; puede explorar regiones distintas del espacio.
- **EHC (Enforced Hill Climbing)** busca agresivamente un estado con mejor h que el actual; si lo encuentra, "salta" a él. Es muy rápido pero puede quedarse atascado (se combina con BFS para salir de mesetas). El planificador FF usa EHC como estrategia principal y GBFS como respaldo.

### 4.4 Parte 3 — Planificadores óptimos: A\* con heurísticas admisibles

**Heurísticas admisibles** (no sobreestiman el coste real): **hMAX**, **hSA**, **lmcut**.  
hADD y hFF no son admisibles (pueden sobreestimar).

Usar el mayor problema que A\* (hMAX) pudo resolver en 1 minuto.

```bash
# BFS e IDS (sin heurística)
timeout 60 python -m pyperplan -s bfs domain.pddl problema.pddl
timeout 60 python -m pyperplan -s ids domain.pddl problema.pddl

# A* con heurísticas admisibles
timeout 60 python -m pyperplan -s astar -H hmax  domain.pddl problema.pddl
timeout 60 python -m pyperplan -s astar -H hsa   domain.pddl problema.pddl
timeout 60 python -m pyperplan -s astar -H lmcut domain.pddl problema.pddl
```

*(Completa la tabla con tus resultados)*

| Algoritmo | Heurística | Tiempo (s) | Nº pasos plan | ¿Óptimo? |
|-----------|-----------|:----------:|:-------------:|:--------:|
| BFS | — | — | — | Sí |
| IDS | — | — | — | Sí |
| A\* | hMAX | — | — | Sí |
| A\* | hSA | — | — | Sí |
| A\* | lmcut | — | — | Sí |

**Discusión:**
- lmcut es típicamente la heurística más informada de las admisibles y suele dar el mejor rendimiento en A\*.
- hMAX es admisible pero poco informada (toma el máximo en lugar de sumar), por lo que A\* con hMAX se comporta parecido a BFS en muchos dominios.
- hSA es admisible y cuenta los átomos necesarios usando conjuntos independientes; su rendimiento varía mucho por dominio.

---

## 5. Requisitos del entorno

```
Sistema:      Ubuntu en WSL (Windows Subsystem for Linux)
Python:       3.8+
pip packages: planutils, pyperplan
Planificadores externos: ff, lama-first (vía planutils)
```

### Instalación rápida (desde WSL, entorno virtual activado)

```bash
pip install planutils pyperplan
planutils install ff
planutils install lama-first
```

---

## 6. Cómo ejecutarlo todo paso a paso

### Paso 1 — Abrir WSL y activar el entorno virtual

```bash
cd ~/LabsPDDL
source venv/bin/activate
```

### Paso 2 — Copiar los ficheros al entorno WSL

```bash
cp -r /mnt/c/Users/05jan/Desktop/Tareas/Uni/3_Curso/2_cuatri/Planificacion\ automatica/Lab/PL1/Planning-practice/parte1 ~/LabsPDDL/
cd ~/LabsPDDL/parte1
```

### Paso 3 — Verificar sintaxis PDDL con pyperplan

```bash
python -m pyperplan domain.pddl problem1.pddl
python -m pyperplan domain.pddl problem2.pddl
```

### Paso 4 — Resolver los problemas manuales con FF

```bash
planutils run ff -o domain.pddl -f problem1.pddl
planutils run ff -o domain.pddl -f problem2.pddl
```

### Paso 5 — Generar un problema con el generador

```bash
python generate-problem.py -d 1 -r 0 -l 3 -p 3 -c 3 -g 3
```

### Paso 6 — Resolver el problema generado con FF

```bash
planutils run ff -o domain.pddl -f drone_problem_d1_r0_l3_p3_c3_g3_ct2.pddl
```

### Paso 7 — Ejecutar pyperplan con distintos algoritmos

```bash
# BFS
python -m pyperplan -s bfs domain.pddl problema.pddl

# A* con hMAX
python -m pyperplan -s astar -H hmax domain.pddl problema.pddl

# GBFS con hFF
python -m pyperplan -s gbfs -H hff domain.pddl problema.pddl
```

---

*Práctica elaborada para la asignatura de Planificación Automática — UAH 2025-26.*
