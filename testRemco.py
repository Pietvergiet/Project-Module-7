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

def checkIsomorph(graph, colors):
	graphs = []
	for i in range(nrOfGraphs):
		graphs.append([])

	nodes = graph.V()
	for j in range(nrOfGraphs):
		for i in range(nrOfNodes):
			# print("i", (i+(j*nrOfNodes)))
			graphs[j].append(nodes[(i+(j*nrOfNodes))].colornum)
			# print((i+(j*nrOfNodes)))

	for i in range(len(graphs)):
		merge_sort(graphs[i])
		# print(i, ":", graphs[i])

	isomorphs = [[]]
	for i in range(len(graphs)):
		if len(graphs[i]) != len(set(graphs[i])):
			isomorphs[0].append(i)
		else:
			added = False
			for j in range(1, len(isomorphs)):
				# print(j, i, graphs[isomorphs[j][0]], graphs[i])
				if(graphs[isomorphs[j][0]] == graphs[i]):
					isomorphs[j].append(i)
					added = True
			if not added:
				isomorphs.append([i])

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
	for i in range(len(rColors)):				# KLEUR
	# for i in range(0, 2):
		nbss = len(rColors[i][0].nbs())
		# print("amount of nbs:", nbss)
		nodes=copy.copy(rColors[i])
		first = True
		while(len(nodes) != 0):
			if not first:
				rColors[nodes[0].colornum].remove(nodes[0])
				nodes[0].colornum = len(rColors)
				rColors.append([nodes[0]])
			first = False
			checkednodes=[]
			# print("nodes", nodes)
			for q in range(1, len(nodes)): 		# nodes
				if getNeighborsColors(nodes[0]) == getNeighborsColors(nodes[q]):				# color neighbors 1 = color neighbors q
					rColors[nodes[q].colornum].remove(nodes[q])
					nodes[q].colornum = nodes[0].colornum
					rColors[nodes[0].colornum].append(nodes[q])
					# print("rColors append, ", nodes[0].colornum, nodes[q], "q: ", q)
					checkednodes.append(nodes[q])
					# nodes.remove(nodes[q])
				# else:
				# 	print("rCOlors", rColors)
				# 	print("remove from", nodes[q].colornum, nodes[q])
				# 	rColors[nodes[q].colornum].remove(nodes[q])
				# 	nodes[q].colornum = len(rColors)
				# 	rColors.append([nodes[q]])
				# 	# print("rColors append new, ", nodes[q], "q: ", q)

			for i in range(len(checkednodes)):
				nodes.remove(checkednodes[i])
			nodes.remove(nodes[0])

			while [] in rColors:
				rColors.remove([])
			
	if(rColors != colors):
		colorRefinement(graph, rColors)
	return rColors






			# print(q)
			# x = 1
			# while x <= nbss:
			# 	# print(x, nbss)
			# 	for j in range(x, 0, -1):
			# 		for k in range(nbss):
			# 			same = False
			# 			for l in range(nbss):
			# 				if rColors[i][x].nbs()[k].colornum == rColors[i][j].nbs()[l].colornum or same:
			# 					same = True
			# 			if not same :
			# 				print(q, j, k, l)
			# 				rColors[i][j].colornum=len(rColors)
			# 				colors.append([rColors[i][j]])
			# 				break
			# 	x+=1			


	# return rColors

def loadGraphs(file):
	L = graphIO.loadgraph(file, readlist=True)
	G=[0 for i in range(len(L[0]))]
	for i in range(len(G)):
		G[i] = L[0][i]
	return G

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

G=loadGraphs('week1/crefBM_4_7.grl')
#print("aantal graphs: ", len(G))-
H = createDisjointUnion(G)
N = ripGraphs([[0,1]], G, H)
print(N)
# nbs = H.V()[0].nbs()
# #print(H[nbs[0]._label])
# graphIO.writeDOT(G[0], 'graph1.dot')
# graphIO.writeDOT(G[1], 'graph2.dot')
# # graphIO.writeDOT(G[2], 'graph3.dot')
# # graphIO.writeDOT(G[3], 'graph4.dot')
# # graphIO.writeDOT(H, 'graph.dot')
# # for i in range(len(G)):
# colors = setColorAsNrNeighbors(H)
# # print("Colors: ", colors)
# colors = colorRefinement(H, colors)
# # print("rColors: ", colors)

# checkIsomorph(H, colors)

# #print("Colors: \n",colors)
graphIO.writeDOT(N, 'ripGraph.dot')
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