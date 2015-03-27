import graphIO
import basicgraphs
import copy
import operator

colors=[]
nodes=[]
nrOfGraphs = 0;
nrOfNodes = 0;

# Maakt de disjoint union van een lijst met graven
def createDisjointUnion(graphs):
	G=basicgraphs.graph()
	# global nrOfGraphs
	# nrOfGraphs = len(graphs)
	# global nrOfNodes
	# nrOfNodes = len(graphs[0].V())
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


def ripGraphs(isomorphs, graphs, disUnion):
	dUnion = copy.copy(disUnion)
	print("Disjoint Union: ", dUnion)
	print("morhps: ", isomorphs[0], "\n graphs: ", graphs)
	if len(isomorphs[0]) < 2:
		print("This graph is isomorph with itself.")
		return None 

	amountpopped = 0
	for i in range(len(graphs)):
		if i not in isomorphs[0]:
			print("Removing graph: ", i)
			nr = i * len(graphs[i].V()) - amountpopped
			for x in range(len(graphs[i].V())):
				E = []
				for nbs in range(len(dUnion.V()[nr].nbs())):
					E.append(dUnion.V()[nr].nbs()[nbs])
				for e in range(len(E)):
					dUnion._E.remove(dUnion.findedge(E[e], dUnion.V()[nr]))						
				print("Removing: ", nr)
				del dUnion._V[nr]
				amountpopped += 1
	return dUnion

# Geeft elke vertex in de graaf een kleur die correspondeert aan zijn degree #DONE
def setColorAsNrNeighbors(graph):
	colors=[[]]
	nodes = [0 for i in range(len(graph.V()))]
	colors[0].append(graph[0]._label)
	for i in range(1, len(graph.V())):
		added = False
		for x in range(len(colors)):
			if graph[colors[x][0]].deg() == graph[i].deg():
				nodes[i] = x
				colors[x].append(graph[i]._label)
				added = True
				break
		if not added:
			nodes[i] = len(colors)
			colors.append([graph[i]._label])

		# graph[i].colornum = graph[i].deg()
		# colors[graph[i].deg()].append(i)
	print("Nodes colored")
	return colors, nodes

	# Geeft elke vertex in de graaf een kleur die correspondeert aan zijn degree #DONE
def setColorAsNrNeighbors2(graphs):
	colors=[]
	global nrOfGraphs
	nrOfGraphs = len(graphs)
	global nrOfNodes
	nrOfNodes = len(graphs[0].V())

	colorPerDegree = []

	nodes = [0 for i in range(nrOfNodes*nrOfGraphs)]

	# colors[0].append(graphs[0][0]._label)
	# colorPerDegree[0] = graphs[0][0].deg()


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



	# nodes = [0 for i in range(len(graph.V()))]
	# colors[0].append(graph[0]._label)
	# for i in range(1, len(graph.V())):
	# 	added = False
	# 	for x in range(len(colors)):
	# 		if graph[colors[x][0]].deg() == graph[i].deg():
	# 			nodes[i] = x
	# 			colors[x].append(graph[i]._label)
	# 			added = True
	# 			break
	# 	if not added:
	# 		nodes[i] = len(colors)
	# 		colors.append([graph[i]._label])

	# 	# graph[i].colornum = graph[i].deg()
	# 	# colors[graph[i].deg()].append(i)
	# print("Nodes colored")
	# return colors, nodes


def getNeighborsColors(node, nodes):
	result=[]
	
	g = node//nrOfNodes
	n = node%nrOfNodes

	nbs = G[g][n].nbs()

	for i in range(len(nbs)):
		result.append(nodes[nbs[i]._label+(g*nrOfNodes)])

	merge_sort(result)

	return result

# def getNeighborsColors(node, nodes):
# 	result=[]

# 	print("gNC: ", disjointGraph[node], disjointGraph[node].nbs())
# 	nbs=disjointGraph[node].nbs()
# 	for i in range(len(nbs)):
# 		result.append(nodes[nbs[i]._label])
# 	merge_sort(result)

