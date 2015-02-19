# Comps 2014
# Larkin Flodin, Avery Johnson, Maraki Ketema, 
# Abby Lewis, Will Schifeling, and  Alex Trautman

import csv
import time
from copy import deepcopy

import random
import copy

taskFeatures = ['xCoord', 'yCoord', 'releaseTime', 'duration', 'deadline', 'priority', 'required', 'timeWindows', 'dependencyTasks']

dayLength = 1440

'''
Sets the priority of a task to a random integer between 1 and priority.
If a task is required, the priority is set to -1 as a placeholder and then
updated in setRequiredOfTask.
'''
def setPriorityOfTask(task, priority, isRequired):
    if isRequired:
        task.append(-1)
    else:
        task.append(random.randint(1, priority))
                   
def setRequiredOfTask(task):
    if task[-1] == -1:
        task.append(1)
    else:
        task.append(0)
        

def setDependencies(taskList, numDependencies):
    changingTaskList = deepcopy(taskList)
    dependencies = []
    for i in range(numDependencies):
        dependency = []
        dependency = random.sample(changingTaskList, 2)
        for task in dependency:
            changingTaskList.remove(task)
        dependencies.append(dependency)
    for dependency in dependencies:
        taskList[taskList.index(dependency[0])].append([taskList.index(dependency[1])])
    for task in taskList:
        if len(task) == 8:
            task.append([])
    
        
def setTimeWindowsOfTask(task, numDays, maxTaskTimeWindows, dayLength, isConsistent):
    timeWindows = []
    releaseTime = task[2]
    duration = task[3]
    deadline = task[4]
    if isConsistent:
        daysWithTimeWindows = range(numDays)
    else:
        daysWithTimeWindows = random.sample(range(numDays), random.randint(1, numDays))
        daysWithTimeWindows.sort()
    for day in range(numDays):
        dayWindows = []
        if day in daysWithTimeWindows:
            numberTimeWindows = random.randint(1, maxTaskTimeWindows)
            numberTimeWindows = min(numberTimeWindows, dayLength / duration)
            # bad things will happen if maxTaskTimeWindows > 3
            if maxTaskTimeWindows == 3:
                maxTimeWindowLength = dayLength / 6
            else:
                maxTimeWindowLength = dayLength / 4
            
            for window in range(numberTimeWindows):
                timeWindowLength = random.randint(duration, maxTimeWindowLength)
                if window == 0:
                    timeWindowStart = random.randint(1 + day * dayLength, (day + 1) * dayLength - timeWindowLength)
                else:
                    timeWindowStart = getTimeWindowStart(dayLength, dayWindows, timeWindowLength, day)
                
                timeWindowEnd = timeWindowStart + timeWindowLength
                dayWindows.append((timeWindowStart, timeWindowEnd))
                dayWindows.sort()
    
        timeWindows.append(dayWindows)
    
    if isConsistent:
        timeWindows = makeConsistent(timeWindows, dayLength)

    task.append(timeWindows)

    # if we are going to do this permanently we should remove release times/deadlines from other functions
    task[2] = getEarliestWindowStart(timeWindows)
    task[4] = getLatestWindowEnd(timeWindows)

def getEarliestWindowStart(timeWindows):
    for day in timeWindows:
        for window in day:
            return window[0]

def getLatestWindowEnd(timeWindows):
    for day in reversed(timeWindows):
        for window in reversed(day):
            return window[1]


'''
Given a list of all time windows for a task, modifies them so that
all the windows occur at the same relative time every day as they do
on the first day.
'''
def makeConsistent(timeWindows, dayLength):
    firstDayWindows = timeWindows[0]
    for dayNumber, day in enumerate(timeWindows):
        timeWindows[dayNumber] = copy.deepcopy(firstDayWindows)
        for index, window in enumerate(firstDayWindows):
            timeWindows[dayNumber][index] = ((window[0] + dayLength * dayNumber), (window[1] + dayLength * dayNumber))
    return timeWindows
    
def getTimeWindowStart(dayLength, dayWindows, timeWindowLength, day):
    isPossible = False
    while not isPossible:   
        position = random.randint(0, len(dayWindows))
        if position == 0:
            earliestStart = 1 + day * dayLength
            latestEnd = dayWindows[0][0]
        elif position == len(dayWindows):
            earliestStart = dayWindows[position - 1][1]
            latestEnd = (day + 1) * dayLength
        else:
            earliestStart = dayWindows[position - 1][1]
            latestEnd = dayWindows[position][0]
        if timeWindowLength <= latestEnd - earliestStart:
            isPossible = True
    return random.randint(earliestStart, latestEnd - timeWindowLength)

