import math

class Point():
    def __init__(self,p = [0,0]):
        self.p = p
    def __sub__(self,other):
        return Point((self.p[0]-other.p[0],self.p[1]-other.p[1]))
    def __abs__(self):
        return Point((abs(self.p[0]),abs(self.p[1])))
    def distance(self,other):
        x = math.pow(abs(self.p[0] - other.p[0]),2)
        y = math.pow(abs(self.p[1] - other.p[1]),2)
        return math.sqrt(x + y)
    
def clamp(min,max,val):
    if val < min:
        return min
    elif val > max:
        return max
    return val

# iterate through objects and return in range ones
def proxCheck(p,r,obj): # 2x frame boost!!! (60fps / 120fps on test)
    inRange = []
    for o in obj:
        match str(type(o)):
            case "<class 'objectV2.Rect'>":
                p1 = Point(p)
                p2 = Point()
                p2.p[0] = clamp(o.p1.p[0],o.p2.p[0],p1.p[0])
                p2.p[1] = clamp(o.p1.p[1],o.p2.p[1],p1.p[1])
                if p1.distance(p2) <= r:
                    inRange.append(o)
            case "<class 'objectV2.Circle'>":
                p1 = Point(p)
                p2 = Point(o.p)
                d = p1.distance(p2) - o.r
                if d <= r:
                    inRange.append(o)
            case _:
                inRange.append(o)
    return inRange

def endpointCalc(p,dir,max,o,pD):
    dir = math.radians(dir)
    pD = math.radians(pD)
    #return raycast(p,dir,l,o,pD)
    stepSize = 10
    x = p[0]
    y = p[1]
    obj = proxCheck(p,max,o)
    for i in range(0,max,stepSize):
        x += math.cos(dir) * stepSize
        y += math.sin(dir) * stepSize
        for o in obj:
            if collision(o,(x,y)):
                return [(x,y),i * math.cos(pD-dir)]
    x = p[0] + math.cos(dir) * max
    y = p[1] + math.sin(dir) * max
    return [(x,y),max]

def collision(obj,p):
    match str(type(obj)):
        case "<class 'objectV2.Rect'>":
            inX = p[0] > obj.p1.p[0] and p[0] < obj.p2.p[0]
            inY = p[1] > obj.p1.p[1] and p[1] < obj.p2.p[1]
            """
            inX = p[0] > obj[0][0] and p[0] < obj[1][0]
            inY = p[1] > obj[0][1] and p[1] < obj[1][1]
            """
            return inX and inY
        case "<class 'objectV2.Circle'>":
            r = math.sqrt(math.pow((p[0]-obj.p1.p[0]),2) + math.pow((p[1] - obj.p1.p[1]),2))
            #r = math.sqrt(math.pow((p[0]-obj[0][0]),2) + math.pow((p[1]-obj[0][1]),2))
            return r <= obj.r
        case _:
            print("collision not supported")

"""def raycast(p,dir,max,objects,pDir):
    stepSize = 10
    x = p[0]
    y = p[1]
    obj = proxCheck(p,max,objects)
    for i in range(0,max,10):
        x += math.cos(dir) * stepSize
        y += math.sin(dir) * stepSize
        for o in obj:
            if collision(o,(x,y)):
                return [(x,y),i * math.cos(pDir-dir)]
    x = p[0] + math.cos(dir) * max
    y = p[1] + math.sin(dir) * max
    return [(x,y),max]"""