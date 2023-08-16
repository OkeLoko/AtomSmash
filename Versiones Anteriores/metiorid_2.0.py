import pygame
import sys
import math
import random

# Inicializar Pygame
pygame.init()

# Configuración de la pantalla
screen_width = 1000  # Ancho de la pantalla
screen_height = 800  # Alto de la pantalla
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Nave Triangular")

# Colores
white = (255, 255, 255)
black = (0, 0, 0)
green = (0, 255, 0)
red = (255, 0, 0)

# Posición, ángulo y velocidad inicial de la nave
ship_x = screen_width // 2
ship_y = screen_height // 2
ship_angle = 0
ship_speed = 0
deceleration = 0.001  # Deceleración aún más gradual
acceleration = 0.001  # Aceleración hacia adelante

# Triángulo representando la nave (punta hacia adelante)
ship_points = [(0, -10), (8, 10), (-8, 10)]

# Lista para almacenar los disparos
bullets = []

# Lista para almacenar los meteoritos
meteorites = []

# Reloj para controlar el framerate
# clock = pygame.time.Clock()

# Función para crear un nuevo meteorito
def create_meteorite():
    side = random.randint(0, 3)  # Lado desde el cual aparece el meteorito (0: arriba, 1: derecha, 2: abajo, 3: izquierda)
    if side == 0:  # Arriba
        x = random.randint(0, screen_width)
        y = -30
    elif side == 1:  # Derecha
        x = screen_width + 30
        y = random.randint(0, screen_height)
    elif side == 2:  # Abajo
        x = random.randint(0, screen_width)
        y = screen_height + 30
    else:  # Izquierda
        x = -30
        y = random.randint(0, screen_height)
    angle = math.atan2(ship_y - y, ship_x - x)
    speed = random.uniform(0.1, 0.5)
    meteorites.append((x, y, angle, speed))

# Bucle principal del juego
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        # Detectar si se presiona la barra espaciadora para disparar
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            bullet_x = ship_x + math.cos(math.radians(ship_angle)) * 20
            bullet_y = ship_y - math.sin(math.radians(ship_angle)) * 20
            bullets.append((bullet_x, bullet_y, ship_angle))
    
    # Capturar las teclas presionadas
    keys = pygame.key.get_pressed()
    
    # Cambiar el ángulo de la nave según las teclas presionadas
    ship_angle += (keys[pygame.K_RIGHT] - keys[pygame.K_LEFT])
    
    # Acelerar hacia adelante con la flecha hacia arriba
    if keys[pygame.K_UP]:
        ship_speed += acceleration
    else:
        ship_speed *= 0.995  # Deceleración gradual cuando no se presiona la tecla de aceleración
    
    # Frenar y avanzar hacia atrás con la flecha hacia abajo
    if keys[pygame.K_DOWN]:
        ship_speed -= deceleration
    
    # Actualizar la posición de la nave
    ship_x += math.cos(math.radians(ship_angle)) * ship_speed
    ship_y -= math.sin(math.radians(ship_angle)) * ship_speed
    
    # Verificar si la nave está fuera del encuadre y ajustar su posición
    ship_x %= screen_width
    ship_y %= screen_height
    
    # Crear nuevos meteoritos aleatoriamente si hay menos de 10
    if len(meteorites) < 10:
        create_meteorite()
    
    # Actualizar la posición de los meteoritos y verificar colisiones
    new_meteorites = []
    for meteorite in meteorites:
        x, y, angle, speed = meteorite
        x += math.cos(angle) * speed
        y += math.sin(angle) * speed
        if 0 <= x < screen_width and 0 <= y < screen_height:
            new_meteorites.append((x, y, angle, speed))
            # Verificar colisión con los disparos
            new_bullets = []
            for bullet in bullets:
                bullet_x, bullet_y, _ = bullet
                distance_squared = (x - bullet_x)**2 + (y - bullet_y)**2
                if distance_squared > 225:  # Radio de colisión al cuadrado
                    new_bullets.append(bullet)  # Mantener el disparo
            bullets = new_bullets
        else:
            create_meteorite()  # Crear un nuevo meteorito si el actual sale del encuadre
    meteorites = new_meteorites
    
    # Limpiar la pantalla
    screen.fill(black)
    
    # Calcular la posición de los puntos del triángulo rotado
    rotated_ship_points = [
        (x * math.cos(math.radians(ship_angle)) - y * math.sin(math.radians(ship_angle)),
         x * math.sin(math.radians(ship_angle)) + y * math.cos(math.radians(ship_angle)))
        for x, y in ship_points
    ]
    
    # Dibujar el triángulo hueco en la pantalla con la rotación
    pygame.draw.polygon(screen, green, [(x + ship_x, y + ship_y) for x, y in rotated_ship_points], 1)
    
    # Actualizar la posición y dibujar los disparos
    new_bullets = []
    for bullet in bullets:
        bullet_x, bullet_y, bullet_angle = bullet
        bullet_x += math.cos(math.radians(bullet_angle)) * 5
        bullet_y -= math.sin(math.radians(bullet_angle)) * 5
        pygame.draw.circle(screen, red, (int(bullet_x), int(bullet_y)), 3)
        if 0 <= bullet_x < screen_width and 0 <= bullet_y < screen_height:
            new_bullets.append((bullet_x, bullet_y, bullet_angle))
    bullets = new_bullets
    
    # Dibujar los meteoritos
    for x, y, _, _ in meteorites:
        pygame.draw.circle(screen, white, (int(x), int(y)), 15)
    
    # Actualizar la pantalla
    pygame.display.flip()
    
    # Limitar el framerate
    # clock.tick(60)

# Salir del juego
pygame.quit()
sys.exit()
