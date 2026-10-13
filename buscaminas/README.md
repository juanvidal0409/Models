# Buscaminas

Buscaminas clásico en Python con interfaz gráfica `tkinter` (no requiere
instalar nada adicional) y **3 niveles de dificultad**:

| Nivel   | Tablero | Minas |
|---------|---------|-------|
| Fácil   | 9 × 9   | 10    |
| Medio   | 16 × 16 | 40    |
| Difícil | 16 × 30 | 99    |

## Instalar tkinter

`tkinter` viene con Python, pero algunos sistemas lo separan en otro paquete.
Comprueba si lo tienes con:

```bash
python -m tkinter
```

Si se abre una ventanita, ya está. Si no, instálalo:

| Sistema           | Comando                                                        |
|-------------------|----------------------------------------------------------------|
| Windows / macOS   | Reinstalar Python desde python.org con la opción "tcl/tk and IDLE" |
| Ubuntu / Debian   | `sudo apt install python3-tk`                                  |
| Fedora            | `sudo dnf install python3-tkinter`                             |
| Arch              | `sudo pacman -S tk`                                            |
| macOS (Homebrew)  | `brew install python-tk`                                       |

Se necesita Python 3.10 o superior.

## Cómo jugar

```bash
cd buscaminas
python main.py
```

- **Clic izquierdo**: revela una casilla. El primer clic nunca es una mina.
- **Clic derecho**: pone o quita una bandera 🚩.
- **Clic izquierdo sobre un número** con todas sus banderas puestas:
  revela automáticamente las casillas vecinas restantes.
- Botón de la cara 🙂: reinicia la partida. Los botones superiores
  cambian de nivel.
- Se gana al revelar todas las casillas que no son minas.

## Archivos

- `niveles.py`: configuración de los 3 niveles (filas, columnas, minas).
- `tablero.py`: lógica del juego (colocación de minas, apertura en
  cascada, banderas, victoria y derrota), independiente de la interfaz.
- `interfaz.py`: ventana `tkinter`, contador de minas y cronómetro.
- `main.py`: punto de entrada.
- `test_tablero.py`: pruebas de la lógica (`python -m unittest test_tablero.py`).
