import random

# calculates cost of clustering, weighted with 1/0
# cost of 1 for each pair with (+), but in different clusters
# cost of 1 for each pair with (-), but in the same cluster
def cost(C, Ep, Em):
    # ij in Ep, but i in C_k and j in C_l, k !=l
    for i in C:
        pass


# assigns vertexes v in V randomly to Red or Blue
def color(V):
    random.shuffle(V)
    R = V[:len(V)//2]
    B = V[len(V)//2:]
    return R, B


# calculate balance between Red and Blue (optimal: 1)
def balance(R, B):
    red = len(R)
    blue = len(B)
    balance = min(red/blue, blue/red)
    return balance


# generates naive fairlets
# step 1) a pair with (+) relation are fairlets, when its elements have two colors
# step 2) all remaining nodes are assigned randomly to a node with another color
def fairlets_naiv(R, B, Ep):
    fairlets = []

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
        fairlets.append([i,j])
        B.remove(i)
        R.remove(j)
    return fairlets