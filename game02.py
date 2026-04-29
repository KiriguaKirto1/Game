import pygame

# Inicializa todos os módulos do pygame
pygame.init()

# Define as dimensões da janela
LARGURA, ALTURA = 720, 720
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Meu primeiro jogo")

# Variável com a cor do fundo em RGB (neste caso, um tom de azul)
COR_FUNDO = (30, 144, 255)

rodando = True
while rodando:
    # Verifica eventos (como clicar no 'X' para fechar)
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False

    # Pintar o fundo da tela
    tela.fill(COR_FUNDO)

    # Atualiza o conteúdo da tela
    pygame.display.flip()

# Encerra o pygame
pygame.quit()

