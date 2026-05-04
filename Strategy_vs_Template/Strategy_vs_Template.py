"""
Demostración Visual: Strategy vs Template Method
================================================
Compara ambos patrones de diseño con ejemplos interactivos de ordenamiento,
mostrando su estructura, código fuente y comportamiento en tiempo real.
"""

import tkinter as tk
from tkinter import ttk, font
import time
import random
import math


# ─────────────────────────────────────────────
#  PATRÓN STRATEGY
# ─────────────────────────────────────────────

class SortStrategy:
    """Interfaz base de Strategy"""
    def sort(self, data: list) -> tuple[list, list]:
        raise NotImplementedError

class BubbleSortStrategy(SortStrategy):
    """Estrategia concreta: Bubble Sort"""
    def sort(self, data: list) -> tuple[list, list]:
        arr = data[:]
        steps = [arr[:]]
        n = len(arr)
        for i in range(n):
            for j in range(n - i - 1):
                if arr[j] > arr[j + 1]:
                    arr[j], arr[j + 1] = arr[j + 1], arr[j]
                    steps.append(arr[:])
        return arr, steps

class SelectionSortStrategy(SortStrategy):
    """Estrategia concreta: Selection Sort"""
    def sort(self, data: list) -> tuple[list, list]:
        arr = data[:]
        steps = [arr[:]]
        n = len(arr)
        for i in range(n):
            min_idx = i
            for j in range(i + 1, n):
                if arr[j] < arr[min_idx]:
                    min_idx = j
            arr[i], arr[min_idx] = arr[min_idx], arr[i]
            steps.append(arr[:])
        return arr, steps

class QuickSortStrategy(SortStrategy):
    """Estrategia concreta: Quick Sort"""
    def sort(self, data: list) -> tuple[list, list]:
        arr = data[:]
        steps = [arr[:]]

        def quicksort(a, low, high):
            if low < high:
                pivot = a[high]
                i = low - 1
                for j in range(low, high):
                    if a[j] <= pivot:
                        i += 1
                        a[i], a[j] = a[j], a[i]
                        steps.append(a[:])
                a[i + 1], a[high] = a[high], a[i + 1]
                steps.append(a[:])
                quicksort(a, low, i)
                quicksort(a, i + 2, high)

        quicksort(arr, 0, len(arr) - 1)
        return arr, steps

class Sorter:
    """Contexto de Strategy — delega el algoritmo a la estrategia inyectada"""
    def __init__(self, strategy: SortStrategy = None):
        self._strategy = strategy

    def set_strategy(self, strategy: SortStrategy):
        self._strategy = strategy

    def execute_sort(self, data: list):
        if not self._strategy:
            raise ValueError("No strategy set")
        return self._strategy.sort(data)


# ─────────────────────────────────────────────
#  PATRÓN TEMPLATE METHOD
# ─────────────────────────────────────────────

class SortTemplate:
    """Clase abstracta con el Template Method"""

    def sort(self, data: list) -> tuple[list, list]:
        """TEMPLATE METHOD — el esqueleto del algoritmo, no se sobreescribe"""
        arr = data[:]
        steps = [arr[:]]
        self._prepare(arr)          # hook opcional
        self._do_sort(arr, steps)   # paso obligatorio (sobreescribir)
        self._cleanup(arr)          # hook opcional
        return arr, steps

    # ── Pasos concretos (hooks opcionales) ──
    def _prepare(self, arr): pass
    def _cleanup(self, arr): pass

    # ── Paso abstracto (DEBE sobreescribirse) ──
    def _do_sort(self, arr, steps):
        raise NotImplementedError

class TemplateBubbleSort(SortTemplate):
    """Subclase concreta: solo define _do_sort"""
    def _do_sort(self, arr, steps):
        n = len(arr)
        for i in range(n):
            for j in range(n - i - 1):
                if arr[j] > arr[j + 1]:
                    arr[j], arr[j + 1] = arr[j + 1], arr[j]
                    steps.append(arr[:])

class TemplateInsertionSort(SortTemplate):
    """Subclase concreta: solo define _do_sort"""
    def _do_sort(self, arr, steps):
        for i in range(1, len(arr)):
            key = arr[i]
            j = i - 1
            while j >= 0 and arr[j] > key:
                arr[j + 1] = arr[j]
                j -= 1
                steps.append(arr[:])
            arr[j + 1] = key
            steps.append(arr[:])

