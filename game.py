class Game():
    def __init__(self,speed,level):
        self.speed = speed
        self.level = level
        self.points = 0
        self.time = 0
        self.gameInit = 0
        self.gameStop=0
        self.totalPlans=0
        self.totalDeaths=0
        self.totalSteps=0

    def incLevel(self):
        self.level = self.level + 1

    def incSpeed(self):
        self.speed = self.speed + 1

    def incPoints(self,points):
        self.points = self.points + points

    def incTime(self):
        self.time = self.time + 1

    def resetTime(self):
        self.time = 30