# Comps 2014
# Larkin Flodin, Avery Johnson, Maraki Ketema, 
# Abby Lewis, Will Schifeling, and  Alex Trautman

from helperFunctions import *
import greedyConstructiveHeuristic
import greedyByOrder
import greedyByPresentChoice
import bruteForce
import timedRandomIteration
import vns
import integerProgram

import time
import csv

import createTests
from writeToCsv import writeNTasks

# from taskManagerIntProg import runIntegerProgram

OUTPUT = [["Algorithm", "Time Ran", "Profit", "Test Name"]]
OUTPUTFILENAME = "TESTRESULTS.csv" 

def runAlreadyCreatedTestsForXTime(testList, timeLimit):    
#    runGreedies(testList)
#    runVNS(testList, timeLimit)
#    runTimedRandomIteration(testList, timeLimit)
    runTimedBruteForce(testList, timeLimit)
#    runIntegerProgram(testList, timeLimit)
#    
    outputOutput()

    
def runTimedRandomIteration(testList, timeLimit):
    for testName in testList:
        start = time.time()
        schedule = timedRandomIteration.randomlyPickBestScheduleUnderTime(testName, timeLimit)
        timeRan = time.time()-start
        addToOutput(schedule, timeRan, testName, "TRI")
        
def runTimedBruteForce(testList, timeLimit):
    for testName in testList:
        start = time.time()
        schedule = bruteForce.runBruteForceAlg(testName, timeLimit)###### THIS WONT WORK YET!!!!! 
        timeRan = time.time()-start
        addToOutput(schedule, timeRan, testName, "TBF")

def runIntegerProgram(testList, timeLimit):
    for testName in testList:
        start = time.time()
        schedule = integerProgram.runIntegerProgram(testName, timeLimit, 0)#?????????????
        timeRan = time.time()-start
        addToOutput(schedule, timeRan, testName, "IP")
    
def runVNS(testList, timeLimit):
    for testName in testList:
        start = time.time()
        schedule = vns.solve1(testName, timeLimit)[0]###### THIS WONT WORK YET!!!!!
        timeRan = time.time()-start
        addToOutput(schedule, timeRan, testName, "VNS")
        
    
def runGreedies(testList):
    greediesList = [greedyByOrder.runGreedyByOrder, greedyConstructiveHeuristic.runGreedyConstructiveHeuristic, greedyByPresentChoice.runGreedyByPresentChoice]
    orderings = [greedyByOrder.orderOptionalByDeadline, greedyByOrder.orderByPriorityOverAvailability, greedyByOrder.orderOptionalByDeadline]
    
    for i in range(len(greediesList)):
        if i == 0:
            for j in range(len(orderings)):
                for testName in testList:
                    start = time.time()
                    schedule = greediesList[i](testName, orderings[j])
                    timeRan = time.time()-start
                    addToOutput(schedule, timeRan, testName, (str(greediesList[i]) + str(orderings[j])))
        else:
            for testName in testList:
                start = time.time()
                schedule = greediesList[i](testName)
                timeRan = time.time()-start
                addToOutput(schedule, timeRan, testName, str(greediesList[i]))

    
def addToOutput(schedule, timeRan, testName, algorithm):
    profit = schedule.getProfit()
    OUTPUT.append([algorithm, timeRan, profit, testName])

def outputOutput():
    with open(OUTPUTFILENAME, 'wb') as f:
        writer = csv.writer(f)
        for row in OUTPUT:
            writer.writerow(row)

            
def main():
    runAlreadyCreatedTestsForXTime(["/Users/mrSchifeling/Desktop/Task-Manager-Comps-2014-2015/willSchedule.csv"], 120)
                                
                    
                    
        
        
        
#def runNComparisons(n):
#    totalOrderedDeadlineProfit, totalOrderedDeadlineTime = 0, 0
#    
#    totalOrderedPriorityProfit, totalOrderedPriorityTime = 0, 0
#    
#    totalOrderedAvailabilityPriorityProfit, totalOrderedAvailabilityPriorityTime = 0, 0
#    for i in range(n):
#        createTests.writeNTasks(inputSize, fileName)
#        
#        
#        greedyByDeadlineOrderSchedule = greedyByOrder.runGreedyByOrder(fileName, greedyByOrder.orderOptionalByDeadline)
#        greedyByPriorityOrderSchedule = greedyByOrder.runGreedyByOrder(fileName, greedyByOrder.orderByPriority)
#        greedyByPriorityAvailabilitySchedule = greedyByOrder.runGreedyByOrder(fileName, greedyByOrder.orderByPriorityOverAvailability)
#        print greedyByDeadlineOrderSchedule.getProfit()
#        totalOrderedDeadlineProfit += greedyByDeadlineOrderSchedule.getProfit()
#        totalOrderedPriorityProfit += greedyByPriorityOrderSchedule.getProfit()
#        totalOrderedAvailabilityPriorityProfit += greedyByPriorityAvailabilitySchedule.getProfit()
#        
#        
#    print "Average totalOrderedDeadlineProfit:" , str(totalOrderedDeadlineProfit/n)
#    print "Average totalOrderedPriorityProfit:" , str(totalOrderedPriorityProfit/n)
#    print "Average totalOrderedAvailabilityPriorityProfit:" , str(totalOrderedAvailabilityPriorityProfit/n)
        


