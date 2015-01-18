# Comps 2014
# Larkin Flodin, Avery Johnson, Maraki Ketema, 
# Abby Lewis, Will Schifeling, and  Alex Trautman

import itertools

import createTasksFromCsv
import helperFunctions
import Objects
from vns import isFeasible
from vns import isBetterSchedule

import datetime

'''
A function given a list of task objects and all the potential task permutations
will create a schedule for each ordering and output one of the schedules with 
the most tasks scheduled.
'''
def findBestSchedule(taskList, permutations):
    bestSchedule = Objects.Schedule()
    for perm in permutations:
        newSchedule = helperFunctions.createOptimalSchedule(taskList, perm)
        #bestScheduleSize = sum(len(route) for route in bestSchedule.routeList)
        #newScheduleSize = sum(len(route) for route in newSchedule.routeList)
        #bestScheduleSize = getScheduleDuration(taskList, bestSchedule)        
        if isBetterSchedule(newSchedule, bestSchedule):
        	bestSchedule = newSchedule
        	print '1'
        '''feasSchedule = isFeasible(taskList, newSchedule)
        if feasSchedule != None:
        	if isBetterSchedule(feasSchedule, bestSchedule):
        		bestSchedule = feasSchedule'''
    return bestSchedule


'''
A function that returns all potential task permutations as a list.
It just takes a number of how many elements you want in your solution.
'''
def getAllPermutations(lengthOfPerms):
    permutations = [i for i in range(lengthOfPerms)]
    #permutations = list(itertools.permutations(permutations, lengthOfPerms))
    permutations = itertools.permutations(permutations, lengthOfPerms)

    return permutations


'''
A function that will run our brute force algorithm to find the
best schedule.
'''
def runBruteForceAlg(csvFile):
    objectList = createTasksFromCsv.getTaskList(csvFile)
    taskOrderings = getAllPermutations(len(objectList))
    bestSchedule = findBestSchedule(objectList, taskOrderings)
    return bestSchedule



'''
Prints the output of runBruteForceAlg in a more
detailed format.
'''
def printBruteForce(csvFile):
    schedule = runBruteForceAlg(csvFile)
    print schedule
    print

def main():
    print
    printBruteForce("test11.csv")
    print datetime.datetime.now()


if __name__ == '__main__':
    main()
    
    
    
