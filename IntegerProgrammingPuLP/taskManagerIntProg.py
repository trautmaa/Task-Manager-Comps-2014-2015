'''
Task Manager Comps

Advisor:
David Liben-Nowell

Group members:
Larkin Flodin, Avery Johnson, Maraki Ketema,
Abby Lewis, Will Schifeling, Alex Trautman

This program uses Python's PuLP - a linear programming libray - to model and solve an integer program that describes our base problem.
'''

from create_tasks_from_csv import *
from pulp import *
from helper_functions import *

task_list = get_task_list("test.csv")
yi_variables = ["y"+str(i) for i in range(len(task_list))]
print yi_variables
#
#'''
#Objective function problem variable created to contain problem data
#'''
#
#prob = LpProblem("Scheduling",LpMaximize)
#
#taskList = makeTasks() #pseudo
#
##make a list of task variables
#taskVariablesList = []
#for task in taskList:
#    taskVariablesList.append(LpVariable(taskName,0,1,LpBinary))
#
##make a list for pairs of task variables
#
##initialize array to none        
#taskPairsList = [[None for i in range len(taskList)] for j in range len(taskList)]
##populate the taskPairsList
#for i in range(len(taskList)):
#    for j in range(len(taskList)):
#        if taskList[i] != taskList[j]:
#            taskPairsList[i][j] = LpVariable(taskList,0,1,LpBinary)
#
##add the objective function to our problem
##prob += (sum of task variables in taskVariablesList) #pseudo
#prob += sum(taskVariablesList)
#
##constraint: each task may only be scheduled directly before or after one other task
#for i in range(len(taskList)):
#    prob += sum(taskPairsList[i][]) <= 1
#
#
#prob += sum(taskPairsList[][i]) <= 1