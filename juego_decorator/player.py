
# Personaje jugable con movimiento tipo Pac-Man (wrap-around en los bordes).

import math
import pygame

from game_object import GameObject
from constants import (
    SCREEN_W, SCREEN_H,
    PLAYER_SPEED, PLAYER_RADIUS,
    PLAYER_COLOR, PLAYER_EYE, MOUTH_COLOR,
)


class Player(GameObject):
    """
    Jugador controlado por teclado.
    Se mueve en 4 direcciones (WASD / flechas).
    Al salir por un borde reaparece en el opuesto usando el operador %.
    """

    def __init__(self, x: float, y: float):
        self.x = float(x)
        self.y = float(y)
        self.radius = PLAYER_RADIUS
        self.speed  = PLAYER_SPEED

        # Componentes de dirección del movimiento
        self.dx = 0.0
        self.dy = 0.0

        # Animación de la boca
        self.mouth_angle   = 0.0    # apertura en grados (0 = cerrado, 40 = abierto)
        self.mouth_speed   = 4.0    # grados por frame
        self.mouth_opening = True   # True = abriéndose, False = cerrándose

        # Ángulo de orientación del sprite (0° = mirando a la derecha)
        self.facing_angle = 0.0

    # Entrada de teclado 
    def handle_input(self) -> None:
        """Lee las teclas presionadas y actualiza dx/dy."""
        keys = pygame.key.get_pressed()
        self.dx = 0.0
        self.dy = 0.0

        if keys[pygame.K_LEFT]  or keys[pygame.K_a]: self.dx = -1
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]: self.dx =  1
        if keys[pygame.K_UP]    or keys[pygame.K_w]: self.dy = -1
        if keys[pygame.K_DOWN]  or keys[pygame.K_s]: self.dy =  1

        # Normaliza la velocidad en diagonal para que no sea más rápida
        if self.dx != 0 and self.dy != 0:
            self.dx *= 0.7071
            self.dy *= 0.7071

        # Actualiza el ángulo de orientación según la dirección
        if self.dx != 0 or self.dy != 0:
            self.facing_angle = math.degrees(math.atan2(self.dy, self.dx))

    # Lógica de actualización 
    def update(self, dt: float) -> None:
        """Mueve el jugador y aplica wrap-around en los cuatro bordes."""
        self.handle_input()

        self.x += self.dx * self.speed
        self.y += self.dy * self.speed

        # Wrap-around: al salir por un borde aparece en el opuesto
        self.x = self.x % SCREEN_W
        self.y = self.y % SCREEN_H

        # Anima la boca solo si el jugador se está moviendo
        if self.dx != 0 or self.dy != 0:
            if self.mouth_opening:
                self.mouth_angle += self.mouth_speed
                if self.mouth_angle >= 40:
                    self.mouth_opening = False
            else:
                self.mouth_angle -= self.mouth_speed
                if self.mouth_angle <= 0:
                    self.mouth_opening = True
        else:
            # Cierra la boca suavemente al detenerse
            self.mouth_angle = max(0, self.mouth_angle - self.mouth_speed)

    # ── Dibujo ────────────────────────────────
    def draw(self, surface: pygame.Surface) -> None:
        """Dibuja el jugador: cuerpo circular, boca animada y ojo."""
        cx, cy = int(self.x), int(self.y)
        r = self.radius

        # Sombra difusa debajo del personaje
        shadow = pygame.Surface((r * 2 + 10, r * 2 + 10), pygame.SRCALPHA)
        pygame.draw.circle(shadow, (0, 0, 0, 60), (r + 5, r + 5), r)
        surface.blit(shadow, (cx - r - 2, cy - r + 4))

        # Cuerpo amarillo
        pygame.draw.circle(surface, PLAYER_COLOR, (cx, cy), r)

        # Boca: polígono en forma de cuña (pie slice) sobre el cuerpo
        if self.mouth_angle > 0.5:
            angle_rad = math.radians(self.facing_angle)
            mouth_rad = math.radians(self.mouth_angle)
            pts = [(cx, cy)]
            steps = 12
            for i in range(steps + 1):
                a = angle_rad - mouth_rad + (2 * mouth_rad * i / steps)
                pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
            if len(pts) >= 3:
                pygame.draw.polygon(surface, MOUTH_COLOR, pts)

        # Ojo desplazado hacia arriba-adelante respecto a la dirección
        eye_x = int(r * 0.3 * math.cos(math.radians(self.facing_angle - 60)))
        eye_y = int(r * 0.3 * math.sin(math.radians(self.facing_angle - 60)))
        pygame.draw.circle(surface, PLAYER_EYE, (cx + eye_x, cy + eye_y), 4)

        # Borde brillante
        pygame.draw.circle(surface, (255, 240, 120), (cx, cy), r, 2)

    @property
    def pos(self) -> tuple:
        """Devuelve la posición actual como tupla (x, y)."""
        return (self.x, self.y)