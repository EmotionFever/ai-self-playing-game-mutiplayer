from object import Object

class Platform(Object):
    def __init__(self,position,sprite_plataform,way):
        self.sprite = sprite_plataform
        self.position = position
        self.way = way

    def move(self,speed):
        if self.way == "right":
            self.position[0] = self.position[0] + speed
        elif self.way == "left":
            self.position[0] = self.position[0] - speed