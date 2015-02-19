import graphIO
import basicgraphs

colors=[]

def createDisjointUnion(graphs):
	G=basicgraphs.graph()
	for i in range(len(graphs)):
		index = len(G.V())
		for j in range(len(graphs[i].V())):
			G.addvertex(graphs[i].V()[j])
		for j in range(len(graphs[i].V())):
			print("Graph: ", i, "Vertex: ", j)
			for x in range(len(graphs[i].V()[j].nbs())):
				nbs = graphs[i].V()[j].nbs()
				print("NBS: ", nbs)
				try: 
					G.addedge(G.V()[j+index], G.V()[int(str(nbs[x]))+index])
					break
				except basicgraphs.GraphError:
					print("Egde is dubbel want logica* \n *previous statement not to be taken sarcastic")
					# G.addedge(G.V()[int(str(nbs[x]))], G.V()[j])
			# print("tail: ", graphs[i].E()[j].tail(), "head: ", graphs[i].E()[j].head())
			# print(e.tail())
			# G.addedge(e.tail(),e.head())
	
	print(G)
	return G


def setColorAsNrNeighbors(graph):
	colors=[[]]
	graph[0].colornum=0
	colors[0].append(graph[0])
	for i in range(1, len(graph.V())):
		added = False
		for x in range(len(colors)):
			if colors[x][0].deg() == graph[i].deg():
				colors[x].append(graph[i])
				added = True
				break
		if not added:
			graph[i].colornum=len(colors)
			colors.append([graph[i]])

		# graph[i].colornum = graph[i].deg()
		# colors[graph[i].deg()].append(i)
	return colors

def loadGraphs(file):
	L = graphIO.loadgraph(file, readlist=True)
	G=[0 for i in range(len(L[0]))]
	for i in range(len(G)):
		G[i] = L[0][i]
	return G

## MAIN

G=loadGraphs('week1/crefBM_4_7.grl')
print("aantal graphs: ", len(G))
H = createDisjointUnion(G)
# graphIO.writeDOT(G[0], 'graph1.dot')
# graphIO.writeDOT(G[1], 'graph2.dot')
# graphIO.writeDOT(G[2], 'graph3.dot')
# graphIO.writeDOT(G[3], 'graph4.dot')
graphIO.writeDOT(H, 'graph.dot')
# for i in range(len(G)):
# 	colors = setColorAsNrNeighbors(G[i])
# 	print(colors)

################
################
################


"""
colors=[[] for j in range(len(G))]

for i in range(len(G)):
	G[i] = L[0][i]
# for i in range(len(G)):
# 	if len(G[0].V()) != len(G[i].V()) or len(G[0].E()) != len(G[i].E()):
# 		G.pop(i)
		
# print(len(G))
for x in range(len(G)):
	for i in range(len(G[x].V())):
		G[x][i].colornum=G[x][i].deg()
		if G[x][i].deg() not in colors[x]:
			colors[x]
			colors[x].append(G[x][i].deg())
			print(colors[x])
			colors[x][colors[x].index(G[x][i].deg())] = []
			print(colors[x])
			colors[x][colors[x].index(G[x][i].deg())].append(i)
		# print(G[x][i].colornum)
sortedcolors=[0 for i in range(len(G))]

print(colors)

"""
# for x in range(len(G)):
# 	sortedcolors[x]=[]
# 	for i in range(len(G[x].V())):
# 		sortedcolors[x].append(G[x][i].colornum)

# for i in range(len(sortedcolors)):
# 	# sortedcolors[i].sort()
# 	print(sortedcolors[i])

# for i in range(len(G)):
# 	for x in range(len(G[i].V())):
		
# 		G[i][x]

# graphIO.writeDOT(G, 'graph.dot')