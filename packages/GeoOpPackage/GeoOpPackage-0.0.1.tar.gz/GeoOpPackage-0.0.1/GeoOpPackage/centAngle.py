import math

def centAngle(diameter, arcLen):
    if(diameter>0):
        centAngle = (arcLen*360.0)/ (math.pi*diameter) 
        return centAngle
    else:
        return 0
