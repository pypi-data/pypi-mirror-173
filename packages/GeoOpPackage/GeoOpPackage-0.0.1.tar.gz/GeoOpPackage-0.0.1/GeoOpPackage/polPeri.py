#Perimeter of regular polygon

def Perimeter(s, n):
    perimeter = 1
    perimeter = n * s
    if(s,n>0):
        return perimeter
    else:
        return 0

# print(Perimeter(2,4))