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
pygame.display.set_caption("Game 06 - Movimento")

# Controle de FPS
relogio = pygame.time.Clock()

# Carregamento das Imagens
personagem = carregar_imagem("idle.png", 85, 85)
obstaculo = carregar_imagem("cactus.png", 80, 80)
objetivo = carregar_imagem("bandeira.png", 75, 75)

# Variáveis de Posicionamento e Movimento
chao = 650
x = 80
y = chao - 85
vel = 5  # Velocidade de movimento

obstaculo_x = 390
obstaculo_y = chao - 80

objetivo_x = 620
objetivo_y = chao - 75

# Loop Principal
rodando = True
while rodando:
    # 1. Gerenciamento de Eventos
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False

    # 2. Lógica de Movimento (Input do Teclado)
    teclas = pygame.key.get_pressed()
    if teclas[pygame.K_RIGHT]:
        x += vel
    if teclas[pygame.K_LEFT]:
        x -= vel

    # 3. Desenho e Renderização
    tela.fill((135, 206, 235))
    
    tela.blit(personagem, (x, y))
    tela.blit(obstaculo, (obstaculo_x, obstaculo_y))
    tela.blit(objetivo, (objetivo_x, objetivo_y))

    pygame.display.flip()
    
    # 4. Limitar a 60 quadros por segundo
    relogio.tick(60)

pygame.quit()