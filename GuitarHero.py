import pygame
import random
import os
import librosa
from pygame import mixer
from tkinter import Tk, filedialog

# Inicializa o pygame
pygame.init()

# Configurações da tela
WIDTH, HEIGHT = 600, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Guitar Hero Simples")

# Cores
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)
DARK_BLUE = (0, 0, 50)

# Notas e teclas
keys = {'a': RED, 's': GREEN, 'd': BLUE}
key_positions = {'a': 150, 's': 300, 'd': 450}
pressed_keys = {key: False for key in keys}  # Para indicar quando uma tecla foi pressionada

# Classe para notas comuns e longas
tempo_caida = 7
class Note:
    def __init__(self, x, y, color, key, long_note=False):
        self.x = x
        self.y = y
        self.color = color
        self.key = key
        self.long_note = long_note
        self.hit = False
        self.length = 100 if long_note else 0  # Tamanho da nota longa

    def move(self):
        self.y += tempo_caida

    def draw(self):
        if self.long_note:
            pygame.draw.rect(screen, self.color, (self.x - 10, self.y, 20, self.length))
        else:
            pygame.draw.circle(screen, self.color, (self.x, self.y), 20)

# Carregar música
root = Tk()
root.withdraw()
music_path = filedialog.askopenfilename(filetypes=[("MP3 Files", "*.mp3")])

# Processar a música para detectar batidas
beat_times = []
if music_path:
    y, sr = librosa.load(music_path, sr=None)
    tempo, beat_frames = librosa.beat.beat_track(y=y, sr=sr)
    beat_times = librosa.frames_to_time(beat_frames, sr=sr)
    mixer.init()
    mixer.music.load(music_path)
    mixer.music.play()

# Lista de notas
notes = []
note_index = 0
score = 0
combo = 0
message = ""
message_timer = 0
start_time = pygame.time.get_ticks() / 1000  # Tempo inicial do jogo

# Especial
special_active = False
special_timer = 0
special_charge = 0

# Loop do jogo
running = True
clock = pygame.time.Clock()
while running:
    screen.fill(DARK_BLUE if special_active else (30, 30, 30))
    current_time = pygame.time.get_ticks() / 1000 - start_time
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.unicode in keys:
                pressed_keys[event.unicode] = True
                for note in notes[:]:
                    if note.key == event.unicode and HEIGHT - 70 <= note.y <= HEIGHT - 30:
                        notes.remove(note)
                        score += 2 if special_active else 1
                        combo += 1
                        special_charge += 1
                        if special_charge >= 20:
                            special_charge = 20  # Limite
                        if combo >= 5:
                            message = f"COMBO {combo}X"
                            message_timer = 30
                        else:
                            message = random.choice(["Boa!", "Excelente!"])
                            message_timer = 20
                    else:
                        combo = 0
            if event.key == pygame.K_SPACE and special_charge >= 20:
                special_active = True
                special_timer = 15 * 30  # 15 segundos a 30 FPS
                special_charge = 0
        if event.type == pygame.KEYUP:
            if event.unicode in keys:
                pressed_keys[event.unicode] = False
    
    # Gerar notas sincronizadas com a música, incluindo notas longas
    if note_index < len(beat_times) and current_time >= beat_times[note_index]:
        key = random.choice(list(keys.keys()))
        long_note = random.random() < 0.2  # 20% de chance de ser uma nota longa
        notes.append(Note(key_positions[key], 0, BLUE if special_active else keys[key], key, long_note))
        note_index += 1
    
    # Atualizar e desenhar notas
    for note in notes[:]:
        note.move()
        note.draw()
        if note.y > HEIGHT:
            notes.remove(note)
            combo = 0
    
    # Desenhar áreas de acerto e sinalizar quando pressionado
    for key, x in key_positions.items():
        color = BLUE if special_active else (keys[key] if pressed_keys[key] else WHITE)
        pygame.draw.rect(screen, color, (x - 25, HEIGHT - 50, 50, 50), 2)
    
    # Exibir pontuação
    font = pygame.font.Font(None, 36)
    text = font.render(f"Pontos: {score}", True, WHITE)
    screen.blit(text, (10, 10))
    
    # Exibir carga do especial
    special_text = font.render(f"Especial: {special_charge}/20", True, YELLOW)
    screen.blit(special_text, (WIDTH - 200, 10))
    
    # Exibir mensagens de combo
    if message_timer > 0:
        combo_font = pygame.font.Font(None, 50)
        combo_text = combo_font.render(message, True, YELLOW if "COMBO" in message else ORANGE)
        screen.blit(combo_text, (WIDTH//2 - combo_text.get_width()//2, HEIGHT//2))
        message_timer -= 1
    
    # Especial ativo
    if special_active:
        special_timer -= 1
        if special_timer <= 0:
            special_active = False
    
    pygame.display.flip()
    clock.tick(30)

pygame.quit()
