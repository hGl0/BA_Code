import random
import networkx as nx
import matplotlib.pyplot as plt

# definiton
# V=Knotenmenge, Ep = Positive, Em = Negative
# ungerichteter Graph => [i,j] oder [j,i],

# draws graph with color mapping of nodes and edges
# all edges in E+ are black, all edges in E- are red
# node color decides by color attribute of node
def draw_graph(G, ax, node_size=300):
    # colors for edges in G
    e_colors = ['red', 'green', 'white']
    edge_color_map = [e_colors[edge] for edge in nx.get_edge_attributes(G, 'weight').values()]
    # map colors of nodes to drawing
    for node in G.nodes:
        if G.nodes[node].get('color'):
            # if nodes are colored
            node_color_map = nx.get_node_attributes(G, 'color').values()
            nx.draw(G,
                    node_size=node_size,
                    node_color=node_color_map,
                    edge_color=edge_color_map,
                    with_labels=True,
                    ax=ax)
        else:
            # if color of nodes is not important
            nx.draw(G,
                    node_size=node_size,
                    edge_color=edge_color_map,
                    with_labels=True,
                    ax=ax)
        break


    # map colors of edges to drawing, accessing colors by index


# implementation and wrapping of cc pivot
def cc_pivot(G):
    V = list(G.nodes())
    Ep = [e for e in G.edges() if nx.get_edge_attributes(G, 'weight')[e]==1]
    Em = [e for e in G.edges() if nx.get_edge_attributes(G, 'weight')[e]==0]
    if len(V) == 0:
        print('No nodes to cluster')
        return
    cluster = _CCPivot_fct(V, Ep, Em)
    return _optik(cluster)


# cc pivot algorithm
def _CCPivot_fct(V, Ep, Em):
    i = random.choice(V)
    C, Vn = [i], []
    #if type(i) == tuple: C.extend(i)
    #else: C.append(i)
    for j in V:
        if j != i:
            if (i, j) in Ep or (j, i) in Ep:
                if type(j) == tuple: C.extend([j[0],j[1]])
                else: C.append(j)
            if (i, j) in Em or (j, i) in Em:
                Vn.append(j)

    # End condition, last cluster found
    if Vn == []:
        return C, []
    return C, _CCPivot_fct(Vn, Ep, Em)


# make up for more beautiful cluster representation
def _optik(A):
    if A[1] == []:
        return [A[0]]
    else:
        return [A[0]] + _optik(A[1])


# calculates cost of clustering, weighted with 1/0
# cost of 1 for each pair with (+), but in different clusters
# cost of 1 for each pair with (-), but in the same cluster
# need to change representation of clustering if nodes are still tuples from fairlets
def cost(C, G):
    Ep = [e for e in G.edges() if nx.get_edge_attributes(G, 'weight')[e] == 1]
    Em = [e for e in G.edges() if nx.get_edge_attributes(G, 'weight')[e] == 0]
    cost = 0
    if type(C[0][0]) == tuple: C = _change_rep(C)

    # if (+) related nodes are not in one cluster
    for pair in Ep:
        if _get_cluster(C, pair[0]) != _get_cluster(C, pair[1]):
            cost += 1
    # if (-) related nodes are in the same cluster
    for pair in Em:
        if _get_cluster(C, pair[0]) == _get_cluster(C, pair[1]):
            cost += 1
    return cost


# get cluster c of node n from clustering C
def _get_cluster(C, n):
    for c in C:
        if n in c:
            return C.index(c)
    # n not in any cluster
    return -1


# change representation of fair clustering C, so normal cost function can be applied
def _change_rep(C):
    clustering = []
    for c in C:
        cluster = []
        for fairlet in c:
            cluster.append(fairlet[0])
            cluster.append(fairlet[1])
        clustering.append(cluster)
    return clustering


# define relation between fairlets by majority vote, if equal amount of relation assign negative relation
# applies for scenario 1 with (-) relations between red and blue nodes
def create_fairlet_relations(fairlets, G):
    E_fp = []
    E_fm = []
    Ep = [e for e in G.edges() if nx.get_edge_attributes(G, 'weight')[e] == 1]
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
                E_fp.append((a,b, 1))
                continue
            if cnt_p <= 2:
                E_fm.append((a,b, 0))
                continue
            #if cnt_p == 2:
            #    if ((a in Ep or (a[1], a[0]) in Ep) or (b in Ep  or (b[1], b[0]) in Ep)) and random.choice([0,1]):
            #        E_fp.append((a,b))
            #        continue
            #    else: E_fm.append((a,b))
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
def create_fairlets(G):
    fairlets = []
    R = [n for n in G.nodes() if nx.get_node_attributes(G, 'color')[n]=='red']
    B = [n for n in G.nodes() if nx.get_node_attributes(G, 'color')[n]=='blue']
    Ep = [e for e in G.edges() if nx.get_edge_attributes(G, 'weight')[e]==1]

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


# creates complete graph with n nodes, which are red or blue
# only (-) relations between different colors, other relation assigned randomly
def generate_complete_graph(n):
    graph = nx.complete_graph(n)
    reds = random.sample(list(graph.nodes()), k=n // 2)
    colored = {}
    blues = [n for n in graph.nodes() if n not in reds]
    for r, b in zip(reds, blues):
        colored[r] = 'red'
        colored[b] = 'blue'
    nx.set_node_attributes(graph, colored, 'color')
    weights = {}
    for e in graph.edges():
        if graph.nodes()[e[0]]['color'] == 'blue' and graph.nodes()[e[1]]['color'] == 'red':
            weights[e] = 0
        elif graph.nodes()[e[1]]['color'] == 'blue' and graph.nodes()[e[0]]['color'] == 'red':
            weights[e] = 0
        else:
            weights[e] = random.choice([0, 1])
    nx.set_edge_attributes(graph, weights, 'weight')
    return graph


# assign weight for "don't care" relation between fairlets based on local neighbourhood
def handle_even(fairlet):
    pass