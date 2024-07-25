import math
import pygame
import physics

class player:
    def __init__(self, x, y, color, size,dir=0):
        self.pos = [x,y]
        self.color = color
        self.size = size
        self.dir = dir
    def move(self, move):
        self.pos[0] += move[0]
        self.pos[1] += move[1]
    def move2(self, move):
        self.pos[0] += math.cos(math.radians(self.dir)) * move
        self.pos[1] += math.sin(math.radians(self.dir)) * move
    def turn(self, turn):
        self.dir += turn
    def draw(self, sur):
        pygame.draw.circle(sur, self.color, self.pos, self.size)
    def collision(self, obj):
        return physics.collision(obj,self.pos)