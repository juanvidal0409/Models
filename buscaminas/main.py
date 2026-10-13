
# Punto de entrada del Buscaminas.

import sys

try:
    import tkinter as tk
except ImportError:
    sys.exit(
        "No se encontró tkinter, necesario para la ventana del juego.\n"
        "Instálalo según tu sistema:\n"
        "  - Windows / macOS: reinstala Python desde python.org marcando\n"
        "    la opción 'tcl/tk and IDLE' (viene marcada por defecto).\n"
        "  - Ubuntu / Debian: sudo apt install python3-tk\n"
        "  - Fedora:          sudo dnf install python3-tkinter\n"
        "  - Arch:            sudo pacman -S tk\n"
        "  - macOS (Homebrew): brew install python-tk"
    )

from interfaz import Buscaminas


def main() -> None:
    raiz = tk.Tk()
    Buscaminas(raiz)
    raiz.mainloop()


if __name__ == "__main__":
    main()
