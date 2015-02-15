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
import pulseOPTW

import time
import csv
import os
import createTests

OUTPUT = [["Algorithm", "Time Ran", "Profit", "Number of Total Tasks", "Number of Required Tasks", "Number of Optional Tasks", "Total Waiting Time", "Total WorkingTime", "Total Distance Traveled", "Test Name"]]
OUTPUTFILENAME = "TESTRESULTS.csv" 


'''
runs all the algorithms you want to with a timeLimit and a list
of test names.  It then outputs the results.
'''
def runAlreadyCreatedTestsForXTime(testList, timeLimit):    
    for test in testList:
        #runGreedies(testList)
        runPulse([test], timeLimit)
        runVNS([test], timeLimit)
        #runTimedRandomIteration(testList, timeLimit)
        #runTimedBruteForce(testList, timeLimit)
        #runIntegerProgram(testList, timeLimit)


    outputOutput()


    
'''
Runs the timed random iteration on our list of testFiles.
'''    
def runTimedRandomIteration(testList, timeLimit):
    for testName in testList:
        start = time.time()
        schedule = timedRandomIteration.randomlyPickBestScheduleUnderTime(testName, timeLimit)
        timeRan = time.time()-start
        addToOutput(schedule, timeRan, testName, "TRI")

        
'''
Runs the timed version of brute force on our list of testFiles.
'''
def runTimedBruteForce(testList, timeLimit):
    for testName in testList:
        start = time.time()
        schedule = bruteForce.runBruteForceAlgWithTimeLimit(testName, timeLimit)###### THIS WONT WORK YET!!!!! 
        timeRan = time.time()-start
        addToOutput(schedule, timeRan, testName, "TBF")

        
'''
Runs the timed version of the integerProgram on our list of testFiles.
'''
def runIntegerProgram(testList, timeLimit):
    for testName in testList:
        start = time.time()
        schedule = integerProgram.runIntegerProgram(testName, timeLimit, 0)#?????????????
        timeRan = time.time()-start
        addToOutput(schedule, timeRan, testName, "IP")
        

def runPulse(testList, timeLimit):
    for testName in testList:
        start = time.time()
        pulseOPTW.setTimes()
        schedule = pulseOPTW.solve(testName) 
        timeRan = time.time()-start
        addToOutput(schedule, timeRan, testName, "Pulse")

'''
Runs vns on our list of testFiles.
'''
def runVNS(testList, timeLimit):
    for testName in testList:
        start = time.time()
        schedule = vns.solve(testName, timeLimit)[0]###### THIS WONT WORK YET!!!!!
        timeRan = time.time()-start
        addToOutput(schedule, timeRan, testName, "VNS")
        
'''
Runs all greedies on our list of testFiles.
'''
def runGreedies(testList):
    greediesList = [greedyByOrder.runGreedyByOrder,  greedyByPresentChoice.runGreedyByPresentChoice]
    orderings = [greedyByOrder.orderOptionalByDeadline, greedyByOrder.orderForReleaseTasks, greedyByOrder.orderByPriorityOverAvailability, greedyByOrder.orderOptionalByDeadline]
    
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
                addToOutput(schedule, timeRan, testName, "GPC")

'''
This function just adds data associated with a result of an
algorithm on a test file to OUTPUT, which will later be written to
a csv file.  More data may should be added but I don't know what???
'''
def addToOutput(schedule, timeRan, testName, algorithm):
    profit = schedule.getProfit()
    numRequiredTasks = schedule.getNumRequired()
    numOptionalTasks = schedule.getNumOptional()
    numTotalTasks = numOptionalTasks + numRequiredTasks
    waitingTime = schedule.getWaitingTime()
    workingTime = schedule.getWorkingTime()
    distanceTraveled = schedule.getDistanceTraveled()
    OUTPUT.append([algorithm, timeRan, profit, numTotalTasks, numRequiredTasks, numOptionalTasks, waitingTime, workingTime, distanceTraveled, testName])

    
'''
Once we have ran all algorithms on all test cases, we can output
the results to a csv.
'''
def outputOutput():
    with open(OUTPUTFILENAME, 'wb') as f:
        writer = csv.writer(f)
        for row in OUTPUT:
            writer.writerow(row)

def getFiles(n):
    testList = []
    for i in range(n):
        testList.append(str(os.getcwd())+"/Testing Folder/testing" +str(i)+".csv")
    return testList
        
def main():
    testList = getFiles(10)
    runAlreadyCreatedTestsForXTime(testList, 10)
                                
if __name__ == '__main__':
	main()
                    