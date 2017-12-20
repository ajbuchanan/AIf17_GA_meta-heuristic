import sys
from collections import defaultdict

BOARDSIZE = 10

OPEN = '.'
WALL = 'x'
GOAL = 'g'
STRT = 's'
XPLR = 'e'
################################
#       NOTE                   #
# Maze[Y][X] or Maze[ROW][COL] #
################################

def generateGraph(filename):
    #Construct a 2d array of the apporpriate size
    Maze = [[0 for x in range(BOARDSIZE)] for y in range(BOARDSIZE)]

    startRow = -1
    startCol = -1
    goalRow = -1
    goalCol = -1

    #read the file in line by line
    lines = [line.rstrip('\n') for line in open(filename)]

    #Go through the list form of the lines from the file and turn it into the 2d array of characters
    for i in range(BOARDSIZE):
        j = 0
        for c in lines[i]:
            if c == STRT:
                startRow = i
                startCol = j
            
            if c == GOAL:
                goalRow = i
                goalCol = i

            Maze[i][j] = c
            j = j + 1
    

    graphQueue = Queue()
    graph = Graph(startCol, startRow, goalCol, goalRow)

    node = Node(startCol, startRow, ManhattanDistance(startCol, startRow, goalCol, goalRow))
    graph.addNode(node)

    col = startCol
    row = startRow

    graphQueue.push(node)

    #Go through and starting from the root space construct the graph from the 2d array of characters
    while not graphQueue.isEmpty():
        node = graphQueue.pop()

        col = node.getCol()
        row = node.getRow()

        Maze[row][col] = XPLR

        # Look Down
        if row+1 < BOARDSIZE and Maze[row+1][col] == OPEN or Maze[row+1][col] == GOAL:
            isGoal = Maze[row+1][col] == GOAL
            downNode = Node(col, row+1, ManhattanDistance(col, row+1, goalCol, goalRow), isGoal)
            graph.addNode(downNode)
            graph.addEdge(node, downNode)

            graphQueue.push(downNode)

        # Look Up
        if row-1 >= 0 and Maze[row-1][col] == OPEN or Maze[row-1][col] == GOAL:
            isGoal = Maze[row-1][col] == GOAL
            upNode = Node(col, row-1, ManhattanDistance(col, row-1, goalCol, goalRow), isGoal)
            graph.addNode(upNode)
            graph.addEdge(node, upNode)

            graphQueue.push(upNode)

        # Look Right
        if col+1 < BOARDSIZE and Maze[row][col+1] == OPEN or Maze[row][col+1] == GOAL:
            isGoal = Maze[row][col+1] == GOAL
            rightNode = Node(col+1, row, ManhattanDistance(col+1, row, goalCol, goalRow), isGoal)
            graph.addNode(rightNode)
            graph.addEdge(node, rightNode)

            graphQueue.push(rightNode)
            
        # Look left
        if col-1 >= 0 and Maze[row][col-1] == OPEN or Maze[row][col-1] == GOAL:
            isGoal = Maze[row][col-1] == GOAL
            leftNode = Node(col-1, row, ManhattanDistance(col-1, row, goalCol, goalRow), isGoal)
            graph.addNode(leftNode)
            graph.addEdge(node, leftNode)

            graphQueue.push(leftNode)

    return graph

def ManhattanDistance(x1, y1, x2, y2):
    dist = abs(x1 - x2) + abs(y1 - y2)
    return dist

class Queue:
    def __init__(self):
        self.list = []
    
    def push(self, thing):
        self.list.append(thing)

    def pop(self):
        return self.list.pop()

    def isEmpty(self):
        return len(self.list) == 0

    def toList(self):
        return self.list

    def __len__(self):
        return len(self.list)

class Stack:
    def __init__(self):
        self.list = []
    
    def push(self, thing):
        self.list.insert(0, thing)
    
    def pop(self):
        return self.list.pop()

    def isEmpty(self):
        return len(self.list) == 0

    def toList(self):
        return self.list

    def __len__(self):
        return len(self.list)

