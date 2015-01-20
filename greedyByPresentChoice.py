# Comps 2014
# Larkin Flodin, Avery Johnson, Maraki Ketema, 
# Abby Lewis, Will Schifeling, and  Alex Trautman

import itertools
import createTasksFromCsv
import helperFunctions

from Objects import Schedule, Route


'''
A function that given a csvFile and the function used to determine which
task we want to do next, this algorithm makes a schedule by picking
one job at a time using a greedy rule that accounts for the current
location and time.
'''
def runGreedyByPresentChoice(csvFile):
    taskList = createTasksFromCsv.getTaskList(csvFile)
    schedule = makeSchedule(taskList)
    return schedule

'''
A function that prints the result of runGreedyByPresentChoice
in a more detailed way.
'''
def printGreedyByPresentChoice(csvFile):
    schedule = runGreedyByPresentChoice(csvFile)
    print schedule
    print
    print "profit is:"
    print schedule.getProfit()

'''
Refer to runGreedyByPresentChoice.
Given a task list, returns a greedily selected schedule.
'''
def makeSchedule(taskList):
    helperFunctions.preprocessTimeWindows(taskList)
    schedule = Schedule()
    lastDay = len(taskList[0].timeWindows)
    for day in range(lastDay):
        schedule.append(Route())

    lastTimeWindowEndings = [0 for i in range(lastDay + 1)]
    for task in taskList:
        for index, day in enumerate(task.timeWindows):
            for timeWindow in day:
                if timeWindow[1] > lastTimeWindowEndings[index]:
                    lastTimeWindowEndings[index] = timeWindow[1]

    insertionSuccesful = True
    while insertionSuccesful:
        insertionSuccesful = False
        bestTaskInfo = (None, None, None, None)
        bestTask = None
        for task in taskList:
            taskInfo = helperFunctions.isTaskInsertable(schedule, task, lastTimeWindowEndings)
            # if task can be finished earliest
            if (taskInfo[2] != None and (bestTaskInfo[2] == None or taskInfo[2] < bestTaskInfo[2])):
                bestTaskInfo = taskInfo
                bestTask = task
        if (bestTaskInfo != None and bestTaskInfo[2] != None):
            insertionSuccesful = True
            isInsertable, endingTime, endingDay, insertPosition = bestTaskInfo
            schedule.routeList[endingDay].taskList.insert(insertPosition, bestTask)
            schedule.routeList[endingDay].endingTimes.insert(insertPosition, endingTime)
            for index, task in enumerate(taskList):
                if (task.id == bestTask.id):
                    taskList.pop(index)
    return schedule

def main():
    print
    printGreedyByPresentChoice("test.csv")
    


if __name__ == '__main__':
    main()
