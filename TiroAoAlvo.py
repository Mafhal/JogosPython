import pygame
import random

# Inicializa o pygame
pygame.init()

# Configurações da tela
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Jogo de Tiro ao Alvo")

# Cores
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)

# Configuração do alvo
target_radius = 30
target_x = random.randint(target_radius, WIDTH - target_radius)
target_y = random.randint(target_radius, HEIGHT - target_radius)
target_color = RED
special_target = False

# Configuração da mira
crosshair_radius = 10
crosshair_x, crosshair_y = WIDTH // 2, HEIGHT // 2
crosshair_types = ["circle", "cross", "square", "dot"]
crosshair_index = 0

# Fonte para exibir a pontuação e tempo
font = pygame.font.Font(None, 36)
score = 0
time_left = 30

# Configuração do tempo
clock = pygame.time.Clock()
start_ticks = pygame.time.get_ticks()

going = True
while going:
    screen.fill(WHITE)
    
    # Atualiza o tempo
    seconds = (pygame.time.get_ticks() - start_ticks) // 1000
    time_left = max(30 - seconds, 0)
    if time_left == 0:
        going = False
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            going = False
        elif event.type == pygame.MOUSEMOTION:
            crosshair_x, crosshair_y = event.pos
        elif event.type == pygame.MOUSEBUTTONDOWN:
            distance = ((crosshair_x - target_x) ** 2 + (crosshair_y - target_y) ** 2) ** 0.5
            if distance <= target_radius:
                if special_target:
                    score += 5
                else:
                    score += 1
                target_x = random.randint(target_radius, WIDTH - target_radius)
                target_y = random.randint(target_radius, HEIGHT - target_radius)
            else:
                score -= 1
                target_x = random.randint(target_radius, WIDTH - target_radius)
                target_y = random.randint(target_radius, HEIGHT - target_radius)
            target_radius = 30 if random.random() > 0.2 else 15
            target_color = RED if target_radius == 30 else GREEN
            special_target = target_color == GREEN
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_k:
                crosshair_index = (crosshair_index + 1) % len(crosshair_types)
    
    # Desenha o alvo
    pygame.draw.circle(screen, target_color, (target_x, target_y), target_radius)
    
    # Desenha a mira
    crosshair_type = crosshair_types[crosshair_index]
    if crosshair_type == "circle":
        pygame.draw.circle(screen, BLACK, (crosshair_x, crosshair_y), crosshair_radius, 2)
    elif crosshair_type == "cross":
        pygame.draw.line(screen, BLACK, (crosshair_x - 15, crosshair_y), (crosshair_x + 15, crosshair_y), 2)
        pygame.draw.line(screen, BLACK, (crosshair_x, crosshair_y - 15), (crosshair_x, crosshair_y + 15), 2)
    elif crosshair_type == "square":
        pygame.draw.rect(screen, BLACK, (crosshair_x - 10, crosshair_y - 10, 20, 20), 2)
    elif crosshair_type == "dot":
        pygame.draw.circle(screen, BLACK, (crosshair_x, crosshair_y), 3)
    
    # Exibe a pontuação e o tempo
    score_text = font.render(f"Pontuação: {score}", True, BLACK)
    time_text = font.render(f"Tempo: {time_left}s", True, BLACK)
    screen.blit(score_text, (10, 10))
    screen.blit(time_text, (10, 40))
    
    pygame.display.flip()
    clock