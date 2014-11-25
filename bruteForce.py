# Comps 2014
# Larkin Flodin, Avery Johnson, Maraki Ketema, 
# Abby Lewis, Will Schifeling, and  Alex Trautman

import itertools

from createTasksFromCsv import *
from writeToCsv import *
from helperFunctions import *

taskFeatures = ['xCoord', 'yCoord', 'releaseTime', 'duration', 'deadline']


'''
A function given a list of task objects and all the potential ways
to order the tasks will create a schedule for each ordering
and output one of the schedules with the most tasks scheduled.
'''
def findMaximalSchedule(objectList, taskOrderings):
    maxSchedule = []
    for taskOrdering in taskOrderings:
        newSchedule = createSchedule(taskOrdering, objectList)
        if len(newSchedule) > len(maxSchedule):
            maxSchedule = newSchedule
    return maxSchedule


'''
A function that returns all potential orderings of tasks as a list.
It just takes a number of how many elements you want to be permutated.
'''
def getAllPermutations(lengthOfPerms):
    permutations = [i for i in range(lengthOfPerms)]
    permutations = list(itertools.permutations(permutations, lengthOfPerms))
    return permutations


'''
A function that will run our brute force algorithm to find the
best schedule.
'''
def runBruteForceAlg(csvFile):
    objectList = getTaskList(csvFile)
    taskOrderings = getAllPermutations(len(objectList))
    bestSchedule = findMaximalSchedule(objectList, taskOrderings)
    return bestSchedule

'''
Prints the output of runBruteForceAlg in a more
detailed format.
'''
def printBruteForce(csvFile):
    schedule = runBruteForceAlg(csvFile)
    printSchedule(schedule)
    print

def main():
    print
    printBruteForce("test.csv")


if __name__ == '__main__':
    main()
    
    
    
