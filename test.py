import operator
import copy
map = [['00','01','02','03'],['10','11','12','13'],['20','21','22','23'],['30','31','32','33']]
print(len(map),len(map[0]))
for i in map:
    print(i)


l = [[0,0,4],[0,0,4]]
l2 = [1,2,3]
l3 = copy.deepcopy(l)
l[0][0] = 4
l[0][2] = 0
l[1][0] = 4
l[1][2] = 0
print(l)
print(l3)
print(operator.eq(l,l3))