import pygame
from object import Object

class Frog(Object):
    def __init__(self,position,sprite_sapo):
        self.sprite = sprite_sapo
        self.initial_pos = position.copy()
        self.position = position.copy()
        self.deaths = 0
        self.animation_counter = 0
        self.animation_tick = 1
        self.way = "down"
        self.can_move = 1

    def moveUp(self):
        if self.position[1] > 39:
            self.position[1] = self.position[1]-13
        if self.animation_counter == 0 and self.way != "up":
            self.way = "up"
            frog_filename = './images/sprite_sheets_up.png'
            self.sprite = pygame.image.load(frog_filename).convert_alpha()
        self.incAnimationCounter()
    
    def moveDown(self):
        if self.position[1] < 473:
            self.position[1] = self.position[1]+13
        if self.animation_counter == 0 and self.way != "down":
            self.way = "down"
            frog_filename = './images/sprite_sheets_down.png'
            self.sprite = pygame.image.load(frog_filename).convert_alpha()
        self.incAnimationCounter()
    
    def moveLeft(self):
        if self.position[0] > 2:
            if self.animation_counter == 2:
                self.position[0] = self.position[0]-13
            else:
                self.position[0] = self.position[0]-14
        if self.animation_counter == 0 and self.way != "left":
            self.way = "left"
            frog_filename = './images/sprite_sheets_left.png'
            self.sprite = pygame.image.load(frog_filename).convert_alpha()
        self.incAnimationCounter()

    def moveRight(self):
        if self.position[0] < 401:
            if self.animation_counter == 2 :
                self.position[0] = self.position[0]+13
            else:
                self.position[0] = self.position[0]+14
        if self.animation_counter == 0 and self.way != "right":
            self.way = "right"
            frog_filename = './images/sprite_sheets_right.png'
            self.sprite = pygame.image.load(frog_filename).convert_alpha()
        self.incAnimationCounter()

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

    def setPositionToInitialPosition(self):
        self.position = self.initial_pos.copy()

    def draw(self, screen):
        current_sprite = self.animation_counter * 30
        screen.blit(self.sprite,(self.position),(0 + current_sprite, 0, 30, 30 + current_sprite))

    def rect(self): 
        return pygame.Rect(self.position[0],self.position[1],30,30)