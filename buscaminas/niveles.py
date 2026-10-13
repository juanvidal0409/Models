
# Configuración de los 3 niveles de dificultad del Buscaminas.

from dataclasses import dataclass


@dataclass(frozen=True)
class Nivel:
    """Describe las dimensiones del tablero y la cantidad de minas."""
    nombre: str
    filas: int
    columnas: int
    minas: int


FACIL   = Nivel("Fácil",   9,  9,  10)
MEDIO   = Nivel("Medio",   16, 16, 40)
DIFICIL = Nivel("Difícil", 16, 30, 99)

NIVELES = [FACIL, MEDIO, DIFICIL]
