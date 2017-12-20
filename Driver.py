from Algorithms import Searcher
from Utility import *
from GeneticAlgorithm import *

'''
graph = generateGraph("Test_Problems/prob1.map")

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
'''

def runProblems(numProbs, probFolder, probFile, probExtension):
    problemGraphs = {}
    problemScores = {}
    for num in range(numProbs):
        print "Problem: " + str(num+1) + "\n"
        
        problemGraphs[num+1] = generateGraph(probFolder + "/" + probFile + str(num+1) + "." + probExtension)

        searcher = Searcher(problemGraphs[num+1])
        res = []
        res.append(searcher.AStarSearch())

        res.append(searcher.BreadthFirstSearch())

        res.append(searcher.DepthFirstSearch())

        res.append(searcher.UniformCostSearch())

        ProbScore = ProblemScore(res)
        problemScores[num+1] = ProbScore
        ProbScore.printScores()
        scores = ProbScore.GetScores()
        resDict = ProbScore.GetResultDict()

        GA = GeneticAlgorithm(100, scores, resDict)

        gaRes = GA.PerformAlgorithm()

        print "Results: "
        gaRes.printResult()

        print ""


runProblems(9, "Test_Problems", "prob", "map")
