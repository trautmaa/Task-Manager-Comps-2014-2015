# Comps 2014
# Larkin Flodin, Avery Johnson, Maraki Ketema, 
# Abby Lewis, Will Schifeling, and  Alex Trautman

import csv

from random import randint


'''
Make sure your input variables make sense!!!!!!!!!
'''
xRange = 60
yRange = 60
releaseTimeRange = 8000
durationRange = 800
deadlineRange = 10080
numDays = 7
dayLength = 1440
priorityRange = 10
likelyhoodOfMandatory = .3 # has to be between .1 and .9

taskFeatures = ['xCoord', 'yCoord', 'releaseTime', 'duration', 'deadline', 'priority', 'required', 'timeWindows']

def setPriorityOfTask(task, priority):
    if randint(0, 10) >= likelyhoodOfMandatory * 10:
        task.append(randint(1, priority))
    else:
        task.append(-1)
                   
def setRequiredOfTask(task):
    if task[-1] == -1:
        task.append(1)
    else:
        task.append(0)
        
def setTimeWindowsOfTask(task, numDays):
    timeWindows = []
    releaseTime = task[2]
    duration = task[3]
    deadline = task[4]
    for day in range(numDays):
        dayWindows = []
        if (((day + 1) * dayLength) - duration - 1) >= releaseTime and deadline >= (day * dayLength + duration):
            maxNumTimeWindows = min((dayLength -1), ((day + 1) * dayLength - releaseTime), deadline) / duration
            endingWindowTime = 0
            for window in range(maxNumTimeWindows):
                if endingWindowTime + duration >= min(deadline, (day + 1) * dayLength):
                    break
                else:
                    startingWindowTime = randint(max(endingWindowTime, releaseTime, day * dayLength), min(deadline, (day + 1) * dayLength - 1) - duration)
                    endingWindowTime = randint((startingWindowTime + duration), min(deadline, (day + 1) * dayLength - 1))
                    dayTimeWindow = (startingWindowTime, endingWindowTime)
                    assert(startingWindowTime >= releaseTime)
                    assert(endingWindowTime <= deadline)
                    assert((endingWindowTime - startingWindowTime) >= duration)
                    assert(endingWindowTime / dayLength == startingWindowTime / dayLength)
                    dayWindows.append(dayTimeWindow)
            
        
        timeWindows.append(dayWindows)
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
        task.append(randint(0, feature)) 
    task.append(randint(1, maxDuration))
    task.append(randint(task[2] + task[3] + 100, deadline))
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
        maxSumProfit = (n+1) * priorityRange + 1
        process(taskList, maxSumProfit)
        for task in taskList:
            writer.writerow(task)
    return csvFile

def main():
    writeNTasks(8, "test.csv")


if __name__ == '__main__':
    main()