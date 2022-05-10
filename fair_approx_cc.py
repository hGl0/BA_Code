from fair_cc_functions import *
#from graph_generation import *
import networkx as nx

# set random seed for debugging
random.seed(42)

# Ep and Em for testing and debugging, two fairlet
R = [2,4,6]
B = [1,3,5]
Ep0_1 = [(1, 5, 1), (3, 5, 1),
         (2, 4, 1), (2, 6, 1), (4, 6, 1)]
Em0_1 = [(1, 2, 0), (1, 4, 0), (1, 6, 0),
         (3, 2, 0), (3, 4, 0), (3, 6, 0),
         (5, 2, 0), (5, 4, 0), (5, 6, 0),
         (1, 3, 0)]
# Ep0_2 = [[1,2], [1,3], [2,4], [3,4]]
# Em0_2 = [[1,4], [2,3]]



# generate graph
G = nx.Graph()
G.add_nodes_from(R, color='red')
G.add_nodes_from(B, color='blue')
G.add_weighted_edges_from(Ep0_1)
G.add_weighted_edges_from(Em0_1)

# draw graph with colors
fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(12, 6))
draw_graph(G, ax1)
G_cluster = cc_pivot(G)
print("Unfair clustering: ", G_cluster)

# create fairlets and their relations
fairlets = create_fairlets(G)
print('Fairlets: ', fairlets)
Ef_p, Ef_m = create_fairlet_relations(fairlets, G)

# create graph from fairlets
G_fair = nx.Graph()
G_fair.add_nodes_from(fairlets)
G_fair.add_weighted_edges_from(Ef_p)
G_fair.add_weighted_edges_from(Ef_m)
cluster_fair = cc_pivot(G_fair)
print('Fair clustering: ', cluster_fair)
costs_fair = cost(cluster_fair, G)
#costs_unfair = cost(G_cluster, G)
print("Costs fair:", costs_fair)
#print("Costs unfair:", costs_unfair)

draw_graph(G_fair, ax=ax2, node_size=1000)

fig, ax = plt.subplots(1)
test_graph = generate_complete_graph(8)
draw_graph(test_graph, ax)
plt.show()

#test_G = generate_uniform_cluster_graph(10, 3, 2)[0]
#nx.draw(test_G, with_labels=True)
#plt.show()
#unfair_cluster_test_G = cc_pivot(test_G)
#print(unfair_cluster_test_G)
#res = {u:w for u, w in nx.get_edge_attributes(G, 'weight') if w > 0}
#print(res)

# More complex example
#V1 = list(range(1, 13))
# V_color,R1,B1 = color(V1)
#Ep1 = [(1, 2), (1, 3), (1, 12), (1, 11), (3, 12), (2, 3), (2, 12), (2, 11), (3, 11), (11, 12), (4, 5), (4, 6), (5, 6),
#       (7, 10), (7, 8), (7, 9),
#       (8, 9), (8, 10), (9, 10), (7, 12), (2, 4)]
#Em1 = [(1, 4), (1, 5), (1, 6), (1, 7), (1, 8), (1, 9), (1, 10), (2, 5), (2, 6), (2, 7), (2, 8), (2, 9), (2, 10), (3, 5),
#       (3, 6), (3, 7), (3, 8), (3, 9), (3, 10), (4, 7), (4, 8), (4, 9), (4, 11), (4, 12), (5, 7), (5, 8), (5, 9),
#       (5, 10), (5, 11), (5, 12), (6, 8), (6, 9), (6, 10), (6, 11), (6, 12), (7, 11), (8, 11), (8, 12), (9, 11), (9, 12),
#       (10, 12), (10, 11), (3, 4), (6, 7), (10, 4)]

#Red, Blue = color(V1)
#äprint("Red: ", Red)
#print('Blue: ', Blue)

#fairlets = fairlets_naive(Red, Blue, Ep1)
#print('Fairlets: ', fairlets)
#E_fp_1, E_fm_1 = fairlets_relations(fairlets, Ep1, Em1)
#print('Positive fairlet relations: \n', E_fp_1)
#print('Negative fairlet relations:\n', E_fm_1)

#fair_cluster = cc_pivot_wrap(fairlets, E_fp_1, E_fm_1)
#cost_fair = cost(fair_cluster, E_fp_1, E_fm_1)
#cost_fair_nodes = cost(change_rep(fair_cluster), Ep1, Em1)

#print('Fair cluster: ', fair_cluster)
#print('Cost of fair clustering (regarding relations of fairlets): ', cost_fair)
#print('Cost of fair clustering (regarding relations of nodes): ', cost_fair_nodes)