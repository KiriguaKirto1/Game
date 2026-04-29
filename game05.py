import pygame
import os

pygame.init()

# Caminho das imagens
BASE = os.path.dirname(os.path.abspath(__file__))
IMG = os.path.join(BASE, "Assets")

def carregar_imagem(nome, largura, altura):
    caminho = os.path.join(IMG, nome)
    imagem = pygame.image.load(caminho).convert_alpha()
    return pygame.transform.scale(imagem, (largura, altura))

# Configurações da Tela
LARGURA = 720
ALTURA = 720
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Game 05 - Objetivo")

# Carregamento das Imagens
personagem = carregar_imagem("idle.png", 85, 85)
obstaculo = carregar_imagem("Cactus.png", 80, 80)
objetivo = carregar_imagem("Bandeira.png", 75, 75)

# Chão e Posições
chao = 650
x = 80
y = chao - 85

obstaculo_x = 390
obstaculo_y = chao - 80

objetivo_x = 620
objetivo_y = chao - 75

# Loop Principal
rodando = True
while rodando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False

    # Desenho
    tela.fill((135, 206, 235)) # Cor do céu
    
    tela.blit(personagem, (x, y))
    tela.blit(obstaculo, (obstaculo_x, obstaculo_y))
    tela.blit(objetivo, (objetivo_x, objetivo_y))

    pygame.display.flip()

pygame.quit()

