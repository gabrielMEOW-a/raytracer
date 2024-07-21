import pygame
import player
import sys

clock = pygame.time.Clock()

# Variables
DISPLAY_HEIGHT = 640
DISPLAY_WIDTH = 800
WHITE = (255,255,255)
BLACK = (0,0,0)

p1 = player.player(0,0,WHITE,10)
p1MoveMap = [False,False,False,False]

pygame.display.init()
screen = pygame.display.set_mode((DISPLAY_WIDTH,DISPLAY_HEIGHT))

def get_keys():
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
            if event.key == pygame.K_UP:
                p1MoveMap[0] = True
            if event.key == pygame.K_DOWN:
                p1MoveMap[1] = True
            if event.key == pygame.K_LEFT:
                p1MoveMap[2] = True
            if event.key == pygame.K_RIGHT:
                p1MoveMap[3] = True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP:
                p1MoveMap[0] = False
            if event.key == pygame.K_DOWN:
                p1MoveMap[1] = False
            if event.key == pygame.K_LEFT:
                p1MoveMap[2] = False
            if event.key == pygame.K_RIGHT:
                p1MoveMap[3] = False

def move(moveMap):
    if moveMap[0]:
        p1.move([0,-1])
    if moveMap[1]:
        p1.move([0,1])
    if moveMap[2]:
        p1.move([-1,0])
    if moveMap[3]:
        p1.move([1,0])

while True:
    get_keys()
    move(p1MoveMap)
    screen.fill(BLACK)
    p1.draw(screen)
    pygame.display.update()
    clock.tick(60)