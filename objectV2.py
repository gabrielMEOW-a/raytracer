import random
from physics import Point

class Rect():
    def __init__(self,p1,p2):
        self.p1 = Point(p1)
        self.p2 = Point(p2)
    def draw(self):
        p1 = self.p1
        p2 = [self.p2.p[0],self.p1.p[1]]
        p3 = self.p2
        p4 = [self.p1.p[0],self.p2.p[1]]
        return [p1,p2,p3,p4]
    def size(self):
        return (self.p2.p[0] - self.p1.p[0],self.p2.p[1] - self.p1.p[1])

class Circle():
    def __init__(self, p, r):
        self.p = Point(p)
        self.r = r
    def size(self):
        return (self.r*2,self.r*2)

# returns pygame format for rectangles
def rect(obj):
    p1 = obj[0]
    p2 = [obj[1][0],obj[0][1]]
    p3 = obj[1]
    p4 = [obj[0][0],obj[1][1]]
    return [p1,p2,p3,p4]

# generate random objects
def genObjects(max,num):
    objects = []
    for i in range(num):
        match random.randint(0,1):
            case 0:
                start = (random.randint(0,max[0]),random.randint(0,max[1]))
                end = (random.randint(start[0],max[0]),random.randint(start[1],max[1]))
                objects.append(Rect(start,end))
            case 1:
                p = (random.randint(0,max[0]),random.randint(0,max[1]))
                radius = random.randint(10,25)
                objects.append(Circle(p,radius))
    return objects