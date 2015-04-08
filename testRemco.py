import graphIO
import basicgraphs
import copy
import operator
import math
import permv2
import basicpermutationgroup

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

			print("---- REMOVING []")
			print(crColors)
			print(nodes)
			while [] in crColors:			# remove empty lists in the colorlist
				crColors.remove([])
			print(crColors)
			print(nodes)
			print("----")

	if(crColors != colors):					# while the colors have changed in this function, do colorRefinement again
		crColors, nodes = colorRefinement(crColors, nodes)

	return crColors, nodes

# Gaat verder kleuren toekennen aan de graven tot het niet meer mogelijk is.
def colorRefinement(colors, nodes, graph1, graph2):
	allowedNotes = []
	if graph1 == -1 or graph2 == -1:
		for i in range(nrOfNodes*nrOfGraphs):
			allowedNotes.append(i)
	else:
		for i in range(nrOfNodes):
			allowedNotes.append(i+(nrOfNodes*graph1))
			allowedNotes.append(i+(nrOfNodes*graph2))
	crColors = copy.deepcopy(colors)
	# print(crColors)
	for i in range(len(crColors)):				# loop through all the colors
		nodesOfColor=copy.deepcopy(crColors[i])				# create a copy of the nodesOfColor
		first = True
		noneAllowed = False
		while(len(nodesOfColor) != 0 and not noneAllowed):					# while nodesOfColor have to be recolored
			n = 0
			allowed = False
			while not allowed and n < len(nodesOfColor):
				# print(n, nodesOfColor[n])
				
				# inp = input("-")
				if nodesOfColor[n] in allowedNotes:
					allowed = True
					# print("allowed!")
				else:
					n += 1
			# print("exit while")
			# if(n == 14):
				# inp = input("-")
			if allowed:
				# log.write(str(n) + " ")
				# log.write(str(nodesOfColor[n]) + str(nodesOfColor) + "\n")
				# print("in allowed")
				if not first:						# if not the first run ----- in the first run the first node doesn't need a new color. After the first run, it does. First node has to be a unique color
					crColors[i].remove(nodesOfColor[n])			# remove first node
					nodes[nodesOfColor[n]] = len(crColors)					# give first node new color
					crColors.append([nodesOfColor[n]])							# add first node to new color index
				first = False
				colorednodes=[nodesOfColor[n]]									# node 0 is always recolored

				# print(nodesOfColor)
				for q in range(len(nodesOfColor)): 									# loop through all the nodesOfColor that have to be recolored
					# print(q, nodesOfColor[q], allowedNotes)
					if nodesOfColor[q] in allowedNotes and nodesOfColor[q] != nodesOfColor[n]:
						if getNeighborsColors(nodesOfColor[n], nodes) == getNeighborsColors(nodesOfColor[q], nodes):	# if colors of the neighbors of 0 and q are the same
							# print("same nbs", nodesOfColor[n], nodesOfColor[q])
							crColors[i].remove(nodesOfColor[q])	
							nodes[nodesOfColor[q]] = nodes[nodesOfColor[n]]			# remove node q from old color index
							crColors[nodes[nodesOfColor[n]]].append(nodesOfColor[q])				# add node q to new color index
							colorednodes.append(nodesOfColor[q])							# add node q to list with recolored nodes

				for x in range(len(colorednodes)):			# loop through all recolored nodes
					nodesOfColor.remove(colorednodes[x])			# remove recolored nodes from nodes that need to be recolored

				# while [] in crColors:			# remove empty lists in the colorlist
				# 	crColors.remove([])
				
				if [] in crColors:
					while [] in crColors:
						i = crColors.index([])
						crColors.pop(i)
						for j in range(len(nodes)):
							if nodes[j] > i:
								nodes[j] -= 1
			else:
				noneAllowed = True
	# print(crColors)



	if(crColors != colors):					# while the colors have changed in this function, do colorRefinement again
		# print("Redo ClrRef")
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
	graphsWithDup = findGraphsWithDup(rColors, rNodes)
	i = 1
	done = False
	while i < len(graphsWithDup.keys()) and not done:
		g = list(graphsWithDup.keys())[i]
		j = 0
		while j < len(graphsWithDup[g]) and not done:
			copyColors = copy.deepcopy(rColors)
			copyNodes = copy.deepcopy(rNodes)
			
			g0 = list(graphsWithDup.keys())[0]				# RECOLOR FIRST NODE OF FIRST GRAPH
			
			node = graphsWithDup[g0][0]
			rColors[rNodes[node]].remove(node)
			rNodes[node] = len(rColors)
			rColors.append([node])

							# RECOLOR FIRST NODE OF NEXT GRAPHS
			node = graphsWithDup[g][j]
			rColors[rNodes[node]].remove(node)
			rNodes[node] = len(rColors)-1
			rColors[rNodes[node]].append(node)
			rColors, rNodes = colorRefinement(rColors, rNodes, list(graphsWithDup.keys())[0], g)
			allColors = getColors(rNodes)
			if(allColors[list(graphsWithDup.keys())[0]] == allColors[g]):
				if len(checkIsomorph(rNodes)[0]) < 2:
					print("ISO1")
					return rColors, rNodes
				else:
					# print("RECURSION")
					rColors, rNodes = individualRef_2(rColors, rNodes)
					# print("---- END RECURSION")
			else:
				rColors = copy.deepcopy(copyColors)
				rNodes = copy.deepcopy(copyNodes)
			j += 1
		i += 1
	return rColors, rNodes	

