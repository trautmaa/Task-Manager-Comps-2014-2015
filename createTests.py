# Comps 2014
# Larkin Flodin, Avery Johnson, Maraki Ketema, 
# Abby Lewis, Will Schifeling, and  Alex Trautman

import csv

from random import randint

taskFeatures = ['xCoord', 'yCoord', 'releaseTime', 'duration', 'deadline', 'priority', 'required', 'timeWindows']

def setPriorityOfTask(task, priority):
    task.append(priority) # This will need to be changed when we do priority...
    
def setRequiredOfTask(task, required):
    task.append(required) # This will need to be changed when we do required...
    
def setTimeWindowsOfTask(task, numDays):
    timeWindows = []
    releaseTime = task[2]
    duration = task[3]
    deadline = task[4]
    for day in range(numDays):
        dayWindows = []
        if ((day+1) * 100 - duration-1) >= releaseTime \
        and deadline >= (day * 100 + duration):
            maxNumTimeWindows = min(99, ((day+1) * 100 - releaseTime), deadline)/duration
            endingWindowTime = 0
            for window in range(maxNumTimeWindows):
                if endingWindowTime + duration >= min(deadline, (day+1) * 100):
                    break
                else:
                    print endingWindowTime, releaseTime, day *100, deadline
                    startingWindowTime = randint(max(endingWindowTime, releaseTime, day *100), min(deadline, (day+1) * 100 - 1) - duration)
                    endingWindowTime = randint((startingWindowTime + duration), min(deadline, (day + 1 ) * 100 - 1))
                    dayTimeWindow = (startingWindowTime, endingWindowTime)
                    assert(startingWindowTime >= releaseTime)
                    assert(endingWindowTime <= deadline)
                    assert((endingWindowTime - startingWindowTime) >= duration)
                    assert(endingWindowTime/100 == startingWindowTime/100)
                    dayWindows.append(dayTimeWindow)
            
        
        timeWindows.append(dayWindows)
    print timeWindows
    print releaseTime, duration, deadline
    print 
    print

    
    
#    dayOne = []
#    dayOneTimeWindow = (0, 1000)
#    dayOne.append(dayOneTimeWindow)
#    timeWindows.append(dayOne)
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
    setRequiredOfTask(task, required)
    setTimeWindowsOfTask(task, numDays)
    

    return task

'''
A function that will write n tasks to a csv file.  It uses
generateTask to create the task to write. Right now the
constraints for generateTask are hard coded but that can 
be changed.  The name of the csv file is returned.
'''
def writeNTasks(n, csvFile):
    with open(csvFile, 'wb') as f:
        writer = csv.writer(f)
        writer.writerow(taskFeatures)
        for i in range(n):
            writer.writerow(generateTask(60, 60, 800, 50, 1000, 1, 0, 10))
    return csvFile

def main():
    writeNTasks(10, "test.csv")


if __name__ == '__main__':
    main()