class Node:
    def __init__(self, col, row, cost, goal=False):
        self.col = col
        self.row = row
        self.goal = goal
        self.cost = cost

    def getCol(self):
        return self.col

    def getRow(self):
        return self.row

    def getCoord(self):
        return (self.col, self.row)

    def getCost(self):
        return self.cost

    def isGoal(self):
        return self.goal

    def __str__(self):
        temp = "ERROR"

        if self.goal:
            temp = "(G," + str(self.col) + "," + str(self.row) + ")"
        else:
            temp = "(" + str(self.col) + "," + str(self.row) + ")"
        
        return temp

class Edge:
    def __init__(self, nFrom, nTo):
        self.fromNode = nFrom
        self.toNode = nTo

    def isFrom(self):
        return self.fromNode

    def isTo(self):
        return self.toNode

    def __str__(self):
        return str(self.fromNode) + "->" + str(self.toNode)

class Graph:
    def __init__(self, sCol, sRow, gCol, gRow):
        self.mNodes = {}
        self.mEdges = defaultdict(list)
        self.startCol = sCol
        self.startRow = sRow
        self.goalCol = gCol
        self.goalRow = gRow

    def addNode(self, node):
        self.mNodes[node.getCol(),node.getRow()] = node

    def addEdge(self, nFrom, nTo):
        tempEdge = Edge(nFrom, nTo)

        self.mEdges[nFrom].append(tempEdge)
    
    def getSuccessors(self, node):
        successors = []
        for edge in self.mEdges[node]:
            successors.append(edge.isTo())

        return successors

    def getNode(self, col, row):
        return self.mNodes[col,row]

    def getRoot(self):
        return self.mNodes[self.startCol,self.startRow]

    def getGoal(self):
        return self.mNodes[self.goalCol,self.goalRow]
    
    def __str__(self):
        retStr = ""
        for node in self.mNodes.itervalues():
            successors = self.mEdges[node]
            retStr += "Node: " + str(node) + " Successors:\n"
            for edge in successors:
                retStr += str(edge) + "\n"

        return retStr

class Result:
    def __init__(self, path, maxQ, num, found, alg):
        self.mPath = path
        self.mMaxQueue = maxQ
        self.mLength = len(path)
        self.mFoundGoal = found
        self.mNumExpanded = num
        self.mAlgUsed = alg

    def getPath(self):
        return self.mPath

    def getMaxQueue(self):
        return self.mMaxQueue

    def getPathLength(self):
        return self.mLength

    def getAlgUsed(self):
        return self.mAlgUsed

    def foundGoal(self):
        return self.mFoundGoal

    def getNumExpanded(self):
        return self.mNumExpanded

    def pathString(self):
        pstring = ""

        for node in self.mPath:
            nodeString = ""
            if node.isGoal():
                nodeString = str(node)
            else:
                nodeString = str(node) + "->"
            
            pstring += nodeString

        return pstring


class ProblemScore:
    def __init__(self, results):
        self.mResults = results
        self.mResDict = {}
        self.mScores = {}

        for result in self.mResults:
            self.mScores[result.getAlgUsed()] = 0

        for res in results:
            self.mResDict[res.getAlgUsed()] = res

        self.__compareResults()

    def __compareResults(self):
        bestExp = sys.maxint
        bestPath = sys.maxint
        bestMaxQ = sys.maxint

        for result in self.mResults:
            if result.getNumExpanded() < bestExp:
                bestExp = result.getNumExpanded()

            if result.getPathLength() < bestPath:
                bestPath = result.getPathLength()
            
            if result.getMaxQueue() < bestMaxQ:
                bestMaxQ = result.getMaxQueue()

        for result in self.mResults:
            name = result.getAlgUsed()
        
            if result.foundGoal():
                self.mScores[name] += 4

            if result.getNumExpanded() == bestExp:
                self.mScores[name] += 1

            if result.getPathLength() == bestPath:
                self.mScores[name] += 1
            
            if result.getMaxQueue() == bestMaxQ:
                self.mScores[name] += 1

    def printScores(self):
        for res in self.mResults:
            alg = res.getAlgUsed()
            print alg + " got score: " + str(self.mScores[alg])

    def getScore(self, alg):
        if self.mScores.has_key(alg):
            return self.mScores[alg]
        else:
            return 0

    def GetScores(self):
        return self.mScores

    def GetResultDict(self):
        return self.mResDict
