from random import random, randrange, randint, shuffle
import networkx as nx

# we represent graphs with the networkx graph library
# we represent clusterings as a list of pairs. Each pair contains a list of the nodes belonging to the cluster and an integer denoting the cluster color.
# n: number of nodes, p: modification probability of each edge, f: number of colors, k: number of clusters in ground truth

# generates a graph where each edge occurs with probability p i.i.d.
def generate_gilbert_graph(n, p, f=1):
    graph = nx.Graph()
    graph.add_nodes_from(range(n))
    for i in graph.nodes():
        for j in graph.nodes():
            if i < j and random() < p:
                graph.add_edge(i, j, color = randrange(f))
    return graph

# creates a perfect cluster graph with k clusters
def generate_uniform_cluster_graph(n, k, f=1):
    graph = nx.Graph()
    graph.add_nodes_from(range(n))
    
    shuf = [*range(n)]
    shuffle(shuf)
    cluster = [0 for i in range(k)]
    clustered = 0
    clustering = [([],0) for i in range(k)]
    for i in range(n):
        x = randrange(k)
        cluster[x]+=1
    for i in range(k):
        c = cluster[i]
        cf = randrange(f)
        clustering[i] = (clustering[i][0], cf)
        for x in range(clustered,clustered+c):
            clustering[i][0].append(shuf[x])
            for y in range(x+1,clustered+c):
                graph.add_edge(shuf[x], shuf[y], color = cf)
        clustered += c
    return graph, clustering
    
# creates a perfect cluster graph and then adds random noise on top of it
def generate_mutated_uniform_cluster_graph(n, k, p, f=1):
    graph1, clustering = generate_uniform_cluster_graph(n=n, k=k, f=f)
    graph2 = generate_gilbert_graph(n=n, p=p, f=f)
    for i, j in graph2.edges():
        if not i < j: continue
        if graph1.has_edge(i,j) and graph1[i][j]['color'] == graph2[i][j]['color']:
            graph1.remove_edge(i,j)
        else:
            graph1.add_edge(i,j, color=graph2[i][j]['color'])
    return graph1, clustering

print(generate_mutated_uniform_cluster_graph(10, 3, 3))
print(generate_uniform_cluster_graph(10,3))