#fileName = "testing.csv"
#inputSize = 50
#
#'''
#Prints the total number of tasks the algorithm with a particular name
#has scheduled, as well as the percentage of tasks it has scheduled.
#'''
#def printAlgResults(algName, totalTasks, possibleTasksCompleted, tasksCompleted, totalTime):
#	print algName, "has scheduled", tasksCompleted, "out of", \
#		possibleTasksCompleted, "or", \
#		(100.0 * tasksCompleted / possibleTasksCompleted), \
#		"percent of possible tasks."
#	if (totalTime != None):
#		print "This algorithm takes", (totalTime / (totalTasks / inputSize)), "seconds on average."
#
#'''
#Loops forever, repeatedly generating new inputs for the problem,
#solving them with all algorithms, and periodically printing
#updates on the aggregate numbers solved by each algorithm.
#'''
#def comparisonLoop():
#	inputsSeen = 0
#	totalTasksSeen = 0
#	tasksCompletedBrute = 0
#	tasksCompletedOrderDeadline = 0
#	tasksCompletedOrderRelease = 0
#	tasksCompletedChoiceStarting = 0
#	tasksCompletedChoiceCompletion = 0
#
#	tasksCompletedIntegerProgram = 0
#	bruteForceTime = 0
#	integerProgramTime = 0
#	while True:
#		inputsSeen += 1
#		totalTasksSeen = inputsSeen * inputSize
## 		writeNTasks(inputSize, fileName)
#		beforeTime = time()
#		tasksCompletedBrute += len(runBruteForceAlg(fileName))
#		bruteForceTime += time() - beforeTime
#		beforeTime = time()
## 		tasksCompletedIntegerProgram += len(runIntegerProgram(fileName))
## 		integerProgramTime += time() - beforeTime
#		tasksCompletedOrderRelease += len(runGreedyByOrder(fileName, orderByRelease))
#		tasksCompletedOrderDeadline += len(runGreedyByOrder(fileName, orderByDeadline))
#		tasksCompletedChoiceStarting += len(runGreedyByPresentChoice(fileName, orderByStartingTime))
#		tasksCompletedChoiceCompletion += len(runGreedyByPresentChoice(fileName, orderByEndingTime))
#		print inputsSeen, "inputs seen total, each of size", inputSize, "."
#		printAlgResults(
#			"Brute force", totalTasksSeen, tasksCompletedBrute, tasksCompletedBrute, bruteForceTime)
## 		printAlgResults(
## 			"Integer program", totalTasksSeen, tasksCompletedBrute, tasksCompletedIntegerProgram, integerProgramTime)
#		printAlgResults(
#			"Greedy by release date", totalTasksSeen, tasksCompletedBrute, tasksCompletedOrderRelease, None)
#		printAlgResults(
#			"Greedy by deadline", totalTasksSeen, tasksCompletedBrute, tasksCompletedOrderDeadline, None)
#		printAlgResults(
#			"Greedy by starting time", totalTasksSeen, tasksCompletedBrute, tasksCompletedChoiceStarting, None)
#		printAlgResults(
#			"Greedy by finish time", totalTasksSeen, tasksCompletedBrute, tasksCompletedChoiceCompletion, None)
#		print
#		if (tasksCompletedBrute != tasksCompletedIntegerProgram):
#			print
#			print "Integer program produced a non-optimal solution, halting comparison for debugging."
#			print
#
#            

#            
#            
#def getNumberOfRequiredAndOptionalTasks(schedule):
#    required, optional = 0, 0
#    for route in schedule:
#        for task in route:
#            if task.required == str(1):
#                required += 1
#            else:
#                optional += 1
#    return required, optional
            
            

if __name__ == '__main__':
	main()
