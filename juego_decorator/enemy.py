
# Enemigo sencillo que persigue al jugador con movimiento suave.

import math
import random
import pygame

from GameObject import GameObject
from constants import (
    SCREEN_W, SCREEN_H,
    ENEMY_RADIUS, ENEMY_SPEED, ENEMY_COLOR,
)


class Enemy(GameObject):
    """
    Enemigo triangular que sigue al jugador.
    Aparece en un borde aleatorio y aplica wrap-around igual que el jugador.
    """

    def __init__(self):
        # Posición aleatoria en los bordes de la pantalla
        side = random.randint(0, 3)
        if side == 0:   self.x, self.y = random.randint(0, SCREEN_W), 0
        elif side == 1: self.x, self.y = SCREEN_W, random.randint(0, SCREEN_H)
        elif side == 2: self.x, self.y = random.randint(0, SCREEN_W), SCREEN_H
        else:           self.x, self.y = 0, random.randint(0, SCREEN_H)

        self.x = float(self.x)
        self.y = float(self.y)
        self.radius = ENEMY_RADIUS
        self.speed  = ENEMY_SPEED + random.uniform(-0.4, 0.4)  # ligera variación

        # Ángulo de rotación del triángulo (gira continuamente)
        self.angle = random.uniform(0, 360)

    #  Lógica 
    def update(self, dt: float, target_x: float = 0, target_y: float = 0) -> None:
        """Persigue la posición del jugador y aplica wrap-around."""
        # Dirección hacia el jugador
        dx = target_x - self.x
        dy = target_y - self.y
        dist = math.hypot(dx, dy)

        if dist > 0:
            self.x += (dx / dist) * self.speed
            self.y += (dy / dist) * self.speed

        # Wrap-around igual que el jugador
        self.x = self.x % SCREEN_W
        self.y = self.y % SCREEN_H

        # Rota el sprite suavemente
        self.angle = (self.angle + 3) % 360

    # update sin argumentos extra (requerido por la interfaz GameObject)
    def update(self, dt: float) -> None:  # type: ignore[override]
        pass  # se llama desde EnemyManager con target

    #  Dibujo 
    def draw(self, surface: pygame.Surface) -> None:
        """Dibuja el enemigo como un triángulo rojo rotante."""
        cx, cy = int(self.x), int(self.y)
        r = self.radius

        # Tres vértices del triángulo separados 120°
        pts = []
        for i in range(3):
            a = math.radians(self.angle + i * 120)
            pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))

        # Relleno
        pygame.draw.polygon(surface, ENEMY_COLOR, pts)
        # Borde blanco para que resalte
        pygame.draw.polygon(surface, (255, 180, 180), pts, 2)

        # Punto central (ojo)
        pygame.draw.circle(surface, (255, 255, 255), (cx, cy), 3)

    @property
    def pos(self) -> tuple:
        return (self.x, self.y)