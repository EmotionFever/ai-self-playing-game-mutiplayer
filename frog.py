import pygame
import random
import numpy as np
from platform2 import Platform
from object import Object
from random import randrange

MOVE_DISTANCE = 39
MOVE_DISTANCE_PREDICTION = 39 #35 esta muito perto

class Node(object):
    point = tuple()
    parent = None

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
        self.known_map =  dict() #dicionario com acoes que nao se devem executar num ponto
        self.desires=[] #TODO RECTS INICIAIS DOS NENUFARES nenufares possiveis de atingir
        aux=0 
        self.canMoveUp=False
        self.canMoveDown=False
        self.canMoveRight=False
        self.canMoveLeft=False
        
        for i in range(5):#estes sao os desires que pode ter (nenufares)
            self.desires.append((47+aux,9))
            aux+=81
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
    
    ############################ REACTIVE ##########################################################################
    
    def frogDecision(self,enemys,platforms_in, screen,sprite_platform,sprite_platform_quad,frogs):
        if(self.can_move==0):
            return
        self.incSteps()
        #criar plataforms
        platforms=platforms_in.copy()
        
        #self.drawRectangle(self.rect(), False, screen)

        # for plat in platforms:
        #     self.drawRectangle(plat.rect(),screen)

        self.canMoveUp = self.position[1] > 39
        self.canMoveDown = self.position[1] < 473
        self.canMoveLeft = self.position[0] > 2
        self.canMoveRight = self.position[0] < 401

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
            #print("Esta na estrada")
            for car in enemys:#verificar se nao bate num carro
                if self.canMoveUp and upRect.colliderect(car.rect()):
                    self.canMoveUp = False
                
                if self.canMoveDown and downRect.colliderect(car.rect()):
                    self.canMoveDown = False

                if self.canMoveLeft and leftRect.colliderect(car.rect()):
                    self.canMoveLeft = False
                
                if self.canMoveRight and rightRect.colliderect(car.rect()):
                    self.canMoveRight = False

                # canMoveUp = canMoveUp and not upRect.colliderect(car.rect())
                # canMoveDown = canMoveDown and not downRect.colliderect(car.rect())
                # canMoveLeft = canMoveLeft and not leftRect.colliderect(car.rect())
                # canMoveRight = canMoveRight and not rightRect.colliderect(car.rect())
                
        #Se o sapo chegou no rio
        #O sapo pode andar se houver um tronco na posicao old: < 240
        elif self.position[1] < 270 and self.position[1] > 40:
            print("Esta no rio")
            self.canMoveUp=False
            self.canMoveDown=False
            self.canMoveLeft=False
            self.canMoveRight=False

            for plat in platforms:#verificar se ele esta em cima de um tonco

                if not self.canMoveUp and upRect.colliderect(plat.rect()):
                    self.canMoveUp = True
                
                if not self.canMoveDown and downRect.colliderect(plat.rect()):
                    self.canMoveDown = True

                if not self.canMoveLeft and leftRect.colliderect(plat.rect()):
                    self.canMoveLeft = True
                
                if not self.canMoveRight and rightRect.colliderect(plat.rect()):
                    self.canMoveRight = True

                # canMoveUp = canMoveUp and upRect.colliderect(plat.rect())
                # canMoveDown = canMoveDown and downRect.colliderect(plat.rect())
                # canMoveLeft = canMoveLeft and leftRect.colliderect(plat.rect())
                # canMoveRight = canMoveRight and rightRect.colliderect(plat.rect())
        #sapo chegou no objetivo
        #elif frog.position[1] < 40 : 

        # Verificar colisoes com o fim do mapa
        if rightRect.x >= 445:
            self.canMoveRight = False
        if leftRect.x <= 0:
            self.canMoveLeft = False
            
        # Verificar colisoes com outros sapos
        for frog in frogs:
            if self.canMoveUp and upRect.colliderect(frog.rect()):
                self.canMoveUp = False
                
            if self.canMoveDown and downRect.colliderect(frog.rect()):
                self.canMoveDown = False

            if self.canMoveLeft and leftRect.colliderect(frog.rect()):
                self.canMoveLeft = False
                
            if self.canMoveRight and rightRect.colliderect(frog.rect()):
                self.canMoveRight = False
        
        # desenhar retangulo ah volta 
        self.drawRectangle(upRect, self.canMoveUp, screen)
        self.drawRectangle(downRect, self.canMoveDown, screen)
        self.drawRectangle(leftRect, self.canMoveLeft, screen)
        self.drawRectangle(rightRect, self.canMoveRight, screen)
        #ate aqui, o sapo ja consegue sabe tudo a sua volta

        print("canMoveUp:" + str(self.canMoveUp))
        print("canMoveDown:" + str(self.canMoveDown))
        print("canMoveLeft:" + str(self.canMoveLeft))
        print("canMoveRight:" + str(self.canMoveRight))

        
        #possible_actions = [true, false, true, true]
        #random entre 0 - 3
        #if possible_actions[random] == true => act() introduzir aleatoriedade 80% - 20% ... 
        possible_actions = [self.canMoveUp,self.canMoveDown,self.canMoveLeft,self.canMoveRight]
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

    ################################# END OF REACTIVE ###################################################################

    ############################ Deliberative ##########################################################
    def deliberativeDecision(self,enemys,platforms_in, screen,sprite_platform,sprite_platform_quad,frogs):#TODO
        self.updateBeliefs(enemys,platforms_in, screen,sprite_platform,sprite_platform_quad,frogs)
        #se nao tem intention, obtem uma nova
        if (self.intention==None):
            self.deliberate()
        #se o plano estiver vazio entao criar um plano
        if (len(self.plan) == 0):
            self.buildPlan()
        #se o plano nao estiver vazio, *tentar* correr a primeira acao usando a funcao sound
        if (self.sound()):
            self.executeAction()
        else:
            self.buildPlan()
        

    def deliberate(self):#escolhe o desire para intention
        if(len(self.desires) !=0 ) :
            self.intention=self.desires[randrange(len(self.desires))]
        self.intention = (209,9)

    def updateBeliefs(self,enemys,platforms_in, screen,sprite_platform,sprite_platform_quad,frogs):
        #olha a volta e melhora o internal state (know_map)
        #ver canMoveUp, canMoveRight.... e atualiza o know_map

        platforms=platforms_in.copy()

        self.canMoveUp    = self.position[1] > 39
        self.canMoveDown  = self.position[1] < 473
        self.canMoveLeft  = self.position[0] > 2
        self.canMoveRight = self.position[0] < 401

        posYUp    = self.position[1] - MOVE_DISTANCE_PREDICTION
        posYDown  = self.position[1] + MOVE_DISTANCE_PREDICTION
        posXRight = self.position[0] + MOVE_DISTANCE_PREDICTION
        posXLeft  = self.position[0] - MOVE_DISTANCE_PREDICTION

        upRect    = pygame.Rect(self.position[0],posYUp,30,30)
        downRect  = pygame.Rect(self.position[0],posYDown,30,30)
        leftRect  = pygame.Rect(posXLeft,self.position[1],30,30)
        rightRect = pygame.Rect(posXRight,self.position[1],30,30)

        #Se o sapo ainda não passou da estrada
        #O sapo pode andar se nao houver um carro na posicao old: > 240
        if self.position[1] > 270 :
            #print("Esta na estrada")
            for car in enemys:#verificar se nao bate num carro
                if self.canMoveUp and upRect.colliderect(car.rect()):
                    self.canMoveUp = False
                if self.canMoveDown and downRect.colliderect(car.rect()):
                    self.canMoveDown = False
                if self.canMoveLeft and leftRect.colliderect(car.rect()):
                    self.canMoveLeft = False
                if self.canMoveRight and rightRect.colliderect(car.rect()):
                    self.canMoveRight = False
                
        #Se o sapo chegou no rio
        #O sapo pode andar se houver um tronco na posicao old: < 240
        elif self.position[1] < 270 and self.position[1] > 40:
            print("Esta no rio")
            self.canMoveUp=False
            self.canMoveDown=False
            self.canMoveLeft=False
            self.canMoveRight=False

            for plat in platforms:#verificar se ele esta em cima de um tonco
                if not self.canMoveUp and upRect.colliderect(plat.rect()):
                    self.canMoveUp = True
                if not self.canMoveDown and downRect.colliderect(plat.rect()):
                    self.canMoveDown = True
                if not self.canMoveLeft and leftRect.colliderect(plat.rect()):
                    self.canMoveLeft = True
                if not self.canMoveRight and rightRect.colliderect(plat.rect()):
                    self.canMoveRight = True
        #sapo chegou no objetivo
        #elif frog.position[1] < 40 : 

        # Verificar colisoes com o fim do mapa
        if rightRect.x >= 445:
            self.canMoveRight = False
        if leftRect.x <= 0:
            self.canMoveLeft = False
        
        # desenhar retangulo ah volta 
        self.drawRectangle(upRect, self.canMoveUp, screen)
        self.drawRectangle(downRect, self.canMoveDown, screen)
        self.drawRectangle(leftRect, self.canMoveLeft, screen)
        self.drawRectangle(rightRect, self.canMoveRight, screen)

        #vamos atualizar o know_map
        posX = self.position[0]
        posY = self.position[1]

        prohibited_actions = []
        if not(self.canMoveUp):
            prohibited_actions.append("up") 
        if not(self.canMoveDown):
            prohibited_actions.append("down")
        if not(self.canMoveLeft):
            prohibited_actions.append("left")
        if not(self.canMoveRight):
            prohibited_actions.append("right")
        #se depois das verificacoes a lista de acoes proibidas nesta posicao continua vazia, nao adicionar ao know_map     
        if len(prohibited_actions) > 0:
            if (posX,posY) not in self.known_map.keys():
                self.known_map[(posX,posY)] = set()
            self.known_map[(posX,posY)].update(prohibited_actions)
        
        #ISTO NAO PODE SAIR DAQUI, ** POR BAIXO DO ATUALIZAR DO KNOW_MAP **
        # Verificar colisoes com outros sapos
        for frog in frogs:
            if self.canMoveUp and upRect.colliderect(frog.rect()):
                self.canMoveUp = False
                
            if self.canMoveDown and downRect.colliderect(frog.rect()):
                self.canMoveDown = False

            if self.canMoveLeft and leftRect.colliderect(frog.rect()):
               self.canMoveLeft = False
                
            if self.canMoveRight and rightRect.colliderect(frog.rect()):
                self.canMoveRight = False
    
    def sound(self):#verifica se a proxima acao leva a morte
        #verifica se não pode executar a proxima acao do plano usando o know_map
        if(len(self.plan) == 0):
            return False
        next_action = self.plan[0]
        if next_action == "up":
            return self.canMoveUp
        if next_action == "down":
            return self.canMoveDown
        if next_action == "left":
            return self.canMoveLeft
        if next_action == "right":
            return self.canMoveRight
        return True
    
    def buildPlan(self):#usando o shortestPath, cria uma lista de acoes a executar
        #FOR pelos RECTS do shortestPath e ve como passar de um rect para outro
        res = self.shortestPath(self.position,self.intention)
        print(self.intention)
        path = [res.point]
        while(res.parent != None):
            res = res.parent
            path.insert(0,res.point)
        # o path tem os varios pontos por onde tem de passar
        print(path)
        self.plan = []
        p1 = path.pop(0)
        while(len(path) > 0):
            p2 = path.pop(0)
            action = self.howToReachFromTo(p1,p2)
            self.plan.append(action)
            p1=p2

        self.plan.append("up")   
        print(self.plan)
            
    def howToReachFromTo(self,p1,p2):#devolve a acao que deve ser executada para ir de um ponto para outro adjacente
        if(abs(p1[0] - p2[0]) < 10 and p1[1] < p2[1]):
            return "down"#nao tenho a certeza se este ta certo
        if(abs(p1[0] - p2[0]) < 10 and  p1[1] > p2[1]):
            return "up"#nao tenho a certeza se este ta certo
        if(p1[0] < p2[0]):
            return "right"
        if(p1[0] > p2[0]):
            return "left"


    def shortestPath(self,p1,p2):#dada a posicao atual e a posicao da intencao, cria uma lista de RECTS por onde tem de passar
        #tem que ter em conta o know_map, para nao fazer acoes que nao deve em certos pontos
        visited = np.zeros(shape=(600,600))
        visited[p1[0],p1[1]] = 1
        queue = []
        n1 = Node()
        n1.point = p1
        queue.append(n1)
        
        row = [0, -39, 39, 0]
        col = [-39, 0, 0, 39]
        #    up,left,right,down
        acts = ["up","left","right","down"]
        
        while(len(queue)>0):
            n = queue.pop(0)
            point = n.point
            for i in range(4):
                x = point[0] + row[i]
                y = point[1] + col[i]
                #if(x == p2[0] and y == p2[1]):
                if(abs(x - p2[0]) < 17  and abs(y - p2[1])< 17):#este 20 aqui nao pode estar certo...
                    ret = Node()
                    ret.point = p2
                    ret.parent = n
                    return ret
                if (((point[0],point[1]) not in self.known_map.keys() or acts[i] not in self.known_map[(point[0],point[1])])):
                    #print(self.known_map)
                    #print("Para o ponto:" + str(point) + " entrei para a acao:"+ acts[i] + ".")
                    aux = visited[x,y] == 0
                    if(visited[x,y] == 0 and x>2 and x<401 and y>39 and y<=475):
                        visited[x,y] = 1
                        new=Node()
                        new.point=(x,y)
                        new.parent= n
                        queue.append(new)
        return None
    
    def executeAction(self):#executa a acao que esta na primeira posicao do plano
        action = self.plan.pop(0)
        print("Posicao:" + str(self.position))
        self.act(action)

    def setPositionToInitialPosition(self):
        self.position = self.initial_pos.copy()

    def draw(self, screen):
        current_sprite = self.animation_counter * 30
        screen.blit(self.sprite,(self.position),(0 + current_sprite, 0, 30, 30 + current_sprite))

    def rect(self): 
        return pygame.Rect(self.position[0],self.position[1],30,30)
    
    def act(self,decision):
        self.moveFrog(decision,1)
