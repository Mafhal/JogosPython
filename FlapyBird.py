import pygame
import random

# Inicializando o pygame
pygame.init()

# Configurações básicas
SCREEN_WIDTH, SCREEN_HEIGHT = 400, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Flappy Bird")
clock = pygame.time.Clock()
FPS = 60

# Cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 150, 255)
DARK_BLUE = (18, 35, 65)  # Azul escuro para o modo noturno
GREEN = (0, 255, 0)
DARK_GREEN = (0, 100, 0)  # Verde escuro para os canos no modo noturno
RED = (255, 0, 0)
COLORS = [(255, 0, 0), (255, 127, 0), (255, 255, 0), (0, 255, 0), (0, 0, 255), (75, 0, 130), (148, 0, 211)]  # Cores do arco-íris

# Configurações do Pássaro
bird_x = 50
bird_y = SCREEN_HEIGHT // 2
bird_radius = 10
bird_velocity = 0
gravity = 0.5
jump_strength = -7  # Reduzido o tamanho do pulo
bird_color = RED  # Cor inicial do pássaro

# Configurações dos Tubos
pipe_width = 50
pipe_gap = 150
pipe_speed = 3
pipes = []
pipe_frequency = 1500  # milissegundos
last_pipe = pygame.time.get_ticks()

# Pontuação
score = 0
font = pygame.font.SysFont("Arial", 30)

# Estados do jogo
night_mode = False
minimalist_mode = False  # Novo estado para o modo minimalista

# Função para desenhar o pássaro
def draw_bird(bird_color):
    pygame.draw.circle(screen, bird_color, (bird_x, int(bird_y)), bird_radius)

# Função para criar tubos
def create_pipe():
    pipe_height = random.randint(100, 400)
    top_pipe = pygame.Rect(SCREEN_WIDTH, 0, pipe_width, pipe_height)
    bottom_pipe = pygame.Rect(SCREEN_WIDTH, pipe_height + pipe_gap, pipe_width, SCREEN_HEIGHT - pipe_height - pipe_gap)
    return {'top': top_pipe, 'bottom': bottom_pipe, 'scored': False}

# Função para desenhar tubos
def draw_pipes(pipes, pipe_color):
    for pipe in pipes:
        pygame.draw.rect(screen, pipe_color, pipe['top'])
        pygame.draw.rect(screen, pipe_color, pipe['bottom'])

# Função para verificar colisões
def check_collision(pipes):
    for pipe in pipes:
        if bird_x + bird_radius > pipe['top'].x and bird_x - bird_radius < pipe['top'].x + pipe_width:
            if bird_y - bird_radius < pipe['top'].height or bird_y + bird_radius > pipe['bottom'].y:
                return True
    if bird_y - bird_radius < 0 or bird_y + bird_radius > SCREEN_HEIGHT:
        return True
    return False

# Função para soltar fogos de artifício
def draw_fireworks():
    for i in range(10):  # Exibindo 10 fogos de artifício
        pygame.draw.circle(screen, (random.randint(150, 255), random.randint(150, 255), random.randint(150, 255)), 
                           (random.randint(0, SCREEN_WIDTH), random.randint(0, SCREEN_HEIGHT)), random.randint(5, 10))

# Loop principal
running = True
rainbow_index = 0  # Índice para mudar as cores do arco-íris

while running:
    # Mudar o fundo e as cores com base no modo minimalista ou não
    if minimalist_mode:
        background_color = WHITE
        bird_color = BLACK
        pipe_color = BLACK
    elif night_mode:
        background_color = DARK_BLUE  # Fundo azul escuro no modo noturno
        bird_color = WHITE
        pipe_color = DARK_GREEN  # Canos verde escuro no modo noturno
    else:
        background_color = BLUE
        bird_color = RED
        pipe_color = GREEN

    screen.fill(background_color)

    # Eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bird_velocity = jump_strength  # Salto normal
            elif event.key == pygame.K_m:
                minimalist_mode = not minimalist_mode  # Alterna o modo minimalista

    # Atualizar posição do pássaro
    bird_velocity += gravity
    bird_y += bird_velocity

    # Gerar novos tubos
    time_now = pygame.time.get_ticks()
    if time_now - last_pipe > pipe_frequency:
        pipes.append(create_pipe())
        last_pipe = time_now

    # Mover tubos
    pipes = [{'top': pipe['top'].move(-pipe_speed, 0), 'bottom': pipe['bottom'].move(-pipe_speed, 0), 'scored': pipe['scored']} for pipe in pipes]
    
    # Remover tubos fora da tela
    pipes = [pipe for pipe in pipes if pipe['top'].x + pipe_width > 0 or pipe['top'].x < SCREEN_WIDTH]

    # Atualizar pontuação
    for pipe in pipes:
        if pipe['top'].x + pipe_width < bird_x and not pipe['scored']:
            score += 1
            pipe['scored'] = True

    # Alterar modos com base na pontuação
    if score >= 10 and score < 15:
        night_mode = False  # Desativa o modo noturno
    elif score >= 15 and score < 20:
        night_mode = False  # Desativa o modo noturno
    elif score >= 20 and score < 25:
        night_mode = True  # Ativa o modo noturno
        bird_color = COLORS[rainbow_index]
        rainbow_index = (rainbow_index + 1) % len(COLORS)  # Efeito arco-íris
    elif score >= 25:
        draw_fireworks()  # Mostrar fogos de artifício
        score_text = font.render("Você Venceu!", True, WHITE)
        screen.blit(score_text, (SCREEN_WIDTH // 3, SCREEN_HEIGHT // 2))
        pygame.display.flip()
        pygame.time.wait(3000)  # Espera 3 segundos antes de fechar
        running = False

    # Desenhar elementos
    draw_bird(bird_color)
    draw_pipes(pipes, pipe_color)
    
    # Exibir pontuação
    score_text = font.render(f"Score: {int(score)}", True, WHITE if night_mode else BLACK)
    screen.blit(score_text, (10, 10))
    
    # Verificar colisões
    if check_collision(pipes):
        running = False

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
  