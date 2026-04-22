import pygame
from abc import ABC, abstractmethod
class GameObject(ABC):
    """
    Clase abstracta que define la interfaz mínima
    que debe implementar cualquier objeto del juego.
    """
    @abstractmethod
    def update(self, dt: float) -> None:
        """Actualiza el estado lógico del objeto. dt = delta time en segundos."""
    @abstractmethod
    def draw(self, surface: pygame.Surface) -> None:
        """Dibuja el objeto en la superficie de pygame dada."""