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

WALL_HEIGHT = 100

CAMERA_WIDTH = DISPLAY_WIDTH * 0.8
MAX_CAST = 250
RAY_NUMS = 100
FOV = 120

moveTicker = 0
turnTicker = 0

p1 = player.player(0,0,WHITE,10)
p1MoveMap = [False,False,False,False,False,False]

objects = object.genObjects((DISPLAY_WIDTH,DISPLAY_HEIGHT),1)
print(objects)
camera = []

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
        match o[2]:
            case 0:
                pygame.draw.polygon(screen,WHITE,object.rect(o))
            case _:
                print('object type not supported')

def sendRays(p,num,fov,dir,dist):
    camera = []
    for i in range(num):
        line = physics.endpointCalc(p,dir-fov/2+i*(fov/num),dist,objects)
        end = line[0]
        camera.append(line[1])
        pygame.draw.line(screen,WHITE,p,end)
    return camera

def drawCamera(cam):
    x = DISPLAY_WIDTH/2 - CAMERA_WIDTH/2
    for c in cam:
        wall = WALL_HEIGHT * (1-(c/MAX_CAST))
        lineLen = DISPLAY_HEIGHT/2 - wall / 2
        pygame.draw.line(screen,WHITE,(x,lineLen),(x,lineLen + wall))
        x += CAMERA_WIDTH / len(cam)

while True:
    get_keys()
    move(p1MoveMap)
    screen.fill(BLACK)
    p1.draw(screen)
    draw(objects)
    camera = sendRays(p1.pos,RAY_NUMS,FOV,p1.dir,MAX_CAST)
    drawCamera(camera)
    pygame.display.update()
    clock.tick(120)