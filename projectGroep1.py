import graphIO
import basicgraphs
import copy
import operator
import math

# Maakt de disjoint union van een lijst met graven
def createDisjointUnion(graphs):
	G=basicgraphs.graph()
	for i in range(len(graphs)):
		index = len(G.V())

		for j in range(len(graphs[i].V())):
			G.addvertex(graphs[i].V()[j])		# Gooi de vertices van graaf i in de graaf
			G[j+index].newLabel(j+index)

		for j in range(len(graphs[i].V())):
			nbs = graphs[i].V()[j].nbs()	# alle neighbours van vertex j in graaf i

			for x in range(len(nbs)):
				try: 														# maakt dezlefde egdes met tussen de vertex en zijn neighbours als in de originele graaf
					G.addedge(G[j+index], G[nbs[x]._label+index])	
				except basicgraphs.GraphError:
					pass
	return G

# returns a list with the colors of the nodes of the graph, grouped by the graph and sorted. Graph 0 at index 0
def getColors(nodes):
	colors=[[] for i in range(nrOfGraphs)]
	for i in range(len(colors)):
		colors[i] = nodes[i*nrOfNodes:(i+1)*nrOfNodes]
		merge_sort(colors[i])
	return colors

# return a list with at index 0 graphs with duplicate colors, grouped by the colors, and at the other indices grouped isomorphs
def checkIsomorph(nodes):									
	colors= getColors(nodes)

	isomorphs = [[]]					# list for the (possible) isomorphs
	for i in range(len(colors)):						# loop through all lists with the colors of the graph
		if len(colors[i]) != len(set(colors[i])):		# Check for duplicates. A set can not contain duplicates
				isomorphs[0].append(i)
		else:											# no duplicates found
			added = False
			for j in range(1, len(isomorphs)):			# loop through all pairs of isomorphs
				if(colors[isomorphs[j][0]] == colors[i]):	# If colors of graph i are the same as the colors of the graph already added
					isomorphs[j].append(i)				# group the graph with his isomorphs
					added = True
			if not added:								# add graph at new index if no matching colors are found
				isomorphs.append([i])
	return isomorphs

def isIsomorph(graph1, graph2, nodes):
	isomorphs = checkIsomorph(nodes)
	for i in range(1, len(isomorphs)):
		if graph1 in isomorphs[i] and graph2 in isomorphs[i]:
			return True
	return False

# prints the graphs, grouped by isomorphs
def printIsomorphs(isomorphs):
	if len(isomorphs[0]) != 0:
		print("Unable to check: ", isomorphs[0])
	for i in range(1, len(isomorphs)):
		if len(isomorphs[i]) == 1:
			print("Not isomorph: ", isomorphs[i])
		else:
			print("Isomorph: ", isomorphs[i])

# Geeft elke vertex in de graaf een kleur die correspondeert aan zijn degree #DONE
def setColorAsNrNeighbors(graphs):
	colors=[]
	global nrOfGraphs
	nrOfGraphs = len(graphs)
	global nrOfNodes
	nrOfNodes = len(graphs[0].V())

	colorPerDegree = []

	nodes = [0 for i in range(nrOfNodes*nrOfGraphs)]

	for g in range(len(graphs)):
		for n in range(len(graphs[g].V())):
			if graphs[g][n].deg() in colorPerDegree:
				color = colorPerDegree.index(graphs[g][n].deg())
				nodes[(g*nrOfNodes)+n] = color
				colors[color].append((g*nrOfNodes)+n)
			else:
				nodes[(g*nrOfNodes)+n] = len(colors)
				colorPerDegree.append(graphs[g][n].deg())
				colors.append([(g*nrOfNodes)+n])
	return colors, nodes

def getNeighborsColors(node, nodes):
	result=[]
	
	g = node//nrOfNodes
	n = node%len(UsedGraphs[g].V())
	try:
		nbs = UsedGraphs[g][n].nbs()
	except IndexError:
		print(g, n)
	for i in range(len(nbs)):
		result.append(nodes[nbs[i]._label+(g*nrOfNodes)])
	merge_sort(result)

	return result

