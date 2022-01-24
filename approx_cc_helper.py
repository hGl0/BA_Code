import random

# calculates cost of clustering, weighted with 1/0
# cost of 1 for each pair with (+), but in different clusters
# cost of 1 for each pair with (-), but in the same cluster
def cost(C, Ep, Em):
    cost = 0

    # if (+) related nodes are not in one cluster
    for pair in Ep:
        if get_cluster(C, pair[0]) != get_cluster(C, pair[1]):
            cost += 1
    # if (-) related nodes are in the same cluster
    for pair in Em:
        if get_cluster(C, pair[0]) == get_cluster(C, pair[1]):
            cost += 1
    return cost


# get cluster c of node n from clustering C
def get_cluster(C, n):
    for c in C:
        if n in c:
            return C.index(c)
    # n not in any cluster
    return -1


# assigns vertexes v in V randomly to Red or Blue
def color(V):
    random.shuffle(V)
    R = V[:len(V)//2]
    B = V[len(V)//2:]
    return R, B


# calculate balance between Red and Blue (optimal: 1)
def balance(R, B):
    # avoid division by 0
    if len(R) == 0 or len(B) == 0:
        return -1
    red = len(R)
    blue = len(B)
    balance = min(red/blue, blue/red)
    return balance


# generates naive fairlets
# step 1) a pair with (+) relation are fairlets, when its elements have two colors
# step 2) all remaining nodes are assigned randomly to a node with another color
def fairlets_naiv(R, B, Ep):
    fairlets = []

    # error case: balance != 1
    if len(R) != len(B):
        return -1
    # if pair in Ep has 2 colors, save as fairlet
    for pair in Ep:
        if pair[0] in R and pair[1] in B:
            fairlets.append(pair)
            B.remove(pair[1])
            R.remove(pair[0])
        if pair[1] in R and pair[0] in B:
            fairlets.append(pair)
            B.remove(pair[0])
            R.remove(pair[1])
    # assign randomly i in B to j in R, when only (-) or same colored (+) are left
    while len(B) > 0:
        i = random.choice(B)
        j = random.choice(R)
        fairlets.append((i,j))
        B.remove(i)
        R.remove(j)
    return fairlets