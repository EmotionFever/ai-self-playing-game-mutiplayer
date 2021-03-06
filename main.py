#! /usr/bin/env python
import pygame 
import random as Random
from pygame.locals import *
from sys import exit
from object import Object
from frog import Frog
#from frogwasd import FrogWASD
from enemy import Enemy
from platform2 import Platform
from game import Game

pygame.init()
pygame.font.init()
pygame.mixer.pre_init(44100, 32, 2, 4096)

#fonts...
font_name = pygame.font.get_default_font()
game_font = pygame.font.SysFont(font_name, 72)
info_font = pygame.font.SysFont(font_name, 24)
menu_font = pygame.font.SysFont(font_name, 36)

screen = pygame.display.set_mode((448,546), 0, 32)

# --- Carregando imagens ---
background_filename = './images/bg.png'
frog_filename = './images/sprite_sheets_up.png'
arrived_filename = './images/frog_arrived.png'
car1_filename = './images/car1.png'
car2_filename = './images/car2.png'
car3_filename = './images/car3.png'
car4_filename = './images/car4.png'
car5_filename = './images/car5.png'
plataform_filename = './images/tronco.png'

background = pygame.image.load(background_filename).convert()
sprite_sapo = pygame.image.load(frog_filename).convert_alpha()
sprite_arrived = pygame.image.load(arrived_filename).convert_alpha()
sprite_car1 = pygame.image.load(car1_filename).convert_alpha()
sprite_car2 = pygame.image.load(car2_filename).convert_alpha()
sprite_car3 = pygame.image.load(car3_filename).convert_alpha()
sprite_car4 = pygame.image.load(car4_filename).convert_alpha()
sprite_car5 = pygame.image.load(car5_filename).convert_alpha()
sprite_plataform = pygame.image.load(plataform_filename).convert_alpha()

pygame.display.set_caption('Frogger')
clock = pygame.time.Clock()

#Funções gerais
#Desenhar a lista dos inimigos/plataformas
def drawList(list):
    for i in list:
        i.draw(screen)

#Mover todos os elementos da lista na direcao adequada
def moveList(list,speed):
    for i in list:
        i.move(speed)
#Remover carros fora do ecra
def destroyEnemys(list):
    for i in list:
        if i.position[0] < -80:
            list.remove(i)
        elif i.position[0] > 516:
            list.remove(i)

#Remover plataformas fora do ecra
def destroyPlataforms(list):
    for i in list:
        if i.position[0] < -100:
            list.remove(i)
        elif i.position[0] > 448:
            list.remove(i)

#Criar os carros
def createEnemys(list,enemys,game):
    for i, tick in enumerate(list):
        list[i] = list[i] - 1
        if tick <= 0:
            if i == 0:
                list[0] = (40*game.speed)/game.level
                position_init = [-55,436]
                enemy = Enemy(position_init,sprite_car1,"right",1)
                enemys.append(enemy)
            elif i == 1:
                list[1] = (30*game.speed)/game.level
                position_init = [506, 397]
                enemy = Enemy(position_init,sprite_car2,"left",2)
                enemys.append(enemy)
            elif i == 2:
                list[2] = (40*game.speed)/game.level
                position_init = [-80, 357]
                enemy = Enemy(position_init,sprite_car3,"right",2)
                enemys.append(enemy)
            elif i == 3:
                list[3] = (30*game.speed)/game.level
                position_init = [516, 318]
                enemy = Enemy(position_init,sprite_car4,"left",1)
                enemys.append(enemy)
            elif i == 4:
                list[4] = (50*game.speed)/game.level
                position_init = [-56, 280]
                enemy = Enemy(position_init,sprite_car5,"right",1)
                enemys.append(enemy)

