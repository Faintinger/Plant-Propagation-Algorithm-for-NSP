from PPA.Population import Population
import random
import math

class ComputeFitness(object):
    @staticmethod
    def compute(population, npop, taskSize, preferences, weigths, skillMatrix, shifts):
        costArr = population.getCost()
        prefArr = ComputeFitness.calculatePreferenceCoverage(population, preferences, shifts)
        #print(costArr);print(prefArr);
        if(len(skillMatrix) > 0):
            skillArr = ComputeFitness.calculateSkillCoverage(population, skillMatrix)
        nurseTotal = len(population.population[0])
        popSize = len(costArr)
        sortCostArr = costArr.copy()
        sortCostArr.sort()
        #print(str(costArr) + "|" + str(sortCostArr))
        lessCost = sortCostArr[0]
        totalCost = sortCostArr[popSize - 1]
        nMovs = []
        population.penalty = [0 for x in range(popSize)]
        for i in range(popSize):
            movs = 1
            gens = 1
            if(i < (popSize * 0.1)):
                movs = math.ceil(taskSize * 0.1 * random.random())
                gens = math.ceil(popSize * 0.9 * random.random())
                movs = 1 if (movs < 1) else movs
                gens = 1 if (gens < 1) else gens
            
            elif(i < (popSize * 0.3)):
                movs = math.ceil(taskSize * 0.3 * random.random())
                gens = math.ceil(popSize * 0.7 * random.random())
                movs = 1 if (movs < 1) else movs
                gens = 1 if (gens < 1) else gens
            
            else:
                movs = math.ceil(taskSize * 0.7 * random.random())
                gens = math.ceil(popSize * 0.1 * random.random())
                movs = 1 if (movs < 1) else movs
                gens = 1 if (gens < 1) else gens
            
            costPer = ((costArr[i] - lessCost) / (totalCost - lessCost)) if ((totalCost - lessCost) > 0) else ((costArr[i] - lessCost) / 1)
            prefPer = (100 - prefArr[i]) / 100
            population.penalty[i] = (float(weigths[0])*costPer) + (float(weigths[1])*prefPer)
            if(len(skillMatrix) > 0):
                skillPer = (100 - skillArr[i]) / 100
                population.penalty[i] = population.getPenalty(i) + (float(weigths[2])*skillPer)
                population.skillPerPopulation = skillArr
            nMovs.append([movs,gens])
        nMovs = [population,nMovs]
        return nMovs

    @staticmethod
    def resetBoundaries(population, npop):
        skill = len(population.skillPerPopulation) > 0
        newPopulation = Population()
        for i in range(npop):
            newPopulation.appendPopulation(population.get(i))
            newPopulation.costPerPopulation.append(population.costPerPopulation[i])
            newPopulation.penalty.append(population.penalty[i])
            newPopulation.preferencePerPopulation.append(population.preferencePerPopulation[i])
            if(skill):
                newPopulation.skillPerPopulation.append(population.skillPerPopulation[i])
        return newPopulation

    @staticmethod
    def calculateSkillCoverage(population, skillMatrix):
        h = len(skillMatrix)
        w = len(skillMatrix[0])
        totalCover = h*w
        popSkillCoverage = []
        popSize = population.getPopulationSize()
        for i in range(popSize):
            cover = 0
            skCover = population.getSkillCoverage(i,w)
            for d in range(h):
                for s in range(w):
                    if(skCover[d][s] >= skillMatrix[d][s]):
                        cover = cover + 1
                    else:
                        cover = cover + (skCover[d][s] / skillMatrix[d][s])
            cover = (cover / totalCover) * 100
            cover = 100 if cover > 100 else cover
            popSkillCoverage.append(cover)
        return popSkillCoverage

    @staticmethod
    def calculatePreferenceCoverage(population, preferences, shiftsNum):
        h = len(preferences)
        popPrefCoverage = []
        popSize = population.getPopulationSize()
        for i in range(popSize):
            cover = 0
            for n in range(h):
                nsCover = population.get(i)[n].getNurseScheduleShifts()
                w = len(nsCover)
                totalCover = h * w * shiftsNum
                for d in range(w):
                    cover = cover + preferences[n][d + (nsCover[d] - 1)]
            #cover = (1 - (cover / totalCover)) * 100 #smaller value the better
            cover = ((cover / totalCover)) * 100 #bigger value the better
            popPrefCoverage.append(cover)
        population.preferencePerPopulation = popPrefCoverage
        return popPrefCoverage