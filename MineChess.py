import pygame
import sys

# Inicializa o Pygame
pygame.init()

# Inicializa um tabuleiro 8x8 vazio
# Inicializa um tabuleiro 8x8 vazio
tabuleiro = [[None for _ in range(8)] for _ in range(8)]

# Adicionar peões ao tabuleiro
# Supondo que 1 representa um Peão Branco e 2 representa um Peão Preto
for i in range(8):
    tabuleiro[6][i] = 1  # Peões Brancos
    tabuleiro[1][i] = 2  # Peões Pretos

# Tamanho da janela e escala do tabuleiro
largura_tabuleiro = 1000
altura_tabuleiro = 1000
escala = 0.4  # Ajustado para 1 para um tamanho maior
largura_janela = int(largura_tabuleiro * escala)
altura_janela = int(altura_tabuleiro * escala)

# Carrega as imagens e ajusta o tamanho
def carregar_e_escalar_imagem(nome_arquivo, escala_peca):
    imagem = pygame.image.load(f"{nome_arquivo}.png")
    tamanho_novo = (int(100 * escala_peca), int(100 * escala_peca))
    return pygame.transform.scale(imagem, tamanho_novo)


tabuleiro_img = pygame.transform.scale(pygame.image.load("tabuleiro.png"), (largura_janela, altura_janela))
escala_casa = 80
escala_peca = 0.7 # Aumenta o tamanho das peças em 50%

peoes = {
    "PeaoBranco": carregar_e_escalar_imagem("PeaoBranco", escala_peca),
    "PeaoPreto": carregar_e_escalar_imagem("PeaoPreto", escala_peca),
    "BispoBranco": carregar_e_escalar_imagem("BispoBranco", escala_peca),
    "BispoPreto": carregar_e_escalar_imagem("BispoPreto", escala_peca),
    "TorreBranco": carregar_e_escalar_imagem("TorreBranco", escala_peca),
    "TorrePreto": carregar_e_escalar_imagem("TorrePreto", escala_peca),
    "RainhaBranco": carregar_e_escalar_imagem("RainhaBranco", escala_peca),
    "RainhaPreto": carregar_e_escalar_imagem("RainhaPreto", escala_peca),
}

# Coordenadas iniciais das peças
posicoes = {
    "PeaoBranco": [(i * escala_casa + (escala_casa - (100 * escala_peca)) / 2, 3 * escala_casa + (escala_casa - (100 * escala_peca)) / 2) for i in range(5)],  # Posicionados na linha 4
    "PeaoPreto": [(i * escala_casa + (escala_casa - (100 * escala_peca)) / 2, 1 * escala_casa + (escala_casa - (100 * escala_peca)) / 2) for i in range(5)],
    "TorreBranco": [(0 * escala_casa + (escala_casa - (100 * escala_peca)) / 2, 4 * escala_casa + (escala_casa - (100 * escala_peca)) / 2), (4 * escala_casa + (escala_casa - (100 * escala_peca)) / 2, 4 * escala_casa + (escala_casa - (100 * escala_peca)) / 2)],  # Posicionados na linha 5
    "TorrePreto": [(0 * escala_casa + (escala_casa - (100 * escala_peca)) / 2, 0 * escala_casa + (escala_casa - (100 * escala_peca)) / 2), (4 * escala_casa + (escala_casa - (100 * escala_peca)) / 2, 0 * escala_casa + (escala_casa - (100 * escala_peca)) / 2)],
    "BispoBranco": [(1 * escala_casa + (escala_casa - (100 * escala_peca)) / 2, 4 * escala_casa + (escala_casa - (100 * escala_peca)) / 2), (3 * escala_casa + (escala_casa - (100 * escala_peca)) / 2, 4 * escala_casa + (escala_casa - (100 * escala_peca)) / 2)],  # Posicionados na linha 5
    "BispoPreto": [(1 * escala_casa + (escala_casa - (100 * escala_peca)) / 2, 0 * escala_casa + (escala_casa - (100 * escala_peca)) / 2), (3 * escala_casa + (escala_casa - (100 * escala_peca)) / 2, 0 * escala_casa + (escala_casa - (100 * escala_peca)) / 2)],
    "RainhaBranco": [(2 * escala_casa + (escala_casa - (100 * escala_peca)) / 2, 4 * escala_casa + (escala_casa - (100 * escala_peca)) / 2)],  # Posicionada na linha 5
    "RainhaPreto": [(2 * escala_casa + (escala_casa - (100 * escala_peca)) / 2, 0 * escala_casa + (escala_casa - (100 * escala_peca)) / 2)],
}

# Variáveis de controle de movimento
peca_selecionada = None
offset_x = 0
offset_y = 0
tipo_peca_selecionada = None

