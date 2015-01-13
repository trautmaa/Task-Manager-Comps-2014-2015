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
def printGreedyByOrder(csvFile, lengthOfDay):
	print runGreedyByOrder(csvFile, lengthOfDay)
	print	
	
'''
A function that will create a schedule based on ordering
all time windows in order of earliest ending and then
creating a schedule by repeatedly picking the first
task with an available time window from that ordering.
'''
def runGreedyByOrder(csvFile, lengthOfDay):
    taskList = createTasksFromCsv.getTaskList(csvFile)
    helperFunctions.preprocessTimeWindows(taskList)
    lastDay = 0
    for task in taskList:
        if len(task.timeWindows) > lastDay:
            lastDay = len(task.timeWindows) - 1

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

    schedule = Schedule()
    for day in range(lastDay + 1):
        schedule.append(Route())

    # the current index in the time windows list
    timeWindowIndex = 0

    while (timeWindowIndex < len(lastTimeWindowsList)):
        currentTask = taskList[lastTimeWindowsList[timeWindowIndex][1]]

        isInsertable, endingTime, endingDay, insertPosition = isTaskInsertable(schedule, currentTask, lengthOfDay)     
        if (isInsertable):
            schedule.routeList[endingDay].taskList.insert(insertPosition, currentTask)
            schedule.routeList[endingDay].endingTimes.insert(insertPosition, endingTime)                    
        timeWindowIndex += 1

    return schedule

def isTaskInsertable(schedule, task, lengthOfDay):
    for dayIndex, day in enumerate(task.timeWindows):
        currentRoute = schedule.routeList[dayIndex]
        for taskIndex in range(-1, len(currentRoute.taskList)):
            if (len(currentRoute.taskList) == 0): # no tasks scheduled on that day
                earliestPotentialStart = 0
                latestPotentialEnd = lengthOfDay * (dayIndex + 1)
            elif (taskIndex == -1): # try to insert before 1st existing task
                nextScheduledTask = currentRoute.taskList[0]
                nextScheduledTaskEnding = currentRoute.endingTimes[0]
                earliestPotentialStart = 0
                latestPotentialEnd = nextScheduledTaskEnding - nextScheduledTask.duration - \
                 helperFunctions.getDistanceBetweenTasks(task, nextScheduledTask)
            elif (taskIndex == len(currentRoute.taskList) - 1): # try to insert after last existing task
                scheduledTask = currentRoute.taskList[-1]
                scheduledTaskEnding = currentRoute.endingTimes[-1]
                earliestPotentialStart = scheduledTaskEnding + helperFunctions.getDistanceBetweenTasks(task, scheduledTask)
                latestPotentialEnd = lengthOfDay * (dayIndex + 1)
            else: # try to insert between 2 tasks
                scheduledTask = currentRoute.taskList[taskIndex]
                scheduledTaskEnding = currentRoute.endingTimes[taskIndex]
                nextScheduledTask = currentRoute.taskList[taskIndex + 1]
                nextScheduledTaskEnding = currentRoute.endingTimes[taskIndex + 1]
                earliestPotentialStart = scheduledTaskEnding + helperFunctions.getDistanceBetweenTasks(task, scheduledTask)
                latestPotentialEnd = nextScheduledTaskEnding - nextScheduledTask.duration - \
                 helperFunctions.getDistanceBetweenTasks(task, nextScheduledTask)

            for timeWindow in day:
                startTime = max(timeWindow[0], earliestPotentialStart)
                endTime = min(timeWindow[1], latestPotentialEnd)
                # print startTime
                # print endTime
                # print (task.duration <= endTime - startTime)
                if (task.duration <= endTime - startTime):
                    assert(startTime <= endTime)
                    # print
                    # print "task inserted with:"
                    # print "duration", task.duration
                    # print "ending time", task.duration + startTime
                    # print
                    return True, startTime + task.duration, dayIndex, taskIndex + 1
    return False, None, None, None

def main():
    print
    printGreedyByOrder("test.csv", 100)
    


if __name__ == '__main__':
    main()
    
