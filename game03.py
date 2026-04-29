import pygame
import os

# 1. Iniciar o pygame
pygame.init()

# 2. Configurações da janela
LARGURA = 720
ALTURA = 720
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Game 03 - Personagem")

# 3. Caminho da pasta de imagens
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PASTA_IMAGENS = os.path.join(BASE_DIR, "Assets")

# 4. Função para carregar imagem
def carregar_imagem(nome, largura, altura):
    caminho = os.path.join(PASTA_IMAGENS, nome)
    try:
        imagem = pygame.image.load(caminho).convert_alpha()
        imagem = pygame.transform.scale(imagem, (largura, altura))
        return imagem
    except pygame.error as e:
        print(f"Erro ao carregar imagem: {caminho}")
        raise SystemExit(e)

# 5. Carregar personagem
personagem = carregar_imagem("idle.png", 85, 85)

# 6. Posição inicial do personagem
x = 80
y = 600

# Controle de FPS
clock = pygame.time.Clock()

# 7. Loop principal
rodando = True
while rodando:
    # Gerenciador de eventos
    for evento in pygame.event.get():                
        if evento.type == pygame.QUIT:
            rodando = False

    # 8. Cor de fundo (Sky Blue)
    tela.fill((135, 206, 235))

    # 9. Desenhar personagem
    tela.blit(personagem, (x, y))

    # 10. Atualizar tela
    pygame.display.flip()
    
    # 60 quadros por segundo
    clock.tick(60)

# 11. Encerrar
pygame.quit()

