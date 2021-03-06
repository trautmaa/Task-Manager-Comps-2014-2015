# Comps 2014
# Larkin Flodin, Avery Johnson, Maraki Ketema, 
# Abby Lewis, Will Schifeling, and  Alex Trautman

import csv

from random import randint

taskFeatures = ['xCoord', 'yCoord', 'releaseTime', 'duration', 'deadline', 'priority', 'required', 'timeWindows']

#taskNames = ['Grocery shopping', 'Get gas', 'Mow the lawn', 'Shovel the driveway', 'Go to laundromat', 'Go to curling practice', 'Meet with comps group', 'Apply to jobs', 'Make travel plans', 'Go to work', 'Take garbage out','Set the table', 'Clear the table', 'Clean room with direction' 'Put away groceries', 'Clean the bathroom with direction', 'Clean the kitchen', 'Dust', 'Vacuum', 'Mow lawn', 'Feed pets', 'Water plants', 'Put laundry in hamper', 'Help with laundry and eventually start doing own laundry', 'Help make dinner/make small meals on own', 'Help wash the car/wash car', 'Make bed', 'Help with yard work', 'Shovel snow', 'Wash dishes/load or empty dishwasher']



def setPriorityOfTask(task, priority):
    task.append(priority) # This will need to be changed when we do priority...
    
def setRequiredOfTask(task, required):
    task.append(required) # This will need to be changed when we do required...
    
def setTimeWindowsOfTask(task, maxNumTimeWindows):
    timeWindows = []
    dayOne = []
    dayOneTimeWindow = (0, 1000)
    dayOne.append(dayOneTimeWindow)
    timeWindows.append(dayOne)
    task.append(timeWindows)

'''
Generates a task as a list so that it may be written to a csv file.
Each parameter is the maximum possible value for that feature. The task
that is returned is: [xCoord, yCoord, releaseTime, duration, deadline]
(where duration is deadline - releaseTime). It is required that deadline
is later or the same as the release time.
'''
def generateTask(xConstraint, yConstraint, releaseTime, maxDuration, deadline, priority, required, maxNumTimeWindows):
    assert (deadline >= releaseTime)
    task = []
    
    for feature in [xConstraint, yConstraint, releaseTime]:
        task.append(randint(0, feature)) 
    task.append(randint(0, maxDuration))
    task.append(randint(task[2] + task[3], deadline))
    setPriorityOfTask(task, priority)
    setRequiredOfTask(task, required)
    setTimeWindowsOfTask(task, maxNumTimeWindows)
    

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
            writer.writerow(generateTask(60, 60, 200, 100, 500, 1, 0, 1))
    return csvFile

def main():
    writeNTasks(8, "test.csv")


if __name__ == '__main__':
    main()