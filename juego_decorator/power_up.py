
# Potenciador recogible en el mapa y gestor de potenciadores activos.

import math
import random
import pygame

from Constants import (
    SCREEN_W, SCREEN_H,
    POWERUP_RADIUS, POWERUP_DURATION, POWERUP_DEFS,
)


# 
#  OBJETO: Un potenciador en el mapa
#
class Powerup:
    """
    Ítem recogible en el suelo.
    Tiene un tipo (speed / shield / magnet), color y posición aleatoria.
    """

    def __init__(self):
        # Elige un tipo aleatorio de los 3 definidos
        defn       = random.choice(POWERUP_DEFS)
        self.name  = defn["name"]
        self.color = defn["color"]

        # Posición aleatoria con margen para no salir de pantalla
        margin = POWERUP_RADIUS + 20
        self.x = float(random.randint(margin, SCREEN_W - margin))
        self.y = float(random.randint(margin, SCREEN_H - margin))

        self.radius  = POWERUP_RADIUS
        self._pulse  = 0.0      # fase de animación de pulso

    def update(self, dt: float) -> None:
        """Anima el pulso del ícono."""
        self._pulse = (self._pulse + dt * 3) % (2 * math.pi)

    def draw(self, surface: pygame.Surface) -> None:
        """Dibuja el potenciador como un diamante pulsante."""
        cx, cy = int(self.x), int(self.y)
        r = self.radius + int(math.sin(self._pulse) * 3)   # radio pulsante

        # Diamante
        pts = [
            (cx,     cy - r),
            (cx + r, cy    ),
            (cx,     cy + r),
            (cx - r, cy    ),
        ]
        pygame.draw.polygon(surface, self.color, pts)
        pygame.draw.polygon(surface, (255, 255, 255), pts, 2)

        # Inicial del tipo en el centro
        font = pygame.font.SysFont("monospace", 11, bold=True)
        label = font.render(self.name[0].upper(), True, (255, 255, 255))
        surface.blit(label, (cx - label.get_width() // 2,
                             cy - label.get_height() // 2))

    def collides_with(self, px: float, py: float, pr: float) -> bool:
        """Devuelve True si el jugador (px, py, radio pr) toca este potenciador."""
        return math.hypot(px - self.x, py - self.y) < self.radius + pr


#  GESTOR: potenciadores en mapa y activos

class PowerupManager:
    """
    Mantiene los potenciadores en el suelo y los activos sobre el jugador.

    Potenciadores activos:
    - Se almacenan en self.active como lista de dicts:
            {"name": str, "color": tuple, "remaining": float}
    - No se acumulan repetidos: si ya está activo, se renueva el tiempo.
    - Si hay varios activos, se dibujan todos los bordes apilados.
    """

    def __init__(self):
        # Ítems en el suelo (hasta POWERUP_COUNT distintos)
        self.items: list[Powerup] = [Powerup() for _ in range(3)]

        # Efectos activos sobre el jugador
        self.active: list[dict] = []

    #  Propiedades de estado
    @property
    def has_speed(self) -> bool:
        return any(a["name"] == "speed" for a in self.active)

    @property
    def has_shield(self) -> bool:
        return any(a["name"] == "shield" for a in self.active)

    @property
    def has_magnet(self) -> bool:
        return any(a["name"] == "magnet" for a in self.active)

    # Actualización 
    def update(self, dt: float, player_x: float, player_y: float,
               player_radius: float) -> None:
        """
        - Mueve ítems hacia el jugador si el imán está activo.
        - Detecta recolección de ítems.
        - Descuenta tiempo de efectos activos y los elimina al expirar.
        - Repone ítems recogidos con uno nuevo.
        """
        # Efecto imán: acerca los ítems al jugador
        if self.has_magnet:
            for item in self.items:
                dx = player_x - item.x
                dy = player_y - item.y
                dist = math.hypot(dx, dy)
                if 0 < dist < 250:
                    item.x += (dx / dist) * 2.5
                    item.y += (dy / dist) * 2.5

        # Animar y detectar colisión
        nuevos = []
        for item in self.items:
            item.update(dt)
            if item.collides_with(player_x, player_y, player_radius):
                self._activar(item.name, item.color)
                # Repone con un ítem nuevo en posición distinta
                nuevos.append(Powerup())
            else:
                nuevos.append(item)
        self.items = nuevos

        # Descuenta el tiempo de los efectos activos
        self.active = [
            {**a, "remaining": a["remaining"] - dt}
            for a in self.active
            if a["remaining"] - dt > 0
        ]

    def _activar(self, name: str, color: tuple) -> None:
        """
        Activa un efecto. Si ya estaba activo lo renueva; si no, lo agrega.
        """
        for a in self.active:
            if a["name"] == name:
                a["remaining"] = POWERUP_DURATION  # renovar tiempo
                return
        # Nuevo efecto
        self.active.append({
            "name": name,
            "color": color,
            "remaining": POWERUP_DURATION,
        })

    #  Dibujo 
    def draw_items(self, surface: pygame.Surface) -> None:
        """Dibuja los potenciadores en el suelo."""
        for item in self.items:
            item.draw(surface)

    def draw_borders(self, surface: pygame.Surface,player_x: float, player_y: float,player_radius: float) -> None:
        """
        Dibuja un borde de color por cada potenciador activo, apilados
        uno encima del otro (anillo exterior → interior).
        """
        cx, cy = int(player_x), int(player_y)
        for i, a in enumerate(self.active):
            r = player_radius + 5 + i * 6          # cada borde un poco más grande
            pygame.draw.circle(surface, a["color"], (cx, cy), r, 3)

    def draw_hud(self, surface: pygame.Surface) -> None:
        """
        Dibuja los indicadores de potenciadores activos en la esquina
        superior derecha con su barra de tiempo restante.
        """
        if not self.active:
            return

        font = pygame.font.SysFont("monospace", 13, bold=True)
        x0   = surface.get_width() - 160
        y0   = 14

        for i, a in enumerate(self.active):
            y = y0 + i * 30
            ratio = a["remaining"] / POWERUP_DURATION
            color = a["color"]

            # Barra de fondo
            pygame.draw.rect(surface, (30, 30, 55), (x0, y, 140, 14), border_radius=4)
            # Barra de progreso
            fill = int(140 * ratio)
            if fill > 0:
                pygame.draw.rect(surface, color, (x0, y, fill, 14), border_radius=4)
            # Borde
            pygame.draw.rect(surface, color, (x0, y, 140, 14), 2, border_radius=4)

            # Nombre y tiempo
            label = font.render(
                f"{a['name'][:6]}  {a['remaining']:.1f}s", True, (220, 220, 220)
            )
            surface.blit(label, (x0 + 4, y - 1))