# Gaat verder kleuren toekennen aan de graven tot het niet meer mogelijk is.
def colorRefinement(colors, nodes, graph1, graph2):
	if len(colors) == 1:
		return colors, nodes
	cNodes = copy.deepcopy(nodes)						# copy of the nodes
	cColors = copy.deepcopy(colors)

	allowedNodes = []									# fill allowed nodes
	if graph1 == -1 or graph2 == -1:
		for i in range(nrOfNodes*nrOfGraphs):
			allowedNodes.append(i)
	else:
		for i in range(nrOfNodes):
			allowedNodes.append(i+(nrOfNodes*graph1))
			allowedNodes.append(i+(nrOfNodes*graph2))
	i = 0
	colorsDone = set(cNodes)
	while i < len(allowedNodes) and len(colorsDone) != 0:
		if cNodes[allowedNodes[i]] in colorsDone:
			colorsDone.remove(cNodes[allowedNodes[i]])
			j = 0
			nrOfColors = copy.deepcopy(len(cColors))
			
			neighbourColors = {}
			while j < len(cColors[cNodes[allowedNodes[i]]]):
				node = cColors[cNodes[allowedNodes[i]]][j]

				allowedNodesNbs = getNeighborsColors(allowedNodes[i], nodes)
				neighbourColors[node] = getNeighborsColors(node, nodes)

				if neighbourColors[node] != allowedNodesNbs:				
					q = nrOfColors
					nbsFound = False
					while q < len(cColors) and not nbsFound:
						if neighbourColors[node] == neighbourColors[cColors[q][0]]:
							cColors[cNodes[node]].remove(node)
							cNodes[node] = q
							cColors[q].append(node)
							nbsFound = True
						q += 1
					if not nbsFound:
						cColors[cNodes[node]].remove(node)
						cNodes[node] = len(cColors)
						cColors.append([node])
				else:
					j += 1
		i += 1
	if cColors != colors:
		cColors, cNodes = colorRefinement(cColors, cNodes, graph1, graph2)
	return cColors, cNodes	

