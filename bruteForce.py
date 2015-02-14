# Comps 2014
# Larkin Flodin, Avery Johnson, Maraki Ketema, 
# Abby Lewis, Will Schifeling, and  Alex Trautman

import itertools

import random
import createTasksFromCsv
import helperFunctions
import Objects
from vns import isFeasible
from vns import isBetterSchedule
import time

import datetime




def findBestScheduleWithTimeLimit(taskList, permutations, timeLimit):
    '''
    A function given a list of task objects and all the potential task permutations
    will create a schedule for each ordering and output one of the best schedules in the
    time it has that is has tried.
    '''
    start = time.time()
    helperFunctions.preprocessTimeWindows(taskList)
    bestSchedule = Objects.Schedule()
    for perm in permutations:
        newSchedule = helperFunctions.createOptimalSchedule(taskList, perm)     
        if isBetterSchedule(newSchedule, bestSchedule):
            bestSchedule = newSchedule
        if time.time()-start >= timeLimit:
            return bestSchedule

    
    return bestSchedule


'''
A function that returns all potential task permutations as a list.
It just takes a number of how many elements you want in your solution.
'''
def getAllPermutations(lengthOfPerms):
    permutations = [i for i in range(lengthOfPerms)]
    permutations = itertools.permutations(permutations, lengthOfPerms)

    return permutations




def runBruteForceAlgWithTimeLimit(csvFile, timeLimit):
    '''
    A function that will run our brute force algorithm to find the
    best schedule it can find in a certain timeLimit.
    '''
    objectList = createTasksFromCsv.getTaskList(csvFile)
    taskOrderings = getAllPermutations(len(objectList))
    bestSchedule = findBestScheduleWithTimeLimit(objectList, taskOrderings, timeLimit)
    return bestSchedule


'''
Prints the output of runBruteForceAlg in a more
detailed format.
'''
def printBruteForce(csvFile, timeLimit):
    schedule = runBruteForceAlgWithTimeLimit(csvFile, timeLimit)
    print schedule
    print schedule.getProfit()
    print
    print "profit is:"
    print schedule.getProfit()
    print

def main():
    print
    printBruteForce("little1.csv")
    print datetime.datetime.now()


if __name__ == '__main__':
    main()
    
    
    
