# Comps 2014
# Larkin Flodin, Avery Johnson, Maraki Ketema, 
# Abby Lewis, Will Schifeling, and  Alex Trautman

import itertools

import createTasksFromCsv
import helperFunctions

from Objects import Schedule, Route

'''
A function that prints the result of runGreedyByOrder
in a more detailed format.
'''
def printGreedyByOrder(csvFile):
	print runGreedyByOrder(csvFile)
	print	
	
'''
A function that will create a schedule based on ordering
all time windows in order of earliest ending and then
creating a schedule by repeatedly picking the first
task with an available time window from that ordering.
'''
def runGreedyByOrder(csvFile):
    taskList = createTasksFromCsv.getTaskList(csvFile)
    helperFunctions.preprocessTimeWindows(taskList)

    # create a list of tuples (time of latest time window ending, taskId)
    lastTimeWindowsList = []
    for task in taskList:
        latestTime = 0
        for day in task.timeWindows:
            for window in day:
                if window[1] >= latestTime:
                    latestTime = window[1]
        lastTimeWindowsList.append((latestTime, task.id))

    lastTimeWindowsList = sorted(lastTimeWindowsList, key=lambda timeIdTuple: timeIdTuple[0])
    taskOrdering = []
    for timeTaskTuple in lastTimeWindowsList:
        taskOrdering.append(timeTaskTuple[1])

    return helperFunctions.createOptimalSchedule(taskList, taskOrdering)

def main():
    print
    printGreedyByOrder("test.csv")
    


if __name__ == '__main__':
    main()
    
