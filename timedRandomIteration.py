# Comps 2014
# Larkin Flodin, Avery Johnson, Maraki Ketema, 
# Abby Lewis, Will Schifeling, and  Alex Trautman


import createTasksFromCsv
import helperFunctions
import time
import random

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
    
def main():
    schedule = randomlyPickBestScheduleUnderTime("test.csv", 120)
    print schedule
    print
    print "priority is: "
    print schedule.getProfit()
    
if __name__ == "__main__":
    main()