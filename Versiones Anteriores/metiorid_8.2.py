import pygame
import sys
import math
import random

# Inicializar Pygame
pygame.init()

# Configuración de la pantalla
# Resolucion de Pantalla = 1280 × 720
screen_width = 1280  # Ancho de la pantalla
screen_height = 720  # Alto de la pantalla
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Metroid 8.2")

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
deceleration = 0.1001  # Deceleración aún más gradual
acceleration = 0.1001  # Aceleración hacia adelante
max_speed = 12  # Velocidad máxima permitida
mini_speed = -4   # Velocidad mínima permitida de reversa

# Triángulo representando la nave (punta hacia adelante)
ship_points = [(0, 10), (-8, -10), (8, -10)]

# Lista para almacenar los disparos
bullets = []

# Lista para almacenar los meteoritos
meteorites = []

# Fuente para mostrar los FPS y la velocidad
font = pygame.font.Font(None, 36)

# Puntaje Inicial
score = 0

# Fuente para mostrar el puntaje
score_font = pygame.font.Font(None,36)

# Reloj para controlar el framerate
clock = pygame.time.Clock()

class Asteroid:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.destroyed = False
        self.explosion_radius = 0  # Radio inicial de la explosión
        self.max_explosion_radius = 40  # Radio máximo de la explosión

def create_meteorite():
    side = random.randint(1, 4)  # Elegir un lado (1: arriba, 2: derecha, 3: abajo, 4: izquierda)
    # angle = random.uniform(0, 2*math.pi)  # Elegir un ángulo aleatorio en radianes
    angle = random.uniform(10,30)
    speed = random.uniform(1, 3)  # Elegir una velocidad aleatoria
    if side == 1:  # Arriba
        x = random.randint(0, screen_width)
        y = 0
    elif side == 2:  # Derecha
        x = screen_width
        y = random.randint(0, screen_height)
    elif side == 3:  # Abajo
        x = random.randint(0, screen_width)
        y = screen_height
    else:  # Izquierda
        x = 0
        y = random.randint(0, screen_height)
    meteorites.append((x, y, angle, speed))

# Función para mostrar los FPS y la velocidad en la pantalla
def show_info():
    fps_text = font.render(f"FPS: {int(clock.get_fps())}", True, green)
    speed_text = font.render(f"Speed: {ship_speed:.2f}", True, green)
    screen.blit(fps_text, (10, 10))
    screen.blit(speed_text, (120, 10))
    score_text = score_font.render(f"Score: {score}", True, green)
    screen.blit(score_text, (280, 10))

