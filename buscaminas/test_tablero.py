
# Pruebas de la lógica del tablero:  python -m unittest test_tablero.py

import unittest

from niveles import NIVELES, FACIL, Nivel
from tablero import Tablero


class TestTablero(unittest.TestCase):

    def test_niveles_tienen_minas_correctas(self):
        for nivel in NIVELES:
            t = Tablero(nivel, semilla=1)
            t.revelar(0, 0)
            minas = sum(c.es_mina for fila in t.casillas for c in fila)
            self.assertEqual(minas, nivel.minas)

    def test_primer_clic_es_seguro(self):
        for semilla in range(50):
            t = Tablero(FACIL, semilla=semilla)
            t.revelar(4, 4)
            self.assertFalse(t.perdido)
            for f, c in t.vecinos(4, 4):
                self.assertFalse(t.casillas[f][c].es_mina)

    def test_bandera_impide_revelar_y_actualiza_contador(self):
        t = Tablero(FACIL, semilla=2)
        t.alternar_bandera(0, 0)
        self.assertEqual(t.minas_restantes, FACIL.minas - 1)
        t.revelar(0, 0)
        self.assertFalse(t.casillas[0][0].revelada)
        t.alternar_bandera(0, 0)
        self.assertEqual(t.minas_restantes, FACIL.minas)

    def test_revelar_mina_pierde(self):
        t = Tablero(FACIL, semilla=3)
        t.revelar(4, 4)
        f, c = next((f, c) for f in range(9) for c in range(9)
                    if t.casillas[f][c].es_mina)
        t.revelar(f, c)
        self.assertTrue(t.perdido)

    def test_revelar_todo_gana(self):
        t = Tablero(FACIL, semilla=4)
        t.revelar(4, 4)
        for f in range(9):
            for c in range(9):
                if not t.casillas[f][c].es_mina:
                    t.revelar(f, c)
        self.assertTrue(t.ganado)
        self.assertEqual(t.minas_restantes, 0)

    def test_acorde_revela_vecinas(self):
        t = Tablero(Nivel("prueba", 3, 3, 1))
        t.casillas[0][0].es_mina = True
        for f in range(3):
            for c in range(3):
                t.casillas[f][c].minas_vecinas = sum(
                    t.casillas[vf][vc].es_mina for vf, vc in t.vecinos(f, c))
        t.minas_colocadas = True
        t.revelar(1, 1)
        t.alternar_bandera(0, 0)
        t.revelar_vecinos(1, 1)
        self.assertTrue(t.ganado)
        self.assertFalse(t.perdido)

if __name__ == "__main__":
    unittest.main()
