import math
pi = math.pi
sqrt = math.sqrt
 
def cylVol(r, h):
    if(r,h>0 ):
        return pi * r * r * h
    else:
        return 0

def cylSurf(r, h):
    if(r,h>0):
        return 2*pi*r*(h + r)
    else:
        return 0

def cylLatSurf(r,h):
    if(r,h>0):
        return 2 * pi * r * h
    else:
        return 0

#print(cylVol(9,5))