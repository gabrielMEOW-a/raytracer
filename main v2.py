import pygame
import playerV2
import sys
import physicsV2
import objectV2
import maze

clock = pygame.time.Clock()

# Variables
DISPLAY_HEIGHT = 640
DISPLAY_WIDTH = 800
WHITE = (255,255,255,127)
BLACK = (0,0,0)

WALL_HEIGHT = 500

CAMERA_WIDTH = DISPLAY_WIDTH * 0.8
MAX_CAST = 250
RAY_NUMS = 100
FOV = 120

moveTicker = 0
turnTicker = 0

p1 = playerV2.player(60,60,WHITE,10)
p1MoveMap = [False,False,False,False,False,False,False,False]
p1prevmove = [0,0]

objects = [] 
print(objects)
wallI = 0
wallTransparency = [0,64,128,192,255]

camera = []

pygame.display.init()
screen = pygame.display.set_mode((DISPLAY_WIDTH,DISPLAY_HEIGHT),pygame.DOUBLEBUF)

# generate map using prim's algorithm
def gen_map():
    m = maze.mazing()
    for i in range(len(m)):
        for j in range(len(m[i])):
            if m[i][j] == "w":
                objects.append(objectV2.Rect([i*40,j*40],[i*40+40,j*40+40]))
    print("done mazing")

# get keys and modify moveMap
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

# check for player collisions
def playerCollision():
    for o in objects:
        if p1.collision(o):
            return True
    return False

# move according to moveMap
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

# transparent objects
def drawTransparent(obj):
    # make new surface and blit onto screen
    s = pygame.Surface(obj.size())
    s.set_alpha(wallTransparency[wallI])
    match str(type(obj)):
        case "<class 'objectV2.Rect'>":
            s.fill(WHITE)
            screen.blit(s,obj.p1)
        case "<class 'objectV2.Circle'>":
            pygame.draw.circle(s,WHITE,obj.p,obj.r)
            screen.blit(s,(obj.p[0]-obj.r,obj.p[1]-obj.r))

# object drawing
def draw(obj):
    for o in obj:
        drawTransparent(o)

        """match o[2]:
            case 0:
                drawTransparent(o)
                #pygame.draw.polygon(screen,WHITE,object.rect(o)) DEPRECATED
            case 1:
                pygame.draw.circle(screen,WHITE,o.p,o.r)
            case _:
                print('object type not supported')"""

# send rays
def sendRays(p,num,fov,dir,dist, pDir):
    camera = []
    for i in range(num):
        line = physicsV2.endpointCalc(p,dir-fov/2+i*(fov/num),dist,objects,pDir)
        end = line[0]
        camera.append(line[1])
        pygame.draw.line(screen,WHITE,p,end)
    return camera

# render rays
def drawCamera(cam):
    x = DISPLAY_WIDTH/2 - CAMERA_WIDTH/2
    for c in cam:
        color = (1-(c/MAX_CAST)) * 255
        wall = WALL_HEIGHT * (1-(c/MAX_CAST))
        lineLen = DISPLAY_HEIGHT/2 - wall / 2
        pygame.draw.line(screen,(color,color,color),(x,lineLen),(x,lineLen + wall))
        x += CAMERA_WIDTH / len(cam)

def drawText():
    pass

#gen_map()

# test objects
objects = [[(307, 324), (771, 452), 0], [(265, 403), 20, 1], 
           [(94, 418), (787, 442), 0], [(489, 273), (526, 491), 0], 
           [(358, 149), (619, 419), 0], [(439, 445), (599, 631), 0], 
           [(84, 535), 12, 1], [(42, 296), 18, 1], 
           [(456, 206), 10, 1], [(607, 0), 17, 1]]

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