import math
pi = math.pi
sqrt = math.sqrt
 
def coneVol(r, h):
    if(r,h>0):
        return (1 / 3) * pi * r * r * h
    else:
        return 0
 
def coneSurf(r, s):
    if(r,s>0):
        return pi * r * s + pi * r * r
    else:
        return 0
    

def coneLatSurf(r,h):
    if(r,h>0):
        return pi * r * sqrt((h*h)+(r*r))
    else:
        return 0

   