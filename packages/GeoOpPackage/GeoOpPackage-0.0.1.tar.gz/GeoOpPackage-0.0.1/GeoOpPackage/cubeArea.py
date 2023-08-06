import math
pi = math.pi
 
def cubeVol(s):
    if(s>0):
        return s*s*s
    else:
        return 0
 
def cubeSurf(s):
    if(s>0):
        return 6*s*s
    else:
        return 0