#Criar plataformas
def createPlatform(list,plataforms,game):
    for i, tick in enumerate(list):
        list[i] = list[i] - 1
        if tick <= 0:
            if i == 0:
                list[0] = (30*game.speed)/game.level
                position_init = [-100,200]
                plataform = Platform(position_init,sprite_plataform,"right")
                plataforms.append(plataform)
            elif i == 1:
                list[1] = (30*game.speed)/game.level
                position_init = [448, 161]
                plataform = Platform(position_init,sprite_plataform,"left")
                plataforms.append(plataform)
            elif i == 2:
                list[2] = (40*game.speed)/game.level
                position_init = [-100, 122]
                plataform = Platform(position_init,sprite_plataform,"right")
                plataforms.append(plataform)
            elif i == 3:
                list[3] = (40*game.speed)/game.level
                position_init = [448, 83]
                plataform = Platform(position_init,sprite_plataform,"left")
                plataforms.append(plataform)
            elif i == 4:
                list[4] = (20*game.speed)/game.level
                position_init = [-100, 44]
                plataform = Platform(position_init,sprite_plataform,"right")
                plataforms.append(plataform)

#Se o sapo esta na estrada, verificar se esta a colidir com um carro
def frogOnTheStreet(frog,enemys,game):
    for i in enemys:
        enemyRect = i.rect()
        frogRect = frog.rect()
        if frogRect.colliderect(enemyRect): # verificar se o sapo esta a colidir com um carro
            frog.frogDead(game)             # dar reset a esse sapo

#
def frogInTheLake(frog,plataforms,game):
    #se o sapo esta sob alguma plataforma Seguro = 1
    seguro = 0
    wayPlataform = ""
    for i in plataforms:
        plataformRect = i.rect()
        frogRect = frog.rect()
        if frogRect.colliderect(plataformRect): # se há uma plataforma por baixo do sapo
            seguro = 1
            wayPlataform = i.way

    if seguro == 0: # se não há plataforma por baixo do sapo
        frog.frogDead(game) # dar reset a esse sapo

    elif seguro == 1: # se está numa plataforma, mover o sapo com a plataforma
        if wayPlataform == "right":
            frog.position[0] = frog.position[0] + game.speed

        elif wayPlataform == "left":
            frog.position[0] = frog.position[0] - game.speed

def frogArrived(frog,chegaram,game):
    if frog.position[0] > 33 and frog.position[0] < 53: #primeira posicao de chegada
        position_init = [43,7] #posicao onde chegou
        createArrived(frog,chegaram,game,position_init) # adicionar o sapo a lista dos chegados

    elif frog.position[0] > 115 and frog.position[0] < 135:
        position_init = [125,7]
        createArrived(frog,chegaram,game,position_init)

    elif frog.position[0] > 197 and frog.position[0] < 217:
        position_init = [207,7]
        createArrived(frog,chegaram,game,position_init)

    elif frog.position[0] > 279 and frog.position[0] < 299:
        position_init = [289,7]
        createArrived(frog,chegaram,game,position_init)

    elif frog.position[0] > 361 and frog.position[0] < 381:
        position_init = [371,7]
        createArrived(frog,chegaram,game,position_init)

    else:
        frog.position[1] = 46
        frog.animation_counter = 0
        frog.animation_tick = 1
        frog.can_move = 1


def whereIsTheFrog(frog):
    #Se o sapo ainda não passou da estrada
    if frog.position[1] > 240 :
        frogOnTheStreet(frog,enemys,game)

    #Se o sapo chegou no rio
    elif frog.position[1] < 240 and frog.position[1] > 40:
        frogInTheLake(frog,plataforms,game)

    #sapo chegou no objetivo
    elif frog.position[1] < 40 :
        frogArrived(frog,chegaram,game)


def createArrived(frog,chegaram,game,position_init):
    sapo_chegou = Object(position_init,sprite_arrived)
    chegaram.append(sapo_chegou)
    frog.setPositionToInitialPosition()
    game.incPoints(10 + game.time) 

    frog.animation_counter = 0
    frog.animation_tick = 1
    frog.can_move = 1
    """
    game.resetTime()
    """


