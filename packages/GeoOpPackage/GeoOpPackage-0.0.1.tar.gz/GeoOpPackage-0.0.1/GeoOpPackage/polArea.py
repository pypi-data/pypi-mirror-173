def polArea(XArr, YArr, NumberofTerms):
        j = NumberofTerms - 1
        area=0.0
        if(XArr,YArr, NumberofTerms>0):
            for i in range(0,NumberofTerms):
                area += (XArr[j] + XArr[i]) * (YArr[j] - YArr[i])
                j = i   # j is previous vertex to i
                return int(abs(area / 2.0))
        else:
            return 0
 
# Driver program to test above function
# X = [0, 2, 4]
# Y = [1, 3, 7]
# n = len(X)
# print(polArea(X, Y, n))