'''
Task Manager Comps

Advisor:
David Liben-Nowell

Group members:
Larkin Flodin, Avery Johnson, Maraki Ketema,
Abby Lewis, Will Schifeling, Alex Trautman

This program uses Python's PuLP - a linear programming libray - to model and solve an integer program that describes our base problem.
'''

import pulp

import createTasksFromCsv
import helperFunctions

from Objects import Route, Task, Schedule


'''
A function that returns a two-dimensional list where the jth entry in the
ith sublist represents the variable (boolean) for if we go from task i to
task j.  Note that if i == j, that entry is None.
'''
def makeXijVariables(numTasks):
    xijVariables = [[None for i in range(numTasks)] for j in range(numTasks)]
    for i in range(numTasks):
        for j in range(numTasks):
            if i != j:
                xijVariables[i][j] = pulp.LpVariable(("x" + str(i) + "," + str(j)), 0, 1, pulp.LpBinary)
    return xijVariables


'''
A function that returns a two-dimensional list where the jth entry in the
ith sublist represents the distance from task i to
task j.  Note that if i == j, that entry is None.
'''
def makeDijConstants(taskList):
    numTasks = len(taskList)
    dijConstants = [[None for i in range(numTasks)] for j in range(numTasks)]
    for i in range(numTasks):
        for j in range(numTasks):
            if i != j:
                dijConstants[i][j] = helperFunctions.getDistanceBetweenTasks(taskList[i], taskList[j])
    return dijConstants


        
'''
We need to add:
    Rule (4) ktSum of yitk = y1
    Changing Connectivity...
    Rule (9) making sure ai fits in its time windows  --> (aitk + si) * yitk <= ait <= bitk(endingOfThatTimeWindow) + B(1-yitk)
    Rule (7)??? kSum of yitk = sum xijt where i != j
'''

'''
THIS MUST BE CHANGED TO DO DAYS!!!!!!!
A function that adds constraints to the problem.  This constraint is
for all jobs i, the sum of the variables xij = the sum of the variables xji
                the sum of the variables xij = yi
'''
def addConnectivityConstraints(prob, xijVariables, xhiVariables, xihVariables, numTasks, yiVariables):
    for i in range(numTasks):
        xjiList = []
        xijList = []
        for j in range(numTasks):
            if i != j:
                xjiList += xijVariables[j][i]
                xijList += xijVariables[i][j]
        prob += pulp.lpSum(xjiList) + xhiVariables[i] == pulp.lpSum(xijList) + xihVariables[i] # for job i sum xij +xhi = sum xji + xih
        prob += pulp.lpSum(xijList) + xihVariables[i] == yiVariables[i] # for job i sum xij = yi
       
    
'''
A function that adds constraints to the problem.  This constraint is
for all jobs i, the task can't be finished before its release time and its service time
                the task will finish before its deadline if it is an included task
'''
def addCompletionTimeConstraints(prob, releaseConstants, serviceTimeConstants, 
                                    aiVariables, deadlineConstants, latestDeadline, yiVariables, numTasks):
    for i in range(numTasks):
        prob += releaseConstants[i] + serviceTimeConstants[i] <= aiVariables[i] # ri + si <= ai
        prob += aiVariables[i] <= deadlineConstants[i] + latestDeadline * (1 - yiVariables[i]) # ai <= B(1 - yi)



'''
A function that adds constraints to the problem.  This constraint is
for all pairs of distinct jobs, if job j comes after job i: then job j can't finish
                                before the finish time of job i + the distance between them
                                + the service time of job j
'''        
def addTravelAndServiceTimeConstraints(prob, aiVariables, dijConstants, serviceTimeConstants,
                                            latestDeadline, xijVariables, numTasks):
    for i in range(numTasks):
        for j in range(numTasks):
            if i != j:
                prob += aiVariables[i] + dijConstants[i][j] + serviceTimeConstants[j] \
                <= aiVariables[j] + latestDeadline *(1 - xijVariables[i][j])


'''
A function that adds all constraints related to the starting location to
the integer program. These constraints are that only 1 task can come immediately
after the start, and that if job i comes immediately after the start, it cannot
finish before its service time + the travel time from the start.
'''
def addStartingLocationConstraints(prob, dhiConstants, serviceTimeConstants, aiVariables,
                                        latestDeadline, xhiVariables, numTasks):
    prob += pulp.lpSum(xhiVariables) == 1
    for i in range(numTasks):
        prob += dhiConstants[i] + serviceTimeConstants[i] \
        <= aiVariables[i] + latestDeadline * (1 - xhiVariables[i])


