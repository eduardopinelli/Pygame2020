"""
Jogo feito em Pygame
Projeto Final - DeSoft
Insper Instituto de Ensino e Pesquisa
Autor: Eduardo Lima Pinelli
"""

import os
import sys
import random
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
        obstaculo1 = pygame.image.load(os.path.join("imagens", "obstaculo1.png")).convert()
        obstaculo2 = pygame.image.load(os.path.join("imagens", "obstaculo2.png")).convert()
        obstaculo3 = pygame.image.load(os.path.join("imagens", "obstaculo3.png")).convert()

        lista_obstaculos = [obstaculo1, obstaculo2, obstaculo3]

        self.image = carrega_sprite(random.choice(lista_obstaculos))
        self.rect = self.image.get_rect()
        self.speedx = 4

    def update(self):
        self.rect.left = 750
        self.rect.y = 280
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
    obstaculos = pygame.sprite.Group()  # criando o grupo de sprites de obstaculos
    sprites.add(obstaculos)

    # Rotinas musica de fundo
    arquivo_mus = os.path.join('sons', 'bg_music.ogg')
    path_mus = os.path.join(os.path.dirname(__file__), arquivo_mus)
    pygame.mixer.music.load(path_mus)  # carrega o arquivo da musica
    pygame.mixer.music.set_volume(0.3)  # ajusta o volume da musica
    pygame.mixer.music.play(-1)  # da play na musica / loop, -1 = infinito

    # Carregando arquivo de som dos tiros
    arquivo_tiro = os.path.join('sons', 'tiro.ogg')
    som_tiro = carrega_som(arquivo_tiro)

    fonte_score = pygame.font.Font(pygame.font.get_default_font(), 20)  # fonte score
    fonte_pause = pygame.font.Font(pygame.font.get_default_font(), 30)  # fonte texto jogo pausado

    rel = pygame.time.Clock()  # obj para controle das atualizacoes de imagem

    pygame.time.set_timer(pygame.USEREVENT, 2000)  # timer de 2 segundos

    score = 0  # pontuacao do jogador

    play = 0  # variavel que indica que o jogo está sendo rodado
    pause = 1  # variavel que indica que o jogo está pausado

    jogo = play  # jogo no inicio está sendo rodado

    # codigo que percebe caso ocorra colisao
    colisao = pygame.sprite.spritecollide(dinossaurinho, obstaculos, False, pygame.sprite.collide_circle)

    # Loop do Jogo

    while True:
        var_tempo = rel.tick(60)  # velocidade de refresh da tela do jogo

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
                    if jogo == play:  # codigo que pausa o jogo por completo
                        pygame.mixer.music.pause()
                        texto_pausa = fonte_pause.render("PAUSE", True, VERDE, CINZA)
                        tela.blit(texto_pausa, ((tela.get_width()-texto_pausa.get_width())/2,
                                                (tela.get_height()-texto_pausa.get_height())/2))
                        jogo = pause
                    else:  # codigo que despausa o jogo
                        pygame.mixer.music.unpause()
                        jogo = play
                if evento.key == pygame.K_UP:
                    som_tiro.play()
                    dinossaurinho.rect.bottom = 220

            if evento.type == pygame.KEYUP:
                if evento.key == pygame.K_UP:
                    dinossaurinho.rect.bottom = 300

            #if evento.type == pygame.KEYUP:
               # if evento.key == pygame.K_UP:
               #     pos_dino[1] = 300 - dinossaurinho.get_height()

            if jogo == pause:
                pygame.display.flip()
                continue

            #if evento.type == pygame.USEREVENT and jogo == play:


            if colisao:  # codigo que roda caso ocorra colisao
                for i in obstaculos:
                    i.kill()
                pygame.display.update()
                tela.fill(BRANCO)
                pygame.display.flip()
                gameover = fonte_pause.render("FIM DE JOGO", True, PRETO, BRANCO)
                tela.blit(gameover, ((tela.get_width()-gameover.get_width()/2),
                                     tela.get_height()-gameover.get_height()/2))

            sprites.draw(tela)
            pygame.display.flip()  # faz a atualização da tela


if __name__ == "__main__":
    main()

main()