# Configurações da janela
janela = pygame.display.set_mode((largura_janela, altura_janela))
pygame.display.set_caption("MiniChess")

def desenhar_tabuleiro():
    janela.blit(tabuleiro_img, (0, 0))

def desenhar_pecas():
    for tipo_peca, lista_posicoes in posicoes.items():
        for pos_x, pos_y in lista_posicoes:
            janela.blit(peoes[tipo_peca], (pos_x, pos_y))

def selecionar_peca(pos_mouse):
    global peca_selecionada, offset_x, offset_y, tipo_peca_selecionada
    for tipo_peca, lista_posicoes in posicoes.items():
        for i, (pos_x, pos_y) in enumerate(lista_posicoes):
            if pos_x <= pos_mouse[0] <= pos_x + 100 * escala and pos_y <= pos_mouse[1] <= pos_y + 100 * escala:
                peca_selecionada = i
                tipo_peca_selecionada = tipo_peca
                offset_x = pos_mouse[0] - pos_x
                offset_y = pos_mouse[1] - pos_y
                return
            
def movimento_valido_peao(pos_atual, pos_destino, cor_peao):
    x_atual, y_atual = pos_atual
    x_destino, y_destino = pos_destino
    delta_x = x_destino - x_atual
    delta_y = abs(y_destino - y_atual)

    # Verifica se o movimento é para frente
    if cor_peao == 1:  # Peão Branco
        mov_valido_frente = delta_x == -1 and delta_y == 0 and tabuleiro[x_destino][y_destino] is None
    else:  # Peão Preto
        mov_valido_frente = delta_x == 1 and delta_y == 0 and tabuleiro[x_destino][y_destino] is None

    # Verifica se o movimento é na diagonal para capturar uma peça
    mov_valido_diagonal = delta_x in [-1, 1] and delta_y == 1 and tabuleiro[x_destino][y_destino] is not None and tabuleiro[x_destino][y_destino] != cor_peao

    return mov_valido_frente or mov_valido_diagonal

def indice_para_pos_pixel(indice):
    indice_linha, indice_coluna = indice
    largura_celula = largura_janela
    altura_celula = altura_janela
    pos_x = indice_coluna * largura_celula
    pos_y = indice_linha * altura_celula
    return (pos_x, pos_y)


def mover_peao(pos_atual, pos_destino):
    if movimento_valido_peao(pos_atual, pos_destino, tabuleiro[pos_atual[0]][pos_atual[1]]):
        # Move a peça
        tabuleiro[pos_destino[0]][pos_destino[1]] = tabuleiro[pos_atual[0]][pos_atual[1]]
        tabuleiro[pos_atual[0]][pos_atual[1]] = None
        return True
    return False

def mover_peca(pos_mouse):
    global peca_selecionada, tipo_peca_selecionada
    if peca_selecionada is not None and tipo_peca_selecionada is not None:
        indice_linha_destino, indice_coluna_destino = pos_mouse_para_indice_tabuleiro(pos_mouse)
        pos_atual = posicoes[tipo_peca_selecionada][peca_selecionada]  # Isso precisa ser convertido para índices do tabuleiro
        pos_destino = (indice_linha_destino, indice_coluna_destino)

        # Aqui você precisa ajustar para verificar se o movimento é válido com base no tabuleiro lógico
        if mover_peao(pos_atual, pos_destino):
            # Atualize a posição gráfica da peça aqui
            nova_pos_x, nova_pos_y = indice_para_pos_pixel(pos_destino)
            posicoes[tipo_peca_selecionada][peca_selecionada] = (nova_pos_x, nova_pos_y)
            peca_selecionada = None  # Deseleciona a peça após o movimento


def pos_mouse_para_indice_tabuleiro(pos_mouse):
    x, y = pos_mouse
    indice_coluna = x // (largura_janela // 8)
    indice_linha = y // (altura_janela // 8)
    return (indice_linha, indice_coluna)


# Loop principal
def main():
    global peca_selecionada, tipo_peca_selecionada
    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                if evento.button == 1:  # Botão esquerdo do mouse
                    pos_mouse = pygame.mouse.get_pos()
                    selecionar_peca(pos_mouse)
            elif evento.type == pygame.MOUSEBUTTONUP:
                if evento.button == 1:  # Botão esquerdo do mouse
                    peca_selecionada = None
                    tipo_peca_selecionada = None
            elif evento.type == pygame.MOUSEMOTION:
                if peca_selecionada is not None:
                    pos_mouse = pygame.mouse.get_pos()
                    mover_peca(pos_mouse)

        # Desenhar o tabuleiro e as peças
        desenhar_tabuleiro()
        desenhar_pecas()

        # Atualizar a tela
        pygame.display.flip()






# Executar o jogo
if __name__ == "__main__":
    main()
