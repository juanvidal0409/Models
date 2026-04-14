from Numero import Numero
from Suma import Suma
from Resta import Resta
from Multiplicacion import Multiplicacion
from Division import Division

# obtiene símbolo según el tipo
def obtener_simbolo(expr):
    
    if isinstance(expr, Suma):
        return "+"
    elif isinstance(expr, Resta):
        return "-"
    elif isinstance(expr, Multiplicacion):
        return "*"
    elif isinstance(expr, Division):
        return "/"
    elif isinstance(expr, Numero):
        return str(expr.valor)


# imprime el árbol con ramas
def imprimir_arbol(expr, prefijo="", es_ultimo=True):
    
    print(prefijo + ("└── " if es_ultimo else "├── ") + obtener_simbolo(expr))
    
    if not isinstance(expr, Numero):
        nuevo_prefijo = prefijo + ("    " if es_ultimo else "│   ")
        
        imprimir_arbol(expr.izquierda, nuevo_prefijo, False)
        imprimir_arbol(expr.derecha, nuevo_prefijo, True)