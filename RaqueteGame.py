import pygame
import sys
import random
import time

# Inicializar o pygame
pygame.init()

# Dimensões da janela
WIDTH, HEIGHT = 800, 600

# Cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
PINK = (255, 105, 180)

# Configurações da tela
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Jogo de Quebrar Bricks")
clock = pygame.time.Clock()

# Raquete
paddle_width = 100
paddle_height = 10
paddle = pygame.Rect(WIDTH // 2 - paddle_width // 2, HEIGHT - 30, paddle_width, paddle_height)
paddle_speed = 7
paddle_timer = 0

# Bola
ball_radius = 10
ball = pygame.Rect(WIDTH // 2, HEIGHT // 2, ball_radius * 2, ball_radius * 2)
balls = [(ball, 5, -5)]  # Cada bola tem sua própria direção

# Bricks
brick_rows, brick_cols = 5, 10
brick_width = WIDTH // brick_cols
brick_height = 30
bricks = []

for row in range(brick_rows):
    for col in range(brick_cols):
        brick = pygame.Rect(col * brick_width, row * brick_height, brick_width - 2, brick_height - 2)
        bricks.append(brick)

# Especiais
specials = []

# Função principal
def main():
    global paddle_width, paddle_timer

    running = True
    while running:
        print(f"Bolas: {len(balls)}, Raquete: {paddle_width}px, Bricks restantes: {len(bricks)}")

        screen.fill(BLACK)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Movimento da raquete
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and paddle.left > 0:
            paddle.move_ip(-paddle_speed, 0)
        if keys[pygame.K_RIGHT] and paddle.right < WIDTH:
            paddle.move_ip(paddle_speed, 0)

        # Atualizar temporizador da raquete
        if paddle_timer > 0:
            paddle_timer -= 1
            if paddle_timer == 0:
                paddle_width = 100
                paddle.width = paddle_width

        # Movimento das bolas
        for i, (ball, ball_dx, ball_dy) in enumerate(balls[:]):
            ball.move_ip(ball_dx, ball_dy)

            # Colisão com paredes
            if ball.left <= 0 or ball.right >= WIDTH:
                ball_dx = -ball_dx
                print("Bola colidiu com a parede lateral")
            if ball.top <= 0:
                ball_dy = -ball_dy
                print("Bola colidiu com o teto")

            # Colisão com a raquete
            if ball.colliderect(paddle):
                ball_dy = -ball_dy
                print("Bola colidiu com a raquete")

            # Colisão com bricks
            for brick in bricks[:]:
                if ball.colliderect(brick):
                    bricks.remove(brick)
                    ball_dy = -ball_dy
                    print(f"Brick destruído: ({brick.x}, {brick.y})")
                    # Chance de especial
                    if random.random() < 0.05:
                        special_color = GREEN if random.random() < 0.5 else PINK
                        special = pygame.Rect(brick.x + brick.width // 2 - 10, brick.y + brick.height // 2 - 10, 20, 20)
                        specials.append((special, special_color))
                    break

            # Atualizar direção da bola no array
            balls[i] = (ball, ball_dx, ball_dy)

            # Game over
            if ball.bottom >= HEIGHT:
                print("Uma bola caiu!")
                balls.remove((ball, ball_dx, ball_dy))
                if not balls:
                    print("Game Over!")
                    running = False

        # Movimento dos especiais
        for special, color in specials[:]:
            special.move_ip(0, 5)
            if special.colliderect(paddle):
                if color == GREEN:
                    print("Especial verde coletado! Raquete aumentada por 10 segundos.")
                    paddle_width = int(paddle_width * 1.2)
                    paddle.width = paddle_width
                    paddle_timer = 600
                elif color == PINK:
                    print("Especial rosa coletado! Bolas duplicadas.")
                    new_balls = []
                    for ball, ball_dx, ball_dy in balls:
                        new_ball = pygame.Rect(ball.x, ball.y, ball.width, ball.height)
                        new_ball_dx = -ball_dx if random.random() < 0.5 else ball_dx
                        new_ball_dy = -abs(ball_dy)  # Sempre vai para cima
                        new_balls.append((new_ball, new_ball_dx, new_ball_dy))
                    balls.extend(new_balls)
                specials.remove((special, color))
            elif special.top > HEIGHT:
                specials.remove((special, color))

        # Desenhar elementos
        pygame.draw.rect(screen, WHITE, paddle)
        for ball, _, _ in balls:
            pygame.draw.ellipse(screen, RED, ball)
        for brick in bricks:
            pygame.draw.rect(screen, BLUE, brick)
        for special, color in specials:
            pygame.draw.ellipse(screen, color, special)

        # Atualizar a tela
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
