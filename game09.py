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
pygame.display.set_caption("Game 09 - Jogo Completo Ajustado")

rel = pygame.time.Clock()
fonte = pygame.font.SysFont(None, 36)

# Tamanhos ajustados
TAM_PERSONAGEM = 120
LARG_OBSTACULO = 90
ALT_OBSTACULO = 100
TAM_OBJETIVO = 120

# Imagens
personagem = carregar_imagem("idle.png", TAM_PERSONAGEM, TAM_PERSONAGEM)
obstaculo_img = carregar_imagem("Cactus.png", LARG_OBSTACULO, ALT_OBSTACULO)
objetivo_img = carregar_imagem("Bandeira.png", TAM_OBJETIVO, TAM_OBJETIVO)

# Chão visual do cenário
chao = 600

# Personagem
x = 70
y = chao - TAM_PERSONAGEM
vel = 5

# Pulo
pulando = False
velocidade_pulo = 0
forca_pulo = -25
gravidade = 0.9

# Obstáculo e objetivo
obstaculo = pygame.Rect(
    360,
    chao - ALT_OBSTACULO,
    LARG_OBSTACULO,
    ALT_OBSTACULO
)

objetivo = pygame.Rect(
    590,
    chao - TAM_OBJETIVO,
    TAM_OBJETIVO,
    TAM_OBJETIVO
)

mensagem = ""
rodando = True

while rodando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False

    teclas = pygame.key.get_pressed()

    # Movimento para direita
    if teclas[pygame.K_RIGHT]:
        x += vel

    # Movimento para esquerda
    if teclas[pygame.K_LEFT]:
        x -= vel

    # Pulo
    if teclas[pygame.K_SPACE] and not pulando:
        pulando = True
        velocidade_pulo = forca_pulo

    # Aplicando gravidade
    if pulando:
        y += velocidade_pulo
        velocidade_pulo += gravidade

        if y >= chao - TAM_PERSONAGEM:
            y = chao - TAM_PERSONAGEM
            pulando = False

    # Caixa de colisão do personagem
    player = pygame.Rect(
        x + 25,
        y + 20,
        70,
        90
    )

    # Colisão com obstáculo
    if player.colliderect(obstaculo):
        x = 70
        y = chao - TAM_PERSONAGEM
        mensagem = "Tente novamente"

    # Colisão com objetivo
    if player.colliderect(objetivo):
        mensagem = "Voce venceu"

    # Desenhar cenário
    tela.fill((135, 206, 235)) # céu azul
    tela.blit(obstaculo_img, (obstaculo.x, obstaculo.y))
    tela.blit(objetivo_img, (objetivo.x, objetivo.y))
    tela.blit(personagem, (x, y))

    # Mostrar mensagem
    if mensagem:
        texto = fonte.render(mensagem, True, (0, 0, 0))
        tela.blit(texto, (30, 30))

    pygame.display.flip()
    rel.tick(60)

pygame.quit()

