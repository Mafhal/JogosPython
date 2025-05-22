import pygame
import random
import time

# Inicializar o pygame
pygame.init()

# Definir as dimensões da tela
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Jogo de Digitação")

# Definir as cores
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)

# Fonte
font = pygame.font.Font(None, 48)

# Lista de palavras para o jogo
words = ["python", "programming", "developer", "pygame", "algorithm"]

# Função para desenhar texto na tela
def draw_text(text, x, y, color):
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, (x, y))

# Função principal do jogo
def game():
    word_index = 0
    total_time = 0
    num_words = len(words)
    word = words[word_index]
    typed_word = ""
    start_time = None
    game_over = False

    while not game_over:
        screen.fill(WHITE)
        draw_text("Digite a palavra: " + word, 150, 100, BLACK)

        # Verificar se o jogador acertou a palavra
        if typed_word == word:
            if start_time is None:
                start_time = time.time()

            time_taken = time.time() - start_time
            total_time += time_taken
            word_index += 1
            if word_index >= num_words:
                game_over = True
            else:
                word = words[word_index]
                typed_word = ""
                start_time = None

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    typed_word = typed_word[:-1]
                else:
                    typed_word += event.unicode

        pygame.time.Clock().tick(60)

    # Calcular média de tempo
    if num_words > 0:
        avg_time = total_time / num_words
        screen.fill(WHITE)
        draw_text(f"Tempo médio por palavra: {avg_time:.2f} segundos", 150, HEIGHT // 2, BLACK)
        pygame.display.update()
        pygame.time.wait(2000)

    pygame.quit()

# Iniciar o jogo
game()
