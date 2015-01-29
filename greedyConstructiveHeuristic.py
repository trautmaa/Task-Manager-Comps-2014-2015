# Comps 2014
# Larkin Flodin, Avery Johnson, Maraki Ketema, 
# Abby Lewis, Will Schifeling, and  Alex Trautman


import itertools

import createTasksFromCsv
import helperFunctions

from Objects import Schedule, Route

def getBestInsertionOfTaskByTime(schedule, task):
    bestScore = 0
    bestSchedule = schedule
    for r in range(len(schedule.routeList)):
        route = schedule[r]
        for position in range(len(route) + 1):
            newRoute = insertTask(route, task, position, r)
            if newRoute == None: 
                pass
            else:
                newSchedule = copy.deepcopy(schedule)
                newSchedule exchangeRoute(newSchedule,newRoute, r)
                waitingTime = getWaitingTimeOfSchedule(newSchedule)  #Maybe this should be just route???
                extraDist = getExtraDistanceFromInsertion(route, position):
                score = getScore(task.priority, waitingTime, extraDist)
                if score >= bestScore:
                    bestSchedule = newSchedule
                    bestScore = score
                        
    return [score, bestSchedule, task]
          
def insertTask(route, task, position, routeIndex): 
    newRoute = copy.deepcopy(route)
    newRoute.taskList.insert(task, position)
    newRoute.endingTimes.insert(None, position)
    if isRouteFeasible(newRoute, routeIndex):
        return newRoute
    else: 
        return None 
    
def exchangeRoute(schedule,route, routeIndex): 
    schedule[routeIndex] = route
    return schedule
    

def getScore(priority, waitingTime, extraDist):
    return float(priority)/(waitingTime * extraDist) # For now, we can talk to DLN
    
    
def getExtraDistanceFromInsertion(route, position):
    if len(route) == 0:
        extraDist = 1
    elif position == 0:
        extraDist = getDistanceBetweenTasks(route[0], route[1])
    elif position == len(route):
        extraDist = getDistanceBetweenTasks(route[position-1], route[position])
    else: 
        extraDist = getDistanceBetweenTasks(route[postion-1], route[position + 1])
        extraDist -= getDistanceBetweenTasks(route[postion], route[position + 1])   
        extraDist -= getDistanceBetweenTasks(route[postion], route[position - 1])
    return extraDist

    
def returnScheduleInsertedWithBestTask(schedule, taskList):
    whichTaskToInsert = []
    for task in taskList:
        whichTaskToInsert.append(getBestInsertionOfTaskByTime(schedule, task))
    whichTaskToInsert = sorted(whichTaskToInsert, reverse = True)
    return whichTaskToInsert[0][1], whichTaskToInsert[0][2] 
        
def runGreedyConstructiveHeuristic(csvFile):
    taskList = createTasksFromCsv.getTaskList(csvFile)
    helperFunctions.preprocessTimeWindows(taskList) 
    
    schedule = Schedule()
    numDays = len(taskList[0].timeWindows)
    for day in range(numDays):
        route = Route()
        schedule.append(route)
    
    numTasks = len(taskList)
    for i in range(numTasks):
        schedule, taskToRemove = returnScheduleInsertedWithBestTask(schedule, taskList)
        taskList.remove(taskToRemove) #I don't know if I can actually do this....
        

def getWaitingTimeOfSchedule(schedule):
    pass




#isTaskInsertable(schedule, currentTask, dayEndings)     
#        if (isInsertable):
#            schedule.routeList[endingDay].taskList.insert(insertPosition, currentTask)
#            schedule.routeList[endingDay].endingTimes.insert(insertPosition, endingTime)

