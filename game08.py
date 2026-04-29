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
pygame.display.set_caption("Game 08 - Jogo Completo")

rel = pygame.time.Clock()
fonte = pygame.font.SysFont(None, 36)

# Imagens
fundo = carregar_imagem("Fundo.png", 720, 720)
personagem = carregar_imagem("idle.png", 80, 80)
obstaculo_img = carregar_imagem("Cactus.png", 80, 80)
objetivo_img = carregar_imagem("Bandeira.png", 75, 75)

chao = 700
x = 80
y = chao - 85
vel = 5

pulando = False
velocidade_pulo = 0
forca_pulo = -20
gravidade = 0.9

# Definição dos Rects de Colisão
obstaculo = pygame.Rect(390, chao - 80, 80, 80)
objetivo = pygame.Rect(620, chao - 75, 75, 75)

mensagem = ""
rodando = True
while rodando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False

    teclas = pygame.key.get_pressed()
    if teclas[pygame.K_RIGHT]: x += vel
    if teclas[pygame.K_LEFT]: x -= vel

    if teclas[pygame.K_SPACE] and not pulando:
        pulando = True
        velocidade_pulo = forca_pulo

    if pulando:
        y += velocidade_pulo
        velocidade_pulo += gravidade
        if y >= chao - 85:
            y = chao - 85
            pulando = False

    # Caixa de colisão dinâmica do player
    player = pygame.Rect(x + 18, y + 12, 50, 68)

    # Verificação de Colisões
    if player.colliderect(obstaculo):
        x = 80
        y = chao - 85
        mensagem = "Tente novamente"

    if player.colliderect(objetivo):
        mensagem = "Você venceu"

    # Desenho
    tela.blit(fundo, (0, 0))
    tela.blit(obstaculo_img, (obstaculo.x, obstaculo_y))
    tela.blit(objetivo_img, (objetivo.x, objetivo.y))
    tela.blit(personagem, (x, y))

    if mensagem:
        texto = fonte.render(mensagem, True, (0, 0, 0))
        tela.blit(texto, (30, 30))

    pygame.display.flip()
    rel.tick(60)

pygame.quit()

