#imports
import pygame 
from pygame.locals import *
from sys import exit 
from random import randint


pygame.init() #inicialização do pygame

pygame.mixer.music.set_volume(0.25)
musica_fundo = pygame.mixer.music.load('musica_fundo.mp3')
pygame.mixer.music.play(-1)

barulho_colisao = pygame.mixer.Sound('uiu.wav')
barulho_colisao.set_volume(1)
#Definir tamanho da janela
largura = 640
altura = 480

x_cobra = int(largura/2)       #para colocar o objeto EXATAMENTE no meio da tela seria preciso 
y_cobra = int(altura/2)        #usar a formula: MEIO = largura_tela/2 - largura_objeto/2

velocidade = 10
x_controle = 10
y_controle = 0

x_maca = randint(40, 600)
y_maca = randint(50, 430)

pontos = 0

fonte = pygame.font.SysFont('arial', 40, True, False)   #Cria a fonte com os parametros: Fonte, Tamanho,
                                                        #Negrito e Italico (respectivamente)



tela = pygame.display.set_mode((largura, altura)) #Cria a janela

pygame.display.set_caption('GAME') #Coloca um título na janela

relogio = pygame.time.Clock()

lista_cobra = []
comprimento_inicial = 5

morreu = False

def aumenta_cobra(lista_cobra):
    for XeY in lista_cobra:
        #XeY = [x, y]
        #XeY[0] = x
        #XeY[1] = y

        pygame.draw.rect(tela, (0,255,0), (XeY[0], XeY[1], 20, 20))

def reiniciar_jogo():
    global pontos, comprimento_inicial,x_cobra,y_cobra,lista_cabeca,lista_cobra,x_maca,y_maca, morreu
    pontos = 0
    comprimento_inicial = 5
    x_cobra = int(largura/2) 
    y_cobra = int(altura/2) 
    lista_cobra = []
    lista_cabeca = []
    x_maca = randint(40, 600)
    y_maca = randint(50, 430)
    morreu = False

#Todo jogo se passa em um loop, para criar o loop fazemos:
while True:
    relogio.tick(30) #define o fps
    
    tela.fill((255,255,255)) #a tela se preenche (com preto) a cada iteração

    mensagem = f'Pontos: {pontos}'
    texto_formatado = fonte.render(mensagem, False, (0,0,0))

    #Para verificar o acontecimento de eventos criamos este outro 'loop':
    for event in pygame.event.get():
        #Se o tipo de evento for 'quit' o jogo fecha:
        if event.type == QUIT:
            pygame.quit()
            exit()

        if event.type == KEYDOWN:
            if (event.key == K_w or event.key == K_UP) and y_controle != velocidade:
                x_controle = 0
                y_controle = -velocidade

            if (event.key == K_a or event.key == K_LEFT) and x_controle != velocidade:
                    x_controle = -velocidade
                    y_controle = 0

            if (event.key == K_s or event.key == K_DOWN) and y_controle != -velocidade:
                x_controle = 0
                y_controle = velocidade

            if (event.key == K_d or event.key == K_RIGHT) and x_controle != -velocidade:
                    x_controle = velocidade
                    y_controle = 0

    x_cobra += x_controle
    y_cobra += y_controle

    #para desenhar um quadrado na tela fazemos o seguinte:
    cobra = pygame.draw.rect(tela, (0,255,0), (x_cobra, y_cobra, 20, 20))  
    maca = pygame.draw.rect(tela, (255,0,0), (x_maca, y_maca, 20, 20))

    if cobra.colliderect(maca):     #Aplica a colisão
        x_maca = randint(40, 600)
        y_maca = randint(50, 430)

        pontos += 1
        barulho_colisao.play()
        comprimento_inicial += 1

    lista_cabeca = []                   #A cabeça deve ser uma lista [x, y] e o corpo
    lista_cabeca.append(x_cobra)        #outra lista, que recebe as posições anteriores
    lista_cabeca.append(y_cobra)        #da cabeça
    lista_cobra.append(lista_cabeca)

    if lista_cobra.count(lista_cabeca) > 1:
        fonte2 = pygame.font.SysFont('Arial', 30, True, False)
        mensagem = f'Perdeu! Aperte espaço para jogar novamente.'
        texto_formatado = fonte2.render(mensagem, True, (0,0,0))
        ret_texto = texto_formatado.get_rect()

        morreu = True
        while morreu:
            tela.fill((255,255,255))
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    exit()
                if event.type == KEYDOWN:
                    if event.key == K_SPACE:
                        reiniciar_jogo()

            ret_texto.center = (largura//2, altura//2)
            tela.blit(texto_formatado, ret_texto)
            pygame.display.update()            

    if x_cobra > largura:
        x_cobra = 0
    
    if x_cobra < 0:
        x_cobra = largura
    
    if y_cobra > altura:
        y_cobra = 0
    
    if y_cobra < 0:
        y_cobra = altura
    

    if len(lista_cobra) > comprimento_inicial:
        del lista_cobra[0]

    aumenta_cobra(lista_cobra)          


    tela.blit(texto_formatado, (450, 40))
    pygame.display.update() #Atualiza a telas