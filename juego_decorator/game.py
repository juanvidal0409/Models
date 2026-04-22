
# Clase principal: inicialización, bucle principal, integración de todos los sistemas.

import pygame
import sys

from constants import (
    SCREEN_W, SCREEN_H, FPS, GAME_DURATION,
    BG_COLOR, GRID_COLOR, TIMER_WARN, TEXT_COLOR,
)
from player import Player
from decorators import TrailDecorator, TimerDecorator
from enemy_manager import EnemyManager
from power_up import PowerupManager


class Game:
    """
    Orquesta todos los sistemas del juego:
    - Jugador con decoradores (rastro + temporizador global)
    - Enemigos que persiguen al jugador
    - Potenciadores recogibles con efectos y bordes de color
    """

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
        pygame.display.set_caption("Pac-Decorator")
        self.clock = pygame.time.Clock()

        self._font_title  = pygame.font.SysFont("monospace", 48, bold=True)
        self._font_normal = pygame.font.SysFont("monospace", 22)
        self._font_small  = pygame.font.SysFont("monospace", 16)

        self._setup_game()

    # Inicialización
    def _setup_game(self) -> None:
        """Crea todos los objetos del juego y apila los decoradores."""
        # Jugador en el centro
        self._player = Player(SCREEN_W // 2, SCREEN_H // 2)

        # Decoradores: rastro visual + temporizador global
        with_trail = TrailDecorator(self._player, self._player)
        with_timer = TimerDecorator(with_trail, GAME_DURATION)

        self.game_object = with_timer
        self._timer_dec  = with_timer

        # Sistemas independientes
        self._enemies  = EnemyManager()
        self._powerups = PowerupManager()

        self.running   = True
        self.game_over = False
        self.player_hit = False     # True = el jugador fue tocado sin escudo

    #  Bucle principal 
    def run(self) -> None:
        while self.running:
            dt = self.clock.tick(FPS) / 1000.0

            self._handle_events()

            if not self.game_over:
                self._update(dt)

            self._render()

        pygame.quit()
        sys.exit()

    # Actualización 
    def _update(self, dt: float) -> None:
        """Actualiza todos los sistemas en orden."""

        # 1. Potenciadores: recolección y efectos activos
        self._powerups.update(
            dt, self._player.x, self._player.y, self._player.radius
        )

        # 2. Aplica efecto de velocidad al jugador
        self._player.speed_mult = 2.0 if self._powerups.has_speed else 1.0

        # 3. Actualiza el jugador (con decoradores)
        self.game_object.update(dt)

        # 4. Actualiza enemigos; detecta colisión con jugador
        hit = self._enemies.update(
            dt,
            self._player.x, self._player.y,
            has_shield=self._powerups.has_shield,
        )

        # 5. Condiciones de fin de partida
        if hit:
            self.game_over  = True
            self.player_hit = True
        if self._timer_dec.time_up:
            self.game_over  = True
            self.player_hit = False

    # ── Eventos ───────────────────────────────
    def _handle_events(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                if self.game_over and event.key == pygame.K_r:
                    self._setup_game()

    # ── Renderizado ───────────────────────────
    def _render(self) -> None:
        self.screen.fill(BG_COLOR)
        self._draw_grid()

        if self.game_over:
            # Dibuja la escena congelada antes del overlay
            self._draw_scene()
            self._draw_game_over()
        else:
            self._draw_scene()
            self._draw_hud()

        pygame.display.flip()

    def _draw_scene(self) -> None:
        """Dibuja todos los objetos del juego en orden de capas."""
        # 1. Potenciadores en el suelo (capa inferior)
        self._powerups.draw_items(self.screen)

        # 2. Bordes de potenciadores activos (debajo del jugador)
        self._powerups.draw_borders(
            self.screen,
            self._player.x, self._player.y, self._player.radius
        )

        # 3. Jugador con rastro (los decoradores dibujan trail → player)
        self.game_object.draw(self.screen)

        # 4. Enemigos (encima del jugador para que sean visibles)
        self._enemies.draw(self.screen)

        # 5. HUD de potenciadores activos (esquina superior derecha)
        self._powerups.draw_hud(self.screen)

    def _draw_grid(self) -> None:
        """Cuadrícula sutil de fondo."""
        step = 40
        for x in range(0, SCREEN_W, step):
            pygame.draw.line(self.screen, GRID_COLOR, (x, 0), (x, SCREEN_H))
        for y in range(0, SCREEN_H, step):
            pygame.draw.line(self.screen, GRID_COLOR, (0, y), (SCREEN_W, y))

    def _draw_hud(self) -> None:
        """Controles en la esquina inferior izquierda."""
        hints = [
            "WASD / flechas  Mover",
            "ESC             Salir",
        ]
        for i, h in enumerate(hints):
            surf = self._font_small.render(h, True, (80, 80, 120))
            self.screen.blit(surf, (12, SCREEN_H - 14 - i * 18))

    def _draw_game_over(self) -> None:
        """Pantalla de fin de partida con motivo (tiempo / capturado)."""
        overlay = pygame.Surface((SCREEN_W, SCREEN_H), pygame.SRCALPHA)
        overlay.fill((10, 10, 25, 210))
        self.screen.blit(overlay, (0, 0))

        if self.player_hit:
            title_txt = "Atrapado!"
            title_clr = (255, 80, 80)
        else:
            title_txt = "Tiempo!"
            title_clr = TIMER_WARN

        title = self._font_title.render(title_txt,                    True, title_clr)
        sub   = self._font_normal.render("Presiona  R  para reiniciar", True, TEXT_COLOR)
        esc   = self._font_small.render("ESC para salir",               True, (100, 100, 140))

        cx, cy = SCREEN_W // 2, SCREEN_H // 2
        self.screen.blit(title, (cx - title.get_width() // 2, cy - 70))
        self.screen.blit(sub,   (cx - sub.get_width()   // 2, cy + 10))
        self.screen.blit(esc,   (cx - esc.get_width()   // 2, cy + 50))