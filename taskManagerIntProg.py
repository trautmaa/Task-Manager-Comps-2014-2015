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
    dij_constants = [[None for i in range(num_tasks)] for j in range(num_tasks)]
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
def add_connectivity_constraints(prob, xij_variables, xhi_variables, xih_variables, num_tasks, yi_variables):
    for i in range(num_tasks):
        xji_list = []
        xij_list = []
        for j in range(num_tasks):
            if i != j:
                xji_list += xij_variables[j][i]
                xij_list += xij_variables[i][j]
        prob += lpSum(xji_list) + xhi_variables[i] == lpSum(xij_list) + xih_variables[i] # for job i sum xij = sum xji + xhi
        prob += lpSum(xij_list) + xih_variables[i] == yi_variables[i] # for job i sum xij = yi
       
    
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
def make_schedule(yi_variables, ai_variables, task_list):
    solved_task_tuples = []
    for index, task_var in enumerate(yi_variables):
        if (task_var.varValue == 1):
            solved_task_tuples.append((task_list[index], ai_variables[index].varValue))
    sorted_task_tuples = sorted(solved_task_tuples, key = lambda tuple:tuple[1])
    solved_task_list = []
    solved_task_completion_times = []
    for taskTuple in sorted_task_tuples:
        solved_task_list.append(taskTuple[0])
        solved_task_completion_times.append(taskTuple[1])
    route = Route()
    route.set_task_list(solved_task_list, solved_task_completion_times)
    schedule = Schedule()
    schedule.add_to_list(route)
    return schedule


'''
Function that, given a list of tasks, constructs and solves an integer program,
returning the resulting schedule.
'''
def integer_program_solve(task_list):
    num_tasks = len(task_list)
    latest_deadline = get_latest_deadline(task_list)
    starting_location = (0, 0) # probably update this eventually

    yi_variables = [LpVariable(("y" + str(i)), 0, 1, LpBinary) for i in range(num_tasks)] # included or not
    ai_variables = [LpVariable(("a" + str(i)), 0, latest_deadline) for i in range(num_tasks)] # completion time
    xij_variables = make_xij_variables(num_tasks)
    service_time_constants = [task.duration for task in task_list]
    xhi_variables = [LpVariable(("xH" + str(i)), 0, 1, LpBinary) for i in range(num_tasks)]
    xih_variables = [LpVariable(("x" + str(i) + "H"), 0, 1, LpBinary) for i in range(num_tasks)]
    dij_constants = make_dij_constants(task_list)
    dhi_constants = [get_distance_between_coords(starting_location, get_coords(task)) for task in task_list]
    deadline_constants = [task.deadline for task in task_list]
    release_constants = [task.release_time for task in task_list]

    # Initialize problem 
    prob = LpProblem("Scheduling", LpMaximize)
    # OBJECTIVE FUNCTION
    prob += lpSum(yi_variables) 


    # Add all constraints
    add_connectivity_constraints(prob, xij_variables, xhi_variables, xih_variables, num_tasks, yi_variables)
    
    add_completion_time_constraints(prob, release_constants, service_time_constants, 
                                    ai_variables, deadline_constants, latest_deadline, yi_variables,
                                    num_tasks)

    add_travel_and_service_time_constraints(prob, ai_variables, dij_constants, 
                                            service_time_constants, latest_deadline, xij_variables,
                                            num_tasks)

    add_starting_location_constraints(prob, dhi_constants, service_time_constants, ai_variables,
                                        latest_deadline, xhi_variables,
                                        num_tasks)

    prob.writeLP("Scheduling.lp")
    prob.solve()
    assert(prob.status == 1) # Problem was solved
    return make_schedule(yi_variables, ai_variables, task_list)

'''
A helper function that does everything but print the solution,
for use in comparing different algorithms.
'''
def run_integer_program(csv_file):
    task_list = get_task_list(csv_file)
    schedule = integer_program_solve(task_list)
    return schedule.route_list[0].task_list

'''    
A main function that will read in the list of tasks from a csv, construct the integer program,
and print the solution it produces.
'''
def main():
    solved_task_list = run_integer_program("test.csv")
    print_schedule(solved_task_list)


if __name__ == '__main__':
    main()
