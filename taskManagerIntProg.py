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
num_tasks = len(task_list)

def get_xij_variables(num_tasks):
    xij_variables = [[None for i in range(num_tasks)] for j in range(num_tasks)]
    for i in range(num_tasks):
        for j in range(num_tasks):
            if i != j:
                xij_variables[i][j] = LpVariable(("x" + str(i) + str(j)), 0, 1, LpBinary)
    return xij_variables

def get_dij_constants(task_list):
    num_tasks = len(task_list)
    dij_constraints = [[None for i in range(num_tasks)] for j in range(num_tasks)]
    for i in range(num_tasks):
        for j in range(num_tasks):
            if i != j:
                dij_constraints[i][j] = get_distance_between_tasks(task_list[i], task_list[j])
    return dij_constraints



yi_variables = [LpVariable(("y"+str(i)), 0, 1, LpBinary) for i in range(num_tasks)] # included or not
ai_variables = [LpVariable(("a"+str(i)), 0, 1000) for i in range(num_tasks)] # ending time
xij_variables = get_xij_variables(num_tasks)
service_time_constants = [task_list[i].duration for i in range(num_tasks)]
dij_constants = get_dij_constants(task_list)
deadline_constants = [task_list[i].deadline for i in range(num_tasks)]

print yi_variables
print ai_variables
print xij_variables
print service_time_constants
print dij_constants
print deadline_constants

'''
Objective function problem variable created to contain problem data
'''
 
prob = LpProblem("Scheduling",LpMaximize)
prob += lpSum(yi_variables) 

print prob
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

