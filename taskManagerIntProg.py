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


'''
A function that returns a two-dimensional list where the jth entry in the
ith sublist represents the variable (boolean) for if we go from task i to
task j.  Note that if i == j, that entry is None.
'''
def make_xij_variables(num_tasks):
    xij_variables = [[None for i in range(num_tasks)] for j in range(num_tasks)]
    for i in range(num_tasks):
        for j in range(num_tasks):
            if i != j:
                xij_variables[i][j] = LpVariable(("x" + str(i) + str(j)), 0, 1, LpBinary)
    return xij_variables


'''
A function that returns a two-dimensional list where the jth entry in the
ith sublist represents the distance from task i to
task j.  Note that if i == j, that entry is None.
'''
def make_dij_constants(task_list):
    num_tasks = len(task_list)
    dij_constraints = [[None for i in range(num_tasks)] for j in range(num_tasks)]
    for i in range(num_tasks):
        for j in range(num_tasks):
            if i != j:
                dij_constants[i][j] = get_distance_between_tasks(task_list[i], task_list[j])
    return dij_constants


'''
A function that adds constraints to the problem.  This constraint is
for all jobs i, the sum of the variables xij = the sum of the variables xji
                the sum of the variables xij = yi
'''
def add_connectivity_constraints(prob, xij_variables, xhi_variables, num_tasks, yi_variables):
    for i in range(num_tasks):
        xji_list = []
        xij_list = []
        for j in range(num_tasks):
            if i != j:
                xji_list += xij_variables[j][i]
                xij_list += xij_variables[i][j]
        prob += lpSum(xji_list) + xhi_variables[i] == lpSum(xij_list) # for job i sum xij = sum xji + xhi
        prob += lpSum(xij_list) == yi_variables[i] # for job i sum xij = yi
       
    
'''
A function that adds constraints to the problem.  This constraint is
for all jobs i, the task can't be finished before its release time and its service time
                the task will finish before its deadline if it is an included task
'''
def add_completion_time_constraints(prob, release_constants, service_time_constants, 
                                    ai_variables, deadline_constants, latest_deadline, yi_variables, num_tasks):
    for i in range(num_tasks):
        prob += release_constants[i] + service_time_constants[i] <= ai_variables[i] # ri + si <= ai
        prob += ai_variables[i] <= deadline_constants[i] + latest_deadline * (1 - yi_variables[i]) # ai <= B(1 - yi)


'''
A function that adds constraints to the problem.  This constraint is
for all pairs of distinct jobs, if job j comes after job i: then job j can't finish
                                before the finish time of job i + the distance between them
                                + the service time of job j
'''        
def add_travel_and_service_time_constraints(prob, ai_variables, dij_constants, service_time_constants,
                                            latest_deadline, xij_variables, num_tasks):
    for i in range(num_tasks):
        for j in range(num_tasks):
            if i != j:
                prob += ai_variables[i] + dij_constants[i][j] + service_time_constants[j] \
                <= ai_variables[j] + latest_deadline *(1 - xij_variables[i][j])


'''
A function that adds all constraints related to the starting location to
the integer program. These constraints are that only 1 task can come immediately
after the start, and that if job i comes immediately after the start, it cannot
finish before its service time + the travel time from the start.
'''
def add_starting_location_constraints(prob, dhi_constants, service_time_constants, ai_variables,
                                        latest_deadline, xhi_variables, num_tasks):
    prob += lpSum(xhi_variables) == 1
    for i in range(num_tasks):
        prob += dhi_constants[i] + service_time_constants[i] \
        <= ai_variables[i] + latest_deadline * (1 - xhi_variables[i])


'''
A function that takes a list of tasks and iterates over them,
returning the latest deadline out of all tasks.
'''
def get_latest_deadline(task_list):
    latest_deadline = 0
    for task in task_list:
        if task.deadline > latest_deadline:
            latest_deadline = task.deadline
    return latest_deadline


'''
A function that takes a solved integer program and converts it into a makeSchedule
object.
'''
def make_schedule(prob):
    # Sort everything by yi, then by ai
    # Then extract the original numbers from the yi variable names
    # task_list = sort something
    route = Route()
    route.set_task_list(task_list)
    schedule = Schedule()
    schedule.set_route_list([route])
    return schedule


'''    
A main function that will read in the list of tasks from a csv, construct the integer program,
and print the solution it produces.
'''
def main():
    task_list = get_task_list("test.csv")
    num_tasks = len(task_list)
    latest_deadline = get_latest_deadline(task_list)

    starting_location = (0, 0) # probably update this eventually

    yi_variables = [LpVariable(("y" + str(i)), 0, 1, LpBinary) for i in range(num_tasks)] # included or not
    ai_variables = [LpVariable(("a" + str(i)), 0, latest_deadline) for i in range(num_tasks)] # completion time
    xij_variables = make_xij_variables(num_tasks)
    service_time_constants = [task.duration for task in task_list]
    xhi_variables = [LpVariable(("xH" + str(i)), 0, 1, LpBinary) for i in range(num_tasks)]
    dij_constants = make_dij_constants(task_list)
    dhi_constants = [get_distance_between_coords(starting_location, get_coords(task)) for task in task_list]
    deadline_constants = [task.deadline for task in task_list]
    release_constants = [task.release_time for task in task_list]

    # Initialize problem 
    prob = LpProblem("Scheduling", LpMaximize)
    # OBJECTIVE FUNCTION
    prob += lpSum(yi_variables) 


    # Add all constraints, WE HAVE YET TO ADD HOME CONSTRAINTS!!!!!!!!!
    add_connectivity_constraints(prob, xij_variables, xhi_variables, num_tasks, yi_variables)
    
    add_completion_time_constraints(prob, release_constants, service_time_constants, 
                                    ai_variables, deadline_constants, latest_deadline, yi_variables,
                                    num_tasks)

    add_travel_and_service_time_constraints(prob, ai_variables, dij_constants, 
                                            service_time_constants, latest_deadline, xij_variables,
                                            num_tasks)

    add_starting_location_constraints(prob, dhi_constants, service_time_constants, ai_variables,
                                        latest_deadline, xhi_variables,
                                        num_tasks)

    prob.solve()

    schedule = make_schedule(prob)
    print_schedule(schedule.route_list[1].task_list)


if __name__ == '__main__':
    main()
