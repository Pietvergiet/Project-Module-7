import graphIO
import basicgraphs

colors=[]

# Maakt de disjoint union van een lijst met graven
def createDisjointUnion(graphs):
	G=basicgraphs.graph()
	for i in range(len(graphs)):
		index = len(G.V())
		for j in range(len(graphs[i].V())):
			G.addvertex(graphs[i].V()[j])		# Gooi de vertices van graaf i in de graaf
			G[j+index].newLabel(j+index)
		for j in range(len(graphs[i].V())):
			#print("Graph: ", i, "Vertex: ", j)
			for x in range(len(graphs[i].V()[j].nbs())):
				nbs = graphs[i].V()[j].nbs()	# alle neighbours van vertex j in graaf i
				#print("NBS: ", nbs)
				try: 														# maakt dezlefde egdes met tussen de vertex en zijn neighbours als in de originele graaf
					G.addedge(G[j+index], G[nbs[x]._label+index])	
					break
				except basicgraphs.GraphError:
					pass
					#print("Egde is dubbel want logica* \n *previous statement not to be taken sarcastic")		# elke neigbour komt 2 keer voor dus hiermee worden de dubbele gevallen afgevangen
	#print(G)
	return G

# Geeft elke vertex in de graaf een kleur die correspondeert aan zijn degree
def setColorAsNrNeighbors(graph):
	colors=[[]]
	graph[0].colornum=0
	colors[0].append(graph[0])
	for i in range(1, len(graph.V())):
		added = False
		for x in range(len(colors)):
			if colors[x][0].deg() == graph[i].deg():
				graph[i].colornum=x
				colors[x].append(graph[i])
				added = True
				break
		if not added:
			graph[i].colornum=len(colors)
			colors.append([graph[i]])

		# graph[i].colornum = graph[i].deg()
		# colors[graph[i].deg()].append(i)
	return colors

# Gaat verder kleuren toekennen aan de graven tot het niet meer mogelijk is.
def colorRefinement(graph, colors):
	rColors = colors
	for i in range(len(rColors)):
		nbss = len(rColors[i][0].nbs())
		print("amount of nbs:", nbss)
		for q in range(len(rColors[i])):
			x = 1
			for j in range(x, 0, -1):
				same = False
				for k in range(nbss):
					for l in range(nbss):
						if rColors[i][j].nbs()[k].colornum == rColors[i][j].nbs()[l] or same:
							same = True
					if not same :
						rColors[i][j].colornum=len(rColors)
						colors.append(rColors[i][j])
						break
			x+=1			


	return rColors

def loadGraphs(file):
	L = graphIO.loadgraph(file, readlist=True)
	G=[0 for i in range(len(L[0]))]
	for i in range(len(G)):
		G[i] = L[0][i]
	return G

## MAIN

G=loadGraphs('week1/crefBM_4_7.grl')
#print("aantal graphs: ", len(G))
H = createDisjointUnion(G)
nbs = H.V()[0].nbs()
#print(H[nbs[0]._label])
# graphIO.writeDOT(G[0], 'graph1.dot')
# graphIO.writeDOT(G[1], 'graph2.dot')
# graphIO.writeDOT(G[2], 'graph3.dot')
# graphIO.writeDOT(G[3], 'graph4.dot')
# graphIO.writeDOT(H, 'graph.dot')
# for i in range(len(G)):
colors = setColorAsNrNeighbors(H)
print("Colors: ", colors)
colors = colorRefinement(H, colors)
print("rColors: ", colors)
#print("Colors: \n",colors)
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