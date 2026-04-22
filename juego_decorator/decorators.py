
# Implementaciones del Patrón Decorator para el juego.

import math
import pygame

from game_object import GameObject
from player import Player
from constants import (
    SCREEN_W, SCREEN_H,
    TIMER_BG, TIMER_FG, TIMER_WARN,
    TRAIL_COLOR, PLAYER_RADIUS,
)


# ─────────────────────────────────────────────
#  BASE DEL DECORATOR
# ─────────────────────────────────────────────
class GameObjectDecorator(GameObject):
    """
    Decorador base: envuelve cualquier GameObject y delega
    update/draw hacia él. Las subclases extienden ese comportamiento.
    """

    def __init__(self, wrapped: GameObject):
        self._wrapped = wrapped     # objeto decorado

    def update(self, dt: float) -> None:
        self._wrapped.update(dt)

    def draw(self, surface: pygame.Surface) -> None:
        self._wrapped.draw(surface)


# ─────────────────────────────────────────────
#  DECORADOR: Temporizador regresivo
# ─────────────────────────────────────────────
class TimerDecorator(GameObjectDecorator):
    """
    Añade un temporizador regresivo en pantalla.
    Expone time_up = True cuando el tiempo llega a cero.
    """

    def __init__(self, wrapped: GameObject, duration: float):
        super().__init__(wrapped)
        self.total     = duration       # duración total en segundos
        self.remaining = duration       # tiempo restante
        self.time_up   = False          # bandera de fin de tiempo

        # Fuentes para la UI del temporizador
        self._font_large = pygame.font.SysFont("monospace", 28, bold=True)

    def update(self, dt: float) -> None:
        super().update(dt)
        if not self.time_up:
            self.remaining = max(0.0, self.remaining - dt)
            if self.remaining == 0:
                self.time_up = True

    def draw(self, surface: pygame.Surface) -> None:
        super().draw(surface)

        bar_w = 200
        bar_h = 18
        bar_x = SCREEN_W // 2 - bar_w // 2
        bar_y = 12

        # Fondo de la barra
        pygame.draw.rect(surface, TIMER_BG, (bar_x - 2, bar_y - 2, bar_w + 4, bar_h + 4),border_radius=5)
        # Relleno proporcional al tiempo restante
        ratio = self.remaining / self.total
        color = TIMER_WARN if ratio < 0.3 else TIMER_FG
        fill_w = int(bar_w * ratio)
        if fill_w > 0:
            pygame.draw.rect(surface, color,(bar_x, bar_y, fill_w, bar_h), border_radius=4)

        # Borde de la barra
        pygame.draw.rect(surface, color, (bar_x - 2, bar_y - 2, bar_w + 4, bar_h + 4), 2, border_radius=5)

        # Número de segundos restantes
        secs  = int(math.ceil(self.remaining))
        label = self._font_large.render(f"{secs:02d}s", True, color)
        surface.blit(label, (SCREEN_W // 2 - label.get_width() // 2,bar_y + bar_h + 4))



#  DECORADOR Rastro de movimiento
class TrailDecorator(GameObjectDecorator):
    """
    Añade un rastro visual detrás del jugador.
    Guarda las últimas MAX_TRAIL posiciones y las dibuja
    con tamaño y opacidad crecientes hacia el frente.
    """

    MAX_TRAIL = 18      # número máximo de puntos en el rastro

    def __init__(self, wrapped: GameObject, player: Player):
        super().__init__(wrapped)
        self._player = player               # referencia al jugador para leer su posición
        self._trail: list[tuple] = []       # historial de posiciones (x, y)

    def update(self, dt: float) -> None:
        # Guarda la posición ANTES de que el jugador se mueva
        self._trail.append(self._player.pos)
        if len(self._trail) > self.MAX_TRAIL:
            self._trail.pop(0)
        super().update(dt)

    def draw(self, surface: pygame.Surface) -> None:
        # Dibuja el rastro primero para que quede detrás del jugador
        n = len(self._trail)
        for i, (tx, ty) in enumerate(self._trail):
            alpha  = int(180 * (i + 1) / n)
            radius = max(3, int(PLAYER_RADIUS * 0.5 * (i + 1) / n))
            # Superficie temporal con canal alpha para transparencia
            s = pygame.Surface((radius * 2 + 2, radius * 2 + 2), pygame.SRCALPHA)
            r, g, b = TRAIL_COLOR
            pygame.draw.circle(s, (r, g, b, alpha), (radius + 1, radius + 1), radius)
            surface.blit(s, (int(tx) - radius - 1, int(ty) - radius - 1))
        super().draw(surface)