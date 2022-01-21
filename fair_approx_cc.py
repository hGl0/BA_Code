# import of cc-pivot 3-approx
from rand_approx_cc import *

# To Do:
# 1) (1,1)-fairlets
# Darstellung von Gewichten in E bzw. Ep und Em
# Vorverarbeitung => Bildung Fairlets


V0 = list(range(1,5))

random.seed(42)
R, B = color_shuffle(V0)
print(R,B)


# 4 Cluster
Ep0_1 = [[1,2], [2,3]]
Em0_1 = [[1,3], [1,4], [2,4],[3,4]]
print(fairlets_naiv(R,B,Ep0_1))

Ep0_2 = [[1,2], [1,3], [2,4], [3,4]]
Em0_2 = [[1,4], [2,3]]

#print("Cluster (expected: 2): ", cc_pivot_wrap(V0, Ep0_2, Em0_2))
#print("Costs: ", cost)

#R, B = color_shuffle(list(range(1,21)))
#print("Red: ", R)
#print("Blue: ", B)
#print("Fairlets incomplete: ", fairlets_naiv(R, B, Ep0_2))


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