from random import *
from Utility import *

class GeneticAlgorithm:
    def __init__(self, numGenerations, scores, numAlg):
        self.mNumGens = numGenerations
        self.mAlgScores = scores
        self.mNumAlgorithms = numAlg

    def createInitalPop(self, numInitPop):
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
        CurrentPopulation = self.createInitalPop(4)

        for i in range(self.mNumGens):

            children = self.GenerateChildren(CurrentPopulation)

            for child in children:
                CurrentPopulation.append(child)

            CurrentPopulation = self.TrimPopulation(CurrentPopulation)

        return self.GeneticAlgorithmResult(self.getBestIndividuals(CurrentPopulation))

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

            if chance > 0.05:
                if individual[i]:
                    individual[i] = False
                else:
                    individual[i] = True

        return individual

    def TrimPopulation(self, population):
        return population[:4]

    def getBestIndividuals(self, population):
        return population[0]

    def GeneticAlgorithmResult(self, individuals):
        return str(individuals)