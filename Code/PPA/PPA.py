from PPA.Population import Population
from PPA.ComputeFitness import ComputeFitness
from NS.File import File
import numpy as np
import sys, os, traceback
import math
import copy


class PPA(object):

    @staticmethod
    def plantPropagationAlgorithm(file, x0, ngen, npop, nrmax, weigths):
        #New Population
        debugFile = File("logger.txt")
        debugFile.writeInFile("Read File ------------ \n")
        debugFile.writeInFile(file.file + "\n")
        #Generate the first population
        population = Population.newPopulation(file, npop)
        failed = population[1]
        debugFile.writeInFile("Failed to create a Population ------------ " + str(failed) + "\n")
        population = population[0]
        gen = 0
        debugFile.writeInFile("New Population ------------ \n")
        population.printPopulation(debugFile)
        #While till ngen populations are created
        while gen < ngen:
            #Compute the fitness of the population
            fitness = ComputeFitness.compute(population, npop, file.getTasksQuantity(),file.getPreferences(), weigths, file.getSkillMatrix(), file.getShiftsPerDay())
            fitness = fitness[1]
            for p in range(len(fitness)):
                #For each population get the fitness of population p
                nr = fitness[p][1]
                r = 0
                #Make nr number of movements
                while r < nr:
                    tempP = PPA.reorderSchedule(population.get(p), fitness[p][0])
                    p1 = Population()
                    p1.appendPopulation(tempP)
                    #If movements are valid add the population
                    if (tempP is not None) & (Population.isValidCoverage(p1.getCoverage(file.getDaysOfSchedule(), file.getShiftsPerDay(), 0), file.getCoverage())): 
                        population.appendPopulation(tempP)
                        r = r + 1
            #Sort the population by penalty
            population = Population.sort(ComputeFitness.compute(population, npop, file.getTasksQuantity(),file.getPreferences(), weigths, file.getSkillMatrix(), file.getShiftsPerDay())[0])
            debugFile.writeInFile("Generation Population ------------ " + str(gen + 1) + "\n")
            print("Generation Population ------------ " + str(gen + 1) + "\n")
            #Keep just the npop number of populations inside of the list
            population = ComputeFitness.resetBoundaries(population, npop)
            population.printPopulation(debugFile)
            gen = gen + 1  
        debugFile.writeInFile("Final Population ------------ \n")
        population.printPopulation(debugFile)
        #return the npop number of schedules
        return population

    @staticmethod
    def reorderSchedule(nursePopulation, nMovs):
        nursePop = copy.deepcopy(nursePopulation)
        nurseQuant = len(nursePop)
        rndNums = np.random.randint(0,nurseQuant,nMovs)
        rndNewAssign = np.random.randint(0,nurseQuant,nMovs)
        taskDebug = ""
        try:
            for i in range(nMovs):
                days = len(nursePop[rndNums[i]].schedule)
                cD = np.random.randint(0,days,1)[0] #math.floor(days * np.random.rand(1)[0])
                if nursePop[rndNums[i]].workDays[cD] == 1:
                    tasksQuant = len(nursePop[rndNums[i]].schedule[cD])
                    if tasksQuant > 0:
                        tD = np.random.randint(0,tasksQuant,1)[0] #math.floor(tasksQuant * np.random.rand(1)[0])
                        taskSwitch = nursePop[rndNums[i]].schedule[cD][tD]
                        taskOrig = nursePop[rndNewAssign[i]].schedule[cD][tD]
                        newShift = np.random.randint(1,nursePop[rndNums[i]].maxShifts+1,1)[0]
                        taskDebug = str(cD) + "day - task: " + str(tD) + " | " + str(tasksQuant) + "- Task switch " + taskSwitch.toString() + " New Shift: " + str(newShift)
                        origShift = taskSwitch.shiftTurn
                        while not (nursePop[rndNums[i]].isAValidShift(taskSwitch)):
                            newShift = np.random.randint(1,nursePop[rndNums[i]].maxShifts+1,1)[0]
                            taskSwitch.shiftTurn = newShift
                        nursePop[rndNums[i]].schedule[cD][tD].shiftTurn = newShift
                        #nursePop[rndNums[i]].schedule[cD][tD] = taskOrig
                        #nursePop[rndNewAssign[i]].schedule[cD][tD] = taskSwitch
                        # Check if the task can be assigned to the new nurse
                        # Switch task
                        #nursePop[rndNums[i]].RemoveTask(cD, taskSwitch)
                        #nursePop[rndNewAssign[i]].RemoveTask(cD, taskOrig)
                        #if(nursePop[rndNums[i]].isAssignable(taskOrig)):
                        #    nursePop[rndNewAssign[i]].AssignTask(taskSwitch)
                        #    nursePop[rndNums[i]].AssignTask(taskOrig)
                        #else:
                        #    nursePop[rndNums[i]].AssignTask(taskSwitch)
                        #    nursePop[rndNewAssign[i]].AssignTask(taskOrig)
            return nursePop
               
        except Exception as e:
            print("failed mov " + taskDebug + "\n")
            #exc_type, exc_obj, exc_tb = sys.exc_info()
            #fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            #print(exc_type, fname, exc_tb.tb_lineno)
            print(traceback.format_exc())

            return None

    @staticmethod
    def sort(population, npop, file, weigths):
        population = ComputeFitness.compute(population, npop, file.getTasksQuantity(),file.getPreferences(), weigths, file.getSkillMatrix(), file.getShiftsPerDay())[0]
        population = Population.sort(population)
        return population
        