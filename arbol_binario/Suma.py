from Operacion import Operacion

# operación suma
class Suma(Operacion):
    
    def evaluar(self):
        return self.izquierda.evaluar() + self.derecha.evaluar()