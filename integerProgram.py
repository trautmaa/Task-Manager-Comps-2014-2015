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
import sys

import createTasksFromCsv
import helperFunctions

from Objects import Route, Task, Schedule
from vns import isFeasible

'''
Returns a three dimensional list of decision variables y i,t,k representing
whether or not task i is scheduled on day t during time window k.
'''
def makeYitkVariables(taskList, numDays):
    numTasks = len(taskList)
    yitkVariables = [[[None for k in range(len(taskList[i].timeWindows[t]))] for t in range(numDays)] for i in range(len(taskList))]
    for i in range(numTasks):
        for t in range(numDays):
            for k in range(len(taskList[i].timeWindows[t])):
                yitkVariables[i][t][k] = pulp.LpVariable(("y," + str(i) + "," + str(t) + "," + str(k)), 0, 1, pulp.LpBinary)
    return yitkVariables

'''
Returns a two dimensional list of variables representing the time at which a task finishes on
a particular day. Variable a i,t represents the finish time of task i on day t.
'''
def makeAitVariables(numTasks, numDays, latestDeadline):
    aitVariables = [[None for t in range(numDays)] for i in range(numTasks)]
    for i in range(numTasks):
        for t in range(numDays):
            aitVariables[i][t] = pulp.LpVariable(("a," + str(i) + "," + str(t)), 0, latestDeadline)
    return aitVariables

'''
A function that returns a three-dimensional list where x t,i,j represents
whether the jth task is scheduled immediately following the ith task
on day t. Note that if i == j, that entry is None.
'''
def makeXijtVariables(numTasks, numDays):
    xijtVariables = [[[None for t in range(numDays)] for j in range(numTasks)] for i in range(numTasks)]
    for i in range(numTasks):
        for j in range(numTasks):
            for t in range(numDays):
                if i != j:
                    xijtVariables[i][j][t] = pulp.LpVariable(("x," + str(i) + "," + str(j) + "," + str(t)), 0, 1, pulp.LpBinary)
    return xijtVariables


'''
A function that returns a two-dimensional list where the jth entry in the
ith sublist represents the distance from task i to
task j.  Note that if i == j, that entry is None.
'''
def makeDijConstants(taskList):
    numTasks = len(taskList)
    dijConstants = [[None for j in range(numTasks)] for i in range(numTasks)]
    for i in range(numTasks):
        for j in range(numTasks):
            if i != j:
                dijConstants[i][j] = helperFunctions.getDistanceBetweenTasks(taskList[i], taskList[j])
    return dijConstants

'''
Returns a list of constants where constant r i,t,k is the beginning of time
window k for task i on day t.
'''
def makeRitkConstants(taskList, numDays):
    numTasks = len(taskList)
    ritkConstants = [[[None for k in range(len(taskList[i].timeWindows[t]))] for t in range(numDays)] for i in range(len(taskList))]
    for i in range(numTasks):
        for t in range(numDays):
            for k, timeWindow in enumerate(taskList[i].timeWindows[t]):
                ritkConstants[i][t][k] = timeWindow[0]
    return ritkConstants

'''
Returns a list of constants where constant f i,t,k is the end of time
window k for task i on day t.
'''
def makeFitkConstants(taskList, numDays):
    numTasks = len(taskList)
    fitkConstants = [[[None for k in range(len(taskList[i].timeWindows[t]))] for t in range(numDays)] for i in range(len(taskList))]
    for i in range(numTasks):
        for t in range(numDays):
            for k, timeWindow in enumerate(taskList[i].timeWindows[t]):
                fitkConstants[i][t][k] = timeWindow[1]
    return fitkConstants

