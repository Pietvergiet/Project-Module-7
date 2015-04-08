import graphIO
import basicgraphs
import copy
import operator

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

def loadGraphs(file):
	L = graphIO.loadgraph(file, readlist=True)
	G=[0 for i in range(len(L[0]))]
	for i in range(len(G)):
		G[i] = L[0][i]
	return G

# Check for number of vertices and edges
def checkLength(graphs):
	indices = []
	for i in range(len(graphs)):
		for j in range(i+1, len(graphs)):
			print(i,j)
			if len(graphs[i].V()) == len(graphs[j].V()) and len(graphs[i].E()) == len(graphs[j].E()):
				indices.append(i)
				indices.append(j)

	result = []
	indices = list(set(indices))
	for i in range(len(indices)):
		result.append(graphs[i])
	return result

def checkConnected(graphs):
	indices = []
	for i in range(len(graphs)):
		for j in range(i+1, len(graphs)):
			# print(graphs[i].isConnected)
			if graphs[i].isConnected() == graphs[j].isConnected():
				indices.append(i)
				indices.append(j)

	result = []
	indices = list(set(indices))
	for i in range(len(indices)):
		result.append(graphs[i])
	print(indices)
	return result

def checkConnectedParts(G):
	K = G.V()
	antb = []		# antb staat voor array nog te behandelen
	avb = []		# avb staat voor array volledig behandeld
	teller = 0
	result = []

	while len(K) > 0:
		teller += 1
		antb.append(K[0])
		K.pop(0)
		while len(antb) > 0:
			for i in range(len(K)):
				if G.adj(K[i], antb[0]) == True:
					antb.append(K[i])
					K.pop(i)
			avb.append(antb[0])
			antb.pop(0)
		result.append(avb)
		avb = []
	return result

G = loadGraphs('week2/test.grl')
print(checkConnectedParts(G[0]))