class TemplateMergeSort(SortTemplate):
    """Subclase concreta: solo define _do_sort"""
    def _do_sort(self, arr, steps):
        def merge_sort(a):
            if len(a) <= 1:
                return a
            mid = len(a) // 2
            left = merge_sort(a[:mid])
            right = merge_sort(a[mid:])
            merged = []
            i = j = 0
            while i < len(left) and j < len(right):
                if left[i] <= right[j]:
                    merged.append(left[i]); i += 1
                else:
                    merged.append(right[j]); j += 1
            merged.extend(left[i:]); merged.extend(right[j:])
            return merged

        result = merge_sort(arr[:])
        for k, v in enumerate(result):
            arr[k] = v
        steps.append(arr[:])


# ─────────────────────────────────────────────
#  INTERFAZ GRÁFICA
# ─────────────────────────────────────────────

DARK_BG    = "#0f1117"
PANEL_BG   = "#1a1d27"
CARD_BG    = "#22263a"
ACCENT_S   = "#00d4aa"   # verde-azulado → Strategy
ACCENT_T   = "#f97316"   # naranja        → Template
TEXT_PRI   = "#e8eaf0"
TEXT_SEC   = "#7b82a0"
BORDER     = "#2e3350"

CODE_STRATEGY = """\
# ── STRATEGY ── composición, no herencia ──────

class SortStrategy:           # interfaz
    def sort(self, data): ...

class BubbleSortStrategy(SortStrategy):
    def sort(self, data):
        # implementación completa aquí
        ...

class QuickSortStrategy(SortStrategy):
    def sort(self, data):
        # implementación completa aquí
        ...

class Sorter:                 # Contexto
    def __init__(self, strategy=None):
        self._strategy = strategy

    def set_strategy(self, s):
        self._strategy = s    # ← swap en tiempo de ejecución

    def execute_sort(self, data):
        return self._strategy.sort(data)

# Uso — el algoritmo se inyecta desde fuera:
sorter = Sorter()
sorter.set_strategy(BubbleSortStrategy())
sorter.execute_sort(data)
sorter.set_strategy(QuickSortStrategy())  # ← cambio dinámico
sorter.execute_sort(data)
"""

CODE_TEMPLATE = """\
# ── TEMPLATE METHOD ── herencia, estructura fija ──

class SortTemplate:           # clase abstracta
    def sort(self, data):     # ← TEMPLATE METHOD
        arr = data[:]         #   esqueleto FIJO
        self._prepare(arr)    #   hook opcional
        self._do_sort(arr)    #   paso ABSTRACTO
        self._cleanup(arr)    #   hook opcional
        return arr

    def _prepare(self, arr): pass   # hook
    def _cleanup(self, arr): pass   # hook

    def _do_sort(self, arr):        # abstracto
        raise NotImplementedError

class TemplateBubbleSort(SortTemplate):
    def _do_sort(self, arr, steps):
        # solo este paso varía
        ...

class TemplateMergeSort(SortTemplate):
    def _do_sort(self, arr, steps):
        # solo este paso varía
        ...

# Uso — el algoritmo queda fijo en la subclase:
sorter = TemplateBubbleSort()
sorter.sort(data)
sorter2 = TemplateMergeSort()
sorter2.sort(data)
"""


