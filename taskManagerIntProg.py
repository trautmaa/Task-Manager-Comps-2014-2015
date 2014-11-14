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

def add_xij_binary_constraints(prob, xij_variables, num_tasks):
    for i in range(num_tasks):
        for j in range(num_tasks):
            if xij_variables[i][j] != None:
                prob += xij_variables[i][j] <= 1
                
def add_connectivity_constraints(prob, xij_variables, num_tasks, yi_variables):
    for i in range(num_tasks):
        xji_list = []
        xij_list = []
        for j in range(num_tasks):
            if i != j:
                xji_list += xij_variables[j][i]
                xij_list += xij_variables[i][j]
        prob += lpSum(xji_list) == lpSum(xij_list) #for job i sum xij = sum xji
        prob += lpSum(xij_list) == yi_variables[i] #for job i sum xij = yi
       
    
    
def add_completion_time_constraints(prob, release_constants, service_time_constants, 
                                    ai_variables, deadline_constants, B, yi_variables):
    for i in range(num_tasks):
        prob += release_constants[i] + service_time_constants[i] <= ai_variables[i] # ri + si <= ai
        prob += ai_variables[i] <= deadline_constants[i] + B * (1 - yi_variables[i]) # ai <= B(1-yi)

        
def add_travel_and_service_time_constraints(prob, ai_variables, dij_constants, service_time_constants,
                                            B, xij_variables):
    for i in range(num_tasks):
        for j in range(num_tasks):
            if i != j:
                prob += ai_variables[i] + dij_constants[i][j] + service_time_constants[j] \
                <= ai_variables[j] + B *(1-xij_variables[i][j])

yi_variables = [LpVariable(("y"+str(i)), 0, 1, LpBinary) for i in range(num_tasks)] # included or not
ai_variables = [LpVariable(("a"+str(i)), 0, 1000) for i in range(num_tasks)] # ending time
xij_variables = get_xij_variables(num_tasks)
service_time_constants = [task_list[i].duration for i in range(num_tasks)]
dij_constants = get_dij_constants(task_list)
deadline_constants = [task_list[i].deadline for i in range(num_tasks)]
release_constants = [task_list[i].release_time for i in range(num_tasks)]
B = 100000000 # Just a big number!

 
prob = LpProblem("Scheduling",LpMaximize)
prob += lpSum(yi_variables) #OBJECTIVE FUNCTION


add_xij_binary_constraints(prob, xij_variables, num_tasks)
add_connectivity_constraints(prob, xij_variables, num_tasks, yi_variables)
add_completion_time_constraints(prob, release_constants, service_time_constants, 
                                ai_variables, deadline_constants, B, yi_variables)

add_travel_and_service_time_constraints(prob, ai_variables, dij_constants, 
                                        service_time_constants, B, xij_variables)

print prob


