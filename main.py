import pygame
import player
import sys
import physics
import object
import maze

clock = pygame.time.Clock()

# Variables
DISPLAY_HEIGHT = 640
DISPLAY_WIDTH = 800
WHITE = (255,255,255,127)
BLACK = (0,0,0)

WALL_HEIGHT = 100

CAMERA_WIDTH = DISPLAY_WIDTH * 0.8
MAX_CAST = 250
RAY_NUMS = 50
FOV = 120

moveTicker = 0
turnTicker = 0

p1 = player.player(60,60,WHITE,10)
p1MoveMap = [False,False,False,False,False,False,False,False]
p1prevmove = [0,0]

objects = [] # object.genObjects((DISPLAY_WIDTH,DISPLAY_HEIGHT),3)
print(objects)
wallI = 0
wallTransparency = [0,64,128,192,255]

camera = []

pygame.display.init()
screen = pygame.display.set_mode((DISPLAY_WIDTH,DISPLAY_HEIGHT),pygame.DOUBLEBUF)

def gen_map():
    m = maze.mazing()
    for i in range(len(m)):
        for j in range(len(m[i])):
            if m[i][j] == "w":
                objects.append([[i*40,j*40],[i*40+40,j*40+40],0])
    print("done mazing")

def get_keys():
    global wallI
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
            if event.key == pygame.K_w:
                p1MoveMap[6] = True
            if event.key == pygame.K_s:
                p1MoveMap[7] = True
            if event.key == pygame.K_SPACE:
                wallI += 1
                wallI = wallI % len(wallTransparency)
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
            if event.key == pygame.K_w:
                p1MoveMap[6] = False
            if event.key == pygame.K_s:
                p1MoveMap[7] = False

def playerCollision():
    for o in objects:
        if p1.collision(o):
            return True
    return False

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
        if moveMap[6]:
            p1.move2(1)
            moveTicker += 1
        if moveMap[7]:
            p1.move2(-1)
            moveTicker += 1
    elif moveTicker > 0:
        moveTicker -= 1
    if turnTicker < 10:
        if moveMap[4]:
            p1.turn(-1)
            turnTicker += 1
        if moveMap[5]:
            p1.turn(1)
            turnTicker += 1
    elif turnTicker > 0:
        turnTicker -= 1

def drawTransparent(obj):
    match obj[2]:
        case 0:
            s = pygame.Surface((obj[1][0] - obj[0][0],obj[1][1] - obj[0][1]))
            s.set_alpha(wallTransparency[wallI])
            s.fill(WHITE)
            screen.blit(s,obj[0])
        case 1:
            s = pygame.Surface((obj[0][0]-obj[1],obj[0][1]-obj[1]),(obj[0][0]+obj[1],obj[0][1]+obj[1]))
            s.set_alpha(wallTransparency[wallI])
            pygame.draw.circle(s,WHITE,obj[0],obj[1])
            screen.blit(s,(obj[0][0]-obj[1],obj[0][1]-obj[1]))

def draw(obj):
    for o in obj:
        match o[2]:
            case 0:
                drawTransparent(o)
                #pygame.draw.polygon(screen,WHITE,object.rect(o))
            case 1:
                pygame.draw.circle(screen,WHITE,o[0],o[1])
            case _:
                print('object type not supported')

def sendRays(p,num,fov,dir,dist, pDir):
    camera = []
    for i in range(num):
        line = physics.endpointCalc(p,dir-fov/2+i*(fov/num),dist,objects,pDir)
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

gen_map()

while True:
    get_keys()
    if not playerCollision():
        move(p1MoveMap)
    screen.fill(BLACK)
    p1.draw(screen)
    draw(objects)
    camera = sendRays(p1.pos,RAY_NUMS,FOV,p1.dir,MAX_CAST,p1.dir)
    drawCamera(camera)
    pygame.display.update()
    clock.tick(120)