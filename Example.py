from Algorithms import Searcher
from Utility import *
from GeneticAlgorithm import *

graph = generateGraph("Test_Problems/prob15.map")

searcher = Searcher(graph)
res = []
res.append(searcher.AStarSearch())

res.append(searcher.BreadthFirstSearch())

res.append(searcher.DepthFirstSearch())

res.append(searcher.UniformCostSearch())

ProbScore = ProblemScore(res)
ProbScore.printScores()
scores = ProbScore.GetScores()
resDict = ProbScore.GetResultDict()

GA = GeneticAlgorithm(50, scores, resDict)

gaRes = GA.PerformAlgorithm()

gaRes.printResult()