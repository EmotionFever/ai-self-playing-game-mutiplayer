#! /usr/bin/env python
import pygame

class Object():
    def __init__(self,position,sprite):
        self.sprite = sprite
        self.position = position

    def draw(self, screen):
        screen.blit(self.sprite,(self.position))

    def rect(self):
        return pygame.Rect(self.position[0],self.position[1],self.sprite.get_width(),self.sprite.get_height())