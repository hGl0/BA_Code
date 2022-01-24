import random

# definiton
# V=Knotenmenge, Ep = Positive, Em = Negative
# ungerichteter Graph => [i,j] oder [j,i],

# implementation of cc pivot
def cc_pivot_wrap(V, Ep, Em):
    if len(V) == 0:
        print('No nodes to cluster')
        return
    cluster = CCPivot(V, Ep, Em)
    return optik(cluster)


# cc pivot algorithm
def CCPivot(V, Ep, Em):
    i = random.choice(V)
    C, Vn = [i], []
    for j in V:
        if j != i:
            if (i, j) in Ep or (j, i) in Ep:
                C.append(j)
            if (i, j) in Em or (j, i) in Em:
                Vn.append(j)

    # End condition, last cluster found
    if Vn == []:
        return C, []
    return C, CCPivot(Vn, Ep, Em)


# make up for more beautiful cluster representation
def optik(A):
    if A[1] == []:
        return [A[0]]
    else:
        return [A[0]] + optik(A[1])


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


# change representation of fair clustering C, so normal cost function can be applied
def change_rep(C):
    clustering = []
    for c in C:
        cluster = []
        for fairlet in c:
            cluster.append(fairlet[0])
            cluster.append(fairlet[1])
        clustering.append(cluster)
    return clustering


# define relation between fairlets by majority vote, if equal amount of relation assign them randomly
def fairlets_relations(fairlets, Ep, Em):
    E_fp = []
    E_fm = []
    for n in range(len(fairlets)):
        a = fairlets[n]
        for m in range(n+1, len(fairlets)):
            cnt_p = 0
            b = fairlets[m]

            i, j = a[0], a[1]
            k, l = b[0], b[1]

            if (i,k) in Ep or (k,i) in Ep:
                cnt_p += 1
            if (i,l) in Ep or (l,i) in Ep:
                cnt_p+=1
            if (j,k) in Ep or (k,j) in Ep:
                cnt_p+=1
            if (j,l) in Ep or (l,j) in Ep:
                cnt_p +=1

            if cnt_p > 2:
                E_fp.append((a,b))
                continue
            if cnt_p < 2:
                E_fm.append((a,b))
                continue
            if cnt_p == 2:
                if ((a in Ep or (a[1], a[0]) in Ep) or (b in Ep  or (b[1], b[0]) in Ep)) and random.choice([0,1]):
                    E_fp.append((a,b))
                    continue
                else: E_fm.append((a,b))
    return E_fp, E_fm


# assigns vertexes v in V randomly to Red or Blue
def color(V):
    random.shuffle(V)
    R = V[:len(V) // 2]
    B = V[len(V) // 2:]
    return R, B


# calculate balance between Red and Blue (optimal: 1)
def balance(R, B):
    # avoid division by 0
    if len(R) == 0 or len(B) == 0:
        return -1
    red = len(R)
    blue = len(B)
    balance = min(red / blue, blue / red)
    return balance


# generates naive fairlets
# step 1) a pair with (+) relation are fairlets, when its elements have two colors
# step 2) all remaining nodes are assigned randomly to a node with another color
def fairlets_naive(R, B, Ep):
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
        fairlets.append((i, j))
        B.remove(i)
        R.remove(j)
    return fairlets
