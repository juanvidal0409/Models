
# Constantes globales compartidas por todos los módulos del juego.

# Pantalla y tiempo 
SCREEN_W, SCREEN_H = 800, 600
FPS = 60
GAME_DURATION = 60        # duración de la partida en segundos

# Jugador
PLAYER_SPEED  = 4
PLAYER_RADIUS = 22

# Enemigos 
ENEMY_RADIUS  = 14
ENEMY_SPEED   = 1.8
ENEMY_COUNT   = 4         # número inicial de enemigos

# Potenciadores 
POWERUP_RADIUS   = 12
POWERUP_DURATION = 5.0    # segundos que dura cada potenciador activo
POWERUP_COUNT    = 3      # número de potenciadores en pantalla a la vez

# Colores y nombres de los 3 potenciadores disponibles
POWERUP_DEFS = [
    {"name": "speed",   "color": (80,  200, 255)},   # azul  → velocidad x2
    {"name": "shield",  "color": (80,  255, 140)},   # verde → escudo (rebota enemigos)
    {"name": "magnet",  "color": (255, 100, 200)},   # rosa  → atrae potenciadores cercanos
]

#  Paleta de colores 
BG_COLOR     = (15,  15,  30)
GRID_COLOR   = (25,  25,  50)
PLAYER_COLOR = (255, 220, 50)
PLAYER_EYE   = (15,  15,  30)
MOUTH_COLOR  = (15,  15,  30)
TIMER_BG     = (30,  30,  55)
TIMER_FG     = (255, 220, 50)
TIMER_WARN   = (255, 80,  80)
TRAIL_COLOR  = (255, 220, 50)
TEXT_COLOR   = (200, 200, 220)
ENEMY_COLOR  = (220, 60,  60)