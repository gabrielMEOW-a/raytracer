import math
import pygame
import physics

class player:
    def __init__(self, x, y, color, size):
        self.pos = [x,y]
        self.color = color
        self.size = size
    def move(self, move):
        self.pos[0] += move[0]
        self.pos[1] += move[1]
    def draw(self, sur):
        pygame.draw.circle(sur, self.color, self.pos, self.size)