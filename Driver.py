from Utility import *

graph = generateGraph("Test_Problems/prob2.map")

print str(graph)


def runProblems(numProbs, probFolder, probFile, probExtension):
    problemGraphs = {}
    for num in range(numProbs):
        problemGraphs[num] = generateGraph(probFolder + "/" + probFile + str(num) + "." + probExtension)