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

OUTPUT = [["Algorithm", "Time Ran", "Profit", "Number Tasks Scheduled", "Number of Required Tasks Schedules", "Number of Optional Tasks Scheduled", 
           "Total Waiting Time", "Total Working Time", "Total Distance Traveled", 
           "Test Name", "Number of Available Tasks", "Number of Days", "Average Duration of the Tasks", 
           "Average Number of Time Windows Per Task", "Average Length of All Time Windows", "Number of Available Release Tasks"]]
OUTPUTFILENAME = "TESTRESULTS" 


'''
runs all the algorithms you want to with a timeLimit and a list
of test names.  It then outputs the results.
'''
def runAlreadyCreatedTestsForXTime(testList, timeLimit): 
    start = time.time()
    constant = 1
    for test in testList:
        print test, "test", "\n"
        runGreedies([test])
        # runPulse([test], timeLimit)
        runVNS([test], timeLimit)
        runTimedRandomIteration([test], timeLimit)
        # runTimedBruteForce([test], timeLimit)
        runIntegerProgram([test], timeLimit)
        if (time.time() - start) >= 3600 * constant: # Outputs every hour...
            constant += 1
            outputOutput(time.time()-start)


    outputOutput("LAST OUTPUT")


    
'''
Runs the timed random iteration on our list of testFiles.
'''    
def runTimedRandomIteration(testList, timeLimit):
    for testName in testList:
        start = time.time()
        schedule = timedRandomIteration.randomlyPickBestScheduleUnderTime(testName, timeLimit)
        timeRan = time.time() - start
        addToOutput(schedule, timeRan, testName, "TRI")

        
'''
Runs the timed version of brute force on our list of testFiles.
'''
def runTimedBruteForce(testList, timeLimit):
    for testName in testList:
        start = time.time()
        schedule = bruteForce.runBruteForceAlgWithTimeLimit(testName, timeLimit)
        timeRan = time.time() - start
        addToOutput(schedule, timeRan, testName, "TBF")

        
'''
Runs the timed version of the integerProgram on our list of testFiles.
'''
def runIntegerProgram(testList, timeLimit):
    for testName in testList:
        start = time.time()
        schedule = integerProgram.runIntegerProgram(testName, timeLimit, 0)[0]
        timeRan = time.time() - start
        addToOutput(schedule, timeRan, testName, "IP")
        

def runPulse(testList, timeLimit):
    for testName in testList:
        start = time.time()
        pulseOPTW.setTimes(timeLimit)
        schedule = pulseOPTW.solve(testName) 
        timeRan = time.time() - start
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
    orderings = [greedyByOrder.orderOptionalByDeadline, greedyByOrder.orderForReleaseTasks, greedyByOrder.orderByPriorityOverAvailability, greedyByOrder.orderByPriority]
    
    for i in range(len(greediesList)):
        if i == 0:
            for j in range(len(orderings)):
                for testName in testList:
                    start = time.time()
                    schedule = greediesList[i](testName, orderings[j])
                    timeRan = time.time()-start
                    if j == 0:
                        algName = "GBOOBD"
                    elif j == 1: 
                        algName = "GBOFRT"
                    elif j == 2:
                        algName = "GBOPOA"
                    else:
                        algName = "GBOOBP"
                    addToOutput(schedule, timeRan, testName, algName)
        else:
            for testName in testList:
                start = time.time()
                schedule = greediesList[i](testName)
                timeRan = time.time()-start
                addToOutput(schedule, timeRan, testName, "GPC")

def getInfoFromSchedule(taskList):
    totalDuration, totalNumTimeWindows, totalTimeWindowLength, numReleaseTasks = 0, 0, 0, 0
    for task in taskList:
        totalDuration += int(task.duration)
        for day in task.timeWindows:
            totalNumTimeWindows += len(day)
            for window in day:
                totalTimeWindowLength += int(window[1]) - int(window[0])
        if len(task.dependencyTasks) != 0:
            numReleaseTasks += 1
    numTasks = len(taskList)
    avgDuration = totalDuration/float(numTasks)
    avgNumTimeWindows = totalNumTimeWindows/float(numTasks)
    avgTimeWindowLength = totalTimeWindowLength/totalNumTimeWindows
    return avgDuration, avgNumTimeWindows, avgTimeWindowLength, numReleaseTasks
        
                
                
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
    taskList = createTasksFromCsv.getTaskList(testName)
    numTasks, numDays = len(taskList), len(taskList[0].timeWindows)
    avgDuration, avgNumTimeWindows, avgLengthTimeWindow, numReleaseTasks = getInfoFromSchedule(taskList)
    OUTPUT.append([algorithm, timeRan, profit, numTotalTasks, numRequiredTasks, numOptionalTasks, waitingTime, workingTime, distanceTraveled, testName[-20:], numTasks, numDays, avgDuration, avgNumTimeWindows, avgLengthTimeWindow, numReleaseTasks])

    
'''
Once we have ran all algorithms on all test cases, we can output
the results to a csv.
'''
def outputOutput(timeStamp):
    outputFile = str(os.getcwd()) + "/Results Folder/" + OUTPUTFILENAME + str(timeStamp) + ".csv"
    with open(outputFile, 'wb') as f:
        writer = csv.writer(f)
        for row in OUTPUT:
            writer.writerow(row)

            
            
def sortAndRenameFiles(testList):
    sortedTestList = []
    for i in range(10):  #### UNDER THE ASSUMPTION THAT WE WONT HAVE MORE THAN 10 OF ONE TEST
        for test in testList:
            if str(i) in test:
                sortedTestList.append(test) 
    for i in range(len(sortedTestList)):
        sortedTestList[i] = str(os.getcwd()) + "/Testing Folder/" + sortedTestList[i]
    return sortedTestList
            

def getFiles():
    testList = []
    path = str(os.getcwd()) + "/Testing Folder/"
    testList = os.listdir(path)
    #testList.remove('.DS_Store')
    testList = sortAndRenameFiles(testList)
    return testList
        
def main():
    testList = getFiles()
    print testList
    runAlreadyCreatedTestsForXTime(testList, 300)
                                
if __name__ == '__main__':
	main()
                    
