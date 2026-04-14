from Operacion import Operacion

# operación resta
class Resta(Operacion):
    
    def evaluar(self):
        return self.izquierda.evaluar() - self.derecha.evaluar()