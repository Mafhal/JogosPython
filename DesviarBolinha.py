import pygame
import random
import time

# Inicializar o Pygame
pygame.init()

# Configurações da tela (vertical)
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 800
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Desvie das Bolinhas!")

# Cores
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)

# Clock para controlar o FPS
clock = pygame.time.Clock()
FPS = 60

# Variáveis do jogador
player_radius = 20
player_x = SCREEN_WIDTH // 2
player_y = SCREEN_HEIGHT - 100
player_speed = 7

# Lista de bolinhas vermelhas (inimigos)
enemies = []
enemy_radius = 20
enemy_speed = 4
enemy_spawn_rate = 1000  # Milissegundos

# Configuração da estrela (power-up)
star_radius = 15
star_x = None
star_y = None
star_active = False
invincible = False
invincibility_timer = 0
star_growth = 2  # Quanto a estrela cresce a cada spawn

# Eventos para spawn
SPAWN_ENEMY_EVENT = pygame.USEREVENT + 1
pygame.time.set_timer(SPAWN_ENEMY_EVENT, enemy_spawn_rate)  # Spawn inicial a cada 1 segundo
SPAWN_STAR_EVENT = pygame.USEREVENT + 2
pygame.time.set_timer(SPAWN_STAR_EVENT, 10000)  # Spawn da estrela a cada 10 segundos
SPEED_UP_EVENT = pygame.USEREVENT + 3
pygame.time.set_timer(SPEED_UP_EVENT, 8000)  # Acelera a cada 8 segundos

# Inicializar contador de tempo e velocidade
start_time = time.time()
speed_multiplier = 1

# Função principal do jogo
def main():
    global player_x, player_y, enemy_speed, star_x, star_y, star_active, invincible, invincibility_timer, enemy_spawn_rate, speed_multiplier, star_radius

    running = True
    while running:
        screen.fill(WHITE)

        # Calcular o tempo sobrevivido
        elapsed_time = int(time.time() - start_time)

        # Eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == SPAWN_ENEMY_EVENT:
                # Criar um novo inimigo
                enemy_x = random.randint(enemy_radius, SCREEN_WIDTH - enemy_radius)
                enemy_y = -enemy_radius  # Começa fora da tela
                enemies.append([enemy_x, enemy_y])
            elif event.type == SPAWN_STAR_EVENT:
                if not star_active:  # Apenas cria uma nova estrela se não existir uma ativa
                    star_x = random.randint(star_radius, SCREEN_WIDTH - star_radius)
                    star_y = random.randint(star_radius, SCREEN_HEIGHT // 2)  # Aparece na parte de cima
                    star_radius += star_growth  # Aumenta o tamanho da estrela
                    star_active = True
            elif event.type == SPEED_UP_EVENT:
                enemy_speed += 1  # Aumenta a velocidade dos inimigos
                enemy_spawn_rate = max(200, enemy_spawn_rate - 100)  # Diminui o intervalo de spawn
                pygame.time.set_timer(SPAWN_ENEMY_EVENT, enemy_spawn_rate)  # Atualiza o intervalo de spawn
                speed_multiplier += 1  # Incrementa o multiplicador de velocidade

        # Movimentação do jogador
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player_x - player_radius > 0:
            player_x -= player_speed
        if keys[pygame.K_RIGHT] and player_x + player_radius < SCREEN_WIDTH:
            player_x += player_speed
        if keys[pygame.K_UP] and player_y - player_radius > 0:
            player_y -= player_speed
        if keys[pygame.K_DOWN] and player_y + player_radius < SCREEN_HEIGHT:
            player_y += player_speed

        # Atualizar posição dos inimigos
        for enemy in enemies:
            enemy[1] += enemy_speed

        # Remover inimigos que saem da tela
        enemies[:] = [enemy for enemy in enemies if enemy[1] < SCREEN_HEIGHT + enemy_radius]

        # Verificar colisões com inimigos
        if not invincible:
            for enemy in enemies:
                dist = ((player_x - enemy[0]) ** 2 + (player_y - enemy[1]) ** 2) ** 0.5
                if dist < player_radius + enemy_radius:
                    print(f"Você perdeu! Sobreviveu por {elapsed_time} segundos.")
                    running = False

        # Verificar colisão com a estrela
        if star_active:
            dist_star = ((player_x - star_x) ** 2 + (player_y - star_y) ** 2) ** 0.5
            if dist_star < player_radius + star_radius:
                invincible = True
                invincibility_timer = pygame.time.get_ticks()  # Marca o início da invencibilidade
                star_active = False

        # Gerenciar invencibilidade
        if invincible:
            if pygame.time.get_ticks() - invincibility_timer > 5000:  # 5 segundos de invencibilidade
                invincible = False

        # Desenhar jogador
        if invincible:
            pygame.draw.circle(screen, GREEN, (player_x, player_y), player_radius)  # Verde para invencível
        else:
            pygame.draw.circle(screen, BLUE, (player_x, player_y), player_radius)

        # Desenhar inimigos
        for enemy in enemies:
            color = BLACK if invincible else RED  # Preto durante invencibilidade
            pygame.draw.circle(screen, color, (enemy[0], enemy[1]), enemy_radius)

        # Desenhar estrela (se ativa)
        if star_active:
            pygame.draw.circle(screen, YELLOW, (star_x, star_y), star_radius)

        # Desenhar contador de tempo
        font = pygame.font.SysFont("Arial", 30)
        time_text = font.render(f"Tempo: {elapsed_time}s", True, BLACK)
        screen.blit(time_text, (10, 10))

        # Desenhar contador de velocidade
        speed_text = font.render(f"Velocidade: {speed_multiplier}X", True, BLACK)
        screen.blit(speed_text, (SCREEN_WIDTH - 200, 10))

        # Atualizar a tela
        pygame.display.flip()

        # Controlar FPS
        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()
