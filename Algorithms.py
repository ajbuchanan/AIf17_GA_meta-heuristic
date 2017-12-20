import sys
from Utility import *

class Searcher:
    def __init__(self, graph):
        self.mGraph = graph

    def DepthFirstSearch(self):
        frontier = Stack()
        currentNode = self.mGraph.getRoot()
        prevNode = currentNode
        path = {}
        numExpanded = 0
        maxQueue = 0

        while not currentNode.isGoal():
            path[currentNode] = prevNode

            successors = self.mGraph.getSuccessors(currentNode)
            numExpanded += 1

            for successor in successors:
                frontier.push(successor)

            if len(frontier) > maxQueue:
                maxQueue = len(frontier)

            prevNode = currentNode
            currentNode = frontier.pop()

        path[currentNode] = prevNode

        print "Finished DFS"
        return self.generateResults(path, currentNode, "DFS", maxQueue, numExpanded)

    def BreadthFirstSearch(self):
        frontier = Queue()
        currentNode = self.mGraph.getRoot()
        prevNode = currentNode
        path = {}
        numExpanded = 0
        maxQueue = 0

        while not currentNode.isGoal():
            path[currentNode] = prevNode

            successors = self.mGraph.getSuccessors(currentNode)
            numExpanded += 1

            for successor in successors:
                frontier.push(successor)

            if len(frontier) > maxQueue:
                maxQueue = len(frontier)

            prevNode = currentNode
            currentNode = frontier.pop()

        path[currentNode] = prevNode

        print "Finished BFS"
        return self.generateResults(path, currentNode, "BFS", maxQueue, numExpanded)

    def AStarSearch(self):
        frontier = []
        visited = []
        path = {}
        gScore = {}
        fScore = {}
        numExpanded = 0
        maxQueue = 0
        foundGoal = False
        currentNode = self.mGraph.getRoot()
        path[currentNode] = currentNode
        goalCol = self.mGraph.getGoal().getCol()
        goalRow = self.mGraph.getGoal().getRow()
        gScore[currentNode] = 0
        fScore[currentNode] = currentNode.getCost()

        frontier.append(currentNode)

        while len(frontier):
            fScoreVal = sys.maxint
            currentIndex = 0

            for i in range(len(frontier)):
                if fScore.has_key(frontier[i]) and fScore[frontier[i]] < fScoreVal:
                    currentNode = frontier[i]
                    currentIndex = i

            del frontier[currentIndex]
            visited.append(currentNode)

            successors = self.mGraph.getSuccessors(currentNode)
            numExpanded += 1

            for successor in successors:
                if successor in visited:
                    continue

                if successor not in frontier:
                    frontier.append(successor)
                    if len(frontier) > maxQueue:
                        maxQueue = len(frontier)

                tempScore = gScore[currentNode] + 1
                if gScore.has_key(successor) and tempScore >= gScore[successor]:
                    continue

                path[successor] = currentNode

                if successor.isGoal():
                    foundGoal = True
                    currentNode = successor
                    break

                gScore[successor] = tempScore
                fScore[successor] = gScore[successor] + successor.getCost()

            if foundGoal:
                break

        print "Finished AS"
        return self.generateResults(path, currentNode, "AS", maxQueue, numExpanded)

    def UniformCostSearch(self):
        frontier = []
        visited = []
        path = {}
        gScore = {}
        fScore = {}
        numExpanded = 0
        maxQueue = 0
        foundGoal = False
        currentNode = self.mGraph.getRoot()
        path[currentNode] = currentNode
        goalCol = self.mGraph.getGoal().getCol()
        goalRow = self.mGraph.getGoal().getRow()
        gScore[currentNode] = 0
        fScore[currentNode] = 1

        frontier.append(currentNode)

        while len(frontier):
            fScoreVal = sys.maxint
            currentIndex = 0

            for i in range(len(frontier)):
                if fScore.has_key(frontier[i]) and fScore[frontier[i]] < fScoreVal:
                    currentNode = frontier[i]
                    currentIndex = i

            del frontier[currentIndex]
            visited.append(currentNode)

            successors = self.mGraph.getSuccessors(currentNode)
            numExpanded += 1

            for successor in successors:
                if successor in visited:
                    continue

                if successor not in frontier:
                    frontier.append(successor)
                    if len(frontier) > maxQueue:
                        maxQueue = len(frontier)

                tempScore = gScore[currentNode] + 1
                if gScore.has_key(successor) and tempScore >= gScore[successor]:
                    continue

                path[successor] = currentNode

                if successor.isGoal():
                    foundGoal = True
                    currentNode = successor
                    break

                gScore[successor] = tempScore
                fScore[successor] = gScore[successor] + 1

            if foundGoal:
                break

        print "Finished UCS"
        return self.generateResults(path, currentNode, "UCS", maxQueue, numExpanded)

    def generateResults(self, path, lastNode, algorithm, maxQ, numX):
        if lastNode.isGoal():
            print "Found Goal"

        truePath = []
        truePath.insert(0, lastNode)        
        prevNode = lastNode
        currentNode = path[lastNode]

        while prevNode is not currentNode:
            truePath.insert(0, currentNode)
            prevNode = currentNode
            currentNode = path[currentNode]

        result = Result(truePath, maxQ, numX, lastNode.isGoal(), algorithm)

        return result