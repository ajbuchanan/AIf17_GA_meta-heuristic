from random import *
from Utility import *

class GeneticAlgorithm:
    def __init__(self, numGenerations, scores, results):
        self.mNumGens = numGenerations
        self.mAlgScores = scores
        self.mNumAlgorithms = len(scores)
        self.mResults = results

    def CreateInitalPop(self, numInitPop):
        print "Creating Inital Population"
        currentPop = []
        for i in range(numInitPop):
            individual = []
            for j in range(self.mNumAlgorithms):
                x = random()

                if x > 0.5:
                    individual.append(True)
                else:
                    individual.append(False)
            
            currentPop.append(individual)

        return currentPop

    def PerformAlgorithm(self):
        print "Starting Algorithm"
        CurrentPopulation = self.CreateInitalPop(4)

        for i in range(self.mNumGens):
            children = self.GenerateChildren(CurrentPopulation)

            for child in children:
                CurrentPopulation.append(child)

            CurrentPopulation = self.TrimPopulation(CurrentPopulation)

        return self.GeneticAlgorithmResult(CurrentPopulation)

    def GenerateChildren(self, population):
        children = []
        items = [0, 1, 2, 3]

        parents = sample(items, 4)

        parent1 = parents[0]
        parent2 = parents[1]
        parent3 = parents[2]
        parent4 = parents[3]

        c1, c2 = self.Crossover(population[parent1], population[parent2])
        c3, c4 = self.Crossover(population[parent3], population[parent4])

        children.append(c1)
        children.append(c2)
        children.append(c3)
        children.append(c4)

        return children

    def Crossover(self, p1, p2):
        cross1 = randint(0, len(p1)-2)
        cross2 = randint(cross1, len(p1)-1)

        c1 = []
        c2 = []

        c1.extend(p1[:cross1])
        c1.extend(p2[cross1:cross2])
        c1.extend(p1[cross2:])

        c2.extend(p2[:cross1])
        c2.extend(p1[cross1:cross2])
        c2.extend(p2[cross2:])

        c1 = self.Mutate(c1)
        c2 = self.Mutate(c2)

        return c1, c2

    def Mutate(self, individual):
        for i in range(len(individual)):
            chance = random()

            if chance < 0.05:
                #print "Mutation!"
                if individual[i]:
                    individual[i] = False
                else:
                    individual[i] = True

        return individual

    def TrimPopulation(self, population):
        retList = []
        for i in range(self.mNumAlgorithms):
            bestKey = 0
            bestScore = 0
            currentKey = 0

            for pop in population:
                score = self.getIndividualsScore(pop)
                if score > bestScore:
                    bestScore = score
                    bestKey = currentKey
                currentKey += 1

            retList.append(population[bestKey])
            del population[bestKey]

        return retList

    def getIndividualsScore(self, individual):
        score = 0.0
        num = 0
        if individual[0]:
            score += self.mAlgScores["AS"]
            num += 1

        if individual[1]:
            score += self.mAlgScores["BFS"]
            num += 1

        if individual[2]:
            score += self.mAlgScores["DFS"]
            num += 1

        if individual[3]:
            score += self.mAlgScores["UCS"]
            num += 1

        if num > 0:
            score = score / num

        return score

    def GeneticAlgorithmResult(self, population):
        individual = self.GetBestOne(population)
        res = GAResult()
        if individual[0]:
            res.addAlgorithm("AS")
            res.addPath("AS", self.mResults["AS"].getPath())

        if individual[1]:
            res.addAlgorithm("BFS")
            res.addPath("BFS", self.mResults["BFS"].getPath())

        if individual[2]:
            res.addAlgorithm("DFS")
            res.addPath("DFS", self.mResults["DFS"].getPath())

        if individual[3]:
            res.addAlgorithm("UCS")
            res.addPath("UCS", self.mResults["UCS"].getPath())

        return res

    def getNumTrue(self, individual):
        numTrue = 0

        if individual[0]:
            numTrue += 1
            
        if individual[1]:
            numTrue += 1
            
        if individual[2]:
            numTrue += 1
            
        if individual[3]:
            numTrue += 1

        return numTrue

    def GetBestOne(self, population):
        bestScore = 0
        bestKey = 0
        bestNumTrue = 0
        currentKey = 0

        for pop in population:
            score = self.getIndividualsScore(pop)
            if score > bestScore:
                numTrue = self.getNumTrue(pop)
                if bestScore > 0 and numTrue > bestNumTrue:
                    bestScore = score
                    bestKey = currentKey
                    bestNumTrue = numTrue
            
            currentKey += 1

        return population[bestKey]

class GAResult:
    def __init__(self):
        self._bestPath = {}
        self._algorithms = []

    def addAlgorithm(self, alg):
        self._algorithms.append(alg)

    def addPath(self, alg, path):
        self._bestPath[alg] = path

    def getPaths(self):
        return self._bestPath

    def getAlgorithms(self):
        return self._algorithms

    def printResult(self):
        print self._algorithms