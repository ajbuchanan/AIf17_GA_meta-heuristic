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

    node = Node(startCol, startRow)
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
            downNode = Node(col, row+1, isGoal)
            graph.addNode(downNode)
            graph.addEdge(node, downNode)

            graphQueue.push(downNode)

        # Look Up
        if row-1 >= 0 and Maze[row-1][col] == OPEN or Maze[row-1][col] == GOAL:
            isGoal = Maze[row-1][col] == GOAL
            upNode = Node(col, row-1)
            graph.addNode(upNode)
            graph.addEdge(node, upNode)

            graphQueue.push(upNode)

        # Look Right
        if col+1 < BOARDSIZE and Maze[row][col+1] == OPEN or Maze[row][col+1] == GOAL:
            isGoal = Maze[row][col+1] == GOAL
            rightNode = Node(col+1, row, isGoal)
            graph.addNode(rightNode)
            graph.addEdge(node, rightNode)

            graphQueue.push(rightNode)
            
        # Look left
        if col-1 >= 0 and Maze[row][col-1] == OPEN or Maze[row][col-1] == GOAL:
            isGoal = Maze[row][col-1] == GOAL
            leftNode = Node(col-1, row, isGoal)
            graph.addNode(leftNode)
            graph.addEdge(node, leftNode)

            graphQueue.push(leftNode)

    return graph

class Queue:
    def __init__(self):
        self.list = []
    
    def push(self, thing):
        self.list.append(thing)

    def pop(self):
        return self.list.pop()

    def isEmpty(self):
        return len(self.list) == 0

class Stack:
    def __init__(self):
        self.list = []
    
    def push(self, thing):
        self.list.insert(0, thing)
    
    def pop(self):
        return self.list.pop()

    def isEmpty(self):
        return len(self.list) == 0

class Node:
    def __init__(self, col, row, goal=False):
        self.col = col
        self.row = row
        self.goal = goal

    def getCol(self):
        return self.col

    def getRow(self):
        return self.row

    def getCoord(self):
        return (self.col, self.row)

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
    
    def __str__(self):
        retStr = ""
        for node in self.mNodes.itervalues():
            successors = self.mEdges[node]
            retStr += "Node: " + str(node) + " Successors:\n"
            for edge in successors:
                retStr += str(edge) + "\n"

        return retStr