# 	return result

def colorRefinement(colors, nodes):
	rColors, rNodes = colorRefinement(colors, nodes, -1, -1)
	return rColors, rNodes


# Gaat verder kleuren toekennen aan de graven tot het niet meer mogelijk is.
def colorRefinement_old(colors, nodes):
	crColors = copy.deepcopy(colors)
	for i in range(len(crColors)):				# loop through all the colors
		nodesOfColor=copy.deepcopy(crColors[i])				# create a copy of the nodesOfColor
		first = True

		while(len(nodesOfColor) != 0):					# while nodesOfColor have to be recolored
			if not first:						# if not the first run ----- in the first run the first node doesn't need a new color. After the first run, it does. First node has to be a unique color
				crColors[i].remove(nodesOfColor[0])			# remove first node
				nodes[nodesOfColor[0]] = len(crColors)					# give first node new color
				crColors.append([nodesOfColor[0]])							# add first node to new color index
			first = False
			colorednodes=[nodesOfColor[0]]									# node 0 is always recolored

			for q in range(1, len(nodesOfColor)): 									# loop through all the nodesOfColor that have to be recolored
				if getNeighborsColors(nodesOfColor[0], nodes) == getNeighborsColors(nodesOfColor[q], nodes):	# if colors of the neighbors of 0 and q are the same
					crColors[i].remove(nodesOfColor[q])	
					nodes[nodesOfColor[q]] = nodes[nodesOfColor[0]]			# remove node q from old color index
					crColors[nodes[nodesOfColor[0]]].append(nodesOfColor[q])				# add node q to new color index
					colorednodes.append(nodesOfColor[q])							# add node q to list with recolored nodes

			for x in range(len(colorednodes)):			# loop through all recolored nodes
				nodesOfColor.remove(colorednodes[x])			# remove recolored nodes from nodes that need to be recolored

			while [] in crColors:			# remove empty lists in the colorlist
				crColors.remove([])

	if(crColors != colors):					# while the colors have changed in this function, do colorRefinement again
		crColors, nodes = colorRefinement(crColors, nodes)

	return crColors, nodes

# Gaat verder kleuren toekennen aan de graven tot het niet meer mogelijk is.
def colorRefinement(colors, nodes, graph1, graph2):
	crColors = copy.deepcopy(colors)
	for i in range(len(crColors)):				# loop through all the colors
		nodesOfColor=copy.deepcopy(crColors[i])				# create a copy of the nodesOfColor
		first = True

		while(len(nodesOfColor) != 0):					# while nodesOfColor have to be recolored
			if not first:						# if not the first run ----- in the first run the first node doesn't need a new color. After the first run, it does. First node has to be a unique color
				crColors[i].remove(nodesOfColor[0])			# remove first node
				nodes[nodesOfColor[0]] = len(crColors)					# give first node new color
				crColors.append([nodesOfColor[0]])							# add first node to new color index
			first = False
			colorednodes=[nodesOfColor[0]]									# node 0 is always recolored

			for q in range(1, len(nodesOfColor)): 									# loop through all the nodesOfColor that have to be recolored
				if getNeighborsColors(nodesOfColor[0], nodes) == getNeighborsColors(nodesOfColor[q], nodes):	# if colors of the neighbors of 0 and q are the same
					crColors[i].remove(nodesOfColor[q])	
					nodes[nodesOfColor[q]] = nodes[nodesOfColor[0]]			# remove node q from old color index
					crColors[nodes[nodesOfColor[0]]].append(nodesOfColor[q])				# add node q to new color index
					colorednodes.append(nodesOfColor[q])							# add node q to list with recolored nodes

			for x in range(len(colorednodes)):			# loop through all recolored nodes
				nodesOfColor.remove(colorednodes[x])			# remove recolored nodes from nodes that need to be recolored

			while [] in crColors:			# remove empty lists in the colorlist
				crColors.remove([])

	if(crColors != colors):					# while the colors have changed in this function, do colorRefinement again
		crColors, nodes = colorRefinement(crColors, nodes, graph1, graph2)

	return crColors, nodes


