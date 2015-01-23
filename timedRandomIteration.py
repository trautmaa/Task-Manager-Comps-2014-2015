# Comps 2014
# Larkin Flodin, Avery Johnson, Maraki Ketema, 
# Abby Lewis, Will Schifeling, and  Alex Trautman


import itertools

import createTasksFromCsv
import helperFunctions
import time
import random

from Objects import Schedule, Route

def randomlyPickBestScheduleUnderTime(csvFile, numSeconds):
    taskList = createTasksFromCsv.getTaskList(csvFile)
    helperFunctions.preprocessTimeWindows(taskList)
    
    bestSchedule, bestProfit = None, 0
    numTasks = len(taskList)
    taskIds = []
    for i in range(numTasks):
        taskIds.append(taskList[i].id)
    
    start = time.time()
    while time.time()< (start + numSeconds):
        orderToTry = random.sample(taskIds, len(taskIds))
        schedule = helperFunctions.createOptimalSchedule(taskList, orderToTry)
        
        if schedule.getProfit() > bestProfit:
            bestProfit = schedule.getProfit()
            bestSchedule = schedule
    return bestSchedule
    
def main():
    print randomlyPickBestScheduleUnderTime("test.csv", 20)
    
    
main()