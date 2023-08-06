import math
pi = math.pi
sqrt = math.sqrt
 
def cuboidVol(l,b,h):
    if(l,b,h>0):
        return l*b*h
    else:
        return 0
 
def cuboidSurf(l,b,h):
    if(l,b,h>0):
        return 2*(l*b + b*h + l*h)
    else:
        return 0

def cuboidLatSurf(l,b,h):
    if(l,b,h>0):
        return 2*h*(l+b)
    else:
        return 0
