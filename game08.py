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
personagem = carregar_imagem("idle.png", 80, 80)
obstaculo_img = carregar_imagem("Cactus.png", 80, 80)
objetivo_img = carregar_imagem("Bandeira.png", 75, 75)

# Chão
chao = 700

# Personagem
x = 80
y = chao - 85
vel = 5

# Pulo
pulando = False
velocidade_pulo = 0
forca_pulo = -20
gravidade = 0.9

# Obstáculo e objetivo
obstaculo = pygame.Rect(390, chao - 80, 80, 80)
objetivo = pygame.Rect(620, chao - 75, 75, 75)

mensagem = ""
rodando = True

while rodando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False

    teclas = pygame.key.get_pressed()

    if teclas[pygame.K_RIGHT]:
        x += vel

    if teclas[pygame.K_LEFT]:
        x -= vel

    if teclas[pygame.K_SPACE] and not pulando:
        pulando = True
        velocidade_pulo = forca_pulo

    if pulando:
        y += velocidade_pulo
        velocidade_pulo += gravidade

        if y >= chao - 85:
            y = chao - 85
            pulando = False

    player = pygame.Rect(x + 18, y + 12, 50, 68)

    if player.colliderect(obstaculo):
        x = 80
        y = chao - 85
        mensagem = "Tente novamente"

    if player.colliderect(objetivo):
        mensagem = "Voce venceu"

    # Desenhar cenário
    tela.fill((135, 206, 235)) # céu azul
    tela.blit(obstaculo_img, (obstaculo.x, obstaculo.y))
    tela.blit(objetivo_img, (objetivo.x, objetivo.y))
    tela.blit(personagem, (x, y))

    if mensagem:
        texto = fonte.render(mensagem, True, (0, 0, 0))
        tela.blit(texto, (30, 30))

    pygame.display.flip()
    rel.tick(60)

pygame.quit()

