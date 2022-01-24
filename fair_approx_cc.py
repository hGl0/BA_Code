from fair_cc_functions import *

# To Do:
# 1) (1,1)-fairlets
# Darstellung von Gewichten in E bzw. Ep und Em
# Vorverarbeitung => Bildung Fairlets
#V0 = list(range(1, 5))
#R, B = color(V0)
#print('Red: ', R)
#print('Blue: ', B)

# Ep and Em for testing and debugging
Ep0_1 = [(1, 2), (2, 3), (1,3)]
Em0_1 = [(1, 4), (2, 4), (3, 4)]
#fairlets = fairlets_naive(R, B, Ep0_1)
#print('Fairlets: ', fairlets)

#E_fp_01, E_fm_01 = fairlets_relations(fairlets, Ep0_1, Em0_1)
#print('Positive vertex relations: \n', Ep0_1)
#print('Negative vertex relations: \n', Em0_1)
#print("Positive fairlet relations: \n", E_fp_01)
#print('Negative fairlet relations: \n', E_fm_01)

# Ep0_2 = [[1,2], [1,3], [2,4], [3,4]]
# Em0_2 = [[1,4], [2,3]]

# More complex example
V1 = list(range(1, 13))
# V_color,R1,B1 = color(V1)
Ep1 = [(1, 2), (1, 3), (1, 12), (1, 11), (3, 12), (2, 3), (2, 12), (2, 11), (3, 11), (11, 12), (4, 5), (4, 6), (5, 6),
       (7, 10), (7, 8), (7, 9),
       (8, 9), (8, 10), (9, 10), (7, 12), (2, 4)]
Em1 = [(1, 4), (1, 5), (1, 6), (1, 7), (1, 8), (1, 9), (1, 10), (2, 5), (2, 6), (2, 7), (2, 8), (2, 9), (2, 10), (3, 5),
       (3, 6), (3, 7), (3, 8), (3, 9), (3, 10), (4, 7), (4, 8), (4, 9), (4, 11), (4, 12), (5, 7), (5, 8), (5, 9),
       (5, 10), (5, 11), (5, 12), (6, 8), (6, 9), (6, 10), (6, 11), (6, 12), (7, 11), (8, 11), (8, 12), (9, 11), (9, 12),
       (10, 12), (10, 11), (3, 4), (6, 7), (10, 4)]

Red, Blue = color(V1)
print("Red: ", Red)
print('Blue: ', Blue)

fairlets = fairlets_naive(Red, Blue, Ep1)
print('Fairlets: ', fairlets)
E_fp_1, E_fm_1 = fairlets_relations(fairlets, Ep1, Em1)
print('Positive fairlet relations: \n', E_fp_1)
print('Negative fairlet relations:\n', E_fm_1)

fair_cluster = cc_pivot_wrap(fairlets, E_fp_1, E_fm_1)
cost_fair = cost(fair_cluster, E_fp_1, E_fm_1)
cost_fair_nodes = cost(change_rep(fair_cluster), Ep1, Em1)

print('Fair cluster: ', fair_cluster)
print('Cost of fair clustering (regarding relations of fairlets): ', cost_fair)
print('Cost of fair clustering (regarding relations of nodes): ', cost_fair_nodes)