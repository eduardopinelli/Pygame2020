"""
Jogo feito em Pygame
Projeto Final - DeSoft
Insper Instituto de Ensino e Pesquisa
Autor: Eduardo Lima Pinelli
"""

import os
import sys
import pygame

# variaveis das cores

CINZA = (127, 127, 127)
ROXO = (255, 0, 255)
BRANCO = (255, 255, 255)
AZUL = (0, 0, 255)
VERDE = (0, 255, 0)
VERMELHO = (255, 0, 0)
PRETO = (0, 0, 0)

# dicionario e funcao para carregamento dos sprites
dict_sprite = {}


def carrega_sprite(sprite):
    if sprite not in dict_sprite:
        try:
            path_sprite = os.path.join(os.path.dirname(__file__), sprite)
            dict_sprite[sprite] = pygame.image.load(path_sprite).convert_alpha()
        except pygame.error:
            print("Erro ao tentar ler arquivo: {0}".format(sprite))
            sys.exit()
    return dict_sprite[sprite]


# dicionario e funcao para carregamento dos sons
dict_som = {}


def carrega_som(som):
    if som not in dict_sprite:
        try:
            path_som = os.path.join(os.path.dirname(__file__), som)
            dict_som[som] = pygame.mixer.Sound(path_som)
        except pygame.error:
            print("Erro ao tentar ler arquivo: {0}".format(som))
            sys.exit()
    return dict_som[som]


# classe do personagem principal

class Personagem(pygame.sprite.Sprite):
    def __init__(self, group):
        super().__init__(group)
        img_dino = os.path.join('imagens', 'personagem.png')
        self.image = carrega_sprite(img_dino)
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.speedy = 0
        self.rect.bottom = 300
        self.rect.x = 50

    def update(self):
        self.rect.y += self.speedy


# classe dos obstaculos

class Obstaculos(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        img_obst = os.path.join("imagens", "obstaculo1.png")

        self.image = carrega_sprite(img_obst)
        self.rect = self.image.get_rect()
        self.speedx = -4
        self.set_posicao(700, 280)
        self.set_velocidade(-2, 0)
        self.rect.left = 700
        self.rect.bottom = 300

    def set_posicao(self, x, y):
        self.pos = pygame.math.Vector2(x, y)

    def set_velocidade(self, vx, vy):
        self.velocidade = pygame.math.Vector2(vx, vy)

    def update(self):
        self.rect.x += self.speedx


def main():

    pygame.init()  # inicializando as rotinas do pygame

    tela = pygame.display.set_mode((750, 300))  # criando a tela e dimensionando

    pygame.display.set_caption("Dinossaurinho")  # adicionando o titulo desejado à tela

    tela.fill(CINZA)  # preenchendo o fundo da tela de cinza

    # criando o personagem principal
    sprites = pygame.sprite.Group()
    dinossaurinho = Personagem(sprites)
    sprites.add(dinossaurinho)

    # Rotinas musica de fundo
    arquivo_mus = os.path.join('sons', 'bg_music.ogg')
    path_mus = os.path.join(os.path.dirname(__file__), arquivo_mus)
    pygame.mixer.music.load(path_mus)  # carrega o arquivo da musica
    pygame.mixer.music.set_volume(0.2)  # ajusta o volume da musica
    pygame.mixer.music.play(-1)  # da play na musica / loop, -1 = infinito

    # Carregando arquivo de som dos tiros
    arquivo_tiro = os.path.join('sons', 'tiro.ogg')
    som_tiro = carrega_som(arquivo_tiro)

    fonte_score = pygame.font.Font(pygame.font.get_default_font(), 20)  # fonte score
    fonte_pause = pygame.font.Font(pygame.font.get_default_font(), 30)  # fonte texto jogo pausado

    rel = pygame.time.Clock()  # obj para controle das atualizacoes de imagem

    pygame.time.set_timer(pygame.USEREVENT, 1500)  # timer de 2 segundos

    score = 0  # pontuacao do jogador

    play = 0  # variavel que indica que o jogo está sendo rodado
    pause = 1  # variavel que indica que o jogo está pausado

    jogo = play  # jogo no inicio está sendo rodado

    pontuacao = 0

    # Loop do Jogo

    while True:
        var_tempo = rel.tick(60)  # velocidade de refresh da tela do jogo
        pontuacao += var_tempo / 60

        eventos = pygame.event.get()  # pega os eventos que ocorrem na interação com o jogo

        for evento in eventos:
            if evento.type == pygame.QUIT:  # evento que aperta no X da janela e encerra o jogo
                pygame.quit()
                sys.exit()

            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:  # evento em que a tecla ESC é apertada e o jogo é encerrado
                    pygame.quit()
                    sys.exit()
                if evento.key == pygame.K_p:  # evento em que a tecla P é apertada e o jogo é pausado
                    if jogo != pause:  # codigo que pausa o jogo por completo
                        pygame.mixer.music.pause()
                        texto_pausa = fonte_pause.render("PAUSE", True, VERDE, CINZA)
                        tela.blit(texto_pausa, ((tela.get_width() - texto_pausa.get_width()) / 2,
                                          (tela.get_height() - texto_pausa.get_height()) / 2))
                        jogo = pause
                    else:  # codigo que despausa o jogo
                        pygame.mixer.music.unpause()
                        jogo = play

                if evento.key == pygame.K_UP:
                    som_tiro.play()
                    dinossaurinho.rect.bottom = 180

            if evento.type == pygame.KEYUP:
                if evento.key == pygame.K_UP:
                    dinossaurinho.rect.bottom = 300

            if evento.type == pygame.USEREVENT and jogo == play:
                obs = Obstaculos()  # criando sprites do personagem e já colocando no grupo de sprite
                sprites.add(obs)

        if jogo == pause:
            pygame.display.flip()
            continue

        tela.fill(CINZA)
        sprites.update()
        sprites.draw(tela)

        texto = fonte_score.render("Pontuação: {0}".format(int(pontuacao)), True, BRANCO)
        tela.blit(texto, ((tela.get_width()-texto.get_width())/2, 0))  # coloca na tela a pontuacao

        pygame.display.flip()  # faz a atualização da tela


if __name__ == "__main__":
    main()

main()