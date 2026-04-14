from Operacion import Operacion

# operación multiplicación
class Multiplicacion(Operacion):
    
    def evaluar(self):
        return self.izquierda.evaluar() * self.derecha.evaluar()