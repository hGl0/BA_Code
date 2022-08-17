import random
import networkx as nx

# draws graph with color mapping of nodes and edges
# all edges in E+ are black, all edges in E- are red
# node color decides by color attribute of node
import numpy as np


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
    Ep = [e for e in G.edges() if nx.get_edge_attributes(G, 'weight')[e] == 1]
    Em = [e for e in G.edges() if nx.get_edge_attributes(G, 'weight')[e] == 0]
    if len(V) == 0:
        print('No nodes to cluster')
        return
    cluster = _CCPivot_fct(V, Ep, Em)
    return _optik(cluster)


# cc pivot algorithm
def _CCPivot_fct(V, Ep, Em):
    i = random.choice(V)
    C, Vn = [i], []
    # if type(i) == tuple: C.extend(i)
    # else: C.append(i)
    for j in V:
        if j != i:
            if (i, j) in Ep or (j, i) in Ep:
                if type(j) == tuple:
                    C.append((j[0], j[1]))
                else:
                    C.append(j)
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
        for m in range(n + 1, len(fairlets)):
            cnt_p = 0
            b = fairlets[m]

            i, j = a[0], a[1]
            k, l = b[0], b[1]

            if (i, k) in Ep or (k, i) in Ep:
                cnt_p += 1
            if (i, l) in Ep or (l, i) in Ep:
                cnt_p += 1
            if (j, k) in Ep or (k, j) in Ep:
                cnt_p += 1
            if (j, l) in Ep or (l, j) in Ep:
                cnt_p += 1

            if cnt_p > 2:
                E_fp.append((a, b, 1))
                continue
            if cnt_p <= 2:
                E_fm.append((a, b, 0))
                continue
    return E_fp, E_fm


