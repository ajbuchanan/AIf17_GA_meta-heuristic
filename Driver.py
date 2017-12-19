from Algorithms import Searcher
from Utility import *

graph = generateGraph("Test_Problems/prob1.map")

searcher = Searcher(graph)

res = searcher.AStarSearch()
print res.pathString()

res = searcher.BreadthFirstSearch()
print res.pathString()

res = searcher.DepthFirstSearch()
print res.pathString()

res = searcher.UniformCostSearch()
print res.pathString()

#runProblems(30, "Test_Problems", "prob", "map")

def runProblems(numProbs, probFolder, probFile, probExtension):
    problemGraphs = {}
    problemScores = {}
    for num in range(numProbs):
        problemGraphs[num+1] = generateGraph(probFolder + "/" + probFile + str(num+1) + "." + probExtension)

        search = Searcher(problemGraphs[num+1])
        results = []

        res = search.AStarSearch()
        results.append(res)
        
        res = search.BreadthFirstSearch()
        results.append(res)
        
        res = search.DepthFirstSearch()
        results.append(res)
        
        res = search.UniformCostSearch()
        results.append(res)

        score = ProblemScore(results)
        problemScores[num+1] = score