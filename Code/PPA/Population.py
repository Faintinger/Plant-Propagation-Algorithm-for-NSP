from NS.Task import Task
from NS.Nurse import Nurse
from NS.Shift import Shift
from NS.Schedule import Schedule
import numpy as np
import math, random
class Population(object):
    def __init__(self):
         self.population = []
         self.costPerPopulation = []
         self.penalty = []
         self.preferencePerPopulation = []
         self.skillPerPopulation = []

    def get(self, i):
        return self.population[i]

    def getPenalty(self, i):
        return self.penalty[i]

    def getPopulationSize(self):
        return len(self.population)

    def appendPopulation(self, population):
       self.population.append(population)

    def getCost(self):
        self.costPerPopulation = []
        size = len(self.population)
        for i in range(size):
            popSize = len(self.population[i])
            costPop = 0
            for j in range(popSize):
                costPop += self.population[i][j].CalculateCost()
            self.costPerPopulation.append(costPop)
        return self.costPerPopulation

    def printPopulation(self, f):
        popSize = self.getPopulationSize()
        popString = ""
        for i in range(popSize):
            n = len(self.population[i])
            for j in range(n):
                popString += self.get(i)[j].getScheduleString()
            if(len(self.costPerPopulation) > 0):
                popString += "Cost = " + str(self.costPerPopulation[i]) + "\n"
            if(len(self.penalty) > 0):
                popString += "Coverage = " + str((1 - self.penalty[i]) * 100) + " Penalty = " + str(self.penalty[i]) + "\n"
                popString += "Preferences = " + str(self.preferencePerPopulation[i]) + "\n"
                popString += "Skill = " + str(self.skillPerPopulation[i]) + "\n" if(len(self.skillPerPopulation) > 0) else ""
        f.writeInFile(popString)

    def getCoverage(self, days, shifts, pos):
        w , h = shifts, days
        cover = [[0 for x in range(w)] for y in range(h)] 
        size = len(self.population)
        if pos < size:
            popSize = len(self.population[pos])
            for j in range(popSize):
                cv = self.population[pos][j].getCoverage()
                for d in range(days):
                    cover[d][cv[d].shiftTurn - 1] = cover[d][cv[d].shiftTurn - 1] + 1
        return cover

    def getSkillCoverage(self, pos, skillMax):
        size = len(self.population)
        if pos < size:
            popSize = len(self.population[pos])
            days = len(self.population[pos][0].workDays)
            skills = skillMax
            w , h = skills, days
            cover = [[0 for x in range(w)] for y in range(h)] 
            for j in range(popSize):
                sk = self.population[pos][j].skill
                sh = self.population[pos][j].getNurseScheduleShifts()
                for d in range(days):
                    if sh[d] != self.population[pos][j].maxShifts:
                        cover[d][sk - 1] = cover[d][sk - 1] + 1
        return cover

    @staticmethod
    def newPopulation(file, npop):
        n = file.getNurseQuantity()
        t = file.getTasksQuantity()
        schedule = file.getDaysOfSchedule()
        shiftsDay = file.getShiftsPerDay()
        shiftHours = file.getHoursPerShift()
        tasks = file.getTasks()
        nurses = file.getNurses()
        na = 0 #Number of nurse to be assigned
        population = Population()
        failedCant = 0
        while population.getPopulationSize() < npop:
            rndNums = np.random.randint(0,n,t)
            #rndShifts = np.random.randint(1,shiftsDay+1,t)
            print(rndNums)
            nursePop = file.getNurses()
            failed = False
            for i in range(t):
                #rndNum = Math.floor(Random.unif(0,1) * n)
                assigned = False
                na = i
                err = 0
                while not assigned:
                    tasks[i].shiftTurn = np.random.randint(1,shiftsDay+1,1)[0] #int(rndShifts[i]) #math.ceil(shiftsDay * random.random())
                    #rndNums = math.floor(n * np.random.rand())
                    #rndNums = rndNums if (rndNums < n) else (rndNums - 1)
                    if na >= t:
                        failed = True
                        i = t
                        break
                    if nursePop[rndNums[na]].isAssignable(tasks[i]):
                        #Assign task to the nurse
                        nursePop[rndNums[na]].AssignTask(tasks[i])
                        print("GEN " + str(population.getPopulationSize()) + " Assigned: to " + str(rndNums[na]) + " task: " + tasks[i].id + " shift: " + str(tasks[i].shiftTurn))
                        na = 0
                        assigned = True
                    else:
                        na = err
                        err = err + 1
                   
            if not failed:
                population.appendPopulation(nursePop)
                pos = population.getPopulationSize() - 1
                cover = population.getCoverage(schedule,shiftsDay, pos)
                if not Population.isValidCoverage(cover, file.getCoverage()):
                    del population.population[pos]
            else:
                failedCant = failedCant + 1
        return [population, failedCant]

    @staticmethod
    def sort(population):
        length = population.getPopulationSize()
        newPop = Population()
        for i in range(length):
            assigned = False
            for j in range(newPop.getPopulationSize()):
                if population.penalty[i] < newPop.penalty[j]:
                    newPop.population.insert(j, population.population[i])
                    newPop.penalty.insert(j, population.penalty[i])
                    newPop.costPerPopulation.insert(j, population.costPerPopulation[i])
                    newPop.preferencePerPopulation.insert(j, population.preferencePerPopulation[i])
                    if len(population.skillPerPopulation) > 0:
                        newPop.skillPerPopulation.insert(j, population.skillPerPopulation[i])
                    assigned = True
                    break
            if not assigned:
                newPop.appendPopulation(population.population[i])
                newPop.costPerPopulation.append(population.costPerPopulation[i])
                newPop.penalty.append(population.penalty[i])
                newPop.preferencePerPopulation.append(population.preferencePerPopulation[i])
                if len(population.skillPerPopulation) > 0:
                        newPop.skillPerPopulation.append(population.skillPerPopulation[i])
        return newPop

    @staticmethod
    def isValidCoverage(populationCoverage, coverage):
        #print(populationCoverage)
        #print(coverage)
        covers = True
        days = len(populationCoverage)
        shifts = len(populationCoverage[0])
        for i in range(days):
            for j in range(shifts):
                if(populationCoverage[i][j] < coverage[i][j]):
                    i = days + 1
                    j = shifts + 1
                    covers = False
                    return covers
        return covers