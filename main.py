import pygame
import player
import sys
import physics
import object

clock = pygame.time.Clock()

# Variables
DISPLAY_HEIGHT = 640
DISPLAY_WIDTH = 800
WHITE = (255,255,255)
BLACK = (0,0,0)

moveTicker = 0
turnTicker = 0

p1 = player.player(0,0,WHITE,10)
p1MoveMap = [False,False,False,False,False,False]

objects = [[[100,100],[110,110]]]

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
            if event.key == pygame.K_a:
                p1MoveMap[4] = True
            if event.key == pygame.K_d:
                p1MoveMap[5] = True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP:
                p1MoveMap[0] = False
            if event.key == pygame.K_DOWN:
                p1MoveMap[1] = False
            if event.key == pygame.K_LEFT:
                p1MoveMap[2] = False
            if event.key == pygame.K_RIGHT:
                p1MoveMap[3] = False
            if event.key == pygame.K_a:
                p1MoveMap[4] = False
            if event.key == pygame.K_d:
                p1MoveMap[5] = False

def move(moveMap):
    global moveTicker
    global turnTicker
    if moveTicker < 10:
        if moveMap[0]:
            p1.move([0,-1])
            moveTicker += 1
        if moveMap[1]:
            p1.move([0,1])
            moveTicker += 1
        if moveMap[2]:
            p1.move([-1,0])
            moveTicker += 1
        if moveMap[3]:
           p1.move([1,0])
           moveTicker += 1
    else:
        moveTicker -= 1
    if turnTicker < 1:
        if moveMap[4]:
            p1.turn(-10)
            turnTicker += 1
        if moveMap[5]:
            p1.turn(10)
            turnTicker += 1
    elif turnTicker > 0:
        turnTicker -= 1

def draw(obj):
    for o in obj:
        pygame.draw.polygon(screen,WHITE,object.rect(o))

def sendRays(p,num,fov,dir):
    for i in range(num):
        end = physics.endpointCalc(p,dir-fov/2+i*(fov/num),100,objects)
        pygame.draw.line(screen,WHITE,p,end)

while True:
    get_keys()
    move(p1MoveMap)
    screen.fill(BLACK)
    p1.draw(screen)
    draw(objects)
    sendRays(p1.pos,100,120,p1.dir)
    pygame.display.update()
    clock.tick(120)