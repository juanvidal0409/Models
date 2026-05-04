# Strategy vs Template Method — Demo Interactivo

Aplicación de escritorio en Python que demuestra de forma visual e interactiva las diferencias entre dos patrones de diseño de comportamiento del catálogo GoF: **Strategy** y **Template Method**. Ambos patrones se aplican al mismo dominio (algoritmos de ordenamiento) para que la comparación sea directa y significativa.

---

## Tabla de contenidos

1. [En qué consiste el programa](#1-en-qué-consiste-el-programa)
2. [Guía de uso](#2-guía-de-uso)
3. [Explicación del código](#3-explicación-del-código)
4. [Cómo se usan los patrones en el código](#4-cómo-se-usan-los-patrones-en-el-código)

---

## 1. En qué consiste el programa

El programa abre una ventana dividida en **dos paneles lado a lado**. Cada panel representa un patrón de diseño y contiene:

- Un **selector de algoritmo** de ordenamiento.
- Una **animación de barras** que muestra el proceso de ordenamiento paso a paso en tiempo real.
- Una **pestaña de código** con el esqueleto del patrón implementado.
- Una **pestaña de estructura** que explica los roles de cada clase participante.

Al pie de la ventana hay una **tabla comparativa** que contrasta los dos patrones en cuatro aspectos: mecanismo, flexibilidad, variación y acoplamiento.

El objetivo es que, al ejecutar el mismo conjunto de datos con ambos paneles en paralelo, el usuario pueda apreciar no solo que los algoritmos se comportan igual en cuanto al resultado, sino que la **forma en que el patrón organiza el código** es radicalmente distinta en cada caso.

### Patrones que se demuestran

**Strategy** (panel izquierdo, color verde-azulado)

Define una familia de algoritmos encapsulados en clases independientes, todos con la misma interfaz. El objeto que necesita ordenar (el *Contexto*) recibe el algoritmo desde afuera y puede intercambiarlo en cualquier momento sin cambiar una sola línea del Contexto. El mecanismo central es la **composición**.

Algoritmos disponibles: Bubble Sort, Selection Sort, Quick Sort.

**Template Method** (panel derecho, color naranja)

Define el *esqueleto* de un algoritmo en una clase base. Los pasos que varían se declaran abstractos y cada subclase los implementa a su manera, pero el flujo general queda fijo y no puede modificarse desde fuera. El mecanismo central es la **herencia**.

Algoritmos disponibles: Bubble Sort, Insertion Sort, Merge Sort.

---

## 2. Guía de uso

### Requisitos

- Python **3.10 o superior**.
- `tkinter` (incluido en la instalación estándar de Python en Windows y macOS; en Linux puede requerir instalación separada).

**Linux (Debian/Ubuntu):**
```bash
sudo apt install python3-tk
```

No se requieren paquetes externos ni entornos virtuales.

### Ejecución

```bash
python design_patterns_demo.py
```

### Descripción de los controles

```
┌──────────────────────────────────────────────────────┐
│  Strategy vs Template Method — Demo Interactivo       │
├─────────────────────┬────────────────────────────────┤
│  Elementos: [slider]│  🔀 Nuevo dato  ▶ Ejecutar ambos│
├─────────────────────┴────────────────────────────────┤
│  [ Panel STRATEGY ]     │  [ Panel TEMPLATE METHOD ]  │
│  Algoritmo: [combo] ▶   │  Algoritmo: [combo] ▶       │
│  ┌─ animación barras ─┐ │  ┌─ animación barras ─┐     │
│  └────────────────────┘ │  └────────────────────┘     │
│  [ Código | Estructura ] │  [ Código | Estructura ]   │
├──────────────────────────────────────────────────────┤
│  Diferencias clave: Mecanismo / Flexibilidad / ...    │
└──────────────────────────────────────────────────────┘
```

| Control | Descripción |
|---|---|
| **Slider "Elementos"** | Ajusta la cantidad de barras a ordenar (entre 8 y 30). Un número mayor produce animaciones más lentas pero muestra con más detalle la diferencia de pasos entre algoritmos. |
| **🔀 Nuevo dato** | Genera un array aleatorio nuevo con la cantidad de elementos seleccionada. Reinicia ambas animaciones. |
| **▶ Ejecutar ambos** | Lanza simultáneamente el algoritmo seleccionado en cada panel. Ideal para comparar el número de pasos lado a lado. |
| **Combo "Algoritmo"** | Selecciona el algoritmo a visualizar en ese panel. Cada panel tiene su propio selector. |
| **▶ Ejecutar** (por panel) | Lanza únicamente el algoritmo de ese panel. |
| **Tab "Código"** | Muestra el esqueleto del patrón con comentarios. El código es el real que se ejecuta (simplificado para legibilidad). |
| **Tab "Estructura"** | Lista los roles del patrón (interfaz, contexto, hooks, paso abstracto) con una breve descripción de cada uno. |
| **Barra inferior** | Tabla comparativa fija con las diferencias clave entre los dos patrones. |

### Flujo de uso recomendado

1. Abrir el programa. Aparece un array aleatorio de 18 elementos en ambos paneles.
2. Pulsar **▶ Ejecutar ambos** para ver ambas animaciones al mismo tiempo.
3. Observar la **barra de estado** de cada panel: muestra el algoritmo activo, el número de pasos realizados y el tiempo transcurrido.
4. Cambiar el algoritmo en un panel y pulsar su **▶ Ejecutar** individual para comparar la diferencia de pasos (por ejemplo, Quick Sort frente a Bubble Sort sobre el mismo array).
5. Pulsar **🔀 Nuevo dato** para regenerar el array y repetir la prueba.
6. Leer las pestañas **Código** y **Estructura** para relacionar lo que se ve en la animación con la implementación.

---

## 3. Explicación del código

El archivo está organizado en tres bloques claramente delimitados.

### Bloque 1 — Patrón Strategy (líneas 19–86)

```
SortStrategy          ← interfaz base
  ├── BubbleSortStrategy
  ├── SelectionSortStrategy
  └── QuickSortStrategy
Sorter                ← Contexto
```

`SortStrategy` es la interfaz que obliga a todas las estrategias a exponer un método `sort(data)` que devuelve una tupla `(resultado, pasos)`. Los pasos son snapshots del array en cada intercambio, usados después por la animación.

`Sorter` es el Contexto: recibe cualquier objeto que cumpla la interfaz `SortStrategy` y lo invoca a través de `execute_sort()`. No sabe ni le importa qué algoritmo está usando internamente.

### Bloque 2 — Patrón Template Method (líneas 93–158)

```
SortTemplate          ← clase abstracta con el template method
  ├── TemplateBubbleSort
  ├── TemplateInsertionSort
  └── TemplateMergeSort
```

`SortTemplate` define el método `sort()` como Template Method: llama en orden a `_prepare()`, `_do_sort()` y `_cleanup()`. Solo `_do_sort()` es abstracto (lanza `NotImplementedError`); los otros dos son hooks con implementación vacía. Cada subclase sobreescribe únicamente `_do_sort()`.

### Bloque 3 — Interfaz gráfica (líneas 164–582)

**Constantes de color** (líneas 165–172): paleta oscura definida como variables de módulo para que puedan referenciarse desde cualquier método sin pasar parámetros.

**`AnimatedBar`** (línea 174): subclase de `tk.Canvas`. Recibe una lista de snapshots (`steps`), los carga con `load()` y los reproduce frame a frame con `play()`. El método `_draw()` calcula el ancho y alto proporcional de cada barra y las dibuja como rectángulos coloreados. El retraso entre frames se calcula dinámicamente (`800 // len(steps)`) para que animaciones con muchos pasos no sean excesivamente lentas.

**`App`** (línea 208): ventana principal. Hereda de `tk.Tk`.

- `_build_ui()`: construye el encabezado, la barra de controles globales, los dos paneles y la barra inferior de diferencias.
- `_build_pattern_panel()`: método reutilizado para construir tanto el panel Strategy como el de Template Method. Recibe el título, color, lista de algoritmos y función de ejecución como parámetros, y devuelve referencias al combo, a la barra animada y a la variable de estado.
- `_build_structure_info()`: construye la pestaña "Estructura" con badges de colores descriptivos de los roles del patrón.
- `_build_diff_bar()`: construye la tabla comparativa inferior con datos fijos.
- `_gen_data()`: genera un array de enteros aleatorios y reinicia ambas barras.
- `_run_strategy()`: instancia el `Sorter` con la estrategia seleccionada, ejecuta el sort y lanza la animación.
- `_run_template()`: instancia la subclase de `SortTemplate` seleccionada, ejecuta `sort()` y lanza la animación.
- `_run_both()`: llama a ambos en secuencia.

---

## 4. Cómo se usan los patrones en el código

### Strategy en detalle

La interfaz `SortStrategy` define el contrato:

```python
class SortStrategy:
    def sort(self, data: list) -> tuple[list, list]:
        raise NotImplementedError
```

Cada algoritmo implementa ese contrato de forma completamente autónoma:

```python
class BubbleSortStrategy(SortStrategy):
    def sort(self, data):
        arr = data[:]
        steps = [arr[:]]
        # lógica completa de bubble sort aquí
        return arr, steps

class QuickSortStrategy(SortStrategy):
    def sort(self, data):
        arr = data[:]
        steps = [arr[:]]
        # lógica completa de quick sort aquí
        return arr, steps
```

El Contexto `Sorter` solo conoce la interfaz, nunca las clases concretas:

```python
class Sorter:
    def __init__(self, strategy: SortStrategy = None):
        self._strategy = strategy

    def set_strategy(self, strategy: SortStrategy):
        self._strategy = strategy          # swap en tiempo de ejecución

    def execute_sort(self, data: list):
        return self._strategy.sort(data)   # delega; no sabe qué hay dentro
```

Cuando el usuario pulsa **▶ Ejecutar** en el panel izquierdo, el método `_run_strategy()` de la App crea un `Sorter` e inyecta la estrategia elegida en el combo:

```python
def _run_strategy(self):
    algo = self._s_refs["var"].get()       # nombre del algoritmo en el combo
    strategy_map = {
        "Bubble Sort":    BubbleSortStrategy(),
        "Selection Sort": SelectionSortStrategy(),
        "Quick Sort":     QuickSortStrategy(),
    }
    sorter = Sorter(strategy_map[algo])    # inyección de la estrategia
    _, steps = sorter.execute_sort(self._data)
    self._s_refs["bar"].load(steps)
    self._s_refs["bar"].play()
```

La clave es que `Sorter` no cambia en absoluto al cambiar de algoritmo. Si mañana se añade un `MergeSortStrategy`, basta con agregarlo al diccionario; `Sorter` y todo lo demás permanece intacto.

### Template Method en detalle

`SortTemplate` define el flujo fijo en `sort()` y declara el paso variable como abstracto:

```python
class SortTemplate:
    def sort(self, data: list) -> tuple[list, list]:
        # TEMPLATE METHOD — este método nunca se sobreescribe
        arr = data[:]
        steps = [arr[:]]
        self._prepare(arr)        # hook: las subclases pueden usarlo o no
        self._do_sort(arr, steps) # ABSTRACTO: cada subclase lo implementa
        self._cleanup(arr)        # hook: las subclases pueden usarlo o no
        return arr, steps

    def _prepare(self, arr): pass   # hook vacío por defecto
    def _cleanup(self, arr): pass   # hook vacío por defecto

    def _do_sort(self, arr, steps):
        raise NotImplementedError   # DEBE implementarse
```

Cada subclase solo sobreescribe `_do_sort()`:

```python
class TemplateBubbleSort(SortTemplate):
    def _do_sort(self, arr, steps):
        n = len(arr)
        for i in range(n):
            for j in range(n - i - 1):
                if arr[j] > arr[j + 1]:
                    arr[j], arr[j + 1] = arr[j + 1], arr[j]
                    steps.append(arr[:])
        # no devuelve nada; modifica arr y steps in-place

class TemplateMergeSort(SortTemplate):
    def _do_sort(self, arr, steps):
        # implementación de merge sort recursivo
        # el resultado se escribe de vuelta en arr
        ...
```

Cuando el usuario pulsa **▶ Ejecutar** en el panel derecho, `_run_template()` instancia directamente la subclase:

```python
def _run_template(self):
    algo = self._t_refs["var"].get()
    template_map = {
        "Bubble Sort":    TemplateBubbleSort(),
        "Insertion Sort": TemplateInsertionSort(),
        "Merge Sort":     TemplateMergeSort(),
    }
    sorter = template_map[algo]           # se elige la subclase concreta
    _, steps = sorter.sort(self._data)    # sort() es el template method
    self._t_refs["bar"].load(steps)
    self._t_refs["bar"].play()
```

Aquí no hay inyección externa: el algoritmo queda fijado en la subclase elegida. El Template Method `sort()` sigue siendo el mismo en todas; lo que cambia es lo que `_do_sort()` hace dentro de cada subclase.

### Diferencia fundamental entre los dos enfoques

| Aspecto | Strategy | Template Method |
|---|---|---|
| Mecanismo | Composición — el algoritmo se inyecta al Contexto | Herencia — el algoritmo se fija en la subclase |
| Cambio de algoritmo | En tiempo de ejecución (`set_strategy`) | En tiempo de compilación (elegir la subclase) |
| Qué varía | El algoritmo completo (toda la lógica de `sort`) | Solo los pasos declarados abstractos (`_do_sort`) |
| Acoplamiento | Bajo — el Contexto solo conoce la interfaz | Mayor — la subclase hereda el estado de la clase base |
| Cuándo elegirlo | Cuando necesitas intercambiar comportamientos dinámicamente o desde fuera de la clase | Cuando el flujo general es fijo y solo quieres que las subclases rellenen pasos concretos |

Ambos patrones resuelven el mismo problema —evitar código duplicado y hacer que los algoritmos sean intercambiables— pero desde ángulos opuestos: Strategy favorece la flexibilidad externa y el bajo acoplamiento, mientras que Template Method favorece el control central del flujo y la reutilización de lógica compartida en la clase base.
