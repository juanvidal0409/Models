from Operacion import Operacion

# operación división
class Division(Operacion):
    
    def evaluar(self):
        if self.derecha.evaluar() == 0:
            raise ZeroDivisionError("División por cero")
        return self.izquierda.evaluar() / self.derecha.evaluar()