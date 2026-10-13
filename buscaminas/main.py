
# Punto de entrada del Buscaminas.

import tkinter as tk

from interfaz import Buscaminas


def main() -> None:
    raiz = tk.Tk()
    Buscaminas(raiz)
    raiz.mainloop()


if __name__ == "__main__":
    main()
