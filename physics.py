import math

def endpointCalc(p,dir,l,o,pD):
    dir = math.radians(dir)
    pD = math.radians(pD)
    return raycast(p,dir,l,o,pD)

def collision(obj,p):
    match obj[2]:
        case 0:
            inX = p[0] > obj[0][0] and p[0] < obj[1][0]
            inY = p[1] > obj[0][1] and p[1] < obj[1][1]
            return inX and inY
        case 1:
            r = math.sqrt(math.pow((p[0]-obj[0][0]),2) + math.pow((p[1]-obj[0][1]),2))
            return r < obj[1]
        case _:
            print("collision not supported")

def raycast(p,dir,l,objects,pDir):
    stepSize = 10
    x = p[0]
    y = p[1]
    for i in range(0,l,10):
        x += math.cos(dir) * stepSize
        y += math.sin(dir) * stepSize
        for obj in objects:
            if collision(obj,(x,y)):
                return [(x,y),i * math.cos(pDir-dir)]
    x = p[0] + math.cos(dir) * l
    y = p[1] + math.sin(dir) * l
    return [(x,y),l]