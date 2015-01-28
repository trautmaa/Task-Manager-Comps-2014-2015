# Comps 2014
# Larkin Flodin, Avery Johnson, Maraki Ketema, 
# Abby Lewis, Will Schifeling, and  Alex Trautman

import csv
import re

taskFeatures = ['xCoord', 'yCoord', 'releaseTime', 'duration', 'deadline', 'priority', 'required', 'timeWindows']
def readInTask(csvFile):
    tasks = []
    with open(csvFile, 'rU') as f:
        for row in f:
            tasks.append(row.split())
    return tasks[2:-1] # tasks[0] is the list of names of the features.

#i 0 = vertex number
#x 1= x coordinate
#y 2= y coordinate
#d 3= service duration or visiting time	
#S 4= profit of the location
#f 5= not relevant
#a 6= not relevant
#list 7= not relevant (length of the list depends on a)
#O 8= opening of time window (earliest time for start of service)
#C 9= closing of time window (latest time for start of service)
   
def writeFromReadInTasks(inputCSVFile, outputCSVFile):
    taskList = readInTask(inputCSVFile)
    with open(outputCSVFile, 'wb') as f:
        writer = csv.writer(f)
        writer.writerow(taskFeatures)
        first = True
        for task in taskList:
            if first:
                newTask = [task[1], task[2], 0, 0, 0.1, 1, 1, [[(0, 0.1)]]]
                writer.writerow(newTask)
                newTask = [task[1], task[2], float(task[8]), 0, float(task[8])+0.1, 1, 1, [[(float(task[8]), float(task[8]) + 0.1)]]]
                first = False
            else:
                newTask = [task[1], task[2], task[8], task[3], (float(task[8]) + float(task[3])), task[4], 0, [[(float(task[8]), float(task[8])+float(task[3]))]]]
            writer.writerow(newTask)
    
for i in range(8):
    writeFromReadInTasks("50_rc10" + str(i+1) + ".txt", "50_rc10" + str(i+1) + ".csv")