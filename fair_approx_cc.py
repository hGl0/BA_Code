import random
import numpy as np

# To Do:
# 1) (1,1)-fairlets
# Darstellung von Gewichten in E bzw. Ep und Em
# Vorverarbeitung => Bildung Fairlets


#-------------------------------------
# definiton
# V=Knotenmenge, Ep = Positive, Em = Negative
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

#calculates cost of clustering, weighted with 1/0
def cost(C, Ep, Em):
    # ij in Ep, but i in C_k and j in C_l, k !=l
    for i in C:
        pass


# assignment of color red = 1, blue = 0
# returns set V_colored, R and B
# 1 = rot
# 0 = blau (grün)
def color(V):
    R, B = [], []
    for k in range(len(V)):
        i = random.choice(range(0,2))
        if i == 1:
            R.append(V[k])
        else:
            B.append(V[k])
    if len(B) == len(R):
        return R, B
    return color(V)

def balance(R, B):
    red = len(R)
    blue = len(B)
    balance = min(red/blue, blue/red)
    return balance

# for unweighted graphs
# idea for weighted graphs: pick min w_lj
def fairlets_naiv(R, B, Ep):
    fairlets = []
    # no match in Ep => random choice
    R_dot = R
    B_dot = B
    for k in B:
        for i in R:
            if [i,k] in Ep or [k,i] in Ep:
                fairlets.append([k,i])
                R_dot.remove(i)
                B_dot.remove(k)
    for l in B:
        j = random.choice(R)
        fairlets.append([l,j])
        B.remove(l)
        R.remove(j)
    return fairlets

# Kosmetik
def optik(A):
    if A[1] == []:
        return [A[0]]
    else:
        return [A[0]] + optik(A[1])


V0 = list(range(1,5))
# 4 Cluster
Ep0_1 = []
Em0_1 = [[1,2], [1,3], [2,3], [1,4], [2,4],[3,4]]


Ep0_2 = [[1,2], [1,3], [2,4], [3,4]]
Em0_2 = [[1,4], [2,3]]

print("Cluster (expected: 2): ", optik(CCPivot(V0, Ep0_2, Em0_2)))
#print("Costs: ", cost)

R, B = color(list(range))
print("Red: ", R)
print("Blue: ", B)
print("Fairlets incomplete: ", fairlets_naiv(R, B, Ep0_2, Em0_2))


'''
# More komplex example
V1 = list(range(1,13))
#V_color,R1,B1 = color(V1)
Ep1 = [[1,2],[1,3],[1,12],[1,11],[3,12],[2,3],[2,12],[2,11],[3,11],[11,12],[4,5],[4,6],[5,6],[7,10],[7,8],[7,9],
      [8,9],[8,10],[9,10]]
Em1 = [[1,4],[1,5],[1,6],[1,7],[1,8],[1,9],[1,10],[2,4],[2,5],[2,6],[2,7],[2,8],[2,9],[2,10],[3,5],[3,6],[3,7],
      [3,8],[3,9],[3,10],[4,7],[4,8],[4,9],[4,11],[4,12],[5,7],[5,8],[5,9],[5,10],[5,11],[5,12],[6,8],[6,9],[6,10],
      [6,11],[6,12],[7,11],[7,12],[8,11],[8,12],[9,11],[9,12],[10,12],[10,11],[3,4],[6,7],[10,4]]

test = CCPivot(V1,Ep1,Em1)

#print("Red: ", R1)
#print("Blue: ", B1)
print("V: ", V1)
print("Cluster: ", optik(test))


#print(test[0])
'''