'''
Returns two two-dimensional lists of variables where x i,h,t or h,i,t
represents whether x is the last or first (respectively) in the
route for day t.
'''
def makeXihtAndXhitVariables(numTasks, numDays):
    xihtVariables = [[None for t in range(numDays)] for i in range(numTasks)]
    xhitVariables = [[None for t in range(numDays)] for i in range(numTasks)]
    for i in range(numTasks):
        for t in range(numDays):
            xihtVariables[i][t] = pulp.LpVariable(("x" + str(i) + ",H," + str(t)), 0, 1, pulp.LpBinary)
            xhitVariables[i][t] = pulp.LpVariable(("x,H," + str(i) + "," + str(t)), 0, 1, pulp.LpBinary)
    return xihtVariables, xhitVariables

'''
We need to add:
    Rule (4) ktSum of yitk = y1
    Changing Connectivity...
    Rule (9) making sure ai fits in its time windows  --> (aitk + si) * yitk <= ait <= bitk(endingOfThatTimeWindow) + B(1-yitk)
    Rule (7)??? kSum of yitk = sum xijt where i != j
'''

'''
Add constraints to the problem that ensure each scheduled job appears in at most
one time window on one day.
'''
def addJobsAppearOnceConstraints(prob, numDays, numTasks, yiVariables, yitkVariables):
    for i in range(numTasks):
        yitkList = []
        for t in range(numDays):
            for k in range(len(yitkVariables[i][t])):
                yitkList.append(yitkVariables[i][t][k])
        prob += pulp.lpSum(yitkList) == yiVariables[i]


'''
A function that adds constraints to the problem.  This constraint is
for all jobs i, the sum of the variables xijt = the sum of the variables xjit
                and the sum of the variables xijt = the sum of variables yitk
'''
def addConnectivityConstraints(prob, xijtVariables, xihtVariables, xhitVariables, yitkVariables, numTasks, numDays, yiVariables):
    for t in range(numDays):
        for i in range(numTasks):
            xjitList = []
            xijtList = []
            for j in range(numTasks):
                if i != j:
                    xjitList += xijtVariables[j][i][t]
                    xijtList += xijtVariables[i][j][t]
            prob += pulp.lpSum(xijtList) + xihtVariables[i][t] == pulp.lpSum(xjitList) + xhitVariables[i][t] # for job i sum xijt = sum xjit
            
            yitkList = []
            for k in range(len(yitkVariables[i][t])):
                yitkList += yitkVariables[i][t][k]
            prob += pulp.lpSum(xijtList) + xihtVariables[i][t] == pulp.lpSum(yitkList) # for job i sum xijt = yitk
       
    
'''
A function that adds constraints to the problem.  This constraint is
for all jobs i on day t with time window k, the task can't be finished before
the time window start + the service time, and
the task will finish before the time window end if it is an included task
'''
def addCompletionTimeConstraints(prob, ritkConstants, serviceTimeConstants, 
                                    aitVariables, fitkConstants, latestTimeWindowEnd, yitkVariables,
                                    numTasks, numDays):
    for i in range(numTasks):
        for t in range(numDays):
            for k in range(len(yitkVariables[i][t])):
                prob += (ritkConstants[i][t][k] + serviceTimeConstants[i]) * yitkVariables[i][t][k] <= aitVariables[i][t] # ritk + si <= ait
                prob += aitVariables[i][t] <= fitkConstants[i][t][k] + latestTimeWindowEnd * (1 - yitkVariables[i][t][k]) # ait <= B(1 - yitk)



'''
A function that adds constraints to the problem.  This constraint is
for all pairs of distinct jobs, if job j comes after job i: then job j can't finish
                                before the finish time of job i + the distance between them
                                + the service time of job j
'''        
def addTravelAndServiceTimeConstraints(prob, aitVariables, dijConstants, 
                                            serviceTimeConstants, latestTimeWindowEnd, xijtVariables,
                                            numTasks, numDays):
    for i in range(numTasks):
        for j in range(numTasks):
            if i != j:
                for t in range(numDays):
                    prob += aitVariables[i][t] + dijConstants[i][j] + serviceTimeConstants[j] \
                    <= aitVariables[j][t] + latestTimeWindowEnd * (1 - xijtVariables[i][j][t])

