import basicgraphs 
import graphIO

L=graphIO.loadgraph('crefBM_4_7.grl',readlist=True)
L1= L[0][0]
V1 = L1.V()
print(L[0][0])
print(L1.E())
for i in range(len(V1)):
	print(V1[i].deg())