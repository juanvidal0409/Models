
# Lógica del Buscaminas, independiente de la interfaz gráfica.

import random

from niveles import Nivel


class Casilla:
    """Una celda del tablero."""

    def __init__(self):
        self.es_mina = False
        self.revelada = False
        self.bandera = False
        self.minas_vecinas = 0


class Tablero:
    """
    Mantiene el estado de una partida:
    - Las minas se colocan en el primer clic, de modo que la primera
      casilla revelada (y sus vecinas) nunca tenga mina.
    - Revelar una casilla sin minas vecinas abre en cascada su zona.
    """

    def __init__(self, nivel: Nivel, semilla=None):
        self.nivel = nivel
        self.filas = nivel.filas
        self.columnas = nivel.columnas
        self.total_minas = nivel.minas
        self._random = random.Random(semilla)
        self.casillas = [[Casilla() for _ in range(self.columnas)]
                         for _ in range(self.filas)]
        self.minas_colocadas = False
        self.perdido = False
        self.ganado = False
        self.reveladas = 0
        self.banderas = 0

    # Consultas
    def vecinos(self, fila: int, col: int):
        """Genera las coordenadas de las (hasta 8) casillas vecinas."""
        for df in (-1, 0, 1):
            for dc in (-1, 0, 1):
                if df == 0 and dc == 0:
                    continue
                f, c = fila + df, col + dc
                if 0 <= f < self.filas and 0 <= c < self.columnas:
                    yield f, c

    @property
    def terminado(self) -> bool:
        return self.perdido or self.ganado

    @property
    def minas_restantes(self) -> int:
        """Contador mostrado al jugador: minas menos banderas puestas."""
        return self.total_minas - self.banderas

    # Preparación
    def _colocar_minas(self, fila_segura: int, col_segura: int) -> None:
        zona_segura = {(fila_segura, col_segura)}
        zona_segura.update(self.vecinos(fila_segura, col_segura))
        candidatas = [(f, c) for f in range(self.filas)
                      for c in range(self.columnas)
                      if (f, c) not in zona_segura]
        # Si el tablero es muy pequeño, solo se protege la casilla pulsada
        if len(candidatas) < self.total_minas:
            candidatas = [(f, c) for f in range(self.filas)
                          for c in range(self.columnas)
                          if (f, c) != (fila_segura, col_segura)]

        for f, c in self._random.sample(candidatas, self.total_minas):
            self.casillas[f][c].es_mina = True

        for f in range(self.filas):
            for c in range(self.columnas):
                self.casillas[f][c].minas_vecinas = sum(
                    self.casillas[vf][vc].es_mina
                    for vf, vc in self.vecinos(f, c))
        self.minas_colocadas = True

    # Acciones del jugador
    def revelar(self, fila: int, col: int) -> None:
        """Revela una casilla. Si es mina, la partida se pierde."""
        if self.terminado:
            return
        casilla = self.casillas[fila][col]
        if casilla.revelada or casilla.bandera:
            return
        if not self.minas_colocadas:
            self._colocar_minas(fila, col)

        if casilla.es_mina:
            casilla.revelada = True
            self.perdido = True
            return

        # Apertura en cascada (iterativa para evitar recursión profunda)
        pendientes = [(fila, col)]
        while pendientes:
            f, c = pendientes.pop()
            actual = self.casillas[f][c]
            if actual.revelada or actual.bandera:
                continue
            actual.revelada = True
            self.reveladas += 1
            if actual.minas_vecinas == 0:
                pendientes.extend(self.vecinos(f, c))

        self._comprobar_victoria()

    def revelar_vecinos(self, fila: int, col: int) -> None:
        """
        "Acorde": sobre un número ya revelado con tantas banderas
        alrededor como su valor, revela el resto de vecinas.
        """
        casilla = self.casillas[fila][col]
        if self.terminado or not casilla.revelada or casilla.minas_vecinas == 0:
            return
        banderas = sum(self.casillas[f][c].bandera
                       for f, c in self.vecinos(fila, col))
        if banderas != casilla.minas_vecinas:
            return
        for f, c in self.vecinos(fila, col):
            self.revelar(f, c)

    def alternar_bandera(self, fila: int, col: int) -> None:
        if self.terminado:
            return
        casilla = self.casillas[fila][col]
        if casilla.revelada:
            return
        casilla.bandera = not casilla.bandera
        self.banderas += 1 if casilla.bandera else -1

    def _comprobar_victoria(self) -> None:
        if self.reveladas == self.filas * self.columnas - self.total_minas:
            self.ganado = True
            # Al ganar se marcan automáticamente todas las minas
            for fila in self.casillas:
                for casilla in fila:
                    if casilla.es_mina and not casilla.bandera:
                        casilla.bandera = True
                        self.banderas += 1
