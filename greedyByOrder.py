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
def printGreedyByOrder(csvFile, orderMethod):
    schedule = runGreedyByOrder(csvFile, orderMethod)
    #print schedule
    print "The", str(orderMethod), "gave a profit of", str(schedule.getProfit())

def orderByPriorityOverAvailability(timeWindowsAndPriorities):
    timeWindowsAndPriorities = sorted(timeWindowsAndPriorities, key=lambda timeIdTuple: timeIdTuple[3], reverse = True)
    return timeWindowsAndPriorities
    
def orderByPriority(timeWindowsAndPriorities):
	timeWindowsAndPriorities = sorted(timeWindowsAndPriorities, key=lambda timeIdTuple: timeIdTuple[0])
	timeWindowsAndPriorities = sorted(timeWindowsAndPriorities, key=lambda timeIdTuple: timeIdTuple[1], reverse = True)
	return timeWindowsAndPriorities

def orderOptionalByDeadline(timeWindowsAndPriorities):
	maxPriority = max(timeWindowsAndPriorities, key= lambda timeWindowsAndPriorities:timeWindowsAndPriorities[1])[1]
	mandatoryTasks = []
	optionalTasks = []
	for tuple in timeWindowsAndPriorities:
		if tuple[1] == maxPriority:
			mandatoryTasks.append(tuple)
		else:
			optionalTasks.append(tuple)
	
	mandatoryTasks = sorted(mandatoryTasks, key=lambda timeIdTuple: timeIdTuple[0]) 
	optionalTasks = sorted(optionalTasks, key=lambda timeIdTuple: timeIdTuple[0])
	orderedTasks = mandatoryTasks + optionalTasks
	return orderedTasks

'''
A function that will create a schedule based on ordering
all time windows in order of earliest ending and then
creating a schedule by repeatedly picking the first
task with an available time window from that ordering.
'''
def runGreedyByOrder(csvFile,orderMethod):
    taskList = createTasksFromCsv.getTaskList(csvFile)
    helperFunctions.preprocessTimeWindows(taskList)

    # create a list of tuples (time of latest time window ending, taskId)
    timeWindowsAndPriorities = []
  
    for task in taskList:
        latestTime = 0
        for day in task.timeWindows:
            for window in day:
                if window[1] >= latestTime:
                    latestTime = window[1]
        timeWindowsAndPriorities.append((latestTime, task.priority, task.id, float(task.priority)/max(float(task.getNumTimeWindows()), 1)))
		
	# sorting by deadline	
    
    timeWindowsAndPriorities = orderMethod(timeWindowsAndPriorities)
    # sorting by priority
    
    taskOrdering = []
    for timeTaskTuple in timeWindowsAndPriorities:
        taskOrdering.append(timeTaskTuple[2])

    return helperFunctions.createOptimalSchedule(taskList, taskOrdering)

def main():
    print "priority"
    printGreedyByOrder("test50.csv", orderByPriority)
    print "deadline"
    printGreedyByOrder("test50.csv", orderOptionalByDeadline)
    print "priority/availability"
    printGreedyByOrder("test50.csv", orderByPriorityOverAvailability)
    
    


if __name__ == '__main__':
    main()
    
