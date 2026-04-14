from Expresion import Expresion

# representa un número (hoja del árbol)
class Numero(Expresion):
    
    def __init__(self, valor):
        self.valor = valor  # guarda el valor

    def evaluar(self):
        return self.valor  # retorna el número