# assigns vertexes v in V randomly to Red or Blue
def color(V):
    random.shuffle(V)
    R = V[:len(V) // 2]
    B = V[len(V) // 2:]
    return R, B


def get_color(G,v):
    return G.nodes[v]['color']

# calculate balance of clustering of G
def balance(C, G):
    all_balances = []
    for c in C:
        red = 0
        blue = 0
        for v in c:
            if get_color(G,v) == 'red': red += 1
            if get_color(G,v) == 'blue': blue+=1
        all_balances.append(min(red/blue, blue/red))
    # avoid division by 0
    if red == 0 or blue == 0:
        return 0
    balance = min(all_balances)
    return balance


# generates naive fairlets
# step 1) a pair with (+) relation are fairlets, when its elements have two colors
# step 2) all remaining nodes are assigned randomly to a node with another color
def create_fairlets(G):
    fairlets = []
    R = [n for n in G.nodes() if nx.get_node_attributes(G, 'color')[n] == 'red']
    B = [n for n in G.nodes() if nx.get_node_attributes(G, 'color')[n] == 'blue']
    Ep = [e for e in G.edges() if nx.get_edge_attributes(G, 'weight')[e] == 1]

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
        # always blue first, red second
        fairlets.append((i, j))
        B.remove(i)
        R.remove(j)
    return fairlets


# creates complete graph with n nodes, which are red or blue
# only (-) relations between different colors, other relation assigned randomly
# basic graph
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


def generate_red_blue_graph(n, red, blue, p1=0.75, p2=0.75):
    if n % 2 or n < 2: return -1
    graph_type = {
        # sparse graphs
        'star': nx.star_graph,  # n+1 nodes
        'bal_bin_tree': nx.full_rary_tree,  # n nodes, extra check for r
        'circle': nx.cycle_graph,  # n nodes
        # dense graphs
        'clique': nx.complete_graph,  # n nodes
        'bipartite': nx.complete_bipartite_graph,  # n nodes, extra check for n1, n2
        'is': nx.empty_graph,
        '3partite': nx.complete_multipartite_graph,
        'erdos_renyi' : nx.erdos_renyi_graph,
    }

    # check for extra parameters, attention to amount of nodes
    if red == 'star':
        red_g = graph_type[red](n // 2 - 1)
    elif red == 'bal_bin_tree':
        red_g = graph_type[red](2, n // 2)
    elif red == 'bipartite':
        m = random.randrange(2, n // 2 - 2)
        red_g = graph_type[red](m, n // 2 - m)
    elif red == '3partite':
        i = random.randrange(1, n // 6 + 1)
        j = random.randrange(1, i + 1)
        k = n // 2 - i - j
        red_g = graph_type[red](i, j, k)
    elif red == 'erdos_renyi':
        red_g = graph_type[red](n//2, p1)
    else:
        red_g = graph_type[red](n // 2)

    if blue == 'star':
        blue_g = graph_type[blue](n // 2 - 1)
    elif blue == 'bal_bin_tree':
        blue_g = graph_type[blue](2, n // 2)
    elif blue == 'bipartite':
        m = random.randrange(2, n // 2 - 2)
        blue_g = graph_type[blue](m, n // 2 - m)
    elif blue == '3partite':
        i = random.randrange(1, n // 6+1)
        j = random.randrange(1, i+1)
        k =n // 2 - i - j
        blue_g = graph_type[blue](i, j, k)
    elif blue == 'erdos_renyi':
        blue_g = graph_type[blue](n//2, p2)
    else:
        blue_g = graph_type[blue](n // 2)

    # rename nodes of red_g to be disjunct to blue_g
    red_g = nx.relabel_nodes(red_g, lambda x: x + n // 2)
    # assign colors
    red_g.add_nodes_from(red_g.nodes, color='red')
    blue_g.add_nodes_from(blue_g.nodes, color='blue')

    # generate graph composed of blue_g and red_g
    graph = nx.compose(blue_g, red_g)
    graph.add_edges_from(graph.edges, weight=1)

    comp_graph = nx.complement(graph)
    graph.add_edges_from(comp_graph.edges, weight=0)

    for e in graph.edges():
        if graph.nodes()[e[0]]['color'] == 'blue' and graph.nodes()[e[1]]['color'] == 'red':
            graph.remove_edge(*e)
        elif graph.nodes()[e[1]]['color'] == 'blue' and graph.nodes()[e[0]]['color'] == 'red':
            graph.remove_edge(*e)
    return graph, red_g, blue_g


# generates incomplete graph with equal amount of red and blue nodes and
# 1) no relations between red and blue nodes
# 2) mandatory (-) or (+) relations between same colored nodes (randomly chosen)
# basic graph, red and blue subgraphs have approximately same density/structure
def generate_incomplete_graph(n):
    graph = nx.complete_graph(n)
    reds = random.sample(list(graph.nodes), k=n // 2)
    colored = {}
    blues = [n for n in graph.nodes() if n not in reds]
    for r, b in zip(reds, blues):
        colored[r] = 'red'
        colored[b] = 'blue'
    nx.set_node_attributes(graph, colored, 'color')
    # generate edges
    weights = {}
    for e in graph.edges():
        if graph.nodes()[e[0]]['color'] == 'blue' and graph.nodes()[e[1]]['color'] == 'red':
            weights[e] = -1
        elif graph.nodes()[e[1]]['color'] == 'blue' and graph.nodes()[e[0]]['color'] == 'red':
            weights[e] = -1
        else:
            weights[e] = random.choice([0, 1])
    nx.set_edge_attributes(graph, weights, 'weight')
    graph.remove_edges_from([e for e in graph.edges() if nx.get_edge_attributes(graph, 'weight')[e] == -1])
    return graph


# assign weight for "don't care" relation between fairlets based on local neighbourhood
def _handle_even(e, G):
    neighbour_common = nx.common_neighbors(G, e[0], e[1])
    cnt_bt_p, cnt_bt_m = 0, 0
    for n in neighbour_common:
        if G.edges()[(e[0], n)]['weight'] == 1 and G.edges()[(e[1], n)]['weight'] == 0: cnt_bt_p += 1
        if G.edges()[(e[0], n)]['weight'] == 0 and G.edges()[(e[1], n)]['weight'] == 1: cnt_bt_p += 1
        if G.edges()[(e[0], n)]['weight'] == 1 and G.edges()[(e[1], n)]['weight'] == 1: cnt_bt_m += 1
    if cnt_bt_p < cnt_bt_m:
        # print('handle even assigned 1 for: ', e)
        # print('with c+ =', cnt_bt_p, 'and c- = ', cnt_bt_m)
        return 1
    elif cnt_bt_m < cnt_bt_p:
        # print('handle even assigned 0 for: ',e)
        # print('with c+ =', cnt_bt_p, 'and c- = ', cnt_bt_m)
        return 0
    else:
        # print('handle even assigned randomly for: ', e)
        # print('with c+ =', cnt_bt_p, 'and c- = ', cnt_bt_m)
        return random.choice([0, 1])


def create_fairlet_relations_incomplete(fairlets, G):
    Ef_p = []
    Ef_m = []
    Ef_n = []
    for idx_f1 in range(len(fairlets)):
        fi = fairlets[idx_f1]
        for idx_f2 in range(idx_f1):
            fj = fairlets[idx_f2]
            if fi == fj: continue
            # fi[0], fj[0] = relation between blue nodes
            # fi[1], fj[1] = relation between red nodes
            if G.edges()[(fi[0], fj[0])]['weight'] == 1 and G.edges()[(fi[1], fj[1])]['weight'] == 1:
                Ef_p.append((fi, fj, 1))
            elif G.edges()[(fi[0], fj[0])]['weight'] == 0 and G.edges()[(fi[1], fj[1])]['weight'] == 0:
                Ef_m.append((fi, fj, 0))
            else:
                Ef_n.append((fi, fj))
    fair_graph = nx.Graph()
    fair_graph.add_nodes_from(fairlets)
    fair_graph.add_weighted_edges_from(Ef_p)
    fair_graph.add_weighted_edges_from(Ef_m)
    for (u, v) in Ef_n:
        if _handle_even((u, v), fair_graph):
            Ef_p.append((u, v, 1))
        else:
            Ef_m.append((u, v, 0))
        fair_graph.add_weighted_edges_from(Ef_p)
        fair_graph.add_weighted_edges_from(Ef_m)
    return Ef_p, Ef_m
