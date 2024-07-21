import math

def vector_merge(v1,v2):
    vr = [(v1[0]+v2[0])/2,(v1[1]+v2[1])/2]
    return vr

def endpointCalc(p,dir,l,o):
    dir = math.radians(dir)
    return raycast(p,dir,l,o)

def collision(obj,p):
    inX = p[0] > obj[0][0] and p[0] < obj[1][0]
    inY = p[1] > obj[0][1] and p[1] < obj[1][1]
    return inX and inY

def raycast(p,dir,l,objects):
    x = p[0]
    y = p[1]
    for i in range(l):
        x += math.cos(dir)
        y += math.sin(dir)
        for obj in objects:
            if collision(obj,(x,y)):
                return (x,y)
    x = p[0] + math.cos(dir) * l
    y = p[1] + math.sin(dir) * l
    return (x,y)