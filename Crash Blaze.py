import pygame
import sys
import math
import random

# Inicialização
pygame.init()
largura, altura = 800, 700
tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption("Crash Simulador")

# Fontes e cores
fonte = pygame.font.SysFont("arial", 24)
fonte_menor = pygame.font.SysFont("arial", 20)
preto = (0, 0, 0)
vermelho = (255, 0, 0)
branco = (255, 255, 255)
cinza = (100, 100, 100)
verde = (0, 255, 0)

# Variáveis
relogio = pygame.time.Clock()
bolinha_pos = [100, altura - 150]
trajetoria = []
tempo = 0
ativo = False
multiplicador = 0
crashado = False
crash_em = random.uniform(1.5, 10)
velocidade = 0.01
camera_offset_y = 0

# Caixa de texto de aposta
input_ativo = False
texto_aposta = ""
input_rect = pygame.Rect(20, altura - 110, 140, 32)
botao_rect = pygame.Rect(180, altura - 110, 100, 32)

# Caixa de texto de crash máximo
crash_input_ativo = False
texto_crash = ""
crash_rect = pygame.Rect(300, altura - 110, 140, 32)

# Simulação de apostas recentes
nomes = ["João", "Pedro", "Lucas", "Ana", "Julia", "Carlos", "Fernando", "Beatriz"]
apostas_recentes = []
aposta_timer = 0

def gerar_aposta():
    nome = random.choice(nomes)
    valor = random.randint(50, 10000)
    return f"{nome} ganhou R${valor}"

def desenhar_interface():
    cor_input = branco if input_ativo else cinza
    pygame.draw.rect(tela, cor_input, input_rect, 2)
    texto_surface = fonte.render(texto_aposta, True, branco)
    tela.blit(texto_surface, (input_rect.x + 5, input_rect.y + 5))

    pygame.draw.rect(tela, cinza, botao_rect)
    botao_texto = fonte.render("Iniciar", True, branco)
    tela.blit(botao_texto, (botao_rect.x + 10, botao_rect.y + 5))

    # Campo do crash max
    cor_crash = branco if crash_input_ativo else cinza
    pygame.draw.rect(tela, cor_crash, crash_rect, 2)
    texto_crash_surface = fonte.render(texto_crash, True, branco)
    tela.blit(texto_crash_surface, (crash_rect.x + 5, crash_rect.y + 5))

    # Apostas recentes
    y_offset = altura - 60
    for aposta in apostas_recentes[-6:][::-1]:
        texto = fonte_menor.render(aposta, True, verde)
        tela.blit(texto, (20, y_offset))
        y_offset += 20

def curva(t):
    x = t * 100
    y = -(math.pow(t, 1.5) * 100)
    return [x, y]

def desenhar_regua(offset_y):
    espaco = 50
    for i in range(0, 100):
        y = altura - 150 - (i * espaco) + offset_y
        if y < -50 or y > altura - 150 + 50:
            continue
        multiplicador_label = i * 0.2
        label = fonte.render(f"{multiplicador_label:.1f}x", True, cinza)
        tela.blit(label, (10, y))
        pygame.draw.line(tela, (50, 50, 50), (60, y), (largura, y), 1)

# Loop principal
while True:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif evento.type == pygame.MOUSEBUTTONDOWN:
            if input_rect.collidepoint(evento.pos):
                input_ativo = True
                crash_input_ativo = False
            elif crash_rect.collidepoint(evento.pos):
                crash_input_ativo = True
                input_ativo = False
            else:
                input_ativo = False
                crash_input_ativo = False
            if botao_rect.collidepoint(evento.pos) and not ativo:
                ativo = True
                tempo = 0
                multiplicador = 0
                bolinha_pos = [100, altura - 150]
                trajetoria.clear()
                crashado = False
                try:
                    crash_em = float(texto_crash)
                except:
                    crash_em = random.uniform(1.5, 10)
        elif evento.type == pygame.KEYDOWN:
            if input_ativo:
                if evento.key == pygame.K_BACKSPACE:
                    texto_aposta = texto_aposta[:-1]
                elif evento.key == pygame.K_RETURN:
                    input_ativo = False
                else:
                    texto_aposta += evento.unicode
            elif crash_input_ativo:
                if evento.key == pygame.K_BACKSPACE:
                    texto_crash = texto_crash[:-1]
                elif evento.key == pygame.K_RETURN:
                    crash_input_ativo = False
                else:
                    texto_crash += evento.unicode

    if ativo and not crashado:
        tempo += velocidade
        multiplicador = tempo * 1.0
        if multiplicador >= crash_em:
            crashado = True

        deslocamento = curva(tempo)
        bolinha_pos = [100 + deslocamento[0], altura - 150 + deslocamento[1]]
        trajetoria.append(list(bolinha_pos))
        camera_offset_y = bolinha_pos[1] - (altura - 150) // 2

    aposta_timer += relogio.get_time()
    if aposta_timer > 1000:
        apostas_recentes.append(gerar_aposta())
        if len(apostas_recentes) > 10:
            apostas_recentes.pop(0)
        aposta_timer = 0

    tela.fill(preto)

    # Parte de cima - jogo
    jogo_surface = pygame.Surface((largura, altura - 150))
    jogo_surface.fill(preto)
    desenhar_regua(camera_offset_y)

    # Rastro transparente
    rastro_surface = pygame.Surface((largura, altura), pygame.SRCALPHA)
    for pos in trajetoria:
        pygame.draw.circle(rastro_surface, (255, 0, 0, 64), (int(pos[0]), int(pos[1] - camera_offset_y)), 4)
    jogo_surface.blit(rastro_surface, (0, 0))

    # Bolinha
    if not crashado:
        pygame.draw.circle(jogo_surface, vermelho, (int(bolinha_pos[0]), int(bolinha_pos[1] - camera_offset_y)), 8)
    else:
        crash_text = fonte.render(f"💥 Crashou em {multiplicador:.2f}x!", True, (255, 100, 100))
        jogo_surface.blit(crash_text, (largura//2 - 100, (altura - 150)//2 - 20))

    # Multiplicador
    mult_texto = fonte.render(f"{multiplicador:.2f}x", True, branco)
    jogo_surface.blit(mult_texto, (largura - 150, 20))

    tela.blit(jogo_surface, (0, 0))

    # Parte inferior
    pygame.draw.rect(tela, (30, 30, 30), (0, altura - 150, largura, 150))
    desenhar_interface()

    pygame.display.update()
    relogio.tick(60)