# Bucle principal del juego
running = True
while running:
    # Capturar eventos de teclado y ventana
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            bullet_x = ship_x + math.cos(math.radians(ship_angle)) * 20
            bullet_y = ship_y - math.sin(math.radians(ship_angle)) * 20
            bullets.append((bullet_x, bullet_y, ship_angle))
    
    # Verificar si una bala impacta a un meteorito
    new_meteorites = []
    for meteorite in meteorites:
        if isinstance(meteorite, Asteroid):
            if meteorite.destroyed:
                if meteorite.explosion_radius <= meteorite.max_explosion_radius:
                    pygame.draw.circle(screen, red, (int(meteorite.x), int(meteorite.y)), meteorite.explosion_radius, 3)
                    meteorite.explosion_radius += 2  # Aumentar el radio para la animación
                else:
                    continue  # Ya se completó la animación, omitir este asteroide
            else:
                # Dibujar el asteroide normalmente
                pygame.draw.circle(screen, white, (int(meteorite.x), int(meteorite.y)), 10, 2)
                new_meteorites.append(meteorite)
        else:
            meteorite_x, meteorite_y, angle, speed = meteorite
            # Dibujar el asteroide normalmente
            pygame.draw.circle(screen, white, (int(meteorite_x), int(meteorite_y)), 10, 2)
            new_meteorites.append((meteorite_x, meteorite_y, angle, speed))
    
    meteorites = new_meteorites
    
    # Capturar las teclas presionadas
    keys = pygame.key.get_pressed()
    
    # Cambiar el ángulo de la nave según las teclas presionadas
    if keys[pygame.K_LEFT]:
        ship_angle += 2.5
    elif keys[pygame.K_RIGHT]:
        ship_angle -= 2.5
        
    # Acelerar hacia adelante con la flecha hacia arriba
    if keys[pygame.K_UP]:
        ship_speed += acceleration
        ship_speed = min(ship_speed, max_speed)  # Limitar velocidad máxima
    else:
        ship_speed *= .955  # Deceleración gradual cuando no se presiona la tecla de aceleración
    
    # Frenar y avanzar hacia atrás con la flecha hacia abajo
    if keys[pygame.K_DOWN]:
        ship_speed -= deceleration
        ship_speed = max(ship_speed, mini_speed)
    
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
    pygame.draw.polygon(screen, green, [(y + ship_x, x + ship_y) for x, y in rotated_ship_points], 1)
    
    # Actualizar la posición y dibujar los disparos
    new_bullets = []
    for bullet in bullets:
        bullet_x, bullet_y, bullet_angle = bullet
        bullet_x += math.cos(math.radians(bullet_angle)) * 20  # Disminuir velocidad de las balas
        bullet_y -= math.sin(math.radians(bullet_angle)) * 20  # Disminuir velocidad de las balas
        pygame.draw.circle(screen, green, (int(bullet_x), int(bullet_y)), 3)
        if 0 <= bullet_x < screen_width and 0 <= bullet_y < screen_height:
            new_bullets.append((bullet_x, bullet_y, bullet_angle))
    bullets = new_bullets

    # Crear meteoritos aleatoriamente
    if random.random() < 0.01:
        create_meteorite()
    
    # Actualizar y dibujar meteoritos
        new_meteorites = []
    for meteorite in meteorites:
        if isinstance(meteorite, Asteroid):
            meteorite_x, meteorite_y = meteorite.x, meteorite.y
            # Realizar animación de explosión aquí (por ejemplo, dibujar círculos concéntricos)
            explosion_radius = 10  # Radio inicial de la explosión
            max_explosion_radius = 40  # Radio máximo de la explosión
            pygame.draw.circle(screen, red, (int(meteorite_x), int(meteorite_y)), explosion_radius, 3)
            explosion_radius += 2  # Aumentar el radio para la animación
            if explosion_radius > max_explosion_radius:
                continue  # Ya se completó la animación, omitir este asteroide
        else:
            meteorite_x, meteorite_y = meteorite
            # Dibujar el asteroide normalmente
            pygame.draw.circle(screen, white, (int(meteorite_x), int(meteorite_y)), 10, 2)
        
        new_meteorites.append(meteorite)
    
    meteorites = new_meteorites
    for meteorite in meteorites:
        meteorite_x, meteorite_y, _, _ = meteorite
        
        if meteorite.destroyed:
            # Realizar animación de explosión aquí (por ejemplo, dibujar círculos concéntricos)
            explosion_radius = 10  # Radio inicial de la explosión
            max_explosion_radius = 40  # Radio máximo de la explosión
            pygame.draw.circle(screen, red, (int(meteorite_x), int(meteorite_y)), explosion_radius, 3)
            explosion_radius += 2  # Aumentar el radio para la animación
            if explosion_radius > max_explosion_radius:
                continue  # Ya se completó la animación, omitir este asteroide
        else:
            # Dibujar el asteroide normalmente
            pygame.draw.circle(screen, white, (int(meteorite_x), int(meteorite_y)), 10, 2)
        
        new_meteorites.append(meteorite)
    meteorites = new_meteorites
    
    # Mostrar los FPS y la velocidad en la esquina superior izquierda
    show_info()
    
    # Actualizar la pantalla
    pygame.display.flip()
    
    # Limitar el framerate
    clock.tick(60)

# Salir del juego
pygame.quit()
sys.exit()