def SqPyrSA(BaseLen, SlantHeight):
    if(BaseLen,SlantHeight>0):
        return(2*BaseLen*SlantHeight + BaseLen*BaseLen)
    else:
        return 0
    

def TriPyrSA(BaseHeight, BaseLength, SideHeight):
    if(BaseHeight, BaseLength, SideHeight>0):
        return 0.5*BaseHeight*BaseLength + 1.5*BaseLength*SideHeight
    else: 
        return 0

def PentPyrSA(BaseHeight, BaseLength, SideHeight):
    if(BaseHeight, BaseLength, SideHeight>0):
        return 2.5*BaseHeight*BaseLength + 2.5*BaseLength*SideHeight
    else: 
        return 0

def HexPyrSA(BaseHeight, BaseLength, SideHeight):
    if(BaseHeight, BaseLength, SideHeight>0):
        return 3*BaseHeight*BaseLength + 3*BaseLength*SideHeight
    else: 
        return 0

