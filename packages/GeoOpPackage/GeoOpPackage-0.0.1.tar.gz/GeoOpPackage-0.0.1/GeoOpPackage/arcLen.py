import math

def arcLen(diameter, angle):
    if angle <= 360 and angle>0 and diameter>0:
        arc = (math.pi*diameter) * (angle/360.0)
        return arc
    else:
       return 0
         
# Driver Code
# diameter = 25.0
# angle = 75.0
# arc_len = arcLen(diameter, angle)
# print(arc_len)