def nextLevel(chegaram,enemys,plataforms,frogs,game):
    if len(chegaram) == 5:
        chegaram[:] = []
        for frog in frogs:
            frog.setPositionToInitialPosition()
        game.incLevel()
        game.incSpeed()
        game.incPoints(100)
        game.resetTime()

text_info = menu_font.render(('Press any button to start!'),1,(0,0,0))
gameInit = 0
# game start we need to press any jey to start the game
while gameInit == 0:
    for event in pygame.event.get():
        if event.type == QUIT:
            exit()
        if event.type == KEYDOWN:
            gameInit = 1

    screen.blit(background, (0, 0))
    screen.blit(text_info,(80,150))
    pygame.display.update()

while True:
    gameInit = 1
    game = Game(3,1)
    key_up = 1
    # initial Frogs at the moment there are 2 
    frog_initial_positions = []
    frogs = []
    frog_initial_positions.append([125,475])
    frog_initial_positions.append([207,475])
    frogs.append(Frog(frog_initial_positions[0],sprite_sapo))
    frogs.append(Frog(frog_initial_positions[1],sprite_sapo))

    enemys = []
    plataforms = []
    chegaram = []
    #30 ticks == 1 segundo
    #ticks_enemys = [120, 90, 120, 90, 150]
    #ticks_plataforms = [90, 90, 120, 120, 60]
    ticks_enemys = [30, 0, 30, 0, 60]
    ticks_plataforms = [0, 0, 30, 30, 30]
    ticks_time = 30
    pressed_keys = 0
    key_pressed = 0

    while True: # before we finished the game when they were all dead

        # Handler to get events from keyboard
        for event in pygame.event.get():
            if event.type == QUIT:
                exit()
            # key up, move up
            if event.type == KEYUP:
                #flag variable to say that key got released, it avoids cliking the same key over and over again
                key_up = 1
            # a key got pressed
            if event.type == KEYDOWN:
                for frog in frogs:
                    if key_up == 1 and frog.can_move == 1 :
                        key_pressed = pygame.key.name(event.key)
                        frog.moveFrog(key_pressed,key_up)
                        frog.cannotMove()
        if not ticks_time:
            ticks_time = 30
            game.incTime()
        else:
            ticks_time -= 1

        createEnemys(ticks_enemys,enemys,game)
        createPlatform(ticks_plataforms,plataforms,game)

        moveList(enemys,game.speed)
        moveList(plataforms,game.speed)

        text_info1 = info_font.render(('Level: {0}               Points: {1}'.format(game.level,game.points)),1,(255,255,255))
        text_info2 = info_font.render(('Time: {0}'.format(game.time)),1,(255,255,255))
        screen.blit(background, (0, 0))
        screen.blit(text_info1,(10,520))
        screen.blit(text_info2,(250,520))
        offset = 0
        for frog in frogs:
            whereIsTheFrog(frog)
            text_info3 = info_font.render(('D: {1}'.format(game.time,frog.deaths)),1,(255,255,255))
            screen.blit(text_info3,(320 + offset*70,520))
            offset += 1
        nextLevel(chegaram,enemys,plataforms,frogs,game)

        drawList(enemys)
        drawList(plataforms)
        drawList(chegaram)

        for frog in frogs:
            frog.animateFrog(key_pressed,key_up)
            frog.draw(screen)

        destroyEnemys(enemys)
        destroyPlataforms(plataforms)

        pygame.display.update()
        time_passed = clock.tick(30)

    while gameInit == 1:
        for event in pygame.event.get():
            if event.type == QUIT:
                exit()
            if event.type == KEYDOWN:
                gameInit = 0

        screen.blit(background, (0, 0))
        text = game_font.render('GAME OVER', 1, (255, 0, 0))
        text_points = game_font.render(('Pontuação: {0}'.format(game.points)),1,(255,0,0))
        text_reiniciar = info_font.render('Pressione qualquer tecla para reiniciar!',1,(255,0,0))
        screen.blit(text, (75, 120))
        screen.blit(text_points,(10,170))
        screen.blit(text_reiniciar,(70,250))

        pygame.display.update()