def gensetGen(colors, nodes, genSet, t):
	gS = genSet
	rColors = copy.deepcopy(colors)
	rNodes = copy.deepcopy(nodes)
	graphsWithDup = findGraphsWithDup(rColors, rNodes)
	# print(graphsWithDup)
	done = False
	g = list(graphsWithDup.keys())[0]
	if len(graphsWithDup.keys()) == 2:
		# for i in range(len(graphsWithDup[g])):
		j=0
		while j < len(graphsWithDup[g]) and not done:
			copyColors = copy.deepcopy(rColors)
			copyNodes = copy.deepcopy(rNodes)

			g0 = list(graphsWithDup.keys())[0]				# RECOLOR FIRST NODE OF FIRST GRAPH
			node = graphsWithDup[0][0]
			rColors[rNodes[node]].remove(node)
			rNodes[node] = len(rColors)
			rColors.append([node])

			node2 = graphsWithDup[1][j]
			rColors[rNodes[node2]].remove(node2)
			rNodes[node2] = len(rColors)-1
			rColors[rNodes[node2]].append(node2)

			rColors, rNodes = colorRefinement(rColors, rNodes, -1, -1)
			allColors = getColors(rNodes)
			# print("MAPPING:", node, "TO", node2%len(rNodes))
			# inp = input("kaas")
			if(allColors[0] == allColors[1]):

				gS[t].append([node, node2])
				# print("APPEND")

				if len(checkIsomorph(rNodes)[0]) >= 2:
					# print("RECURSION")
					rColors, rNodes, gS, t = gensetGen(rColors, rNodes, gS, t)
					# print("---- END RECURSION")
				else:
					rColors = copy.deepcopy(copyColors)
					rNodes 	= copy.deepcopy(copyNodes)
					# print("PLUS 1!!")
					t += 1
				if len(gS) == t:
					gS.append([])
				rColors = copy.deepcopy(copyColors)
				rNodes 	= copy.deepcopy(copyNodes)
			else:
				rColors = copy.deepcopy(copyColors)
				rNodes = copy.deepcopy(copyNodes)
			j += 1
		rColors = copy.deepcopy(colors)
		rNodes = copy.deepcopy(nodes)
	return rColors, rNodes, gS, t


def automorphismCount(graph):
	aNodes = len(graph.V())
	G = [graph, copy.deepcopy(graph)]
	colors = []
	nodes = []
	colors, nodes = setColorAsNrNeighbors2(G)
	colors, nodes = colorRefinement(colors, nodes, -1, -1)
	# print(colors)
	genSet = [[]]
	t = 0
	colors, nodes, genSet, t = gensetGen(colors, nodes, genSet, 0)
	return t

def stabOrder(P):
	sO = 1
	Orbitss = []
	stabilizer = P
	while stabilizer != []:
		el = el = basicpermutationgroup.FindNonTrivialOrbit(stabilizer)
		orbit = basicpermutationgroup.Orbit(stabilizer, el, False)
		# print(orbit)
		Orbitss.append(len(orbit))
		stabilizer = basicpermutationgroup.Stabilizer(stabilizer, el)

	for i in range(len(Orbitss)):
		sO = sO*Orbitss[i]
	return sO

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
G=loadGraphs('week2/cubes6.grl')

colors, nodes = setColorAsNrNeighbors2(G)
print("-- Nodes colors as Nr of Neighbors")
colors, nodes = colorRefinement(colors, nodes, -1, -1)
print("-- Color Refinement done")
if len(checkIsomorph(nodes)[0]) != 0:
	colors, nodes = individualRef_2(colors, nodes)
	print("-- Individual Refinement done")
	

print("-- Count Isomorphs")
printIsomorphs(checkIsomorph(nodes))
print("Isomorphs: ", automorphismCount(G[0]))