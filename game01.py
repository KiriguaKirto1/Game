import pygame

# Inicializando o Pygame
pygame.init()

# Definindo o tamanho da janela
LARGURA, ALTURA = 720, 720
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Nome da janela")

# Loop principal do jogo
rodando = True
while rodando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False

    # Preencher o fundo (opcional, para não deixar rastro)
    tela.fill((0, 0, 0))

    # Atualizar a tela
    pygame.display.flip()

# Finalizar o Pygame
pygame.quit()