class AnimatedBar(tk.Canvas):
    """Canvas que anima una secuencia de pasos de ordenamiento"""

    def __init__(self, master, accent, **kw):
        super().__init__(master, bg=CARD_BG, highlightthickness=0, **kw)
        self.accent = accent
        self._steps = []
        self._step_idx = 0
        self._after_id = None
        self._animating = False

    def load(self, steps):
        self._steps = steps
        self._step_idx = 0
        self._animating = False
        if self._after_id:
            self.after_cancel(self._after_id)
        self._draw(steps[0] if steps else [])

    def play(self, delay_ms=60):
        if self._animating:
            return
        self._animating = True
        self._tick(delay_ms)

    def _tick(self, delay_ms):
        if self._step_idx >= len(self._steps):
            self._animating = False
            return
        self._draw(self._steps[self._step_idx])
        self._step_idx += 1
        self._after_id = self.after(delay_ms, lambda: self._tick(delay_ms))

    def _draw(self, arr):
        self.delete("all")
        if not arr:
            return
        w = self.winfo_width() or 300
        h = self.winfo_height() or 160
        n = len(arr)
        bar_w = max(2, (w - 10) // n - 2)
        max_v = max(arr) if arr else 1
        pad = 5

        for i, v in enumerate(arr):
            bar_h = int((v / max_v) * (h - 20))
            x0 = pad + i * (bar_w + 2)
            y0 = h - bar_h - 5
            x1 = x0 + bar_w
            y1 = h - 5
            # gradient-ish effect: tip más brillante
            self.create_rectangle(x0, y0, x1, y1, fill=self.accent,
                                  outline="", width=0)
            # tip highlight
            self.create_rectangle(x0, y0, x1, y0 + 3,
                                  fill="white", outline="", stipple="gray50")


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Strategy vs Template Method — Patrones de Diseño")
        self.configure(bg=DARK_BG)
        self.geometry("1200x820")
        self.minsize(900, 680)
        self.resizable(True, True)

        self._data = []
        self._build_ui()
        self._gen_data()

    # ── construcción ──────────────────────────

    def _build_ui(self):
        # fuentes
        self.fnt_title  = font.Font(family="Courier", size=18, weight="bold")
        self.fnt_sub    = font.Font(family="Courier", size=10)
        self.fnt_label  = font.Font(family="Courier", size=11, weight="bold")
        self.fnt_code   = font.Font(family="Courier", size=9)
        self.fnt_btn    = font.Font(family="Courier", size=10, weight="bold")
        self.fnt_badge  = font.Font(family="Courier", size=8, weight="bold")

        # ── encabezado ───────────────────────
        hdr = tk.Frame(self, bg=DARK_BG, pady=14)
        hdr.pack(fill="x", padx=20)

        tk.Label(hdr, text="Strategy  vs  Template Method",
                 font=self.fnt_title, bg=DARK_BG, fg=TEXT_PRI).pack(side="left")
        tk.Label(hdr, text=" Patrones de Diseño — Demo Interactivo",
                 font=self.fnt_sub, bg=DARK_BG, fg=TEXT_SEC).pack(side="left", padx=8, pady=3)

        # ── separador ────────────────────────
        tk.Frame(self, bg=BORDER, height=1).pack(fill="x", padx=20)

        # ── controles globales ───────────────
        ctrl = tk.Frame(self, bg=DARK_BG, pady=10)
        ctrl.pack(fill="x", padx=20)

        tk.Label(ctrl, text="Elementos:", font=self.fnt_sub,
                 bg=DARK_BG, fg=TEXT_SEC).pack(side="left")
        self.var_n = tk.IntVar(value=18)
        tk.Scale(ctrl, from_=8, to=30, orient="horizontal", variable=self.var_n,
                 bg=DARK_BG, fg=TEXT_PRI, troughcolor=PANEL_BG,
                 highlightthickness=0, length=130, showvalue=True,
                 font=self.fnt_sub).pack(side="left", padx=(4, 16))

        for txt, cmd in [("🔀  Nuevo dato", self._gen_data),
                         ("▶  Ejecutar ambos", self._run_both)]:
            tk.Button(ctrl, text=txt, command=cmd,
                      font=self.fnt_btn, bg=PANEL_BG, fg=TEXT_PRI,
                      activebackground=BORDER, activeforeground=TEXT_PRI,
                      relief="flat", padx=14, pady=5,
                      cursor="hand2").pack(side="left", padx=4)

        # ── contenido principal ──────────────
        main = tk.Frame(self, bg=DARK_BG)
        main.pack(fill="both", expand=True, padx=20, pady=(0, 16))
        main.columnconfigure(0, weight=1)
        main.columnconfigure(1, weight=1)
        main.rowconfigure(0, weight=1)

        self._strategy_panel = self._build_pattern_panel(
            main, "Strategy", ACCENT_S,
            "Composición — el algoritmo se inyecta al contexto desde afuera.",
            ["Bubble Sort", "Selection Sort", "Quick Sort"],
            self._run_strategy, CODE_STRATEGY, col=0)

        self._template_panel = self._build_pattern_panel(
            main, "Template Method", ACCENT_T,
            "Herencia — el esqueleto del algoritmo queda fijo en la superclase.",
            ["Bubble Sort", "Insertion Sort", "Merge Sort"],
            self._run_template, CODE_TEMPLATE, col=1)

        # ── barra inferior de diferencias ────
        self._build_diff_bar()

    def _build_pattern_panel(self, parent, title, accent,
                              subtitle, algos, run_cmd, code, col):
        frame = tk.Frame(parent, bg=PANEL_BG,
                         highlightbackground=BORDER, highlightthickness=1)
        frame.grid(row=0, column=col, sticky="nsew",
                   padx=(0, 8) if col == 0 else (8, 0))
        frame.rowconfigure(3, weight=1)
        frame.columnconfigure(0, weight=1)

        # encabezado del panel
        hdr = tk.Frame(frame, bg=accent)
        hdr.grid(row=0, column=0, sticky="ew")
        tk.Label(hdr, text=f"  {title}  ", font=self.fnt_label,
                 bg=accent, fg=DARK_BG, pady=6).pack(side="left")
        tk.Label(hdr, text=subtitle, font=self.fnt_sub,
                 bg=accent, fg=DARK_BG, wraplength=360,
                 justify="left").pack(side="left", padx=6)

        # selector de algoritmo
        sel_row = tk.Frame(frame, bg=PANEL_BG, pady=8)
        sel_row.grid(row=1, column=0, sticky="ew", padx=12)

        tk.Label(sel_row, text="Algoritmo:", font=self.fnt_sub,
                 bg=PANEL_BG, fg=TEXT_SEC).pack(side="left")
        var = tk.StringVar(value=algos[0])
        combo = ttk.Combobox(sel_row, values=algos, textvariable=var,
                             state="readonly", width=18, font=self.fnt_sub)
        combo.pack(side="left", padx=6)

        tk.Button(sel_row, text="▶ Ejecutar",
                  command=run_cmd,
                  font=self.fnt_btn, bg=accent, fg=DARK_BG,
                  activebackground=accent, relief="flat",
                  padx=10, pady=3, cursor="hand2").pack(side="left", padx=6)

        self._status_lbl = getattr(self, "_status_lbl_s", None)
        status_var = tk.StringVar(value="Listo")
        status_lbl = tk.Label(sel_row, textvariable=status_var,
                              font=self.fnt_sub, bg=PANEL_BG, fg=TEXT_SEC)
        status_lbl.pack(side="right", padx=4)

        # animación de barras
        bar = AnimatedBar(frame, accent, height=160)
        bar.grid(row=2, column=0, sticky="ew", padx=12, pady=(0, 6))

        # notebook: código / info
        nb = ttk.Notebook(frame)
        nb.grid(row=3, column=0, sticky="nsew", padx=12, pady=(0, 12))

        code_frame = tk.Frame(nb, bg=CARD_BG)
        nb.add(code_frame, text=" Código ")

        code_txt = tk.Text(code_frame, font=self.fnt_code,
                           bg=CARD_BG, fg="#a8d8a8" if accent == ACCENT_S else "#ffcc88",
                           insertbackground=TEXT_PRI, relief="flat",
                           wrap="none", state="normal",
                           padx=8, pady=6)
        sb = tk.Scrollbar(code_frame, command=code_txt.yview,
                          bg=CARD_BG, troughcolor=CARD_BG)
        code_txt.config(yscrollcommand=sb.set)
        sb.pack(side="right", fill="y")
        code_txt.pack(fill="both", expand=True)
        code_txt.insert("1.0", code)
        code_txt.config(state="disabled")

        info_frame = tk.Frame(nb, bg=CARD_BG)
        nb.add(info_frame, text=" Estructura ")
        self._build_structure_info(info_frame, title, accent)

        # guardar refs
        refs = {"var": var, "bar": bar, "status": status_var}
        if col == 0:
            self._s_refs = refs
        else:
            self._t_refs = refs
        return frame

    def _build_structure_info(self, parent, pattern, accent):
        items = []
        if pattern == "Strategy":
            items = [
                ("Interfaz / Strategy",   "Define el contrato del algoritmo.", accent),
                ("Clases concretas",       "Cada una implementa el algoritmo completo.", TEXT_SEC),
                ("Contexto (Sorter)",      "Guarda una referencia a la estrategia activa.", TEXT_SEC),
                ("Clave: composición",     "El algoritmo se INYECTA → cambio en runtime.", "#ffd700"),
                ("Ventaja",                "Intercambias algoritmos sin tocar el contexto.", "#aaffaa"),
                ("Cuándo usarlo",          "Múltiples variantes intercambiables del mismo comportamiento.", TEXT_SEC),
            ]
        else:
            items = [
                ("Clase abstracta",        "Define el Template Method con el esqueleto.", accent),
                ("Template Method",        "Orquesta los pasos; NO se sobreescribe.", TEXT_SEC),
                ("Hooks (opcionales)",     "_prepare, _cleanup — las subclases los pueden pisar.", TEXT_SEC),
                ("Paso abstracto",         "_do_sort DEBE implementarse en cada subclase.", "#ffd700"),
                ("Clave: herencia",        "El flujo queda FIJO; solo varían los pasos concretos.", "#ffcc88"),
                ("Cuándo usarlo",          "Algoritmos con la misma estructura pero pasos diferentes.", TEXT_SEC),
            ]

        for i, (label, desc, color) in enumerate(items):
            row = tk.Frame(parent, bg=CARD_BG,
                           highlightbackground=BORDER, highlightthickness=1)
            row.pack(fill="x", padx=8, pady=3)

            badge = tk.Label(row, text=f"  {label}  ",
                             font=self.fnt_badge, bg=color if color not in (TEXT_SEC,) else PANEL_BG,
                             fg=DARK_BG if color not in (TEXT_SEC,) else TEXT_SEC,
                             padx=4, pady=3)
            badge.pack(side="left")
            tk.Label(row, text=desc, font=self.fnt_sub,
                     bg=CARD_BG, fg=TEXT_PRI, wraplength=300,
                     justify="left", padx=6, pady=3).pack(side="left")

    def _build_diff_bar(self):
        bar = tk.Frame(self, bg=CARD_BG,
                       highlightbackground=BORDER, highlightthickness=1)
        bar.pack(fill="x", padx=20, pady=(0, 10))

        tk.Label(bar, text="  Diferencias clave:  ",
                 font=self.fnt_label, bg=CARD_BG, fg=TEXT_PRI,
                 pady=4).grid(row=0, column=0, rowspan=2)

        diffs = [
            ("Mecanismo",    "Composición",  "Herencia"),
            ("Flexibilidad", "Alta — swap en runtime", "Media — fijo en subclase"),
            ("Variación",    "Toda la lógica del algoritmo", "Solo los pasos definidos como abstractos"),
            ("Acoplamiento", "Bajo — interfaz compartida", "Mayor — hereda de la superclase"),
        ]

        tk.Label(bar, text="Aspecto", font=self.fnt_badge,
                 bg=CARD_BG, fg=TEXT_SEC, padx=8).grid(row=0, column=1)
        tk.Label(bar, text="Strategy", font=self.fnt_badge,
                 bg=ACCENT_S, fg=DARK_BG, padx=10).grid(row=0, column=2, padx=4)
        tk.Label(bar, text="Template Method", font=self.fnt_badge,
                 bg=ACCENT_T, fg=DARK_BG, padx=10).grid(row=0, column=3, padx=4)

        for i, (aspect, sv, tv) in enumerate(diffs):
            tk.Label(bar, text=aspect, font=self.fnt_sub,
                     bg=CARD_BG, fg=TEXT_SEC, padx=8,
                     anchor="w").grid(row=i + 1, column=1, sticky="w")
            tk.Label(bar, text=sv, font=self.fnt_sub,
                     bg=CARD_BG, fg=ACCENT_S, padx=8,
                     anchor="w").grid(row=i + 1, column=2, sticky="w")
            tk.Label(bar, text=tv, font=self.fnt_sub,
                     bg=CARD_BG, fg=ACCENT_T, padx=8,
                     anchor="w").grid(row=i + 1, column=3, sticky="w")

    # ── lógica de datos y ejecución ───────────

    def _gen_data(self):
        n = self.var_n.get()
        self._data = [random.randint(2, 100) for _ in range(n)]
        if hasattr(self, "_s_refs"):
            self._s_refs["bar"].load([self._data])
            self._s_refs["status"].set("Listo")
        if hasattr(self, "_t_refs"):
            self._t_refs["bar"].load([self._data])
            self._t_refs["status"].set("Listo")

    def _run_strategy(self):
        algo = self._s_refs["var"].get()
        strategy_map = {
            "Bubble Sort":    BubbleSortStrategy(),
            "Selection Sort": SelectionSortStrategy(),
            "Quick Sort":     QuickSortStrategy(),
        }
        sorter = Sorter(strategy_map[algo])
        t0 = time.perf_counter()
        _, steps = sorter.execute_sort(self._data)
        elapsed = (time.perf_counter() - t0) * 1000

        delay = max(20, 800 // len(steps))
        self._s_refs["bar"].load(steps)
        self._s_refs["bar"].play(delay)
        self._s_refs["status"].set(
            f"{algo} | {len(steps)} pasos | {elapsed:.2f} ms")

    def _run_template(self):
        algo = self._t_refs["var"].get()
        template_map = {
            "Bubble Sort":    TemplateBubbleSort(),
            "Insertion Sort": TemplateInsertionSort(),
            "Merge Sort":     TemplateMergeSort(),
        }
        sorter = template_map[algo]
        t0 = time.perf_counter()
        _, steps = sorter.sort(self._data)
        elapsed = (time.perf_counter() - t0) * 1000

        delay = max(20, 800 // len(steps))
        self._t_refs["bar"].load(steps)
        self._t_refs["bar"].play(delay)
        self._t_refs["status"].set(
            f"{algo} | {len(steps)} pasos | {elapsed:.2f} ms")

    def _run_both(self):
        self._run_strategy()
        self._run_template()


# ─────────────────────────────────────────────

if __name__ == "__main__":
    app = App()
    app.mainloop()