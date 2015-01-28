# Comps 2014
# Larkin Flodin, Avery Johnson, Maraki Ketema, 
# Abby Lewis, Will Schifeling, and  Alex Trautman

import sys
import createTasksFromCsv
import helperFunctions
import time
import random

defaultTimeLimit = 15

'''
Reads a list of tasks from a file, and tries to create schedules using
randomly selected permutations of tasks. Stops and
returns the best schedule after numSeconds seconds have passed.
'''
def randomlyPickBestScheduleUnderTime(csvFile, numSeconds):
    taskList = createTasksFromCsv.getTaskList(csvFile)
    helperFunctions.preprocessTimeWindows(taskList)
    
    bestSchedule, bestProfit = None, 0
    taskIds = [task.id for task in taskList]
    
    start = time.time()
    while time.time() < (start + numSeconds):
        # Get a random permutation
        orderToTry = random.sample(taskIds, len(taskIds))
        schedule = helperFunctions.createOptimalSchedule(taskList, orderToTry)
        
        if schedule.getProfit() > bestProfit:
            bestProfit = schedule.getProfit()
            bestSchedule = schedule
    return bestSchedule

def processCommandLineArgs(args):
    if len(sys.argv) > 1:
        try:
            timeLimit = int(sys.argv[1])
        except ValueError:
            print "command line argument not an integer"
            exit()
        return timeLimit
    else:
        return defaultTimeLimit
    
def main():
    timeLimit = processCommandLineArgs(sys.argv)
    schedule = randomlyPickBestScheduleUnderTime("toptw0.csv", timeLimit)
    print schedule
    print
    print "priority is: "
    print schedule.getProfit()
    
if __name__ == "__main__":
    main()