import graphIO
import basicgraphs
import copy
import operator

colors=[]
nrOfGraphs = 0;
nrOfNodes = 0;

# Maakt de disjoint union van een lijst met graven
def createDisjointUnion(graphs):
	G=basicgraphs.graph()
	global nrOfGraphs
	nrOfGraphs = len(graphs)
	global nrOfNodes
	nrOfNodes = len(graphs[0].V())
	# print(nrOfGraphs, nrOfNodes)
	for i in range(len(graphs)):
	# for i in range(0, 1):
		# print("Graph ", i)
		index = len(G.V())
		for j in range(len(graphs[i].V())):
			G.addvertex(graphs[i].V()[j])		# Gooi de vertices van graaf i in de graaf
			G[j+index].newLabel(j+index)

		for j in range(len(graphs[i].V())):
			#print("Graph: ", i, "Vertex: ", j)
			nbs = graphs[i].V()[j].nbs()	# alle neighbours van vertex j in graaf i
			# print("NBS: ", j, nbs)
			for x in range(len(nbs)):
				# print(x)
				try: 														# maakt dezlefde egdes met tussen de vertex en zijn neighbours als in de originele graaf
					G.addedge(G[j+index], G[nbs[x]._label+index])
					# print("Edge from ", j, "to ", nbs[x]._label)	
					
				except basicgraphs.GraphError:
					pass
					#print("Egde is dubbel want logica* \n *previous statement not to be taken sarcastic")		# elke neigbour komt 2 keer voor dus hiermee worden de dubbele gevallen afgevangen
	#print(G)
	print("Disjoint created!")
	return G

def checkIsomorph(graph):				# return a list with at index 0 graphs with duplicate colors, grouped by the colors, and at the other indices grouped isomorphs					
	colors=[[] for i in range(nrOfGraphs)]		# creates a list of len nrOfGraphes filled with empty lists

	nodes = graph.V()					# fills the list with the colors, grouped per graph, graph 0 at index 0	
	for j in range(nrOfGraphs):
		for i in range(nrOfNodes):
			colors[j].append(nodes[(i+(j*nrOfNodes))].colornum)

	for i in range(len(colors)):		# sorts the lists with colors from low to high
		merge_sort(colors[i])
		# print(i, ":", colors[i])

	isomorphs = [[]]					# list for the (possible) isomorphs

	for i in range(len(colors)):						# loop through all lists with the colors of the graph
		if len(colors[i]) != len(set(colors[i])):		# Check for duplicates. A set can not contain duplicates
			added = False
			for j in range(len(isomorphs[0])):			# loop through all possible pairs of isomorphs, but colors contain duplicates
				# print(i, j, len(isomorphs[0][0]))
				if len(isomorphs[0][j]) != 0 and colors[i] == colors[isomorphs[0][j][0]]:		# If a graph is added and colors of the graph i are the same as the colors of the graph already added
					isomorphs[0][j].append(i)			# add the graph to the pair of possible isomorphs
					added = True
			if not added:								# add graph at new index if no matching colors are found
				isomorphs[0].append([i])
		else:											# no duplicates found
			added = False
			for j in range(1, len(isomorphs)):			# loop through all pairs of isomorphs
				if(colors[isomorphs[j][0]] == colors[i]):	# If colors of graph i are the same as the colors of the graph already added
					isomorphs[j].append(i)				# group the graph with his isomorphs
					added = True
			if not added:								# add graph at new index if no matching colors are found
				isomorphs.append([i])

	printIsomorphs(isomorphs)

	return isomorphs

# prints the graphs, grouped by isomorphs
def printIsomorphs(isomorphs):
	if len(isomorphs[0]) != 0:
		print("Unable to check: ", isomorphs[0])
	for i in range(1, len(isomorphs)):
		if len(isomorphs[i]) == 1:
			print("Not isomorph: ", isomorphs[i])
		else:
			print("Isomorph: ", isomorphs[i])





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
	print("Nodes colored")
	return colors


def getNeighborsColors(node):
	result=[]
	for i in range(len(node.nbs())):
		result.append(node.nbs()[i].colornum)

	merge_sort(result)
	# print("nbs", result) 
	return result

# Gaat verder kleuren toekennen aan de graven tot het niet meer mogelijk is.
def colorRefinement(graph, colors):
	rColors = copy.copy(colors)
	for i in range(len(rColors)):				# loop through all the colors
		nodes=copy.copy(rColors[i])				# create a copy of the nodes
		first = True

		while(len(nodes) != 0):					# while nodes have to be recolored
			if not first:						# if not the first run ----- in the first run the first node doesn't need a new color. After the first run, it does. First node has to be a unique color
				rColors[nodes[0].colornum].remove(nodes[0])			# remove first node
				nodes[0].colornum = len(rColors)					# give first node new color
				rColors.append([nodes[0]])							# add first node to new color index
			first = False
			colorednodes=[nodes[0]]									# node 0 is always recolored

			for q in range(1, len(nodes)): 									# loop through all the nodes that have to be recolored
				if getNeighborsColors(nodes[0]) == getNeighborsColors(nodes[q]):	# if colors of the neighbors of 0 and q are the same
					rColors[nodes[q].colornum].remove(nodes[q])				# remove node q from old color index
					nodes[q].colornum = nodes[0].colornum					# give node q same color as node 0
					rColors[nodes[0].colornum].append(nodes[q])				# add node q to new color index
					colorednodes.append(nodes[q])							# add node q to list with recolored nodes

			for i in range(len(colorednodes)):			# loop through all recolored nodes
				nodes.remove(colorednodes[i])			# remove recolored nodes from nodes that need to be recolored

			while [] in rColors:			# remove empty lists in the colorlist
				rColors.remove([])
			
	if(rColors != colors):					# while the colors have changed in this function, do colorRefinement again
		colorRefinement(graph, rColors)
	return rColors

# load the graphs into a list
def loadGraphs(file):
	L = graphIO.loadgraph(file, readlist=True)
	G=[0 for i in range(len(L[0]))]
	for i in range(len(G)):
		G[i] = L[0][i]
	return G

#sorts a list
def merge_sort(alist):
    if len(alist)>1:
        mid = len(alist)//2
        lefthalf = alist[:mid]
        righthalf = alist[mid:]

        merge_sort(lefthalf)
        merge_sort(righthalf)

        i=0
        j=0
        k=0
        while i<len(lefthalf) and j<len(righthalf):
            if lefthalf[i] < righthalf[j]:
                alist[k]=lefthalf[i]
                i=i+1
            else:
                alist[k]=righthalf[j]
                j=j+1
            k=k+1

        while i<len(lefthalf):
            alist[k]=lefthalf[i]
            i=i+1
            k=k+1

        while j<len(righthalf):
            alist[k]=righthalf[j]
            j=j+1
            k=k+1


## MAIN

G=loadGraphs('week2/trees11.grl')
#print("aantal graphs: ", len(G))-
H = createDisjointUnion(G)
nbs = H.V()[0].nbs()
#print(H[nbs[0]._label])
# graphIO.writeDOT(G[0], 'graph1.dot')
# graphIO.writeDOT(G[1], 'graph2.dot')
# graphIO.writeDOT(G[2], 'graph3.dot')
# graphIO.writeDOT(G[3], 'graph4.dot')
graphIO.writeDOT(H, 'graph.dot')
# for i in range(len(G)):
colors = setColorAsNrNeighbors(H)
# print("Colors: ", colors)
colors = colorRefinement(H, colors)
# print("rColors: ", colors)

checkIsomorph(H)

#print("Colors: \n",colors)
graphIO.writeDOT(H, 'graph_colors.dot')