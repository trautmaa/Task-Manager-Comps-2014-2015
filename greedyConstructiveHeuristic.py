# Comps 2014
# Larkin Flodin, Avery Johnson, Maraki Ketema, 
# Abby Lewis, Will Schifeling, and  Alex Trautman


import itertools

import createTasksFromCsv
import helperFunctions
import copy

from Objects import Schedule, Route
from vns import isRouteFeasible


'''
For a particular unscheduled task, attempts to calculate a score measuring
how beneficial inserting that task would be in each position in the schedule, based on
priority, waiting time, and added distance.

@param schedule: current partially created schedule
@param task: the task being checked
@return: tuple containing score, new schedule with insertion, and task
'''
def getBestInsertionOfTaskByTime(schedule, task):
    bestScore = 0
    bestSchedule = schedule
    # for each route in the schedule 
    for index, route in enumerate(schedule.routeList):
        # position relative to tasks that are already in the route...
        for position in range(len(route) + 1):
            # inserts task into route. Returns None if task insertion was infeasible
            newRoute = insertTask(route, task, position, index)
            if newRoute != None:
                newSchedule = copy.deepcopy(schedule)
                # inserting new route into the position of the old route
                newSchedule[index] = newRoute
                # calculates waiting time of the schedule (with the addition of new route)
                waitingTime = getWaitingTimeOfSchedule(newSchedule)  # Maybe this should be just route???
                # calculates distance values for the new schedule
                extraDist = getExtraDistanceFromInsertion(newRoute, position)
                score = getScore(task.priority, waitingTime, extraDist)
                if score >= bestScore:
                    bestSchedule = newSchedule
                    bestScore = score

    return (bestScore, bestSchedule, task)
          
'''
Attempts to insert a task between two other tasks in a schedule.

@param route: the route to add the task to
@param task: the task to add
@param position: the relative position at which to add the task
@param: routeIndex: the index of the route in the schedule
@return: the new route with the task inserted, or None if the insertion is infeasible
'''
def insertTask(route, task, position, routeIndex): 
    newRoute = copy.deepcopy(route)
    newRoute.taskList.insert(position, task)
    # running isFeasible will set the ending time
    newRoute.endingTimes.insert(position, None)
    # Returns None if not feasible
    newRoute = isRouteFeasible(newRoute, routeIndex)[0]
    print newRoute
    return newRoute

'''
Returns the score by which potential task insertions are compared.

@param priority: the priority of the task
@param waitingTime: the total waiting time of the new schedule
@param extraDist: the extra distance the insertion causes
@return: the (float) score of the insertion
'''
def getScore(priority, waitingTime, extraDist):
    priorityWeighting = .05 # placeholder, should compute based on priority per time unit of available tasks or something
    return float(priority) - (priorityWeighting * (waitingTime + extraDist)) # For now, we can talk to DLN  
    
'''
Calculates the extra distance inserting a task will incur relative to the
old schedule.

@param route: the route the task is being added to
@param position: the relative position of the insertion
@return: the extra distance resulting from the insertion of the task
'''
def getExtraDistanceFromInsertion(route, position):
    if len(route) == 0:
        extraDist = 0
    elif position == 0:
        # before first task
        extraDist = getDistanceBetweenTasks(route[0], route[1])
    elif position == len(route):
        # after last task
        extraDist = getDistanceBetweenTasks(route[position - 1], route[position])
    else:
        # triangle inequality
        extraDist = getDistanceBetweenTasks(route[position], route[position + 1])
        extraDist += getDistanceBetweenTasks(route[position], route[position - 1])
        extraDist -= getDistanceBetweenTasks(route[position - 1], route[position + 1])
    return extraDist

'''
Calculates the total amount of waiting time in a schedule.

@param schedule: the schedule to calculate waiting time for
@return: the total waiting time
'''
def getWaitingTimeOfSchedule(schedule):
    totalWaitingTime = 0
    for route in schedule:
        totalWaitingTime += getWaitingTimeOfRoute(route)
    return totalWaitingTime

'''
Calculates the total waiting time for a particular route.

@param route: the route to calculate waiting time for
@return: the total waiting time of the route
'''
def getWaitingTimeOfRoute(route):
    if len(route) == 0:
        return 0
    else:
        # accounts for time before first task starts
        totalWaitingTime = route.endingTimes[0] - route[0].duration
        for i in range(len(route) - 1):
            # add waiting time between task i and task i + 1
            firstTask = route[i]
            endingTimeOfFirstTask = route.endingTimes[i]
            secondTask = route[i + 1]
            startingTimeOfSecondTask = route.endingTimes[i + 1] - secondTask.duration
            distanceBetweenTasks = getDistanceBetweenTasks(route[i], route[i + 1])
            taskWaitTime = startingTimeOfSecondTask - endingTimeOfFirstTask - distanceBetweenTasks
            totalWaitingTime += taskWaitTime
        return totalWaitingTime

'''
Iterates over each possible task and evaluates the best possible location to
insert each one, then returns the schedule and task that are the best of those.

@param schedule: the partially created schedule
@param taskList: the list of unscheduled tasks
@return: tuple (schedule, task) of the new schedule with the given task inserted
'''
def returnScheduleInsertedWithBestTask(schedule, taskList):
    whichTaskToInsert = []
    for task in taskList:
        # appends a tuple of form (score, schedule, task)
        whichTaskToInsert.append(getBestInsertionOfTaskByTime(schedule, task))
    whichTaskToInsert = sorted(whichTaskToInsert, key = lambda scoreTuple: scoreTuple[0], reverse = True)
    bestSchedule, bestTask = whichTaskToInsert[0][1], whichTaskToInsert[0][2]
    return bestSchedule, bestTask
        
'''
Runs the constructive heuristic for a given test file and returns the resulting
schedule.

@param csvFile: the test file to run
@return: the completed schedule
'''
def runGreedyConstructiveHeuristic(csvFile):
    taskList = createTasksFromCsv.getTaskList(csvFile)
    helperFunctions.preprocessTimeWindows(taskList) 
    
    schedule = Schedule()
    numDays = len(taskList[0].timeWindows)
    for day in range(numDays):
        route = Route()
        schedule.append(route)
    
    for task in taskList:
        schedule, taskToRemove = returnScheduleInsertedWithBestTask(schedule, taskList)
        taskList.remove(taskToRemove) # I don't know if I can actually do this....
    return schedule
        
'''
Runs the constructive heuristic and prints the schedule.
'''
def main():
    schedule = runGreedyConstructiveHeuristic("test.csv")
    print
    print schedule
    print
    print "priority is: ", schedule.getProfit()
    print

if __name__ == '__main__':
    main()

