import graphIO
import basicgraphs
import operator
import math
import time
import copy
import projectGroep1 as G
import preprocessing as Pre

def timer(graphs):
	graph1 = copy.deepcopy(graphs)

	G.UsedGraphs = graph1
	colors1, colors2, colors3, colors4 = [], [], [], []
	nodes1, nodes2, nodes3, nodes4 = [], [], [], []
	found = True

	noPre = time.time()
	colors1, nodes1 = G.setColorAsNrNeighbors(graph1)
	colors1, nodes1 = G.colorRefinement(colors1, nodes1, -1, -1)
	colors1, nodes1, found = G.individualRef(colors1, nodes1)
	noPre = time.time() - noPre
	# G.printIsomorphs(G.checkIsomorph(nodes1))

	graph2 = copy.deepcopy(graphs)
	VeE = time.time()
	graph2 = Pre.checkLength(graph2)
	G.UsedGraphs = graph2
	colors2, nodes2 = G.setColorAsNrNeighbors(graph2)
	colors2, nodes2 = G.colorRefinement(colors2, nodes2, -1, -1)
	colors2, nodes2, found = G.individualRef(colors2, nodes2)
	VeE = time.time() - VeE
	# G.printIsomorphs(G.checkIsomorph(nodes2))

	graph3 = copy.deepcopy(graphs)
	con = time.time()
	graph3 = Pre.checkConnected(graph3)
	G.UsedGraphs = graph3
	colors3, nodes3 = G.setColorAsNrNeighbors(graph3)
	colors3, nodes3 = G.colorRefinement(colors3, nodes3, -1, -1)
	colors3, nodes3, found = G.individualRef(colors3, nodes3)
	con = time.time() - con
	# G.printIsomorphs(G.checkIsomorph(nodes3))

	graph4 = copy.deepcopy(graphs)
	both = time.time()
	graph4 = Pre.checkLength(graph4)
	graph4 = Pre.checkConnected(graph4)
	G.UsedGraphs = graph4
	colors4, nodes4 = G.setColorAsNrNeighbors(graph4)
	colors4, nodes4 = G.colorRefinement(colors4, nodes4, -1, -1)
	colors4, nodes4, found = G.individualRef(colors4, nodes4)
	both = time.time() - both
	# G.printIsomorphs(G.checkIsomorph(nodes4))

	print("Time without preprocessing: ", round(noPre, 2))
	print("Time with checking for length edges and vertices: ", round(VeE, 2), "Precenctage difference: ", round(((noPre-VeE)/noPre)*100, 2), "%")
	print("Time with checking for connectivity: ", round(con, 2), "Precenctage difference: ", round(((noPre-con)/noPre)*100, 2), "%")
	print("Time with checking for both: ", round(both, 2), "Precenctage difference: ", round(((noPre-both)/noPre)*100, 2), "% \n")


def main():
	graph = G.loadGraphs("week2/cubes5.grl")
	print("Test with all isomorphic graphs: ")
	timer(graph)

	graph1 = G.loadGraphs("test/cubes5_VeE.grl")
	print("Test with one graph with less vertices/egdes: ")
	timer(graph1)

	graph2 = G.loadGraphs("test/cubes5_con.grl")
	print("Test with one disconnected graph: ")
	timer(graph2)

	graph3 = G.loadGraphs("test/cubes5_both.grl")
	print("Test with one disconnected and one with less vertices/edges: ")
	timer(graph3)

main()