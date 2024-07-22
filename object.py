import random

def rect(obj):
    p1 = obj[0]
    p2 = [obj[1][0],obj[0][1]]
    p3 = obj[1]
    p4 = [obj[0][0],obj[1][1]]
    return [p1,p2,p3,p4]

def genObjects(max,num):
    objects = []
    for i in range(num):
        match random.randint(0,1):
            case 0:
                start = (random.randint(0,max[0]),random.randint(0,max[1]))
                end = (random.randint(start[0],max[0]),random.randint(start[1],max[1]))
                objects.append([start,end,0])
            case 1:
                p = (random.randint(0,max[0]),random.randint(0,max[1]))
                radius = random.randint(10,25)
                objects.append([p,radius,1])
    return objects