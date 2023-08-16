import pygame
import sys
import math

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
    if keys[pygame.K_LEFT]:
        ship_angle += 1
    elif keys[pygame.K_RIGHT]:
        ship_angle -= 1
        
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
    if ship_x < 0:
        ship_x = screen_width
    elif ship_x > screen_width:
        ship_x = 0
    if ship_y < 0:
        ship_y = screen_height
    elif ship_y > screen_height:
        ship_y = 0
    
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
        bullet_x += math.cos(math.radians(bullet_angle)) * 1  # Disminuir velocidad de las balas
        bullet_y -= math.sin(math.radians(bullet_angle)) * 1  # Disminuir velocidad de las balas
        pygame.draw.circle(screen, green, (int(bullet_x), int(bullet_y)), 3)
        if 0 <= bullet_x < screen_width and 0 <= bullet_y < screen_height:
            new_bullets.append((bullet_x, bullet_y, bullet_angle))
    bullets = new_bullets
    
    # Actualizar la pantalla
    pygame.display.flip()


# Salir del juego
pygame.quit()
sys.exit()
