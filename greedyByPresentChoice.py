# Comps 2014
# Larkin Flodin, Avery Johnson, Maraki Ketema, 
# Abby Lewis, Will Schifeling, and  Alex Trautman

import itertools
import createTasksFromCsv
import helperFunctions


'''
A function that given a csvFile and the function used to determine which
task we want to do next, this algorithm makes a schedule by picking
one job at a time using a greedy rule that accounts for the current
location and time.
'''
def runGreedyByPresentChoice(csvFile, orderFunction):
    taskList = createTasksFromCsv.getTaskList(csvFile)
    schedule = selectSchedule(taskList, orderFunction)
    return schedule

'''
A function that prints the result of runGreedyByPresentChoice
in a more detailed way.
'''
def printGreedyByPresentChoice(csvFile, orderFunction):
    taskList, taskOrdering = runGreedyByPresentChoice(csvFile, orderFunction)
    schedule = helperFunctions.createSchedule(taskOrdering, taskList)
    print schedule
    print

'''
Refer to runGreedyByPresentChoice.
Given a method and a task list, returns a greedily selected schedule.
'''
def selectSchedule(taskList, orderFunction):
    taskOrdering = []
    originalTaskList = [item for item in taskList]
    schedule, presentLocation, presentTime = [], (0, 0), 0 # presentLocation is arbitrary.
    task = getNextTask(
        presentTime, presentLocation, taskList, orderFunction)
    taskOrdering.append(originalTaskList.index(task))
    while (task != None):
        schedule.append(task)
        presentTime = helperFunctions.getEndingTime(presentLocation, presentTime, task) 
        presentLocation = helperFunctions.getCoords(task)
        del taskList[taskList.index(task)]
        task = getNextTask(
            presentTime, presentLocation, taskList, orderFunction)
        if task != None:
            taskOrdering.append(originalTaskList.index(task))
    return originalTaskList, taskOrdering

'''
A function that given a present time and location along with a tasks list, and
a method that will return the next task that can be started or finished depending on the method.
'''
def getNextTask(startingTime, startingLocation, remainingTasksList, orderFunction):
    finishableTasks = []
    for task in remainingTasksList:
        finishable, endingTime = helperFunctions.isFinishableTask(
            task, startingLocation, startingTime)
        if finishable:
            finishableTasks.append(task)
    if len(finishableTasks) == 0:
        return None
    finishableTasks = orderFunction(finishableTasks, startingLocation, startingTime)
    return finishableTasks[0]
    
    

def main():
    print
    printGreedyByPresentChoice("test.csv", helperFunctions.orderByStartingTime)
    printGreedyByPresentChoice("test.csv", helperFunctions.orderByEndingTime)
    


if __name__ == '__main__':
    main()
