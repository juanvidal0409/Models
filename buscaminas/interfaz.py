
# Interfaz gráfica del Buscaminas con tkinter (incluido en Python).

import tkinter as tk

from niveles import NIVELES, FACIL, Nivel
from tablero import Tablero

TAM_CASILLA = 28

# Paleta de colores
COLOR_FONDO     = "#1e1e2e"
COLOR_OCULTA    = "#8c9ab8"
COLOR_REVELADA  = "#e4e8f0"
COLOR_EXPLOSION = "#ff5c5c"
COLOR_TEXTO     = "#e4e8f0"

# Color de cada número de minas vecinas
COLORES_NUMEROS = {
    1: "#1f5fd1", 2: "#2a8a2a", 3: "#d12020", 4: "#1b1b8f",
    5: "#8f1b1b", 6: "#1b8f8f", 7: "#000000", 8: "#666666",
}


class Buscaminas:
    """Ventana principal: selector de nivel, marcadores y tablero."""

    def __init__(self, raiz: tk.Tk):
        self.raiz = raiz
        self.raiz.title("Buscaminas")
        self.raiz.configure(bg=COLOR_FONDO)
        self.raiz.resizable(False, False)

        self.nivel: Nivel = FACIL
        self.tablero: Tablero | None = None
        self.segundos = 0
        self._id_reloj = None
        self.botones: list[list[tk.Label]] = []

        self._crear_barra_superior()
        self.marco_tablero = tk.Frame(self.raiz, bg=COLOR_FONDO)
        self.marco_tablero.pack(padx=10, pady=(0, 10))

        self.nueva_partida()

    # Construcción de la interfaz
    def _crear_barra_superior(self) -> None:
        barra = tk.Frame(self.raiz, bg=COLOR_FONDO)
        barra.pack(fill="x", padx=10, pady=10)

        marco_niveles = tk.Frame(barra, bg=COLOR_FONDO)
        marco_niveles.pack()
        self.var_nivel = tk.StringVar(value=self.nivel.nombre)
        for nivel in NIVELES:
            tk.Radiobutton(
                marco_niveles, text=nivel.nombre, value=nivel.nombre,
                variable=self.var_nivel, indicatoron=False, width=9,
                command=lambda n=nivel: self.cambiar_nivel(n),
                bg=COLOR_OCULTA, selectcolor="#f5c542",
                font=("Helvetica", 11, "bold"),
            ).pack(side="left", padx=3)

        marcadores = tk.Frame(barra, bg=COLOR_FONDO)
        marcadores.pack(fill="x", pady=(8, 0))
        estilo = {"bg": COLOR_FONDO, "fg": COLOR_TEXTO,
                  "font": ("Courier", 16, "bold")}
        self.lbl_minas = tk.Label(marcadores, **estilo)
        self.lbl_minas.pack(side="left")
        self.lbl_tiempo = tk.Label(marcadores, **estilo)
        self.lbl_tiempo.pack(side="right")
        self.btn_cara = tk.Button(marcadores, font=("Helvetica", 16),
                                  command=self.nueva_partida, width=3)
        self.btn_cara.pack()

    def _crear_casillas(self) -> None:
        for widget in self.marco_tablero.winfo_children():
            widget.destroy()
        self.botones = []
        for f in range(self.nivel.filas):
            fila = []
            for c in range(self.nivel.columnas):
                celda = tk.Frame(self.marco_tablero, width=TAM_CASILLA,
                                 height=TAM_CASILLA)
                celda.grid(row=f, column=c, padx=1, pady=1)
                celda.pack_propagate(False)
                lbl = tk.Label(celda, bg=COLOR_OCULTA, relief="raised", bd=2,
                               font=("Helvetica", 12, "bold"))
                lbl.pack(fill="both", expand=True)
                lbl.bind("<Button-1>", lambda e, f=f, c=c: self._clic_izquierdo(f, c))
                lbl.bind("<Button-2>", lambda e, f=f, c=c: self._clic_derecho(f, c))
                lbl.bind("<Button-3>", lambda e, f=f, c=c: self._clic_derecho(f, c))
                fila.append(lbl)
            self.botones.append(fila)

    # Control de la partida
    def cambiar_nivel(self, nivel: Nivel) -> None:
        self.nivel = nivel
        self.nueva_partida()

    def nueva_partida(self) -> None:
        self._detener_reloj()
        self.tablero = Tablero(self.nivel)
        self.segundos = 0
        self._crear_casillas()
        self._actualizar()

    def _iniciar_reloj(self) -> None:
        if self._id_reloj is None:
            self._id_reloj = self.raiz.after(1000, self._tic)

    def _tic(self) -> None:
        self.segundos = min(self.segundos + 1, 999)
        self._id_reloj = self.raiz.after(1000, self._tic)
        self._actualizar_marcadores()

    def _detener_reloj(self) -> None:
        if self._id_reloj is not None:
            self.raiz.after_cancel(self._id_reloj)
            self._id_reloj = None

    # Eventos del ratón
    def _clic_izquierdo(self, f: int, c: int) -> None:
        if self.tablero.casillas[f][c].revelada:
            self._acorde(f, c)
            return
        self._iniciar_reloj()
        self.tablero.revelar(f, c)
        self._actualizar()

    def _clic_derecho(self, f: int, c: int) -> None:
        self.tablero.alternar_bandera(f, c)
        self._actualizar()

    def _acorde(self, f: int, c: int) -> None:
        self.tablero.revelar_vecinos(f, c)
        self._actualizar()

    # Dibujo
    def _actualizar(self) -> None:
        if self.tablero.terminado:
            self._detener_reloj()
        for f in range(self.nivel.filas):
            for c in range(self.nivel.columnas):
                self._pintar_casilla(f, c)
        self._actualizar_marcadores()

    def _actualizar_marcadores(self) -> None:
        self.lbl_minas.config(text=f"💣 {self.tablero.minas_restantes:03d}")
        self.lbl_tiempo.config(text=f"⏱ {self.segundos:03d}")
        if self.tablero.ganado:
            cara = "😎"
        elif self.tablero.perdido:
            cara = "😵"
        else:
            cara = "🙂"
        self.btn_cara.config(text=cara)

    def _pintar_casilla(self, f: int, c: int) -> None:
        casilla = self.tablero.casillas[f][c]
        lbl = self.botones[f][c]
        perdido = self.tablero.perdido

        if casilla.revelada:
            if casilla.es_mina:
                lbl.config(text="💣", bg=COLOR_EXPLOSION, relief="sunken", bd=1)
            else:
                n = casilla.minas_vecinas
                lbl.config(text=str(n) if n else "", bg=COLOR_REVELADA,
                           fg=COLORES_NUMEROS.get(n, "black"),
                           relief="sunken", bd=1)
        elif casilla.bandera:
            # Al perder, las banderas mal puestas se marcan con una X
            if perdido and not casilla.es_mina:
                lbl.config(text="❌", bg=COLOR_OCULTA, relief="raised", bd=2)
            else:
                lbl.config(text="🚩", bg=COLOR_OCULTA, relief="raised", bd=2)
        elif perdido and casilla.es_mina:
            lbl.config(text="💣", bg=COLOR_REVELADA, relief="sunken", bd=1)
        else:
            lbl.config(text="", bg=COLOR_OCULTA, relief="raised", bd=2)
