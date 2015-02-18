import graphIO
import basicgraphs

L = graphIO.loadgraph('week1/crefBM_4_7.grl', readlist=True)
G=[0 for i in range(len(L[0]))]

for i in range(len(G)):
	G[i] = L[0][i]

for i in range(len(G)):
	if len(G[0].V()) != len(G[i].V()) or len(G[0].E()) != len(G[i].E()):
		G.pop(i)
		
print(len(G))
for x in range(len(G)):
	G[x] = L[0][x]
	print("Graph ", x)
	for i in range(len(G[x].V())):
		G[x][i].colornum=G[x][i].deg()
		print(G[x][i].colornum)