def individualRef_old(graph, colors):
	
	isDone = False

	rColors = copy.copy(colors)
	# print(colorlist)
	while(not isDone):
		for i in range(nrOfGraphs):
		# for i in range(1):
			colorlist = getColors(graph)
			if len(colorlist[i]) != len(set(colorlist[i])) :					# check for a dub
				print(colorlist[i], set(colorlist[i]))

				# print("dub i", i)
				j = 0
				dupColor = -1
				# print(colorlist[i])
				while dupColor == -1 and j < len(colorlist[i]) -1:			# finding dup color
					if colorlist[i][j] == colorlist[i][j+1]:
						dupColor = colorlist[i][j]
					j += 1

				# print(dupColor, rColors)
				# print("YOLO",rColors[dupColor])
				graphsWithDup = {}
				for x in range(len(rColors[dupColor])):
					g = (int(rColors[dupColor][x]._label)//nrOfNodes)
					graphsWithDup[g] = []
				for x in range(len(rColors[dupColor])):
					g = (int(rColors[dupColor][x]._label)//nrOfNodes)
					graphsWithDup[g].append(rColors[dupColor][x])

				print("Graphs: ", graphsWithDup)
				g = list(graphsWithDup.keys())[0]
				node = graphsWithDup[g][0]

				rColors[node.colornum].remove(node)
				node.colornum = len(rColors)
				rColors.append([node])



				testColors = copy.deepcopy(rColors)
				print("r", rColors)
				print("t", testColors)
				print(rColors is testColors)
				for k in range(1, len(graphsWithDup.keys())):
					g = list(graphsWithDup.keys())[k]
					n = 0
					isIso = False
					while not isIso and n < len(graphsWithDup[g]):
						node = graphsWithDup[g][n]
						print("color", rColors, node.colornum, node)
						rColors[node.colornum].remove(node)
						node.colornum = len(rColors)-1
						rColors[node.colornum].append(node)
						# print("print", testColors, node)

						# print("rColors: ", rColors)
						rColors = colorRefinement(rColors)



						if getColors(graph)[i] == getColors(graph)[g]:
							isIso = True
						else:
							# rColors = testColors
							for y in range(len(rColors)):
								

								for z in range(len(rColors[y])):
									# print(rColors[y][z]._label)
									# print("print2", rColors, node)
									
									yy = 0
									zz = 0
									found = False

									while not found and yy < len(testColors):
										while not found and zz < len(testColors[yy]):
											# print("--", found, y, z, yy, zz)
											if rColors[y][z]._label == testColors[yy][zz]._label:
												graph.V()[rColors[y][z]._label].colornum = testColors[yy][zz].colornum
												# print("-------------------------------------")
												found = True
												z = -1
											zz += 1
										yy += 1


							for y in range(2, len(rColors)):
								# for z in range(len(rColors[y])):
								while len(rColors[y]) > 0:
									print(rColors, y)			
									rColors[graph.V()[rColors[y][0]._label].colornum].append(graph.V()[rColors[y][0]._label])
									rColors[y].remove(rColors[y][0])

						n += 1
						print("getColors", getColors(graph))
				print("yeey")
		if len(checkIsomorph(graph)[0]) == 0:
			isDone = True	

def findGraphsWithDup(colors, nodes):
	for i in range(nrOfGraphs):
		colorlist = getColors(nodes)
		if len(colorlist[i]) != len(set(colorlist[i])) :					# check for a dub
			j = 0
			dupColor = -1
			# print(colorlist[i])
			while dupColor == -1 and j < len(colorlist[i]) -1:			# finding dup color
				if colorlist[i][j] == colorlist[i][j+1]:
					dupColor = colorlist[i][j]
				j += 1
			graphsWithDup = {}
			for x in range(len(colors[dupColor])):
				g = (int(colors[dupColor][x])//nrOfNodes)
				graphsWithDup[g] = []
			for x in range(len(colors[dupColor])):
				g = (int(colors[dupColor][x])//nrOfNodes)
				graphsWithDup[g].append(colors[dupColor][x])
	return graphsWithDup


def individualRef_2(colors, nodes):
	rColors = copy.deepcopy(colors)
	rNodes = copy.deepcopy(nodes)

	print(rNodes)
	print(rColors)
	graphsWithDup = findGraphsWithDup(rColors, rNodes)

	g = list(graphsWithDup.keys())[0]				# RECOLOR FIRST NODE OF FIRST GRAPH
	node = graphsWithDup[g][0]
	rColors[rNodes[node]].remove(node)
	rNodes[node] = len(rColors)
	rColors.append([node])
	# for i in range(1, len(graphsWithDup.keys())):
	# print(graphsWithDup)
	# for i in range(1, 2):
	i = 1
	done = False
	print("GRAPHS!", graphsWithDup)
	while i < len(graphsWithDup.keys()) and not done:
	# for i in range(1, len(graphsWithDup.keys())):
		g = list(graphsWithDup.keys())[i]
		j = 0
		while j < len(graphsWithDup[g]) and not done:
			print()
			print(list(graphsWithDup.keys())[i], j, "------------------")
			print(graphsWithDup)
			copyColors = copy.deepcopy(rColors)
			copyNodes = copy.deepcopy(rNodes)
							# RECOLOR FIRST NODE OF NEXT GRAPHS
			# g = 1
			node = graphsWithDup[g][j]
			rColors[rNodes[node]].remove(node)
			rNodes[node] = len(rColors)-1
			rColors[rNodes[node]].append(node)

			
			print("B", rColors, rNodes)
			rColors, rNodes = colorRefinement(rColors, rNodes)
			print("A", rColors, rNodes)
			allColors = getColors(rNodes)
			print(g, allColors[0], allColors[g])
			# inp = input("hi")

			if(allColors[0] == allColors[g]):
				if len(checkIsomorph(rNodes)[0]) < 2:
					print("ISO1")
					return rColors, rNodes
				else:
					print("RECURSION")
					rColors, rNodes = individualRef_2(rColors, rNodes)
					print("---- END RECURSION")
					if(allColors[0] == allColors[g]):
						print("ISO2")
						if len(checkIsomorph(rNodes)[0]) < 2:
							return rColors, rNodes
						else:
							isomorphs = checkIsomorph(rNodes)
							for x in range(len(isomorphs[0])):
								# rColors[isomorphs[0][x]] = copy.deepcopy(copyColors[isomorphs[0][x]])
								for y in range(x*nrOfNodes, (x+1)*nrOfNodes):
									rNodes[y] = copy.deepcopy(copyNodes[y])
						# return rColors, rNodes
					# return rColors, rNodes
			else:
				print("NOT RECURSION!")
				if len(checkIsomorph(rNodes)[0]) >= 2:
					rColors = copy.deepcopy(copyColors)
					rNodes = copy.deepcopy(copyNodes)
			j += 1
		i += 1
	# if len(checkIsomorph(rNodes)[0]) >= 2:


	return rColors, rNodes	

# def individualRef(colors, nodes):
	
# 	isDone = False
# 	print("COLORS: ", colors)
# 	rColors = copy.deepcopy(colors)
# 	rNodes = copy.deepcopy(nodes)
# 	# print(colorlist)
# 	while(not isDone):
# # <<<<<<< HEAD
# 		# for i in range(nrOfGraphs):
# 		# for i in range(1):
# 		# for i in range(1):
# 		i = 0
# 		colorlist = getColors(rNodes)
# 		# print(i, colorlist)
# 		if len(colorlist[i]) != len(set(colorlist[i])) :					# check for a dub
# 			# print(colorlist[i], set(colorlist[i]))

# 			# print("dub i", i)
# 			j = 0
# 			dupColor = -1
# 			# print(colorlist[i])
# 			while dupColor == -1 and j < len(colorlist[i]) -1:			# finding dup color
# 				if colorlist[i][j] == colorlist[i][j+1]:
# 					dupColor = colorlist[i][j]
# 				j += 1

# 			# print(dupColor, rColors)
# 			# print("YOLO",rColors[dupColor])
# 			graphsWithDup = {}
# 			for x in range(len(rColors[dupColor])):
# 				# print("rcolors: ", rColors, rColors[dupColor])
# 				g = (int(rColors[dupColor][x])//nrOfNodes)
# 				graphsWithDup[g] = []
# 			for x in range(len(rColors[dupColor])):
# 				g = (int(rColors[dupColor][x])//nrOfNodes)
# 				graphsWithDup[g].append(rColors[dupColor][x])

# 			print("Graphs: ", graphsWithDup)
# 			g = list(graphsWithDup.keys())[0]
# 			node = graphsWithDup[g][0]
# 			print("RCOLOR1:", rColors)
# 			rColors[rNodes[node]].remove(node)
# 			rNodes[node] = len(rColors)
# 			rColors.append([node])
# 			print("RCOLOR:", rColors)

# 			for k in range(1, len(graphsWithDup.keys())):
# 				g = list(graphsWithDup.keys())[k]
# 				node = graphsWithDup[2][0]
# 				print(rNodes, node)
# 				rColors[rNodes[node]].remove(node)
# 				rNodes[node] = len(rColors)-1
# 				rColors[rNodes[node]].append(node)
# 				print("RCOLOR3:", rColors)
# 			# print("rColors: ", rColors)
# 			rColors, rNodes = colorRefinement(rColors, rNodes)
# 			print("rColors: ", rColors)
# 			# print("yeey")
# =======

# 		graphsWithDup = findGraphsWithDup(rColors, rNodes)

# 		print("Graphs: ", graphsWithDup)
# 		g = list(graphsWithDup.keys())[0]
# 		node = graphsWithDup[g][0]
# 		# print("RCOLOR1:", rColors)
# 		rColors[rNodes[node]].remove(node)
# 		rNodes[node] = len(rColors)
# 		rColors.append([node])
# 		print("NODES", rNodes)
# 		# print("RCOLOR:", rColors)


# 		for k in range(1, len(graphsWithDup.keys())):
# 			g = list(graphsWithDup.keys())[k]
# 			m = 0
# 			isomorph = False
# 			copyColors = copy.deepcopy(rColors)
# 			copyNodes = copy.deepcopy(rNodes)
# 			while m < len(graphsWithDup[g]) and not isomorph:
# 				print(g, m)
# 				# print(node, rColors, rNodes)
# 				node = graphsWithDup[g][m]
# 				print("cb", rColors)
# 				print("nb", rNodes)
# 				rColors[rNodes[node]].remove(node)
# 				rNodes[node] = len(rColors)-1
# 				rColors[rNodes[node]].append(node)
# 				print("ca", rColors)
# 				print("na", rNodes)
# 				# inputv = input("hoi")
# 				rColors, rNodes = colorRefinement(rColors, rNodes)
# 				print("ccr", rColors)
# 				print("ncr", rNodes)
# 				if isIsomorph(list(graphsWithDup.keys())[0], list(graphsWithDup.keys())[k], rNodes):
# 					isomorph = True
# 					print("ISOOOOOO")
# 				else:
# 					m += 1
# 					# print("before", rNodes)
# 					rColors = copy.deepcopy(copyColors)
# 					rNodes = copy.deepcopy(copyNodes)
# 					# print("after", rNodes)

# 			# for k in range(1, len(graphsWithDup.keys())):
# 			# 	g = list(graphsWithDup.keys())[k]
# 			# 	node = graphsWithDup[g][0]
# 			# 	print(rNodes, node)
# 			# 	rColors[rNodes[node]].remove(node)
# 			# 	rNodes[node] = len(rColors)-1
# 			# 	rColors[rNodes[node]].append(node)
# 			# 	print("RCOLOR3:", rColors)
# 			# # print("rColors: ", rColors)
# 			# rColors, rNodes = colorRefinement(rColors, rNodes)
# 			# print("rColors: ", rColors)
# 			# # print("yeey")
# >>>>>>> f92ad233749832854e6779db3b534341c56ac66f
# 		if len(checkIsomorph(rNodes)[0]) < 2:
# 			isDone = True	
# 		i += 1
# 		i%nrOfGraphs
# 	return rColors, rNodes

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

## MAIN

global G
G = loadGraphs('week1/crefBM_4_9.grl')
# G=loadGraphs('week2/cubes3.grl')
#print("aantal graphs: ", len(G))-
global disjointGraph
disjointGraph = createDisjointUnion(G)
nbs = disjointGraph.V()[0].nbs()
#print(disjointGraph[nbs[0]._label])
# graphIO.writeDOT(G[0], 'graph1.dot')
# graphIO.writeDOT(G[1], 'graph2.dot')
# graphIO.writeDOT(G[2], 'graph3.dot')
# graphIO.writeDOT(G[3], 'graph4.dot')

# for i in range(len(G)):
colors, nodes = setColorAsNrNeighbors(disjointGraph)
colors2, nodes2 = setColorAsNrNeighbors2(G)
T = (colors == colors2)
T2 = (nodes == nodes2)
print(colors)
print(colors2)
print(nodes)
print(nodes2)
print(T, T2)
nbc = getNeighborsColors(16, nodes)
nbc2 = getNeighborsColors2(16, nodes)
print(nbc)
print(nbc2)
# colors, nodes = colorRefinement(colors, nodes)
# printIsomorphs(checkIsomorph(nodes))

# colors, nodes = individualRef_2(colors, nodes)
# print(colors, nodes)
# Q = giveColor(disjointGraph, nodes)
# graphIO.writeDOT(Q, 'graph.dot')
# <<<<<<< HEAD
# colors, nodes = individualRef(colors, nodes)
# colors[0].remove(0)
# colors[0].remove(16)
# colors.append([0])
# colors[-1].append(16)
# nodes[0] = len(colors)-1
# nodes[16] = len(colors)-1
# colors, nodes = colorRefinement(colors, nodes)
# printIsomorphs(checkIsomorph(nodes))
# colors[0].remove(1)
# colors[0].remove(19)
# colors.append([1])
# colors[-1].append(19)
# nodes[1] = len(colors)-1
# nodes[19] = len(colors)-1
# colors, nodes = colorRefinement(colors, nodes)
# printIsomorphs(checkIsomorph(nodes))
# colors[0].remove(4)
# colors[0].remove(21)
# colors.append([4])
# colors[-1].append(21)
# nodes[4] = len(colors)-1
# nodes[21] = len(colors)-1
# colors, nodes = colorRefinement(colors, nodes)
# printIsomorphs(checkIsomorph(nodes))
# colors, nodes = individualRef(colors, nodes)
# =======
# >>>>>>> f92ad233749832854e6779db3b534341c56ac66f
# printIsomorphs(checkIsomorph(nodes))

# colors, nodes = individualRef_2(colors, nodes)
# print(Isomorphs(checkIsomorph(nodes)))
# print(colors, nodes)
# Q = giveColor(disjointGraph, nodes)
# graphIO.writeDOT(Q, 'graphinf.dot')
# print("COLOR: ", colors, "NODES: ", nodes)

# print("Colors: ", colors)
# colors = colorRefinement(colors)
# # print("rColors: ", len(colors))
# # print("NODE 22", disjointGraph.V()[22].colornum)

# printIsomorphs(checkIsomorph(disjointGraph))
# graphIO.writeDOT(disjointGraph, 'graph_colors.dot')
# individualRef(disjointGraph, colors)
# printIsomorphs(checkIsomorph(disjointGraph))
# graphIO.writeDOT(disjointGraph, 'graph_colors_2.dot')
#print("Colors: \n",colors)

