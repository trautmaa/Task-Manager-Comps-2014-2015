# Comps 2014
# Larkin Flodin, Avery Johnson, Maraki Ketema, 
# Abby Lewis, Will Schifeling, and  Alex Trautman

import createTasksFromCsv, math, Objects

'''
A function given two task objects will return the euclidean distance
between them. I should check if **.5 is faster than math.sqrt()?
'''
def getDistanceBetweenTasks(taskA, taskB):
    return getDistanceBetweenCoords(getCoords(taskA), getCoords(taskB))


'''
A function that returns the distance between 2 tuple coordinates.
'''
def getDistanceBetweenCoords(locationA, locationB):
    return int(math.ceil(((locationA[0] - locationB[0]) ** 2 + (locationA[1] - locationB[1]) ** 2) ** 0.5))

'''
A function that returns a tuple of a task's coordinates.
'''
def getCoords(task):
    return (task.x, task.y)

def addAllTasksToSched(sched, taskList):
    for task in taskList:
        if task.id not in sched:
            sched += task
    return sched

'''
Given a list of tasks, returns them in reverse deadline order. It's a terrible
schedule and therefore perfect for testing VNS.
'''
def orderByStupid(taskList):
    taskList = sorted(taskList, key=lambda task: task.deadline)
    taskList.reverse()
    return taskList

'''
A function that will output a task list in a semi-readable fashion.
Help from http://stackoverflow.com/questions/5084743/how-to-print-pretty-string-output-in-python
'''
def printSchedule(schedule):
    currentTime = 0
    lastLocation = (0, 0)
    template = "{0:10}{1:10}{2:25}{3:15}{4:15}{5:15}{6:15}" # column widths: 8, 10, 15, 7, 10, 10, 10
    print template.format("Start", "Finish", "Task Name", "Location", "Release", "Deadline", "TravelTimeFromPrevious")
    for i, task in enumerate(schedule):
        startingTime = getStartingTimeOfNextTask(
            currentTime, lastLocation, getCoords(task), task.releaseTime)
        finishingTime = startingTime + task.duration
        if i == 0:
            print template.format(str(startingTime)[0:6], str(finishingTime)[0:6], str(task.id)[0:20], str(getCoords(task)), str(task.releaseTime)[0:4], str(task.deadline)[0:4], str(getDistanceBetweenCoords(lastLocation, getCoords(task)))[0:4])
        elif i != (len(schedule) - 1):
            print template.format(str(startingTime)[0:6], str(finishingTime)[0:6], str(task.id)[0:20], str(getCoords(task)), str(task.releaseTime)[0:4], str(task.deadline)[0:4], str(getDistanceBetweenTasks(task, schedule[i -1]))[0:4])
        currentTime = finishingTime
        lastLocation = getCoords(task)

'''
For each task in the taskList, make sure the time windows do not occur before the release time
or after the deadlines
'''
def preprocessTimeWindows(taskList):
    for task in taskList:
        for day in task.timeWindows:
            tw = 0
            while tw < len(day):
                if day[tw][1] < task.releaseTime or day[tw][0] > task.deadline:
                    day.remove(day[tw])
                    break
                if day[tw][0] < task.releaseTime:
                    day[tw] = (task.releaseTime, day[tw][1])
                if day[tw][1] > task.deadline:
                    day[tw] = (day[tw][0], task.deadline)
                tw += 1
                
                  
def printRouteJourney(route):
    if len(route) == 0:
        return
    for t in range(len(route) - 1):
         task = route[t]
         nextTask = route[t + 1]
         print "doing task", task.id, ": ", route.endingTimes[t] - task.duration, "to", route.endingTimes[t], "task duration: ", task.duration
         dist = getDistanceBetweenTasks(task, nextTask)
         print "traveling from", task.x, task.y, "at", route.endingTimes[t], "to", nextTask.x, nextTask.y, "at", route.endingTimes[t] + dist
    t = len(route) - 1
    task = route[t]
    print "doing task", task.id, ": ", route.endingTimes[t] - task.duration, "to", route.endingTimes[t]
    print "\n"
              
def printScheduleJourney(sched):
    for r in range(len(sched)):
        route = sched[r]
        print "day", r
        printRouteJourney(route)

'''
A function that will write n tasks to a csv file.  It uses
generateTask to create the task to write. Right now the
constraints for generateTask are hard coded but that can 
be changed.  The name of the csv file is returned.
''' 
def writeTasks(csvFile, schedule):
    taskList = []
    taskFeatures = ['xCoord', 'yCoord', 'releaseTime', 'duration', 'deadline', 'priority', 'required', 'timeWindows']
    with open(csvFile, 'wb') as f:
        writer = csv.writer(f)
        writer.writerow(taskFeatures)
        for r in range(len(schedule)):
            route = schedule[r]
            for t in range(len(schedule[r])):
                task = []
                task.append(route[t].x)
                task.append(route[t].y)
                task.append(route[t].releaseTime)
                task.append(route[t].duration)
                task.append(route[t].deadline)
                task.append(route[t].priority)
                task.append(route[t].required)
                task.append(route[t].timeWindows)
                taskList.append(task)
            taskList.append([])
        print "taskList", taskList
        for task in taskList:
            writer.writerow(task)
    return csvFile