'''
Generates a task as a list so that it may be written to a csv file.
Each parameter is the maximum possible value for that feature. The task
that is returned is: [xCoord, yCoord, releaseTime, duration, deadline]
(where duration is deadline - releaseTime). It is required that deadline
is later or the same as the release time.
'''
def generateTask(xConstraint, yConstraint, releaseTime, minDuration, maxDuration, deadline, priority,
    isRequired, isConsistent, numDays, maxNumTimeWindows, dayLength):
    assert (deadline >= releaseTime)
    task = []
    
    for feature in [xConstraint, yConstraint, releaseTime]:
        task.append(random.randint(0, feature)) 
    task.append(random.randint(minDuration, maxDuration))
    task.append(random.randint(task[2] + task[3], deadline))
    setPriorityOfTask(task, priority, isRequired)
    setRequiredOfTask(task)
    setTimeWindowsOfTask(task, numDays, maxNumTimeWindows, dayLength, isConsistent)

    return task

'''
Checks to see if a task had priority set to -1 as a placeholder for being
required, and if so, replaces that priority with a priority larger
than the sum of all optional task priorities (effectively infinite).
'''
def changeRequiredTasksProfit(taskList, maxSumProfit):
    for task in taskList:
        if task[-2] == 1:
            task[-3] = maxSumProfit

'''
A function that will write n tasks to a csv file.  It uses
generateTask to create the task to write.

@param dayLength: the length of the day
@param n: the number of tasks to write to the csv
@param xRange: the highest x value a task's location will be set to
@param yRange: the highest y value a task's location will be set to
@param releaseTimeRange: the latest a task's release time can be set (global across days)
@param durationMin: the shortest duration that can be set for a task
@param durationMax: the longest duration that can be set for a task
@param deadlineRange: the latest deadline a task can be assigned (global across days)
@param priorityRange: the highest priority an optional task can be assigned
@param numberRequired: the number of tasks to be set to be required
@param numDays: the number of days in the scheduled
@param maxNumTimeWindows: the highest number of time windows a task can be given
@param numberDependencies: the number of tasks to be given a dependency on one other task
@param numberConsistent: the number of tasks that have the same time windows every day
@param csvFile: the name of the csv file to write the schedule to

@return: the name of the csv file
'''
def writeNTasks(dayLength, n, xRange, yRange, releaseTimeRange, durationMin, durationMax, deadlineRange,
    priorityRange, numberRequired, numDays, maxNumTimeWindows, numberDependencies, numberConsistent, csvFile):
    taskList = []
    
    isRequired = [False for task in range(n)]
    isConsistent = [False for task in range(n)]
    requiredIndices = random.sample(range(n), numberRequired)
    consistentIndices = random.sample(range(n), numberConsistent)
    for i in requiredIndices:
        isRequired[i] = True
    for i in consistentIndices:
        isConsistent[i] = True

    with open(csvFile, 'wb') as f:
        writer = csv.writer(f)
        writer.writerow(taskFeatures)
        for i in range(n):
            taskList.append(generateTask(xRange, yRange, releaseTimeRange, durationMin, durationMax,
                deadlineRange, priorityRange, isRequired[i], isConsistent[i], numDays, maxNumTimeWindows, dayLength))
        maxSumProfit = (n + 1) * priorityRange + 1
        changeRequiredTasksProfit(taskList, maxSumProfit)
        setDependencies(taskList, numberDependencies)
        for task in taskList:
            writer.writerow(task)
    return csvFile

def main():

    # make sure these make sense!
    numberOfTasks = 64
    numDays = 3
    xRange = 60
    yRange = 60
    durationMin = 1 # tasks will receive durations no shorter than this
    durationMax = 120 # tasks will receive durations no longer than this

    # these do nothing right now:
    releaseTimeRange = (dayLength * numDays) - durationMax # tasks will receive release times no later than this
    deadlineRange = dayLength * numDays # tasks will be assigned deadlines no later than this

    priorityRange = 10 # optional tasks assigned priority between 1 and this
    numberRequired = 6 # number of required tasks
    maxTaskTimeWindows = 2 # max number of time windows a task can have on a particular day
    numberDependencies = 0 # percent of tasks with 1 dependency (must be <.5 right now)
    numberConsistent = 0
    assert(numberDependencies <= numberOfTasks / 2)
    for i in range(10):
        writeNTasks(dayLength, numberOfTasks, xRange, yRange, releaseTimeRange,
            durationMin, durationMax, deadlineRange, priorityRange, numberRequired,
            numDays, maxTaskTimeWindows, numberDependencies, numberConsistent, "testing" + str(i)             + ".csv")


if __name__ == '__main__':
    main()