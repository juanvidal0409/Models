
# Gestiona la creación, actualización y colisiones de los enemigos.

import math
import pygame
from enemy import Enemy
from constants import ENEMY_COUNT, ENEMY_RADIUS, PLAYER_RADIUS


class EnemyManager:
    """
    Crea y actualiza todos los enemigos.
    Detecta colisión con el jugador.
    Si el jugador tiene escudo (shield), los enemigos rebotan.
    """

    def __init__(self):
        self.enemies: list[Enemy] = [Enemy() for _ in range(ENEMY_COUNT)]

    def update(self, dt: float, player_x: float, player_y: float,  has_shield: bool = False) -> bool:
        """
        Actualiza todos los enemigos y devuelve True si alguno
        tocó al jugador (sin escudo).
        """
        hit = False
        for e in self.enemies:
            # Perseguir al jugador
            dx = player_x - e.x
            dy = player_y - e.y
            dist = math.hypot(dx, dy)
            if dist > 0:
                e.x += (dx / dist) * e.speed
                e.y += (dy / dist) * e.speed
            e.x %= 800   # wrap-around (usa valores directos para evitar import circular)
            e.y %= 600
            e.angle = (e.angle + 3) % 360

            # Detección de colisión con el jugador
            if dist < ENEMY_RADIUS + PLAYER_RADIUS:
                if has_shield:
                    # Rebota: invierte la dirección del enemigo
                    if dist > 0:
                        e.x -= (dx / dist) * (ENEMY_RADIUS + PLAYER_RADIUS - dist + 2)
                        e.y -= (dy / dist) * (ENEMY_RADIUS + PLAYER_RADIUS - dist + 2)
                else:
                    hit = True

        return hit

    def draw(self, surface: pygame.Surface) -> None:
        """Dibuja todos los enemigos."""
        for e in self.enemies:
            e.draw(surface)