import math
pi = math.pi
 
def sphVol(r):
    if(r>0):
        return (1.3333)*pi * r * r * r 
    else:
        return 0
 
def sphSurf(r):
    if(r>0):
        return 4*pi*r*r
    else:
        return 0