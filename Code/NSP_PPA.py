from NS.File import File
from PPA.PPA import PPA
from PPA.Population import Population
import sys, os, traceback, decimal
def main():
    debugFile = File("logger.txt")
    resultsFile = File("results.txt")
    npop = input("Insert population number: ")
    path = input("Insert File Path: ")
    ngen = input("Insert the quantity of population generations to process: ")
    nruns = input("Insert the run times of the algorithm: ")
    print("Insert the percentages of the next categories * the sum must be 1 *")
    sum = 0
    weigths = []
    try:
        while(sum != 1.0):
            if(sum != 0):
                print("The percentages do not sum 1")
            costPer = decimal.Decimal(input("Insert the percentage of cost weight: "))
            prefPer = decimal.Decimal(input("Insert the percentage of preferences weight: "))
            skillPer = decimal.Decimal(input("Insert the percentage of skill weight *Optional*: "))
            sum = costPer + prefPer + skillPer
            print(str(costPer) + " " + str(prefPer) + " " + str(skillPer) + str(sum))
            weigths = [costPer, prefPer, skillPer]

        x0 = 0
        nrmax = 0
        npop = int(npop)
        ngen = int(ngen)
        nruns = int(nruns)
        f = File(path)
        f.readFile()
        f.loadFile()
        fResults = Population()
        
        for i in range(nruns):
            results = PPA.plantPropagationAlgorithm(f, x0, ngen, npop, nrmax, weigths)
            fResults.appendPopulation(results.get(0))
        
        debugFile.writeInFile("Best Populations ------------ \n")
        resultsFile.writeInFile("Best Populations ------------ \n")
        fResults = PPA.sort(fResults,npop,f,weigths)
        fResults.printPopulation(debugFile)
        fResults.printPopulation(resultsFile)
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)
        print(traceback.format_exc())

if __name__ == '__main__':
    main()
