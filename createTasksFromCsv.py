# Comps 2014
# Larkin Flodin, Avery Johnson, Maraki Ketema, 
# Abby Lewis, Will Schifeling, and  Alex Trautman

import csv
import re

import Objects

'''
Given a csv file, this function will call the readInTask
function to retrieve the tasks and with those will call 
makeObjects that returns a list of task objects, which
is then returned.
'''
def getTaskList(csvFile):
    tasksFromCsv = readInTask(csvFile)
    taskList = makeObjects(tasksFromCsv)
    return taskList

'''
Given a csv file, it will read a row from the csv and 
turn that into a list of a task's features. Each task 
will be appended to the tasks list and finally the 
tasks list will be returned.
'''
def readInTask(csvFile):
    tasks = []
    with open(csvFile, 'rU') as f:
        reader = csv.reader(f, delimiter = ",")
        for row in reader:
            tasks.append(row)
    return tasks[1:] # tasks[0] is the list of names of the features.

    

'''
A function that returns a list of task objects.
It takes a list of tasks in list form, and converts
them to objects and adds them to the taskList.
'''
def makeObjects(attributeList):
    taskList = []
    for i in range(len(attributeList)):
        newObject = Objects.Task(i)
        taskList.append(newObject)
        # taskList[i][j] is xcoord, ycoord, release time, duration, deadline, priority, required
        for j in range(len(attributeList[i])): 
            if (j == 0): # x coordinate value
                taskList[i].setX(attributeList[i][0])
            
            if (j == 1): # y coordinate value
                taskList[i].setY(attributeList[i][1])
                
            if (j == 2): # release time
                taskList[i].setReleaseTime(attributeList[i][2])
                
            if (j == 3): # duration
                taskList[i].setDuration(attributeList[i][3])
                
            if (j == 4): # deadline
                taskList[i].setDeadline(attributeList[i][4])
            
            if (j == 5): # priority
                taskList[i].setPriority(attributeList[i][5])
                
            if (j == 6): # required
                taskList[i].setRequired(attributeList[i][6])
            
            if (j == 7): # time windows
                taskList[i].setTimeWindows(getTimeWindows(attributeList[i][7]))
                
            if (j == 8):
                taskList[i].setTaskDependency(attributeList[i][8])
                
            # With added features, we must add statements here.
    return taskList

'''
Takes in all the time windows and puts them into a form that VNS can use 
(distinguishing between days).
'''
def getTimeWindows(timeWindowString):
    days = []
    result = timeWindowString[1:-1]
    result = re.split("\],", result)
    for day in result:
        timeWindows = []
        if re.match(".*\[\].*", day) or re.match(".*\[\s*$", day):
            days.append([])
            continue
        day = re.split("\),", day)
        for tw in range(len(day)):
            timeWindow = day[tw]
            twStart = re.search("([0-9]+),", timeWindow)
            twStart = re.search("[0-9]+", twStart.group())
            twEnd = re.search(",\s*([0-9]+)", timeWindow)
            twEnd = re.search("[0-9]+", twEnd.group())
            timeWindows.append((int(twStart.group()), int(twEnd.group())))
        days.append(timeWindows)
    return days


def main():
    for task in makeObjects(readInTask("newTest.csv")):
        print task
        
if __name__ == '__main__':
    main()
