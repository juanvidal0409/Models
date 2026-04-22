
 EXPLICACIÓN DEL CÓDIGO


El juego usa el Patrón Decorator de la Programación Orientada a
Objetos. La idea es que en lugar de crear una clase gigante con
todo, se "envuelven" objetos uno dentro de otro para agregar
funcionalidades sin modificar el original.


  ARCHIVOS Y CLASES



  constants.py 

Almacena todos los valores fijos del juego en un solo lugar:
tamaño de pantalla, velocidades, colores, duración del timer,
configuración de los 3 potenciadores, etc.

Tenerlos aquí evita números "mágicos" dispersos por el código
y facilita ajustar el juego cambiando un solo archivo.


  game_object.py  →  clase GameObject

Es la interfaz base (clase abstracta) que deben cumplir todos
los objetos del juego. Define dos métodos obligatorios:

  - update(dt): actualiza la lógica del objeto.
                dt es el tiempo transcurrido en segundos desde
                el último frame (delta time), lo que hace que
                el juego corra igual de rápido sin importar los
                FPS de la máquina.

  - draw(surface): dibuja el objeto en la pantalla.

Cualquier clase que herede de GameObject DEBE implementar
estos dos métodos, o Python lanzará un error.


  player.py  →  clase Player

Representa al personaje amarillo controlable por el jugador.
Hereda de GameObject.

Responsabilidades:
  - Leer el teclado (WASD / flechas) en handle_input().
  - Mover el personaje sumando dx/dy a la posición.
  - Aplicar wrap-around con el operador %:
        self.x = self.x % SCREEN_W
    Al salir por la derecha, reaparece por la izquierda, etc.
  - Animar la boca: abre y cierra un ángulo mientras se mueve.
  - Dibujar el cuerpo circular, la boca (polígono tipo cuña),
    el ojo y el borde brillante.
  - Exponer speed_mult: si un potenciador de velocidad está
    activo, game.py ajusta este valor a 2.0 y el jugador se
    mueve el doble de rápido.


  decorators.py  →  3 clases


  GameObjectDecorator (base del patrón)
  
  Envuelve cualquier GameObject. Su update() y draw() solo
  delegan al objeto interno (self._wrapped). Las subclases
  heredan esto y agregan su comportamiento extra.

  TrailDecorator
  
  Agrega el rastro visual amarillo detrás del jugador.
  Guarda las últimas 18 posiciones del jugador en una lista.
  En draw() las dibuja ANTES que el jugador (para que queden
  detrás), con tamaño y opacidad crecientes hacia el frente,
  usando superficies con canal alpha (SRCALPHA).

  TimerDecorator
  
  Agrega el temporizador global de la partida (60 segundos).
  En update() resta dt a self.remaining y activa time_up=True
  cuando llega a cero. En draw() dibuja la barra de progreso
  centrada en la parte superior y el número de segundos.
  Cambia a color rojo cuando queda menos del 30% del tiempo.


  enemy.py  →  clase Enemy

Representa un enemigo individual: un triángulo rojo rotante.

  - Aparece en un borde aleatorio de la pantalla al crearse.
  - Su lógica de movimiento (perseguir al jugador) la maneja
    EnemyManager, no la clase Enemy directamente, para mantener
    esta clase simple y solo responsable de dibujarse.
  - draw() construye los 3 vértices del triángulo girando 120°
    entre cada uno alrededor del centro, y los rota cada frame.


  enemy_manager.py  →  clase EnemyManager

Gestiona la lista de todos los enemigos activos.

  - Crea ENEMY_COUNT enemigos al iniciar.
  - En update() mueve cada enemigo hacia el jugador calculando
    la dirección con atan2/hypot y sumando a su posición.
  - Aplica wrap-around a los enemigos también.
  - Detecta colisión midiendo la distancia entre el centro del
    enemigo y el jugador; si es menor que la suma de los radios,
    hay colisión.
  - Si el jugador tiene escudo activo, en vez de marcar hit=True
    empuja al enemigo en dirección contraria (rebote).
  - Devuelve hit=True a game.py para que este decida si terminar
    la partida.


  power_up.py  →  2 clases


  Powerup
  
  Un ítem recogible en el suelo. Tiene un tipo aleatorio entre
  los 3 definidos en constants.py (speed, shield, magnet).
  Se dibuja como un diamante pulsante con la inicial del tipo.
  collides_with() comprueba si el jugador lo tocó.

  PowerupManager
  
  Gestiona todos los potenciadores del juego, tanto los que
  están en el suelo como los que están activos sobre el jugador.

  Ítems en el suelo:
    - Siempre hay 3 en pantalla. Cuando uno es recogido,
      se reemplaza automáticamente por uno nuevo.

  Efectos activos (self.active):
    - Es una lista de dicts: {name, color, remaining}.
    - _activar() agrega un nuevo efecto O renueva el tiempo si
      el mismo tipo ya estaba activo (no se acumulan duplicados).
    - En update() se descuenta dt de remaining y se eliminan
      los que llegaron a 0.

  Efecto imán:
    - Si has_magnet es True, cada ítem en el suelo que esté
      a menos de 250px del jugador se mueve hacia él.

  draw_borders():
    - Por cada efecto activo dibuja un anillo de su color
      alrededor del jugador, apilados hacia afuera.
    - Si hay 3 activos: 3 anillos concéntricos de 3 colores.

  draw_hud():
    - Muestra en la esquina superior derecha una barra por cada
      efecto activo con su nombre y el tiempo restante (5s).


  game.py  →  clase Game

Clase principal que orquesta todo el juego.

  __init__():
    Inicializa pygame, crea la ventana y llama a _setup_game().

  _setup_game():
    Crea el Player, le apila TrailDecorator y TimerDecorator,
    y crea el EnemyManager y PowerupManager. Esto también
    sirve para reiniciar la partida (tecla R).

  run():
    El bucle principal. En cada frame:
      1. Mide el tiempo transcurrido (dt) con clock.tick().
      2. Procesa eventos (teclado, cerrar ventana).
      3. Llama a _update(dt) si la partida sigue activa.
      4. Llama a _render() siempre.

  _update(dt):
    Orden de actualización cada frame:
      1. PowerupManager: recolección e ítems en suelo.
      2. Aplica speed_mult al jugador según potenciadores.
      3. game_object.update() → cadena de decoradores → Player.
      4. EnemyManager: mueve enemigos y detecta colisión.
      5. Revisa condiciones de fin de partida.

  _render():
    Limpia la pantalla, dibuja la cuadrícula, llama a
    _draw_scene() y superpone la pantalla de fin si aplica.

  _draw_scene():
    Orden de capas (de atrás hacia adelante):
      1. Potenciadores en el suelo.
      2. Bordes de colores del jugador (anillos de potenciadores).
      3. Jugador con rastro (decoradores).
      4. Enemigos.
      5. HUD de efectos activos.


  main.py

Punto de entrada. Solo crea una instancia de Game y llama run().
Se protege con "if __name__ == '__main__'" para que no se
ejecute si otro archivo importa este módulo.

