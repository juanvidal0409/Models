from Expresion import Expresion

# clase base para operaciones (+, -, *, /)
class Operacion(Expresion):
    
    def __init__(self, izquierda, derecha):
        self.izquierda = izquierda  # hijo izquierdo
        self.derecha = derecha     # hijo derecho