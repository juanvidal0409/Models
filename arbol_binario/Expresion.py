# clase base para todas las expresiones
from abc import ABC, abstractmethod

class Expresion(ABC):
    
    @abstractmethod
    def evaluar(self):
        pass