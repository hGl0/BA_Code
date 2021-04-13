import random
import numpy as np


# definiton
# V=Knotenmenge, Ep = Positive, Em = Negative
# ungerichteter Graph => [i,j] oder [j,i],

def CCPivot(V, Ep, Em):
    i = random.choice(V)
    C, Vn = [i], []
    for j in V:
        if j != i:
            if [i, j] in Ep or [j, i] in Ep:
                C.append(j)
            if [i, j] in Em or [j, i] in Em:
                Vn.append(j)

# End condition, last cluster found
    if Vn == []:
        return C, []
    return C, CCPivot(Vn, Ep, Em)

# Test
# G=(E,V) mit
V= list(range(1,13))

Ep = [[1,2],[1,3],[1,12],[1,11],[3,12],[2,3],[2,12],[2,11],[3,11],[11,12],[4,5],[4,6],[5,6],[7,10],[7,8],[7,9],
      [8,9],[8,10],[9,10]]
Em = [[1,4],[1,5],[1,6],[1,7],[1,8],[1,9],[1,10],[2,4],[2,5],[2,6],[2,7],[2,8],[2,9],[2,10],[3,5],[3,6],[3,7],
      [3,8],[3,9],[3,10],[4,7],[4,8],[4,9],[4,11],[4,12],[5,7],[5,8],[5,9],[5,10],[5,11],[5,12],[6,8],[6,9],[6,10],
      [6,11],[6,12],[7,11],[7,12],[8,11],[8,12],[9,11],[9,12],[10,12],[10,11],[3,4],[6,7],[10,4]]

# Kosmetik
def optik(A):
    if A[1] == []:
        return [A[0]]
    else:
        return [A[0]] + optik(A[1])

test = CCPivot(V,Ep,Em)
print(test)
print(optik(test))


#print(test[0])



