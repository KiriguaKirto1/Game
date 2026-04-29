import pygame
import sys

# =========================
# CONFIGURAÇÕES INICIAIS
# =========================
pygame.init()

LARGURA = 900
ALTURA = 500
TELA = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Mini Plataforma - Aula Python")

RELOGIO = pygame.time.Clock()
FPS = 60

# Cores
AZUL_CEU = (120, 190, 255)
VERDE = (80, 180, 80)
MARROM = (120, 75, 35)
BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)
VERMELHO = (220, 50, 50)
AMARELO = (255, 220, 80)
ROXO = (150, 80, 200)

# Física
GRAVIDADE = 0.8
FORCA_PULO = -15
VELOCIDADE_JOGADOR = 5

# =========================
# CLASSES DO JOGO
# =========================
class Jogador:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 45, 60)
        self.vel_y = 0
        self.no_chao = False
        self.vivo = True
        self.direcao = 1
        self.frame_animacao = 0

    def mover(self, teclas, plataformas):
        dx = 0

        if teclas[pygame.K_LEFT] or teclas[pygame.K_a]:
            dx = -VELOCIDADE_JOGADOR
            self.direcao = -1
        if teclas[pygame.K_RIGHT] or teclas[pygame.K_d]:
            dx = VELOCIDADE_JOGADOR
            self.direcao = 1

        if (teclas[pygame.K_SPACE] or teclas[pygame.K_UP] or teclas[pygame.K_w]) and self.no_chao:
            self.vel_y = FORCA_PULO
            self.no_chao = False

        # Movimento horizontal
        self.rect.x += dx
        for plataforma in plataformas:
            if self.rect.colliderect(plataforma):
                if dx > 0:
                    self.rect.right = plataforma.left
                elif dx < 0:
                    self.rect.left = plataforma.right

        # Movimento vertical
        self.vel_y += GRAVIDADE
        self.rect.y += self.vel_y
        self.no_chao = False

        for plataforma in plataformas:
            if self.rect.colliderect(plataforma):
                if self.vel_y > 0:
                    self.rect.bottom = plataforma.top
                    self.vel_y = 0
                    self.no_chao = True
                elif self.vel_y < 0:
                    self.rect.top = plataforma.bottom
                    self.vel_y = 0

        # Limites da tela
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > LARGURA:
            self.rect.right = LARGURA

        if self.rect.top > ALTURA:
            self.vivo = False

        self.frame_animacao += 1

    def desenhar(self, tela):
        # Corpo
        pygame.draw.rect(tela, ROXO, self.rect, border_radius=8)

        # Rosto
        olho_y = self.rect.y + 15
        if self.direcao == 1:
            pygame.draw.circle(tela, BRANCO, (self.rect.x + 30, olho_y), 5)
            pygame.draw.circle(tela, PRETO, (self.rect.x + 32, olho_y), 2)
        else:
            pygame.draw.circle(tela, BRANCO, (self.rect.x + 15, olho_y), 5)
            pygame.draw.circle(tela, PRETO, (self.rect.x + 13, olho_y), 2)

        # Animação simples das pernas
        if self.no_chao:
            movimento = 5 if (self.frame_animacao // 10) % 2 == 0 else -5
        else:
            movimento = 0

        pygame.draw.line(tela, PRETO, (self.rect.x + 12, self.rect.bottom), (self.rect.x + 12 + movimento, self.rect.bottom + 12), 4)
        pygame.draw.line(tela, PRETO, (self.rect.x + 33, self.rect.bottom), (self.rect.x + 33 - movimento, self.rect.bottom + 12), 4)


class Inimigo:
    def __init__(self, x, y, limite_esq, limite_dir):
        self.rect = pygame.Rect(x, y, 45, 40)
        self.vel_x = 2
        self.limite_esq = limite_esq
        self.limite_dir = limite_dir
        self.vivo = True
        self.animacao_morte = 0
        self.frame_animacao = 0

    def atualizar(self):
        if self.vivo:
            self.rect.x += self.vel_x

            if self.rect.left <= self.limite_esq or self.rect.right >= self.limite_dir:
                self.vel_x *= -1

            self.frame_animacao += 1
        else:
            if self.animacao_morte < 30:
                self.animacao_morte += 1

    def desenhar(self, tela):
        if self.vivo:
            pygame.draw.rect(tela, VERMELHO, self.rect, border_radius=10)

            # Olhos
            pygame.draw.circle(tela, BRANCO, (self.rect.x + 13, self.rect.y + 13), 5)
            pygame.draw.circle(tela, BRANCO, (self.rect.x + 32, self.rect.y + 13), 5)
            pygame.draw.circle(tela, PRETO, (self.rect.x + 13, self.rect.y + 13), 2)
            pygame.draw.circle(tela, PRETO, (self.rect.x + 32, self.rect.y + 13), 2)

            # Perninhas animadas
            movimento = 4 if (self.frame_animacao // 10) % 2 == 0 else -4
            pygame.draw.line(tela, PRETO, (self.rect.x + 10, self.rect.bottom), (self.rect.x + 10 + movimento, self.rect.bottom + 8), 3)
            pygame.draw.line(tela, PRETO, (self.rect.x + 35, self.rect.bottom), (self.rect.x + 35 - movimento, self.rect.bottom + 8), 3)
        else:
            # Animação de morte: inimigo achatado e desaparecendo
            altura = max(5, 40 - self.animacao_morte)
            inimigo_morto = pygame.Rect(self.rect.x, self.rect.bottom - altura, self.rect.width, altura)
            pygame.draw.rect(tela, AMARELO, inimigo_morto, border_radius=8)

    def terminou_morte(self):
        return not self.vivo and self.animacao_morte >= 30


# =========================
# FUNÇÕES AUXILIARES
# =========================
def desenhar_fundo(tela):
    tela.fill(AZUL_CEU)

    # Sol
    pygame.draw.circle(tela, AMARELO, (760, 80), 45)

    # Nuvens
    pygame.draw.circle(tela, BRANCO, (120, 90), 25)
    pygame.draw.circle(tela, BRANCO, (150, 80), 35)
    pygame.draw.circle(tela, BRANCO, (185, 90), 25)

    pygame.draw.circle(tela, BRANCO, (440, 120), 22)
    pygame.draw.circle(tela, BRANCO, (470, 110), 32)
    pygame.draw.circle(tela, BRANCO, (505, 120), 22)

    # Montanhas simples
    pygame.draw.polygon(tela, (90, 150, 100), [(0, 400), (160, 190), (320, 400)])
    pygame.draw.polygon(tela, (70, 130, 90), [(240, 400), (450, 160), (660, 400)])
    pygame.draw.polygon(tela, (90, 150, 100), [(580, 400), (760, 210), (940, 400)])


def desenhar_plataformas(tela, plataformas):
    for plataforma in plataformas:
        pygame.draw.rect(tela, MARROM, plataforma)
        grama = pygame.Rect(plataforma.x, plataforma.y, plataforma.width, 12)
        pygame.draw.rect(tela, VERDE, grama)


def desenhar_texto(tela, texto, tamanho, cor, x, y):
    fonte = pygame.font.SysFont("arial", tamanho, bold=True)
    imagem = fonte.render(texto, True, cor)
    tela.blit(imagem, (x, y))


def reiniciar_jogo():
    jogador = Jogador(80, 300)

    plataformas = [
        pygame.Rect(0, 440, 900, 60),
        pygame.Rect(180, 350, 160, 30),
        pygame.Rect(430, 280, 170, 30),
        pygame.Rect(680, 360, 150, 30),
    ]

    inimigos = [
        Inimigo(360, 400, 300, 620),
        Inimigo(470, 240, 430, 600),
        Inimigo(700, 320, 680, 830),
    ]

    return jogador, plataformas, inimigos, False, False


# =========================
# LOOP PRINCIPAL
# =========================
jogador, plataformas, inimigos, game_over, venceu = reiniciar_jogo()

while True:
    RELOGIO.tick(FPS)

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_r and (game_over or venceu):
                jogador, plataformas, inimigos, game_over, venceu = reiniciar_jogo()

    teclas = pygame.key.get_pressed()

    if not game_over and not venceu:
        jogador.mover(teclas, plataformas)

        for inimigo in inimigos:
            inimigo.atualizar()

            if inimigo.vivo and jogador.rect.colliderect(inimigo.rect):
                # Se o jogador estiver caindo e bater por cima, derrota o inimigo
                if jogador.vel_y > 0 and jogador.rect.bottom - inimigo.rect.top < 25:
                    inimigo.vivo = False
                    jogador.vel_y = -10
                else:
                    jogador.vivo = False
                    game_over = True

        inimigos = [inimigo for inimigo in inimigos if not inimigo.terminou_morte()]

        if not jogador.vivo:
            game_over = True

        if len(inimigos) == 0:
            venceu = True

    desenhar_fundo(TELA)
    desenhar_plataformas(TELA, plataformas)

    for inimigo in inimigos:
        inimigo.desenhar(TELA)

    jogador.desenhar(TELA)

    desenhar_texto(TELA, "Use A/D ou setas para mover | Espaço para pular", 22, PRETO, 20, 20)
    desenhar_texto(TELA, f"Inimigos restantes: {len(inimigos)}", 22, PRETO, 20, 50)

    if game_over:
        pygame.draw.rect(TELA, (0, 0, 0), (250, 160, 400, 150), border_radius=15)
        desenhar_texto(TELA, "VOCÊ PERDEU!", 40, VERMELHO, 315, 190)
        desenhar_texto(TELA, "Aperte R para reiniciar", 25, BRANCO, 325, 245)

    if venceu:
        pygame.draw.rect(TELA, (0, 0, 0), (250, 160, 400, 150), border_radius=15)
        desenhar_texto(TELA, "VOCÊ VENCEU!", 40, VERDE, 315, 190)
        desenhar_texto(TELA, "Aperte R para jogar de novo", 25, BRANCO, 300, 245)

    pygame.display.update()
