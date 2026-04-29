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

# Tela
LARGURA = 720
ALTURA = 720
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Game 07 - Pulo")

rel = pygame.time.Clock()

# Imagens
personagem = carregar_imagem("idle.png", 85, 85)
obstaculo = carregar_imagem("Cactus.png", 80, 80)
objetivo = carregar_imagem("Bandeira.png", 75, 75)

# Chão e Variáveis do Personagem
chao = 700
x = 80
y = chao - 85
vel = 5

# Variáveis do Pulo
pulando = False
velocidade_pulo = 0
forca_pulo = -20
gravidade = 0.9

# Objetos
obstaculo_x = 390
obstaculo_y = chao - 80

objetivo_x = 620
objetivo_y = chao - 75

rodando = True
while rodando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False

    teclas = pygame.key.get_pressed()

    # Movimento Horizontal
    if teclas[pygame.K_RIGHT]:
        x += vel
    if teclas[pygame.K_LEFT]:
        x -= vel

    # Iniciar Pulo
    if teclas[pygame.K_SPACE] and not pulando:
        pulando = True
        velocidade_pulo = forca_pulo

    # Lógica do Pulo e Gravidade
    if pulando:
        y += velocidade_pulo
        velocidade_pulo += gravidade

        if y >= chao - 85:
            y = chao - 85
            pulando = False

    # Desenho
    tela.fill((135, 206, 235))
    
    tela.blit(personagem, (x, y))
    tela.blit(obstaculo, (obstaculo_x, obstaculo_y))
    tela.blit(objetivo, (objetivo_x, objetivo_y))

    pygame.display.flip()
    rel.tick(60)

pygame.quit()