''' Given a list of tasks and an ordering on the tasks (a list of integers),
schedules whichever tasks are possible to schedule
from that ordering and returns that schedule. We believe (?) this is
an optimal schedule for that ordering.'''
def createOptimalSchedule(taskList, taskOrdering):
    lastDay = len(taskList[0].timeWindows)

    # Create a list with the integer of the latest time anything could be scheduled
    # in any particular day. Used as a proxy for the end of the day.
    dayEndings = [0 for i in range(lastDay + 1)]
    for task in taskList:
        for index, day in enumerate(task.timeWindows):
            for timeWindow in day:
                if timeWindow[1] > dayEndings[index]:
                    dayEndings[index] = timeWindow[1]

    schedule = Objects.Schedule()
    for day in range(lastDay):
        schedule.append(Objects.Route())

    # the current index in the time windows list
    timeWindowIndex = 0

    while (timeWindowIndex < len(taskOrdering)): ### maybe this will work...
        currentTask = taskList[taskOrdering[timeWindowIndex]]
        
        isInsertable, endingTime, endingDay, insertPosition = isTaskInsertable(schedule, currentTask, dayEndings, taskList)
        #print currentTask, isInsertable
        if (isInsertable):
            schedule.routeList[endingDay].taskList.insert(insertPosition, currentTask)
            schedule.routeList[endingDay].endingTimes.insert(insertPosition, endingTime)                    
        timeWindowIndex += 1

    return schedule


def areDependencyTasksInSchedule(schedule, task, taskList):
    latestRoute, latestPosition = -1, 0
    for taskId in task.dependencyTasks:
        task = taskList[int(taskId)]
        included = False
        for i in range(len(schedule)):
            if task in schedule[i]:
                included = True
                if i > latestRoute:
                    latestRoute = i
                    if schedule[i].taskList.index(task) > latestPosition:
                        latestPosition = schedule[i].taskList.index(task)
        if not included:
            return False, None, None
    return True, latestRoute, latestPosition

    


''' Given a partial schedule, a task, and a list containing the endings of
the latest time windows for each day,
returns False if the task is not insertable, and if it is returns
True, the (earliest) ending time of that task, the (earliest) day on which it can be scheduled,
and the position in the schedule it should be inserted.'''
def isTaskInsertable(schedule, task, dayEndings, taskList):
    dependenciesInSchedule, startingRoute, startingPosition = areDependencyTasksInSchedule(schedule, task, taskList)
    if not dependenciesInSchedule:
        return False, None, None, None
    for dayIndex in range(startingRoute, len(schedule)):
        if not dayIndex == startingRoute:
            startingPosition = -1
        dayTimeWindows = task.timeWindows[dayIndex]
        currentRoute = schedule.routeList[dayIndex]
        for taskIndex in range(startingPosition, len(currentRoute.taskList)):
            if (len(currentRoute.taskList) == 0): # no tasks scheduled on that day
                earliestPotentialStart = 0
                latestPotentialEnd = dayEndings[dayIndex]
            elif (taskIndex == -1): # try to insert before 1st existing task
                nextScheduledTask = currentRoute.taskList[0]
                nextScheduledTaskEnding = currentRoute.endingTimes[0]
                earliestPotentialStart = 0
                latestPotentialEnd = nextScheduledTaskEnding - nextScheduledTask.duration - \
                getDistanceBetweenTasks(task, nextScheduledTask)
            elif (taskIndex == len(currentRoute.taskList) - 1): # try to insert after last existing task
                scheduledTask = currentRoute.taskList[-1]
                scheduledTaskEnding = currentRoute.endingTimes[-1]
                earliestPotentialStart = scheduledTaskEnding + getDistanceBetweenTasks(task, scheduledTask)
                latestPotentialEnd = dayEndings[dayIndex]
            else: # try to insert between 2 tasks
                scheduledTask = currentRoute.taskList[taskIndex]
                scheduledTaskEnding = currentRoute.endingTimes[taskIndex]
                nextScheduledTask = currentRoute.taskList[taskIndex + 1]
                nextScheduledTaskEnding = currentRoute.endingTimes[taskIndex + 1]
                earliestPotentialStart = scheduledTaskEnding + getDistanceBetweenTasks(task, scheduledTask)
                latestPotentialEnd = nextScheduledTaskEnding - nextScheduledTask.duration - \
                getDistanceBetweenTasks(task, nextScheduledTask)

            for timeWindow in dayTimeWindows:
                startTime = max(timeWindow[0], earliestPotentialStart)
                endTime = min(timeWindow[1], latestPotentialEnd)
                if (task.duration <= endTime - startTime):
                    assert(startTime <= endTime)
                    return True, startTime + task.duration, dayIndex, taskIndex + 1
    return False, None, None, None
    

def main():
    taskList = createTasksFromCsv.getTaskList("test.csv")
    preprocessTimeWindows(taskList)   

if __name__ == "__main__":
    main()
        
