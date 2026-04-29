import pygame
import os

# Iniciar o pygame
pygame.init()

# Caminho da pasta de imagens
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PASTA_IMAGENS = os.path.join(BASE_DIR, "Assets")

# Função para carregar imagem
def carregar_imagem(nome, largura, altura):
    caminho = os.path.join(PASTA_IMAGENS, nome)
    try:
        imagem = pygame.image.load(caminho).convert_alpha()
        imagem = pygame.transform.scale(imagem, (largura, altura))
        return imagem
    except pygame.error as e:
        print(f"Erro ao carregar imagem {caminho}: {e}")
        return pygame.Surface((largura, altura))

# Criar a janela
LARGURA = 720
ALTURA = 720
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Game 04 - Obstáculo")

# Carregar imagens
personagem = carregar_imagem("idle.png", 85, 85)
obstaculo = carregar_imagem("Pedra.png", 80, 80)

# Posições
x = 300
y = 600

obstaculo_x = 390
obstaculo_y = 620

# Loop principal
relogio = pygame.time.Clock()
rodando = True
while rodando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False

    # Cor de fundo (Sky Blue)
    tela.fill((135, 206, 235))

    # Desenhar na tela
    tela.blit(personagem, (x, y))
    tela.blit(obstaculo, (obstaculo_x, obstaculo_y))

    # Atualizar tela
    pygame.display.flip()
    
    # Limitar a 60 FPS
    relogio.tick(60)

# Encerrar
pygame.quit()