'''
A function that adds constraints that ensure that if there is a task in the schedule
on a given day, there is both a first task for that day and a last task for that day.
'''
def addFirstLastTaskConstraints(prob, numTasks, numDays, xihtVariables, xhitVariables):
    for t in range(numDays):
        xihtList = []
        xhitList = []
        for i in range(numTasks):
            xihtList.append(xihtVariables[i][t])
            xhitList.append(xhitVariables[i][t])
        prob += pulp.lpSum(xihtList) == pulp.lpSum(xhitList)
        prob += pulp.lpSum(xihtList) <= 1
        prob += pulp.lpSum(xhitList) <= 1


def printDebugInfo(prob, yiVariables, yitkVariables, aitVariables, xijtVariables,
    xihtVariables, xhitVariables):
    print
    print prob
    print
    for var in yiVariables:
        print var, var.varValue
    print
    for task in yitkVariables:
        for day in task:
            for windowVar in day:
                print windowVar, windowVar.varValue
    print
    for task in aitVariables:
        for dayVar in task:
            print dayVar, dayVar.varValue
    print
    for i in xijtVariables:
        for j in i:
            for dayVar in j:
                if dayVar != None:
                    print dayVar, dayVar.varValue
    print
    for task in xihtVariables:
        for dayVar in task:
            print dayVar, dayVar.varValue
    print
    for task in xhitVariables:
        for dayVar in task:
            print dayVar, dayVar.varValue
    print


'''
A function that takes a list of tasks and iterates over them,
returning the latest time window ending of any task.
'''
def getLatestDeadline(taskList):
    latestDeadline = 0
    for task in taskList:
        for day in task.timeWindows:
            for timeWindow in day:
                if timeWindow[1] > latestDeadline:
                    latestDeadline = timeWindow[1]
    return latestDeadline


'''
A function that takes a solved integer program and converts it into a makeSchedule
object.
'''
def makeSchedule(yiVariables, yitkVariables, aitVariables, numDays, taskList):
    solvedTaskTuples = [[] for day in range(numDays)]
    for taskIndex, taskVar in enumerate(yiVariables):
        if taskVar.varValue == 1:
            for day in range(numDays):
                for timeWindowVar in yitkVariables[taskIndex][day]:
                    if timeWindowVar.varValue == 1:
                        solvedTaskTuples[day].append((taskList[taskIndex], aitVariables[taskIndex][day].varValue))
    
    for index, day in enumerate(solvedTaskTuples):
        # sort by completion time
        solvedTaskTuples[index] = sorted(day, key = lambda tuple:tuple[1])
    
    solvedTaskList = [[] for day in range(numDays)]
    solvedTaskCompletionTimes = [[] for day in range(numDays)]
    for day in range(numDays):
        for taskTuple in solvedTaskTuples[day]:
            solvedTaskList[day].append(taskTuple[0])
            solvedTaskCompletionTimes[day].append(taskTuple[1])
    
    schedule = Schedule()
    for day in range(numDays):
        route = Route()
        route.setTaskList(solvedTaskList[day], solvedTaskCompletionTimes[day])
        schedule.append(route)
    return schedule


