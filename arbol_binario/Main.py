from Numero import Numero
from Suma import Suma
from Resta import Resta
from Multiplicacion import Multiplicacion
from Print import imprimir_arbol

# construye la expresión (5 + 3) * (10 - 2)
expr = Multiplicacion(
    Suma(Numero(5), Numero(3)),
    Resta(Numero(10), Numero(2))
)

print("Árbol:")
imprimir_arbol(expr)

print("\nResultado:", expr.evaluar())