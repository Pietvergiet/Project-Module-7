import sys, os
import unittest
import preprocessing as p

class testPreprocessing(unittest.TestCase):

	def testSizeList(self):
		self.maxDiff = None
		G = p.loadGraphs('test/testSize.grl')
		self.assertEqual(str(p.checkLength(G)), str(p.loadGraphs('test/testSizePredicted.grl')))

	def testConnected(self):
		self.maxDiff = None
		G = p.loadGraphs('test/testConnected.grl')
		self.assertTrue(G[0].isConnected())
		self.assertFalse(G[1].isConnected())
		self.assertTrue(G[2].isConnected())
		self.assertTrue(G[3].isConnected())

	def testConnectedList(self):
		self.maxDiff = None
		G = p.loadGraphs('test/testConnected.grl')
		self.assertEqual(str(p.checkConnected(G)), str(p.loadGraphs('test/testConnectedPredicted.grl')))

if __name__ == '__main__':
	unittest.main()