'''
A function that takes a list of tasks and iterates over them,
returning the latest deadline out of all tasks.
'''
def getLatestDeadline(taskList):
    latestDeadline = 0
    for task in taskList:
        if task.deadline > latestDeadline:
            latestDeadline = task.deadline
    return latestDeadline


'''
A function that takes a solved integer program and converts it into a makeSchedule
object.
'''
def makeSchedule(yiVariables, aiVariables, taskList):
    solvedTaskTuples = []
    for index, taskVar in enumerate(yiVariables):
        if (taskVar.varValue == 1):
            solvedTaskTuples.append((taskList[index], aiVariables[index].varValue))
    sortedTaskTuples = sorted(solvedTaskTuples, key = lambda tuple:tuple[1])
    solvedTaskList = []
    solvedTaskCompletionTimes = []
    for taskTuple in sortedTaskTuples:
        solvedTaskList.append(taskTuple[0])
        solvedTaskCompletionTimes.append(taskTuple[1])
    route = Route()
    route.setTaskList(solvedTaskList, solvedTaskCompletionTimes)
    schedule = Schedule()
    schedule.append(route)
    return schedule


'''
Function that, given a list of tasks, constructs and solves an integer program,
returning the resulting schedule.
'''
def integerProgramSolve(taskList):
    numTasks = len(taskList)
    latestDeadline = getLatestDeadline(taskList)
    startingLocation = (0, 0) # probably update this eventually

    yiVariables = [pulp.LpVariable(("y" + str(i)), 0, 1, pulp.LpBinary) for i in range(numTasks)] # included or not
    aiVariables = [pulp.LpVariable(("a" + str(i)), 0, latestDeadline) for i in range(numTasks)] # completion time
    xijVariables = makeXijVariables(numTasks)
    xhiVariables = [pulp.LpVariable(("xH" + str(i)), 0, 1, pulp.LpBinary) for i in range(numTasks)]
    xihVariables = [pulp.LpVariable(("x" + str(i) + "H"), 0, 1, pulp.LpBinary) for i in range(numTasks)]
    dijConstants = makeDijConstants(taskList)
    dhiConstants = [helperFunctions.getDistanceBetweenCoords(startingLocation, helperFunctions.getCoords(task)) for task in taskList]
    deadlineConstants = [task.deadline for task in taskList]
    releaseConstants = [task.releaseTime for task in taskList]
    serviceTimeConstants = [task.duration for task in taskList]

    # Initialize problem 
    prob = pulp.LpProblem("Scheduling", pulp.LpMaximize)
    # OBJECTIVE FUNCTION
    prob += pulp.lpSum(yiVariables) 


    # Add all constraints
    addConnectivityConstraints(prob, xijVariables, xhiVariables, xihVariables, numTasks, yiVariables)
    
    addCompletionTimeConstraints(prob, releaseConstants, serviceTimeConstants, 
                                    aiVariables, deadlineConstants, latestDeadline, yiVariables,
                                    numTasks)

    addTravelAndServiceTimeConstraints(prob, aiVariables, dijConstants, 
                                            serviceTimeConstants, latestDeadline, xijVariables,
                                            numTasks)

    addStartingLocationConstraints(prob, dhiConstants, serviceTimeConstants, aiVariables,
                                        latestDeadline, xhiVariables,
                                        numTasks)
    
    prob += pulp.lpSum(xihVariables) == 1 # Ending job constraint

    # Gurobi model variables can be set using keyword arguments
    # (https://docs.python.org/2/tutorial/controlflow.html#keyword-arguments)
    # refer to http://www.gurobi.com/documentation/6.0/reference-manual/refman
    # for specific parameter documentation
    # e.g.: solver = pulp.solvers.GUROBI(OutputFlag = 0, Threads = 4, TimeLimit = 120)
    solver = pulp.solvers.GUROBI(TimeLimit = 60)
    prob.solve(solver)
    assert(prob.status == 1) # Problem was solved
    return makeSchedule(yiVariables, aiVariables, taskList)

'''
A helper function that does everything but print the solution,
for use in comparing different algorithms.
'''
def runIntegerProgram(csvFile):
    taskList = createTasksFromCsv.getTaskList(csvFile)
    schedule = integerProgramSolve(taskList)
    return schedule

'''    
A main function that will read in the list of tasks from a csv, construct the integer program,
and print the solution it produces.
'''
def main():
    solvedSchedule = runIntegerProgram("test.csv")
    print
    helperFunctions.printScheduleJourney(solvedSchedule)
    print


if __name__ == '__main__':
    main()