'''
Function that, given a list of tasks, constructs and solves an integer program,
returning the resulting schedule.
'''
def integerProgramSolve(taskList, timeLimit):
    numTasks = len(taskList)
    mostDaysTask = max(taskList, key = lambda task : len(task.timeWindows))
    numDays = len(mostDaysTask.timeWindows)
    latestTimeWindowEnd = getLatestDeadline(taskList)

    yiVariables = [pulp.LpVariable(("y" + str(i)), 0, 1, pulp.LpBinary) for i in range(numTasks)] # included or not
    yitkVariables = makeYitkVariables(taskList, numDays) # task i scheduled on day t in time window k
    aitVariables = makeAitVariables(numTasks, numDays, latestTimeWindowEnd) # completion time
    xijtVariables = makeXijtVariables(numTasks, numDays) # task j scheduled following task i on day t
    xihtVariables, xhitVariables = makeXihtAndXhitVariables(numTasks, numDays) # task i scheduled first/last in the day

    dijConstants = makeDijConstants(taskList)
    priorityConstants = [task.getProfit() for task in taskList]
    fitkConstants = makeFitkConstants(taskList, numDays) # ends of time window k for task i on day t
    ritkConstants = makeRitkConstants(taskList, numDays) # starts of time window k for task i on day t
    serviceTimeConstants = [task.duration for task in taskList]

    # Initialize problem 
    prob = pulp.LpProblem("Scheduling", pulp.LpMaximize)
    # OBJECTIVE FUNCTION
    prob += sum([(yiVariables[i] * priorityConstants[i]) for i in range(len(yiVariables))])


    # Add all constraints
    addJobsAppearOnceConstraints(prob, numDays, numTasks, yiVariables, yitkVariables)

    addConnectivityConstraints(prob, xijtVariables, xihtVariables, xhitVariables, yitkVariables, numTasks, numDays, yiVariables)
    
    addCompletionTimeConstraints(prob, ritkConstants, serviceTimeConstants, 
                                    aitVariables, fitkConstants, latestTimeWindowEnd, yitkVariables,
                                    numTasks, numDays)

    addTravelAndServiceTimeConstraints(prob, aitVariables, dijConstants, 
                                            serviceTimeConstants, latestTimeWindowEnd, xijtVariables,
                                            numTasks, numDays)

    addFirstLastTaskConstraints(prob, numTasks, numDays, xihtVariables, xhitVariables)


    # Gurobi model variables can be set using keyword arguments
    # (https://docs.python.org/2/tutorial/controlflow.html#keyword-arguments)
    # refer to http://www.gurobi.com/documentation/6.0/reference-manual/refman
    # for specific parameter documentation
    # e.g.: solver = pulp.solvers.GUROBI(OutputFlag = 0, Threads = 4, TimeLimit = 120)

    if timeLimit < 0:
        solver = pulp.solvers.GUROBI(OutputFlag = 0)
    else:
        solver = pulp.solvers.GUROBI(OutputFlag = 0, TimeLimit = timeLimit)

    prob.solve(solver)

    # for debugging infeasible models:
    # model = prob.solverModel
    # model.computeIIS()
    # model.write("gurobiModel.ilp")

    # for debugging feasible models:
    # printDebugInfo(prob, yiVariables, yitkVariables, aitVariables, xijtVariables, xihtVariables, xhitVariables)
    
    assert(prob.status == 1) # Problem was solved
    return makeSchedule(yiVariables, yitkVariables, aitVariables, numDays, taskList)

'''
A helper function that does everything but print the solution,
for use in comparing different algorithms.
'''
def runIntegerProgram(csvFile, timeLimit = -1):
    taskList = createTasksFromCsv.getTaskList(csvFile)
    helperFunctions.preprocessTimeWindows(taskList)
    schedule = integerProgramSolve(taskList, timeLimit)
    assert(isFeasible(taskList, schedule))
    return schedule

'''    
A main function that will read in the list of tasks from a csv, construct the integer program,
and print the solution it produces.
'''
def main():
    if len(sys.argv) > 1:
        try:
            timeLimit = int(sys.argv[1])
        except TypeError:
            print "time limit argument not an integer"
            exit()
    else:
        timeLimit = -1
    solvedSchedule = runIntegerProgram("test.csv", timeLimit)
    print
    if timeLimit != -1:
        print "WARNING: As a time limit was set, output may not be optimal."
        print
    print solvedSchedule
    print
    print "profit is: " + str(solvedSchedule.getProfit())
    print


if __name__ == '__main__':
    main()
