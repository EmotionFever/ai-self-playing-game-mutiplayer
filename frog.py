import pygame
import random
import numpy as np
from platform2 import Platform
from object import Object
from random import randrange

MOVE_DISTANCE = 39
MOVE_DISTANCE_PREDICTION = 39 #35 esta muito perto

class Frog(Object):
    def __init__(self,position,sprite_sapo):
        self.sprite = sprite_sapo
        self.initial_pos = position.copy()
        self.position = position.copy()
        self.deaths = 0
        self.steps = 0
        self.animation_counter = 0
        self.animation_tick = 1
        self.way = "down"
        self.can_move = 1
        self.known_map =  {} #dicionario com acoes que nao se devem executar num ponto
        self.desires = [] #TODO RECTS INICIAIS DOS NENUFARES nenufares possiveis de atingir
        self.intention = None #nenufar que este sapo quer atingir
        self.plan = [] #sequencia de acoes a tomar

    def moveUp(self):
        if self.position[1] > 39:
            self.position[1] = self.position[1]-MOVE_DISTANCE
        if self.animation_counter == 0 and self.way != "up":
            self.way = "up"
            frog_filename = './images/sprite_sheets_up.png'
            self.sprite = pygame.image.load(frog_filename).convert_alpha()
        #self.incAnimationCounter()
    
    def moveDown(self):
        if self.position[1] < 473:
            self.position[1] = self.position[1]+MOVE_DISTANCE
        if self.animation_counter == 0 and self.way != "down":
            self.way = "down"
            frog_filename = './images/sprite_sheets_down.png'
            self.sprite = pygame.image.load(frog_filename).convert_alpha()
        #self.incAnimationCounter()
    
    def moveLeft(self):
        if self.position[0] > 31:
            if self.animation_counter == 2:
                self.position[0] = self.position[0]-MOVE_DISTANCE
            else:
                self.position[0] = self.position[0]-MOVE_DISTANCE-1
        if self.animation_counter == 0 and self.way != "left":
            self.way = "left"
            frog_filename = './images/sprite_sheets_left.png'
            self.sprite = pygame.image.load(frog_filename).convert_alpha()
        #self.incAnimationCounter()

    def moveRight(self):
        if self.position[0] < 401:
            if self.animation_counter == 2 :
                self.position[0] = self.position[0]+MOVE_DISTANCE
            else:
                self.position[0] = self.position[0]+MOVE_DISTANCE+1
        if self.animation_counter == 0 and self.way != "right":
            self.way = "right"
            frog_filename = './images/sprite_sheets_right.png'
            self.sprite = pygame.image.load(frog_filename).convert_alpha()
        #self.incAnimationCounter()

    def moveFrog(self,key_pressed, key_up):
        #Tem que fazer o if das bordas da tela ainda
        #O movimento na horizontal ainda não ta certin
        if key_up == 1:
            if key_pressed == "up":
                self.moveUp()
            elif key_pressed == "down":
                self.moveDown()
            if key_pressed == "left":
                self.moveLeft()
            elif key_pressed == "right":
                self.moveRight()

    def animateFrog(self,key_pressed,key_up):
        if self.animation_counter != 0 :
            if self.animation_tick <= 0 :
                self.moveFrog(key_pressed,key_up)
                self.animation_tick = 1
            else :
                self.animation_tick = self.animation_tick - 1

    def setPos(self,position):
        self.position = position

    def incDeaths(self):
        self.deaths += 1

    def incSteps(self):
        self.steps += 1

    def cannotMove(self):
        self.can_move = 0

    def incAnimationCounter(self):
        self.animation_counter = self.animation_counter + 1
        if self.animation_counter == 3 :
            self.animation_counter = 0
            self.can_move = 1

    def frogDead(self,game):
        self.setPositionToInitialPosition()
        self.incDeaths()
        game.resetTime()
        self.animation_counter = 0
        self.animation_tick = 1
        self.way = "UP"
        self.can_move = 1

    def drawRectangle(self, rectangle, canMove, screen):#Usado para debug
        colorCannotMove = (255,0,0)
        colorCanMove = (0,130,0)
        color = colorCanMove if canMove else colorCannotMove
        
        # Drawing Rectangle
        pygame.draw.rect(screen, color, rectangle,  3)
        pygame.display.flip()
    
    def frogDecision(self,enemys,platforms_in, screen,sprite_platform,sprite_platform_quad,frogs):
        if(self.can_move==0):
            return
        self.incSteps()
        #criar plataforms
        platforms=platforms_in.copy()
        
        #self.drawRectangle(self.rect(), False, screen)

        # for plat in platforms:
        #     self.drawRectangle(plat.rect(),screen)

        canMoveUp = self.position[1] > 39
        canMoveDown = self.position[1] < 473
        canMoveLeft = self.position[0] > 2
        canMoveRight = self.position[0] < 401

        posYUp = self.position[1]-MOVE_DISTANCE_PREDICTION
        posYDown = self.position[1]+MOVE_DISTANCE_PREDICTION
        posXRight = self.position[0]+MOVE_DISTANCE_PREDICTION
        posXLeft = self.position[0]-MOVE_DISTANCE_PREDICTION

        upRect = pygame.Rect(self.position[0],posYUp,30,30)
        downRect = pygame.Rect(self.position[0],posYDown,30,30)
        leftRect = pygame.Rect(posXLeft,self.position[1],30,30)
        rightRect = pygame.Rect(posXRight,self.position[1],30,30)

        #Se o sapo ainda não passou da estrada
        #O sapo pode andar se nao houver um carro na posicao old: > 240
        if self.position[1] > 270 :
            print("Esta na estrada")
            for car in enemys:#verificar se nao bate num carro
                if canMoveUp and upRect.colliderect(car.rect()):
                    canMoveUp = False
                
                if canMoveDown and downRect.colliderect(car.rect()):
                    canMoveDown = False

                if canMoveLeft and leftRect.colliderect(car.rect()):
                    canMoveLeft = False
                
                if canMoveRight and rightRect.colliderect(car.rect()):
                    canMoveRight = False

                # canMoveUp = canMoveUp and not upRect.colliderect(car.rect())
                # canMoveDown = canMoveDown and not downRect.colliderect(car.rect())
                # canMoveLeft = canMoveLeft and not leftRect.colliderect(car.rect())
                # canMoveRight = canMoveRight and not rightRect.colliderect(car.rect())
                
        #Se o sapo chegou no rio
        #O sapo pode andar se houver um tronco na posicao old: < 240
        elif self.position[1] < 270 and self.position[1] > 40:
            print("Esta no rio")
            canMoveUp=False
            canMoveDown=False
            canMoveLeft=False
            canMoveRight=False

            for plat in platforms:#verificar se ele esta em cima de um tonco

                if not canMoveUp and upRect.colliderect(plat.rect()):
                    canMoveUp = True
                
                if not canMoveDown and downRect.colliderect(plat.rect()):
                    canMoveDown = True

                if not canMoveLeft and leftRect.colliderect(plat.rect()):
                    canMoveLeft = True
                
                if not canMoveRight and rightRect.colliderect(plat.rect()):
                    canMoveRight = True

                # canMoveUp = canMoveUp and upRect.colliderect(plat.rect())
                # canMoveDown = canMoveDown and downRect.colliderect(plat.rect())
                # canMoveLeft = canMoveLeft and leftRect.colliderect(plat.rect())
                # canMoveRight = canMoveRight and rightRect.colliderect(plat.rect())
        #sapo chegou no objetivo
        #elif frog.position[1] < 40 : 

        # Verificar colisoes com o fim do mapa
        if rightRect.x >= 445:
            canMoveRight = False
        if leftRect.x <= 0:
            canMoveLeft = False
            
        # Verificar colisoes com outros sapos
        for frog in frogs:
            if canMoveUp and upRect.colliderect(frog.rect()):
                canMoveUp = False
                
            if canMoveDown and downRect.colliderect(frog.rect()):
                canMoveDown = False

            if canMoveLeft and leftRect.colliderect(frog.rect()):
                canMoveLeft = False
                
            if canMoveRight and rightRect.colliderect(frog.rect()):
                canMoveRight = False
        
        # desenhar retangulo ah volta 
        self.drawRectangle(upRect, canMoveUp, screen)
        self.drawRectangle(downRect, canMoveDown, screen)
        self.drawRectangle(leftRect, canMoveLeft, screen)
        self.drawRectangle(rightRect, canMoveRight, screen)
        #ate aqui, o sapo ja consegue sabe tudo a sua volta

        print("canMoveUp:" + str(canMoveUp))
        print("canMoveDown:" + str(canMoveDown))
        print("canMoveLeft:" + str(canMoveLeft))
        print("canMoveRight:" + str(canMoveRight))

        
        #possible_actions = [true, false, true, true]
        #random entre 0 - 3
        #if possible_actions[random] == true => act() introduzir aleatoriedade 80% - 20% ... 
        possible_actions = [canMoveUp,canMoveDown,canMoveLeft,canMoveRight]
        actions = ["up","down","left","right"]

        if self.position[1] > 270 : #esta na estrada
            priority = np.array([0.55, 0.05, 0.2, 0.2]) 
        else: #esta no rio
            priority = np.array([0.4,0.3,0.15,0.15])#0.6, 0.15, 0.125, 0.125


        possible_actions_int = np.array(possible_actions).astype(int)
        probs = np.multiply(priority,possible_actions) 

        if np.sum(probs) == 0:
            return

        probs = probs / (np.sum(probs)) #normalize
        
        return np.random.choice(actions,p=probs)


 #        if canMoveUp:#livre ou possivel ir para cima
 #            v = np.delete(np.array(possible_actions).astype(int), 0) # substitui o vector possible_actions para ints
 #            if np.sum(v) == 0:
 #                return "up"
 #            else:
 #                v = v / (np.sum(v)) * 0.2
 #                probs = np.insert(v, 0, 0.8)
 #                return np.random.choice(actions,p=probs)
 #        else:
 #            v = np.delete(np.array(possible_actions).astype(int), 1) # delete down

 #            v = np.array(possible_actions).astype(int) # [false, TF ,TF ,TF] => [0, 0-1, 0-1,0-1]
 #            if canMoveLeft or canMoveRight: 
 #                v = v / (np.sum(v)) * 0.2 * 0.8
            
 #            if not canMoveLeft and not canMoveRight:
 #                return "down"

 #            if canMoveDown:
                

 #            return np.random.choice(actions,p=v)




        # elif canMoveRight and canMoveLeft: #se nao pode ir para cima tenta ir para os lados (isto nao e verdade)
        #     v = np.delete(np.array(possible_actions).astype(int), 3) # substitui o vector possible_actions para ints
        #     if np.sum(v) == 0:
        #         return "right"
        #     else:
        #         v = v / (np.sum(v)) * 0.2
        #         probs = np.insert(v, 3, 0.8)
        #         return np.random.choice(actions,p=probs)

        # elif canMoveLeft:
        #     v = np.delete(np.array(possible_actions).astype(int), 2) # substitui o vector possible_actions para ints
        #     if np.sum(v) == 0:
        #         return "left"
        #     else:
        #         v = v / (np.sum(v)) * 0.2
        #         probs = np.insert(v, 2, 0.8)
        #         return np.random.choice(actions,p=probs)

        # elif canMoveDown:
        #     v = np.delete(np.array(possible_actions).astype(int), 1) # substitui o vector possible_actions para ints
        #     if np.sum(v) == 0:
        #         return "down"
        #     else:
        #         v = v / (np.sum(v)) * 0.2
        #         probs = np.insert(v, 1, 0.8)
        #         return np.random.choice(actions,p=probs)

        # else: #
        #     return ""
        #bloqueado de todos lados
            # nao faz nada

    #Deliberative

    def deliberate(self):#escolhe o desire para intention
        if(len(desires) !=0 ) :
            self.intention=self.desires[randrange(len(self.desires))]

    def updateBeliefs(self):#olha a volta e melhora o internal state (know_map)
        #ver canMoveUp, canMoveRight.... e atualiza o know_map
        return
    
    def sound(self):#verifica se a proxima acao leva a morte
        #verifica se não pode executar a proxima acao do plano usando o know_map
        return True
    
    def buildPlan(self):#usando o shortestPath, cria uma lista de acoes a executar
        #FOR pelos RECTS do shortestPath e ve como passar de um rect para outro
        return

    def shortestPath(self):#dada a posicao atual e a posicao da intencao, cria uma lista de RECTS por onde tem de passar
        #tem que ter em conta o know_map, para nao fazer acoes que nao deve em certos pontos
        return None
    
    def executeAction(self):#executa a acao dada
        return


    def setPositionToInitialPosition(self):
        self.position = self.initial_pos.copy()

    def draw(self, screen):
        current_sprite = self.animation_counter * 30
        screen.blit(self.sprite,(self.position),(0 + current_sprite, 0, 30, 30 + current_sprite))

    def rect(self): 
        return pygame.Rect(self.position[0],self.position[1],30,30)
    
    def act(self,decision):
        self.moveFrog(decision,1)