def findGraphsWithDup(colors, nodes):
	graphsWithDup = {}
	i = 0
	while i < nrOfGraphs and graphsWithDup == {}:
		colorlist = getColors(nodes)
		if len(colorlist[i]) != len(set(colorlist[i])) :					# check for a dub
			j = 0
			dupColor = -1
			while dupColor == -1 and j < len(colorlist[i]) -1:			# finding dup color
				if colorlist[i][j] == colorlist[i][j+1]:
					dupColor = colorlist[i][j]
				j += 1
			
			for x in range(len(colors[dupColor])):
				g = (int(colors[dupColor][x])//nrOfNodes)
				graphsWithDup[g] = []
			for x in range(len(colors[dupColor])):
				g = (int(colors[dupColor][x])//nrOfNodes)
				graphsWithDup[g].append(colors[dupColor][x])
		i += 1
	return graphsWithDup

def findGraphsWithDup_2(colors, nodes, graph1, graph2):
	graphsWithDup = {}
	i = 0

	colorlist = getColors(nodes)
	if len(colorlist[graph1]) != len(set(colorlist[graph1])) :					# check for a dub
		j = 0
		dupColor = -1
		while dupColor == -1 and j < len(colorlist[graph1]) -1:			# finding dup color
			if colorlist[graph1][j] == colorlist[graph1][j+1]:
				dupColor = colorlist[graph1][j]
			j += 1

		graphsWithDup[graph1] = []
		graphsWithDup[graph2] = []
		for x in range(len(colors[dupColor])):
			g = (int(colors[dupColor][x])//nrOfNodes)
			if g == graph1 or g == graph2:
				graphsWithDup[g].append(colors[dupColor][x])

	return graphsWithDup

def individualRef(colors, nodes, graph1, graph2):
	rColors = copy.deepcopy(colors)
	rNodes = copy.deepcopy(nodes)
	graphsWithDup = findGraphsWithDup_2(rColors, rNodes, graph1, graph2)
	if graph1 in graphsWithDup and graph2 in graphsWithDup:
		g = graph2
		j = 0
		while j < len(graphsWithDup[g]):
			copyColors = copy.deepcopy(rColors)
			copyNodes = copy.deepcopy(rNodes)
			
			g0 = graph1							# RECOLOR FIRST NODE OF FIRST GRAPH
			node = graphsWithDup[g0][0]
			rColors[rNodes[node]].remove(node)
			rNodes[node] = len(rColors)
			rColors.append([node])
			node = graphsWithDup[g][j]
			rColors[rNodes[node]].remove(node)
			rNodes[node] = len(rColors)-1
			rColors[rNodes[node]].append(node)
			rColors, rNodes = colorRefinement(rColors, rNodes, g0, g)
			allColors = getColors(rNodes)
			if(allColors[g0] == allColors[g]):
				if len(allColors[g0]) == len(set(allColors[g0])):
					return rColors, rNodes, True
				else:
					rColors, rNodes, found = individualRef(rColors, rNodes, graph1, graph2)
					if found:
						return rColors, rNodes, found
					else:
						rColors = copy.deepcopy(copyColors)
						rNodes = copy.deepcopy(copyNodes)
			else:
				rColors = copy.deepcopy(copyColors)
				rNodes = copy.deepcopy(copyNodes)
			j += 1
	return rColors, rNodes, False	

def autCounter(colors, nodes, t):
	count = t
	rColors = copy.deepcopy(colors)
	rNodes = copy.deepcopy(nodes)
	graphsWithDup = findGraphsWithDup(rColors, rNodes)
	i = 1
	while i < len(graphsWithDup.keys()):
		g = list(graphsWithDup.keys())[i]
		j = 0
		while j < len(graphsWithDup[g]):
			copyColors = copy.deepcopy(rColors)
			copyNodes = copy.deepcopy(rNodes)
			
			g0 = list(graphsWithDup.keys())[0]				# RECOLOR FIRST NODE OF FIRST GRAPH
			node = graphsWithDup[g0][0]
			rColors[rNodes[node]].remove(node)
			rNodes[node] = len(rColors)
			rColors.append([node])
			node = graphsWithDup[g][j]
			rColors[rNodes[node]].remove(node)
			rNodes[node] = len(rColors)-1
			rColors[rNodes[node]].append(node)
			rColors, rNodes = colorRefinement(rColors, rNodes, g0, g)
			allColors = getColors(rNodes)
			if(allColors[g0] == allColors[g]):
				if len(checkIsomorph(rNodes)[0]) == 0:
					count += 1
					if count <= 100:
						if count%10 == 0:
							print(count)
					elif count > 100:
						if count%100 ==0:
							print(count)
				else:
					rColors, rNodes, count = gensetGen(rColors, rNodes, count)
				rColors = copy.deepcopy(copyColors)
				rNodes = copy.deepcopy(copyNodes)
			else:
				rColors = copy.deepcopy(copyColors)
				rNodes = copy.deepcopy(copyNodes)
			j += 1
		i += 1
	return rColors, rNodes, count

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

def giveColor(graph, nodes):
	cGraph = copy.deepcopy(graph)
	for i in range(len(nodes)):
		cGraph[i].colornum = nodes[i]

	return cGraph

def createDOT(nodes):
	disjointGraph = createDisjointUnion(UsedGraphs)
	filename = input("Enter filename for .dot file: ")
	Q = giveColor(disjointGraph, nodes)
	string = filename + ".dot"
	graphIO.writeDOT(Q, string)
	print(".dot file created")

def doIndRef(colors, nodes, graphs):
	iso = []
	toDo = []
	for i in range(len(graphs)):
		toDo.append(i)
	for i in range(len(graphs)):
		if i in toDo:
			for j in range(i+1, len(graphs)):
				
				if j in toDo and getColors(nodes)[i] == getColors(nodes)[j]:
					print(i, j)
					cColors = copy.deepcopy(colors)
					cNodes = copy.deepcopy(nodes)
					colors, nodes, found = individualRef(cColors, cNodes, i, j)
					if found:
						added = False
						print("Iso's:", i, j)
						if i in toDo:
							toDo.remove(i)
						if j in toDo:
							toDo.remove(j)
						x = 0
						while x < len(iso) and not added:
							if i in iso[x]:
								iso[x].append(j)
								added = True
							elif j in iso[x]:
								iso[x].append(i)
								added = True
							x += 1
						if not added:
							iso.append([i, j])

					colors = cColors
					nodes = cNodes
	return iso

def automorphismCount(graphs):
	global UsedGraphs
	retVal = {}
	for i in range(len(graphs)):
		print("Graph", i)
		G = [graphs[i], copy.deepcopy(graphs[i])]
		UsedGraphs = G	
		colors = []
		nodes = []
		colors, nodes = setColorAsNrNeighbors(G)
		colors, nodes = colorRefinement(colors, nodes, -1, -1)
		t = 0
		colors, nodes, t = autCounter(colors, nodes, 0)
		retVal[i] = t
	return retVal

def searchIsomorphs(graphs):
	global UsedGraphs
	UsedGraphs = graphs
	colors, nodes = setColorAsNrNeighbors(UsedGraphs)
	print("-- Nodes colored as Nr of Neighbors")
	colors, nodes = colorRefinement(colors, nodes, -1, -1)
	print("-- Color Refinement done")
	isomorphs = doIndRef(colors, nodes, UsedGraphs)
	print("-- Individual Refinement done")
	return isomorphs

def AutGI(graphs):
	iso = searchIsomorphs(graphs)
	uniqueGraphs = []
	retVal = {}
	for i in range(len(iso)):
		uniqueGraphs.append(graphs[iso[i][0]])
		# print("Graphs: ", str(iso[i]))
	autos = automorphismCount(uniqueGraphs)
	for i in range(len(iso)):
		retVal[str(iso[i])] = autos[i]
		# retVal[str(iso[i])] = automorphismCount(graphs[iso[i][0]])
	return retVal

def main():
	typeinput = input("Choose 1 for GI, 2 for AUT or 3 for both: ")
	if typeinput != '1' and typeinput != '2' and typeinput != '3':
		print(" Wrong input")
		return
	filename = input("Please enter filename: ")
	G = loadGraphs(filename)
	if typeinput == '1':
		print("Isomorphs:")	
		iso = searchIsomorphs(G)
		for i in range(len(iso)):
			print(iso[i])
	elif typeinput == '2':
		print("Counting....")
		retVal = automorphismCount(G)
		print("Automorphs:")
		for i in range(len(retVal.keys())):
			print(list(retVal.keys())[i], ":", retVal[list(retVal.keys())[i]])
	elif typeinput == '3':
		auto = AutGI(G)
		print("Isomorphs, Automorphs:")
		for i in range(len(auto.keys())):
			print(list(auto.keys())[i], ":", auto[list(auto.keys())[i]])


## MAIN

if __name__ == "__main__":
	main()