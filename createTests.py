# Comps 2014
# Larkin Flodin, Avery Johnson, Maraki Ketema, 
# Abby Lewis, Will Schifeling, and  Alex Trautman

import csv

from copy import deepcopy

import random


'''
Make sure your input variables make sense!!!!!!!!!
'''
numberOfTasks = 30
dayLength = 1440
numDays = 2
xRange = 60
yRange = 60
durationRange = 200 # tasks will receive durations no longer than this
releaseTimeRange = (dayLength * numDays) - durationRange # tasks will receive release times no earlier than this
deadlineRange = dayLength * numDays # tasks will be assigned deadlines no later than this
priorityRange = 3 # optional tasks assigned priority between 1 and this
likelyhoodOfMandatory = .1 # between 0 and 1, chance a task is generated as mandatory
maxTaskTimeWindows = 3 # max number of time windows a task can have on a particular day
numDependencies = 15
assert(numDependencies <= numberOfTasks/2)

taskFeatures = ['xCoord', 'yCoord', 'releaseTime', 'duration', 'deadline', 'priority', 'required', 'timeWindows', 'dependencyTasks']

def setPriorityOfTask(task, priority):
    if random.random() >= likelyhoodOfMandatory:
        task.append(random.randint(1, priority))
    else:
        task.append(-1)
                   
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
        print len(task)
    
        
def setTimeWindowsOfTask(task, numDays):
    timeWindows = []
    releaseTime = task[2]
    duration = task[3]
    deadline = task[4]    
    for day in range(numDays):
        dayWindows = []
        # if a time window can be scheduled on that day for this task
        if (((day + 1) * dayLength) - duration - 1) >= releaseTime and deadline >= (day * dayLength + duration):

            # either deadline / duration, or dayLength / duration, or (endOfDay - releaseTime) / duration
            maxNumTimeWindows = min((dayLength - 1), ((day + 1) * dayLength - releaseTime), deadline) / duration
            # further constrain by global parameter
            maxNumTimeWindows = min(maxNumTimeWindows, maxTaskTimeWindows)
            endingWindowTime = 0
            for window in range(maxNumTimeWindows):
                if endingWindowTime + duration >= min(deadline, (day + 1) * dayLength):
                    break
                else:
                    startingWindowTime = random.randint(max(endingWindowTime, releaseTime, day * dayLength), min(deadline, (day + 1) * dayLength - 1) - duration)
                    endingWindowTime = random.randint((startingWindowTime + duration), min(deadline, (day + 1) * dayLength - 1))
                    dayTimeWindow = (startingWindowTime, endingWindowTime)
                    assert(startingWindowTime >= releaseTime)
                    assert(endingWindowTime <= deadline)
                    assert((endingWindowTime - startingWindowTime) >= duration)
                    assert(endingWindowTime / dayLength == startingWindowTime / dayLength)
                    dayWindows.append(dayTimeWindow)
            
        
        timeWindows.append(dayWindows)
    
    # to replicate old conditions:
    # task.append([[releaseTime, deadline]])

    task.append(timeWindows)

'''
Generates a task as a list so that it may be written to a csv file.
Each parameter is the maximum possible value for that feature. The task
that is returned is: [xCoord, yCoord, releaseTime, duration, deadline]
(where duration is deadline - releaseTime). It is required that deadline
is later or the same as the release time.
'''
def generateTask(xConstraint, yConstraint, releaseTime, maxDuration, deadline, priority, required, numDays):
    assert (deadline >= releaseTime)
    task = []
    
    for feature in [xConstraint, yConstraint, releaseTime]:
        task.append(random.randint(0, feature)) 
    task.append(random.randint(1, maxDuration))
    task.append(random.randint(task[2] + task[3], deadline))
    setPriorityOfTask(task, priority)
    setRequiredOfTask(task)
    setTimeWindowsOfTask(task, numDays)

    return task

def process(taskList, maxSumProfit):
    for task in taskList:
        if task[-2] == 1:
            task[-3] = maxSumProfit

'''
A function that will write n tasks to a csv file.  It uses
generateTask to create the task to write. Right now the
constraints for generateTask are hard coded but that can 
be changed.  The name of the csv file is returned.
'''
def writeNTasks(n, csvFile):
    taskList = []
    with open(csvFile, 'wb') as f:
        writer = csv.writer(f)
        writer.writerow(taskFeatures)
        for i in range(n):
            taskList.append(generateTask(xRange, yRange, releaseTimeRange, durationRange, deadlineRange, priorityRange, 0, numDays))
        maxSumProfit = (n + 1) * priorityRange + 1
        process(taskList, maxSumProfit)
        setDependencies(taskList, numDependencies)
        for task in taskList:
            writer.writerow(task)
    return csvFile

def main():
    writeNTasks(numberOfTasks, "test.csv")


if __name__ == '__main__':
    main()