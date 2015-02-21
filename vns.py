# Comps 2014
# Larkin Flodin, Avery Johnson, Maraki Ketema, 
# Abby Lewis, Will Schifeling, and  Alex Trautman

import greedyByPresentChoice
import greedyByOrder
# import integerProgram
import createTasksFromCsv
import helperFunctions
import Objects
import time
import math
import random
import copy
import csv
from createTests import dayLength
from collections import deque
import sys, os

# Number of seconds VNS is allowed to run

# random.seed(211680280677)


'''
@return: an ordering of tasks
'''
def solve(csvFile, stoppingCondition):
    
    global schedSteps
    
    
    # keep track of the schedules as vns progresses
    schedSteps = []
    
    # Get a greedy algorithm to then modify with VNS
    taskList = createTasksFromCsv.getTaskList(csvFile)
    helperFunctions.preprocessTimeWindows(taskList)
    
    greedyByPrioritySol = greedyByOrder.runGreedyByOrder(csvFile, greedyByOrder.orderByPriority)
    greedyByPriorityAvailabilitySol = greedyByOrder.runGreedyByOrder(csvFile, greedyByOrder.orderByPriorityOverAvailability)
    greedyByDeadlineSol = greedyByOrder.runGreedyByOrder(csvFile, greedyByOrder.orderOptionalByDeadline)
    greedyByPresentChoiceSol = greedyByPresentChoice.runGreedyByPresentChoice(csvFile)
    solutionList = [greedyByPrioritySol, greedyByPriorityAvailabilitySol, greedyByDeadlineSol, greedyByPresentChoiceSol]
    bestGreedy = max(solutionList, key=lambda schedule : schedule.getProfit())
    incumbentProfit = bestGreedy.getProfit()

    appendToSchedSteps("Initial schedule to be improved by VNS", bestGreedy)
            
    assert(isFeasible(taskList, bestGreedy))
    # print bestGreedy
    
    modTasks = bestGreedy[:]
    currSchedule = createSchedule(copy.deepcopy(bestGreedy))
    bestGreedy.resetEndingTimes()
    # Modify the greedy algorithm
    currSchedule = vns(taskList, currSchedule, stoppingCondition)
    assert(isFeasible(taskList, currSchedule)) 
    for r in range(len(bestGreedy)):
        route = bestGreedy[r]
        isRouteActuallyFeasible(route, r, "after VNS run")    

    
    print "Profit of Greedy Schedule is: "
    print bestGreedy.getProfit()
    print "Profit of VNS Schedule is: "
    print currSchedule.getProfit()
    


    return currSchedule, schedSteps, incumbentProfit

'''
@return: best schedule found in time limit
'''
def vns(taskList, currSchedule, stoppingCondition):
    
#     print "********** Entering VNS **********"


    global unplannedTasks
    global prevUnplanned
    global routesModified
    routesModified = []
    
    unplannedTasks = deque(taskList[:])
   
    for day in currSchedule:
        for task in day:
            unplannedTasks.remove(task)
    
    # Number of neighborhood structures
    nHoodMax = 17
    
    # Number of iterations since last bestSolution update
    numIterations = 0
    
    currSchedule = isFeasible(taskList, currSchedule)
    
    currSchedule.resetEndingTimes()
    
    for r in range(len(currSchedule)):
        route = currSchedule[r]
        isRouteActuallyFeasible(route, r,"After first call to isFeasible from VNS")
        
    if currSchedule == None:
        print "Your incumbent solution is infeasible, try again"
        exit(1)
    
    currSchedule.resetEndingTimes
    bestSchedule = currSchedule
    
    initTime = time.time()
    
    iterCount = 0
    
    # until the stopping condition is met
    while time.time() - initTime < stoppingCondition:
        # If we have gone through all neighborhood structures, start again
        nHood = 1
#         appendToSchedSteps("OUTSIDE vns little while loop", currSchedule)
        
        while nHood < nHoodMax and time.time() - initTime < stoppingCondition:
            currSchedule = copy.deepcopy(currSchedule)
            currSchedule.resetEndingTimes()
            prevUnplanned = copy.deepcopy(unplannedTasks)
            
            iterCount += 1
            
            appendToSchedSteps("Schedule before shaking", currSchedule)
            
            shakeSolution = shaking(currSchedule, nHood)
            
            appendToSchedSteps("Schedule after shaking, before iterative improvement", shakeSolution)
            
            iterSolution = iterativeImprovement(taskList, shakeSolution, nHood)
            
            appendToSchedSteps("Schedule after iterativeImprovent", iterSolution)
            

            # make sure the modified solution is still feasible. 
            # If it is not, try again
            # If it is, and it is a better solution, update bestSolution
            
            appendToSchedSteps("Schedule after iterative improvement, before checking Feasibility", iterSolution)
            feasibleSchedule = isFeasible(taskList, iterSolution)
#             appendToSchedSteps("Sched after isFeasible", feasibleSchedule)
            
            
            # if feasible and better
            #     accept it as the new solution, reset nHood of numIterations
            
            if (feasibleSchedule != None):

                # If our solution is better than the current solution, update.
                if isBetterSchedule(feasibleSchedule, currSchedule):
                    currSchedule = feasibleSchedule
                    appendToSchedSteps("We have found a BETTER schedule!", currSchedule)
                    nHood = 1
                # Otherwise, increment nHood
                else:
                    appendToSchedSteps("Our schedule is WORSE than our best so far", currSchedule)
                    nHood += 1
                
                # If our solution is better than the best solution so far, update.
                if isBetterSchedule(feasibleSchedule, bestSchedule):
                    bestSchedule = feasibleSchedule
                    numIterations = 0
                    
                # If we have gone 8000 iterations with no improvement to bestSolution
                # If criteria for selection are true, select a new currSchedule
                elif numIterations > 8000:
                    numIterations = 0
                    
                    if nHood > 8:
                        appendToSchedSteps("Our schedule is not better, but we have iterated 8000 times", feasibleSchedule)
                        currSchedule = feasibleSchedule
                        nHood = 1
                        unplannedTasks = prevUnplanned
                        
                    # Criteria for nHoods 1-8:
                    # If the new solution is not more than .5% longer (distance), accept
                    elif calcTotalDistance(iterSolution) >= .995 * calcTotalDistance(currSchedule):
                        currSchedule = feasibleSchedule
                        appendToSchedSteps("Our schedule is not better but we have iterated 8000 times and the new solution isn't too long", currSchedule)
                        unplannedTasks = prevUnplanned
                else:
                    appendToSchedSteps("Schedule was NONE", feasibleSchedule)
                    numIterations += 1 
                    unplannedTasks = prevUnplanned
            else:
                numIterations += 1
                unplannedTasks = prevUnplanned
                nHood += 1

    for r in range(len(bestSchedule)):
        route = bestSchedule[r]
        isRouteActuallyFeasible(route, r, "end of VNS")
#    print "********** Exiting VNS **********"
    
    return bestSchedule


'''
@return: modified solution
'''
def shaking(currSchedule, nHood):
#     print "********** Entering shaking **********"
       
    currSchedule = copy.deepcopy(currSchedule)
    
    # Based on the neighborhood perform a different operation
    if nHood < 8:
        newSchedule = crossExchange(currSchedule, nHood)
        
    elif nHood >= 8 and nHood <= 12:
        newSchedule = optionalExchange1(currSchedule, nHood)
        
    else:
        newSchedule = optionalExchange2(currSchedule, nHood)
    
#     appendToSchedSteps("Finished shaking", newSchedule)
#     print "********** Exiting shaking **********"
    return newSchedule

'''
@param currSchedule: list (schedule) of lists (days/routes) of task objects
@return: modified schedule
'''
def crossExchange(currSchedule, nHood):
#     print "********** Entering crossExchange **********"
    
    currSchedule = copy.deepcopy(currSchedule)
    
    if len(currSchedule) <= 1:
#         print "********** Exiting crossExchange **********"
        return currSchedule
    
    # choose two distinct random days
    day1 = random.randint(0, len(currSchedule) - 1)
    day2 = random.randint(0, len(currSchedule) - 1)
    while (day1 == day2):
        day2 = random.randint(0, len(currSchedule) - 1)
        
    # find the length of the routes:
    len1 = len(currSchedule[day1])
    len2 = len(currSchedule[day2])
    
    # for route1 (removed and inserted into day2)
    if len1 == 0:
        route1Len = 0
    else:
        route1Len = random.randint(1, min(len1, nHood))
    # for route2 (removed and inserted into day1)
    if len2 == 0:
        route2Len = 0
    else:
        route2Len = random.randint(0, min(len2, nHood))
    
#     appendToSchedSteps("Swapping parts of routes %d and %d in CROSS EXCHANGE" %(day1, day2), currSchedule)
#     appendToSchedSteps("route %d, len %d, route %d, len %d" %(day1, route1Len, day2, route2Len), currSchedule)
    
    routeSegment1 = getRouteSegment(currSchedule, day1, day2, route1Len)
    routeSegment2 = getRouteSegment(currSchedule, day2, day1, route2Len)

    route1Start, route1End = routeSegment1[0], routeSegment1[1]
    route2Start, route2End = routeSegment2[0], routeSegment2[1]
    
#     appendToSchedSteps("route %d start %d end %d" %(day1, route1Start, route1End), currSchedule)
#     appendToSchedSteps("route %d start %d end %d" %(day2, route2Start, route2End), currSchedule)
    
    if route1End - route1Start == 0 and route2End - route2Start == 0:
        return currSchedule 

    route1 = currSchedule[day1][route1Start : route1End]
    route2 = currSchedule[day2][route2Start : route2End]
    
    tasks1 = currSchedule[day1][:route1Start] + route2 + currSchedule[day1][route1End:]
    tasks2 = currSchedule[day2][:route2Start] + route1 + currSchedule[day2][route2End:]

    # setting route and  new day to be what they should be
    newDay1 = Objects.Route()
    newDay1.setTaskList(tasks1, [None] * len(tasks1))
    
    # starting index of the sub-route we will be removing
    newDay2 = Objects.Route()
    newDay2.setTaskList(tasks2, [None] * len(tasks2))
    
#     appendToSchedSteps("new day %d" %(day1), newDay1, day1)
#     appendToSchedSteps("new day %d" %(day2), newDay2, day2)
    
    for task in route2:
        unplannedTasks.append(task)
    
    # remove route1 from day1, remove route2 from day2, insert route1 into day2 where route2 was
    currSchedule[day1] = newDay1
    currSchedule[day2] = newDay2
    
    for i in range(len(routesModified)):
        routesModified.pop()
    routesModified.append(day1)
    routesModified.append(day2)
    
#     print "********** Exiting crossExchange **********"
    appendToSchedSteps("At the end of CROSS EXCHANGE", currSchedule)
    return currSchedule

'''
Select random segment of tasks within a given day and route
such that those tasks all have time windows in a new day
@return start and end index tuple of route segment
'''
def getRouteSegment(currSchedule, origDay, newDay, segmentLength):
    n = 0

    # whole route for day one
    origRoute = currSchedule[origDay]
    # start index of the current route we are looking at 
    currRouteStart = 0
    # start index of the longest route
    longestRouteStart = 0
    # length of longest route 
    longestRouteLen = 0
    
    # list of possible start indices for routes in day 1 of valid length s.t each task has a time window in day 2 
    possRoutes = []
    
    # origRoute: choose random segment w/ customers who have a valid time window in newDay
    # if there is no such route, choose the longest route.
    while n < len(origRoute):
        # checking to see if the current route is longer than longest route, if it is update 
        # longest route start and length
        if (n - currRouteStart) > longestRouteLen:
            longestRouteStart = currRouteStart
            longestRouteLen = n - currRouteStart
        
        # if task n has a valid time window in day 2, check to see if the route from curr start to n is 
        # long enough, if so add it to possible list of routes
        
        if len(origRoute[n].timeWindows[newDay]) > 0 :
            if n - currRouteStart == segmentLength - 1:
                possRoutes.append(currRouteStart)
                currRouteStart += 1
        # move on to the next route if previous conditional statement was no satisfied 
        else:
            currRouteStart = n + 1
        n += 1
    
    # if we found a viable route, choose a random one 
    if len(possRoutes) > 1:
        route1Start = possRoutes[random.randint(0, len(possRoutes) - 1)]
    # if there is only one, choose that one
    elif len(possRoutes) == 1:
        route1Start = possRoutes[0]
    # otherwise choose longest 
    else:
        route1Start = longestRouteStart
        segmentLength = longestRouteLen
    
    return (route1Start, route1Start + segmentLength)
    
    
'''
Selects a random day, removes some tasks, and adds some other unplanned tasks to that day
@return: modified schedule
'''
def optionalExchange1(currSchedule, nHood):
#     print "********** Entering optExchange1**********"
#     print currSchedule
#     printUnplanned()
    
    # select the number of tasks to remove and add from unplanned according to nHood Index
    numToRemove = nHood - 9
    numToAdd = 1
    
    if nHood == 12:
        numToRemove = 0
        numToAdd = 2

    # pick a random day and starting time to exchange customers
    day = random.randint(0, len(currSchedule) - 1)
    
    pos = random.randint(0, len(currSchedule[day]))
    
    if numToRemove > 0:
        required = []
        # using the numToRemove and numToAdd values, add and remove however many customers you need to
        for task in currSchedule[day][pos:pos + numToRemove]:
            if task.required == 0:
                unplannedTasks.append(task)
            else:
                required.append(task)
        newDay = currSchedule[day][:pos] + required + currSchedule[day][pos + numToRemove:]
        
    else:
        newDay = currSchedule[day][:]

    # selecting which unplanned tasks to add
    addingTasks = []
    t = 0
    firstNotAdded = -1
    if len(unplannedTasks) > 0:
        popped = unplannedTasks.popleft()
    while t < numToAdd and len(unplannedTasks) > 0 and firstNotAdded != popped.id:
        firstNotAdded = popped.id
        if len(popped.timeWindows[day]) > 0:
            addingTasks.append(popped)
            popped = unplannedTasks.popleft()
            t += 1
        else:
            unplannedTasks.append(popped)
        updatePrevUnplanned(popped)
          
    # adding new tasks to day 
    newDay = newDay[:pos] + addingTasks + newDay[pos:]
    
    newRoute = Objects.Route()
    
    for task in newDay:
        newRoute.append(task, None)
    
     # replace the chosen days with the updated days   
    currSchedule[day] = newRoute
    
    for i in range(len(routesModified)):
        routesModified.pop()
    routesModified.append(day)
    
#     print "********** Exiting optExchange1 **********"
    appendToSchedSteps("At the end of OPTIONAL EXCHANGE 1", currSchedule)

    return currSchedule

'''
Removes tasks from a random day/position and adds removed tasks to unplanned tasks. 
@return: modified solution
'''
def optionalExchange2(currSchedule, nHood):
#     print "********** Entering optExchange2 **********"

    currSchedule = copy.deepcopy(currSchedule)
    
    # pick a random day and position
    
    # pick a random day and starting time to exchange customers
    day = random.randint(0, len(currSchedule) - 1)
    
    # calculate number to remove (nHood-12)
    numToRemove = min(nHood - 12, len(currSchedule[day]) - 1)
    
    if len(currSchedule[day]) - numToRemove - 1 == 0:
        pos = 0
    else:
        pos = random.randint(0, len(currSchedule[day]) - numToRemove - 1)
    
    
    required = []
    # using the numToRemove value, remove however many customers you need to
    for task in currSchedule[day][pos:pos + numToRemove]:
        if task.required == 0:
            unplannedTasks.append(task)
        else:
            required.append(task)

    newDay = currSchedule[day][:pos] + required + currSchedule[day][pos + numToRemove:]

    newRoute = Objects.Route()
    for task in newDay:
        newRoute.append(task, None)

    currSchedule[day] = newRoute
    
#     print "********** Exiting optExchange2 **********"
    
    for i in range(len(routesModified)):
        routesModified.pop()
    
    routesModified.append(day)
    
    appendToSchedSteps("At the end of OPTIONAL EXCHANGE 2", currSchedule)
    return currSchedule


'''
@return: modified solution
'''
def iterativeImprovement(taskList, currSchedule, nHood):
#     print "********** Entering iterativeImprovement **********"

    # If nHood< 13: do 3-OPT
    if nHood < 13:
        # only currSchedule because we believe edges are being removed and inserted within the solution
        newSchedule = threeOPT(taskList, currSchedule)

    # Otherwise: Best Insertion
    else:
        newSchedule = bestInsertion(taskList, currSchedule)

#     print "********** Exiting iterativeImprovement **********"
#     appendToSchedSteps("At the end of iterative improvement", newSchedule)
    return newSchedule  
'''
@return: solution that has been modified by 3-Opt
'''
def threeOPT(taskList, currSchedule):
#     print "********** Entering threeOPT **********"
#     appendToSchedSteps("About to  start 3-OPT", currSchedule)
#     appendToSchedSteps("routesModed for 3opt, %s" %(str(routesModified)), currSchedule)

    currSchedule = copy.deepcopy(currSchedule)
    
    # generate a list of all routes that are longer than 3
    possRoutes = []
    for r in range(len(routesModified)):
        routeIndex = routesModified[r]
        if len(currSchedule[routeIndex]) > 3:
            possRoutes.append(routeIndex)
            
    # If there are no such routes, give up.
    if len(possRoutes) == 0:
#         appendToSchedSteps("sched too short in threeOPT", currSchedule)
        return currSchedule
    
    # pick a random day from those routes
    day = possRoutes[random.randint(0, len(possRoutes) - 1)]
    currRoute = currSchedule[day]
    
    # Set the initial length and feasibility to the duration of the route
    # and the current feasibility.
    currLength, currFeasibility = getRouteDurationWithFeasibility(currRoute, day, taskList)
    numTasks = len(currRoute)
    
#     appendToSchedSteps("Working with route %d in 3OPT, numTasks %d" %(day, numTasks), currRoute, day)
    
    # swap sections of 3 or less from k to j with segments from j+1 to n
    for k in range(numTasks - 2):
        topRange = min(k + 4, numTasks - 2)
        for j in range(k + 1, topRange):
            
            #switch the segments to get the new route
            newRoute = switchChains(k, j, currRoute)
            
            #calculate the duration and feasibility of the new route
            newLength, newFeasibility = getRouteDurationWithFeasibility(newRoute, day, taskList)
            
            if newRouteDominates(currLength, currFeasibility, newLength, newFeasibility):
                currSchedule[day] = newRoute
#                     print "********** Exiting threeOPT ***************"   
#                 appendToSchedSteps("Found a better route in 3-OPT", currSchedule)
    
                return currSchedule
            
    appendToSchedSteps("No better schedule found in 3-OPT", currSchedule)
#     print "********** Exiting threeOPT ***************"       
    return currSchedule

'''
check to see if the new route dominates the old route
'''
def newRouteDominates(currLen, currFeas, newLen, newFeas):
    if currLen >= newLen and newFeas <= currFeas:
        if newLen < currLen or newFeas < currFeas:
            return True
    return False

def switchChains(k, j, currRoute):
    newRoute = copy.deepcopy(currRoute)
    chain1 = newRoute[0:k + 1]
    chain2 = newRoute[k + 1:j + 1]
    chain3 = newRoute[j + 1:len(currRoute)]
    newTaskList = chain1 + chain3 + chain2
    newRoute.setTaskList(newTaskList, [None] * len(newTaskList))
    return newRoute

'''
@return: solution that has been modified by 3-Opt
'''
def bestInsertion(taskList, currSchedule):
#     print "********** Entering bestInsertion **********"
    appendToSchedSteps("Entering bestInsertion", currSchedule)
    currSchedule = copy.deepcopy(currSchedule)

    # Keep track of the first task we try to add, stop if we try to add it again
    if len(unplannedTasks) == 0:
        appendToSchedSteps("Exiting bestInsertion: unplannedTasks" + str(unplannedTasks), currSchedule)
        return currSchedule
    currTask = unplannedTasks.popleft()
    firstTaskID = currTask.id
    firstTime = True
    
    # While this is or our first iteration or the current task isn't the first one we tried to add
    while firstTime or firstTaskID != currTask.id:
        
        # It's no longer the first time and update prevUnplanned
        firstTime = False
        updatePrevUnplanned(currTask)
        
        # Initialize the bestAdditionalDistance and bestSpot
        # This is the smallest added distance the current task can add
        bestAdditionalDistance = float("inf")
        # This is the best spot for the current task to be added (route, spot in route)
        bestSpot = [-1, -1]
        foundSpot = False
        
        # For each route in the schedule
        for routeIndex in range(len(currSchedule)):
            
            # Set the current route
            route = currSchedule[routeIndex]
            
            if len(currTask.timeWindows[routeIndex]) == 0:
                break
            
            if len(route) > 0:
                # Try adding the current unplanned task at location 0
                # Get the distance from current unplanned to the original first task
                dist = helperFunctions.getDistanceBetweenTasks(currTask, route[0])

            else:
                dist = 0
            
            # If this distance is better than what we have found before, update our variables
            if dist < bestAdditionalDistance:
                bestAdditionalDistance = dist
                bestSpot = [routeIndex, 0]
                foundSpot = True
            
            # For each additional spot in the route calculate the distance added from adding that task
            for t in range(1, len(route)):
                # Get the next task
                task = route[t]
                
                # Calculate the additional distance needed by adding in the task at this location
                
                # Get the distance from the original task to the new unplanned task
                dist = helperFunctions.getDistanceBetweenTasks(currTask, task)
                
                # Add the distance from the current unplanned task to the next planned task
                dist += helperFunctions.getDistanceBetweenTasks(currTask, route[t - 1])
                
                # Subtract the distance from the original two tasks
                dist -= helperFunctions.getDistanceBetweenTasks(task, route[t - 1])
                
                # If we have found a better distance and thus spot, update
                if dist < bestAdditionalDistance:
                    bestAdditionalDistance = dist
                    bestSpot = [routeIndex, t]
            
            if len(route) >= 1:
                # Check the distance of adding the unplanned task to the end
                dist = helperFunctions.getDistanceBetweenTasks(currTask, route[-1])
            
                # If we have found a better distance and thus spot, update
                if dist < bestAdditionalDistance:
                    bestAdditionalDistance = dist
                    bestSpot = [routeIndex, len(route)]
                    foundSpot = True
        
#         print "best spot for task", currTask.id, "is", bestSpot
        
        # Create the new route with the added unplanned task
        newRoute = copy.deepcopy(currSchedule[bestSpot[0]])
        newRoute.taskList = newRoute.taskList[:bestSpot[1]] + [currTask] + newRoute.taskList[bestSpot[1]:]
        newRoute.resetEndingTimes()
        
        # If that new route is under the dayLength, put it back in the schedule
        if isRouteUnderTimeLimit(newRoute) and foundSpot:
            currSchedule[bestSpot[0]] = newRoute
            if len(unplannedTasks) == 0:
                break
            currTask = unplannedTasks.popleft()
            firstTaskID = currTask.id
            
        
        # If we did not find a place for this unplannedTask, increment counter and add it back to unplanned
        else:
            unplannedTasks.append(currTask)
            currTask = unplannedTasks.popleft()

            
        # Get the next unplanned task
    appendToSchedSteps("Finished bestInsertion", currSchedule)
#     print "********** Exiting bestInsertion **********"
    return currSchedule

def isRouteUnderTimeLimit(route):
    totalTime = 0
    
    if len(route) == 0:
        return True
    
    for t in range(len(route) - 1):
        task = route[t]
        totalTime += task.duration
        totalTime += helperFunctions.getDistanceBetweenTasks(task, route[t + 1])
    
    totalTime += route[-1].duration    
    
    return totalTime < dayLength

def isFeasible(taskList, currSchedule):
#     print "********** Entering isFeasible **********"
    appendToSchedSteps("Beginning to check feasibility", currSchedule)

    currSchedule = copy.deepcopy(currSchedule)
    newSchedule = copy.deepcopy(currSchedule)
    for r in range(len(currSchedule)):
        newRoute, infeas = isRouteFeasible(currSchedule[r], r)
        if infeas > 0 or newRoute == None:
#             print "********** Exiting isFeasible **********"
            return None
        else:
            newSchedule[r] = newRoute
#     appendToSchedSteps("Before minRoute:", newSchedule)

    for r in range(len(newSchedule)):
        newSchedule[r] = minRoute(taskList, newSchedule[r], r)

    appendToSchedSteps("At the end of isFeasible", newSchedule)
    #     print "********** Exiting isFeasible **********"
    return newSchedule

def isRouteFeasible(currRoute, routeIndex):
#     print "********** Entering isRouteFeasible **********"
    currRoute = copy.deepcopy(currRoute)
#     appendToSchedSteps("Beginning route feasibility check", currRoute, routeIndex)

    # for each task except the first, add travel time from prev task to curr task
    # to the duration of task, then subtract that same time from each time window
    # start, and from release time.
    for t in range(1, len(currRoute)):
        task = currRoute[t]

        # include travel time in these duplicate tasks. (added to duration of task,
        # subtract from release time and time window starts)
        travelTime = helperFunctions.getDistanceBetweenTasks(task, currRoute[t - 1])
        task.duration = task.duration + travelTime
        
        task.releaseTime = task.releaseTime - travelTime
        for tw in range(len(task.timeWindows[routeIndex])):
            oldTW = task.timeWindows[routeIndex][tw]
            newTW = (int(math.floor(oldTW[0] - travelTime)), oldTW[1])
            task.timeWindows[routeIndex][tw] = newTW
#     appendToSchedSteps("Added travel time to route %d" % (routeIndex), currRoute, routeIndex)
    oldRoute = copy.deepcopy(currRoute)
    
    currRoute = tightenTWStarts(currRoute, routeIndex)
    currRoute = tightenTWEnds(currRoute, routeIndex)
    
    if currRoute != None:
#         print "********** Exiting isRouteFeasible1 **********"
        return currRoute, 0
    
    currRoute = oldRoute
    
    routeLen, infeas = calcLengthOfInfeasibleRoute(currRoute, routeIndex)


#     print "********** Exiting isRouteFeasible2 **********"
#     appendToSchedSteps("Route %d is NOT FEASIBLE after tightening, return None"  %(routeIndex), currRoute, routeIndex)
    return None, infeas
                    
'''
This function, used by threeOPT, calculates the best length of this
schedule, even if it is infeasible, and returns both the length and
the infeasibility.
'''
def getRouteDurationWithFeasibility(route, routeIndex, taskList):
    currRoute = copy.deepcopy(route)
    
    currRoute = isRouteFeasible(currRoute, routeIndex)[0]
    if currRoute == None:
        currRoute = copy.deepcopy(route)
#         appendToSchedSteps("getting length of infeasible route", currRoute, routeIndex)
        return calcLengthOfInfeasibleRoute(currRoute, routeIndex)
    
    currRoute = minRoute(taskList, currRoute, routeIndex)
    
    routeLen = currRoute.endingTimes[-1] - currRoute.endingTimes[0] + currRoute.taskList[0].duration
    
    currRoute.resetEndingTimes
    return routeLen, 0

                    
'''
Given an infeasible route, this schedules each task as early as possible
to find the duration and infeasibility of this route, scheduled. 
@param route: an infeasible route
@param routeIndex: the index of that route
@return: the duration of route, scheduled as early as possible
@return: the infeasibility value of the route  
'''
def calcLengthOfInfeasibleRoute(route, routeIndex):
    infeas = 0
    lastTaskEnd = route[0].releaseTime
    
    # find proper time window for this task (after end of last task)
    # if not available, add all of duration to infeas
    # if available but it doesn't fit, put the task as early as possible within tw,
    # add any duration spent outside of tw to infeas
    first = True
    start = lastTaskEnd
    for t in range(len(route)):
        task = route[t]
        timeWindows = task.timeWindows[routeIndex]
        selectedIndex = None
        for tw in range(len(timeWindows)):
            if timeWindows[tw][1] > lastTaskEnd:
                selectedIndex = tw
                break
        if selectedIndex == None:
            infeas += task.duration
            lastTaskEnd = lastTaskEnd + task.duration
            route.endingTimes[t] = lastTaskEnd
            first = False
        else:
            selectedTW = timeWindows[selectedIndex]
            if max(lastTaskEnd, selectedTW[0]) + task.duration > selectedTW[1]:
                infeas += max(lastTaskEnd, selectedTW[0]) + task.duration - selectedTW[1]
            lastTaskEnd = max(lastTaskEnd, selectedTW[0]) + task.duration
            route.endingTimes[t] = lastTaskEnd
        if first:
            start = lastTaskEnd - task.duration
            first = False
    return lastTaskEnd - start, infeas
            
    
'''
@return: modified schedule with tightened tw starts
'''
def tightenTWStarts(currRoute, routeIndex):
#     print "********** Entering tightenTWStarts **********"
    currRoute = copy.deepcopy(currRoute)
    
    if currRoute == None:
#         print "********** Exiting tightenTWStarts 1 **********"
        return None
    if len(currRoute) == 0:
        return currRoute
    
    taskIndex = 0
    task = currRoute.taskList[taskIndex]
    tw = task.timeWindows[routeIndex]
    
    while taskIndex < len(currRoute) - 1 and len(currRoute.taskList[taskIndex].timeWindows[routeIndex]) > 0 :
        task = currRoute.taskList[taskIndex]
        tw = task.timeWindows[routeIndex]
        twNext = currRoute.taskList[taskIndex + 1].timeWindows[routeIndex]
         # if duration of task i does not fit in its first tw or it can fit between the start of its second time window
         #  and the start of the next task's first tw
        if (len(tw) > 0 and len(twNext) > 0) and ((task.duration > tw[0][1] - tw[0][0]) or\
         (len(tw) > 1 and (task.duration + tw[1][0] < twNext[0][0]))):
            # remove that task's first tw
            tw = tw[1:]
            task.timeWindows[routeIndex] = tw
            if len(tw) == 0:
                break
        else:
            # if duration of task i at the start of its first tw ends before the start of the next task's first tw
            if len(tw) > 0 and len(twNext) > 0 and task.duration + tw[0][0] < twNext[0][0]:
                # resetting tw start: no overlap
                
                # set the beginning of that time window to be the minimum of the the ending time of task i's first time window
                # and the start of task i+1's first time window
                tw[0] = (min(twNext[0][0], tw[0][1]) - task.duration, tw[0][1])
                
            # elif the duration of task i set at the beginning of its first tw overlaps any tws for the next task
            elif len(tw) > 0 and len(twNext) > 0 and task.duration + tw[0][0] > twNext[0][0]:
                # resetting twNext starts: overlap
                # reset the beginnings of all time windows to be as early as possible
                # after the end of task i (with i scheduled as early as possible)
                for w in range(len(twNext)):
                    twNext[w] = (max(tw[0][0] + task.duration, twNext[w][0]), twNext[w][1])
            
            task.timeWindows[routeIndex] = tw
            currRoute.taskList[taskIndex + 1].timeWindows[routeIndex] = twNext
            
            taskIndex += 1
    
    task = currRoute.taskList[taskIndex]
    tw = task.timeWindows[routeIndex] 
    
    if taskIndex == len(currRoute) - 1 and len(currRoute.taskList[taskIndex].timeWindows[routeIndex]) > 0 and task.duration > tw[0][1] - tw[0][0]:
            # remove that task's first tw
            tw = tw[1:]
            task.timeWindows[routeIndex] = tw
    
    for task in currRoute:
        removeBadTimeWindows(task, routeIndex)
    
    if taskIndex < len(currRoute.taskList) - 1 or anyEmptyTWLists(currRoute, routeIndex):
        # print "********** Exiting tightenTWStarts 2 **********"
        
        return None
    # print "********** Exiting tightenTWStarts 3 **********"
#     appendToSchedSteps("Route %d is FEASIBLE after tightening time window STARTS" % (routeIndex), currRoute, routeIndex)
    return currRoute

'''
@return: modified schedule with tightened tw ends
'''
def tightenTWEnds(currRoute, routeIndex):
#     print "********** Entering tightenTWEnds **********"
    currRoute = copy.deepcopy(currRoute)


    if currRoute == None:
#         print "********** Exiting tightenTWEnds1 **********"
        return None
    if len(currRoute) == 0:
        return currRoute
    
    taskIndex = len(currRoute.taskList) - 1
    task = currRoute.taskList[taskIndex]
    tw = task.timeWindows[routeIndex]
    while taskIndex > 0 and len(currRoute.taskList[taskIndex].timeWindows[routeIndex]) > 0:
        
        task = currRoute.taskList[taskIndex]
        
        tw = task.timeWindows[routeIndex]
        
        twPrev = currRoute.taskList[taskIndex - 1].timeWindows[routeIndex]
        
        # print "route[" + str(taskIndex) + "] =", task.id
        # print "Initial tw =", tw
        # print "prevTW =", twPrev
        
        # if duration of task i does not fit in its last tw or it can fit between the end of its second to last time w
        #  and the end of the previous task's last tw:
        
        if (task.duration > tw[-1][1] - tw[-1][0]) or (len(tw) > 1 and task.duration + tw[-2][0] < twPrev[-1][0]):
            tw = tw[:-1]
            # print "tw after remove:", tw
            task.timeWindows[routeIndex] = tw
            if len(tw) == 0:
                # print "\tExiting on task:", taskIndex
                break
            
            task.timeWindows[routeIndex] = tw
            currRoute.taskList[taskIndex - 1].timeWindows[routeIndex] = twPrev
            
        else:
            # if duration of task i at the end of its last tw starts before the end of the previous task's last tw
            if len(tw) > 0 and len(twPrev) > 0 and tw[-1][1] - task.duration > twPrev[-1][1]:
                # resetting twPrev ends: no overlap
                # set the end of that tw to be the maximum of the the starting time of task i's last time w
                # and the end of task i-1's last time w
                oldTW = (tw[-1][0], tw[-1][1])
                tw[-1] = (tw[-1][0], max(twPrev[-1][1], tw[-1][0]) + task.duration)
                task.timeWindows[routeIndex] = tw
                currRoute.taskList[taskIndex - 1].timeWindows[routeIndex] = twPrev
            # if the duration of task i set at the end of its last tw overlaps any tws for the previous customer
            elif len(tw) > 0 and len(twPrev) > 0 and tw[-1][1] - task.duration < twPrev[-1][1]:
                # resetting twPrev ends: overlap"
                # reset the endings of all time windows to be as late as possible
                # before the beginning of task i (with i scheduled as late as possible)
                w = 0
                while w < len(twPrev):
                    twPrev[w] = (twPrev[w][0], min(tw[-1][1] - task.duration, twPrev[w][1]))
                    if twPrev[w][1] < twPrev[w][0]:
                        twPrev = twPrev[:w] + twPrev[w+1:]
                    else:
                        w += 1

            task.timeWindows[routeIndex] = tw
            currRoute.taskList[taskIndex - 1].timeWindows[routeIndex] = twPrev
            taskIndex -= 1
        
    task = currRoute.taskList[taskIndex]
    tw = task.timeWindows[routeIndex]
    twIndex = 0
    
    if taskIndex == len(currRoute) - 1 and len(currRoute.taskList[taskIndex].timeWindows[routeIndex]) > 0 and task.duration > tw[0][1] - tw[0][0]:
           # remove that task's first tw
           tw = tw[1:]
           task.timeWindows[routeIndex] = tw
    
    for task in currRoute:
        removeBadTimeWindows(task, routeIndex)
    
    if taskIndex > 0 or anyEmptyTWLists(currRoute, routeIndex):
#         print "********** Exiting tightenTWEnds2 **********"
        return None
    
#     print "********** Exiting tightenTWEnds3 **********"
#     appendToSchedSteps("Route %d is FEASIBLE after tightening time window ENDS" % (routeIndex), currRoute, routeIndex)
    return currRoute

def removeBadTimeWindows(task, routeIndex):
    timeWindows = task.timeWindows[routeIndex]
    tw = 0
    while tw < len(timeWindows):
        timeWindow = timeWindows[tw]
        if timeWindow[1] < timeWindow[0] + task.duration:
            timeWindows = timeWindows[:tw] + timeWindows[tw+1:]
        else:
            tw += 1
    task.timeWindows[routeIndex] = timeWindows

def anyEmptyTWLists(route, routeIndex):
    for t in range(len(route)):  
        task = route[t]
        if len(task.timeWindows[routeIndex]) < 1:
            # print "THE TWS for task", task.id, "was EMPTY"
            return True
    return False

'''
@return: shortest duration of this schedule ordering
'''
def minRoute(taskList, currRoute, routeIndex):
#     print "********** Entering minRoute **********"
    appendToSchedSteps("Entering minRoute on route %d"%(routeIndex), currRoute, routeIndex)

    bestRoute = copy.deepcopy(currRoute)
    
    
    # Minimize each route
    
    if len(currRoute) == 0:
        return resetTasks(currRoute, taskList)
    
    # keep track of what tw index each task has been assigned
    assignedTWs = [0] * len(currRoute)        
    
    # set the ending times for each task in the route by scheduling
    # all tasks as early as possible (start at the beginning of the
    # first time window. This is feasible because of preprocessing
    for t in range(len(currRoute)):
        task = currRoute[t]
        
        currRoute.endingTimes[t] = task.duration + task.timeWindows[routeIndex][0][0]
 
    # Find the dominant version of this route (shortest possible route
    # with this ending time.
    
    latestWaitingTask = getLatestWaitingTask(currRoute)
    if latestWaitingTask == -1:
        return resetTasks(currRoute, taskList)
    
    appendToSchedSteps("Route before first domRout", bestRoute, routeIndex)
    bestRoute = dominantRoute(currRoute, assignedTWs, routeIndex)

    latestWaitingTask = getLatestWaitingTask(bestRoute)
    appendToSchedSteps("Route before minRoute while", bestRoute, routeIndex)

    # While this there are still tasks with waiting time and the latest
    # waiting task has time windows to switch to
    while latestWaitingTask > -1 and assignedTWs[latestWaitingTask] < len(currRoute[latestWaitingTask].timeWindows[routeIndex]) - 1:
        
        # move the latest waiting task to its next time window.
        appendToSchedSteps("Route BEFORE switchTimeWindows in minRoute", bestRoute, routeIndex)
        newRoute = switchTimeWindows(bestRoute, latestWaitingTask, routeIndex, assignedTWs)
        appendToSchedSteps("Route AFTER switchTimeWindows in minRoute", bestRoute, routeIndex)
        
        if newRoute == None:
            break
        # find the shortest route with that ending time
        appendToSchedSteps("Route BEFORE dominantRoute in minRoute", bestRoute, routeIndex)
        newRoute = dominantRoute(newRoute, assignedTWs, routeIndex)
        appendToSchedSteps("Route AFTER dominantRoute in minRoute", bestRoute, routeIndex)
        
        # if it's better than the best so far, update the best.
        if(getMinRouteDuration(newRoute) < getMinRouteDuration(bestRoute)):
            bestRoute = newRoute
        latestWaitingTask = getLatestWaitingTask(newRoute)
        
    appendToSchedSteps("Route at end of minRoute, before task revert", bestRoute, routeIndex)

    # Set bestRoute tasks to be the original tasks from the tasklist
    # We do this to remove changes we made to time windows in the
    # preprocessing steps

    bestRoute = resetTasks(bestRoute, taskList)
    appendToSchedSteps("Route at end of minRoute", bestRoute, routeIndex)

    # print "********** Exiting minRoute **********"
    return bestRoute

def resetTasks(route, taskList):
    route = copy.deepcopy(route)
    for t in range(len(route)):
        route[t] = taskList[route[t].id]
    return route

'''
@return: the index for the last task with waiting time in the route
'''
def getLatestWaitingTask(currRoute):
    for task in range(len(currRoute) - 1, 0, -1):
        if currRoute.endingTimes[task] - currRoute[task].duration > currRoute.endingTimes[task - 1]:
            return task - 1
    return -1

'''
@return: the updated schedule after moving the latestWaitingTask to the next 
time window and updating the other tasks
'''
def switchTimeWindows(currRoute, latestWaitingTaskIndex, day, assignedTWs):
    # print "********** Entering switchTimeWindows **********"

    currRoute = copy.deepcopy(currRoute)
    
#     isRouteActuallyFeasible(currRoute, day, "beginning of switchTimeWindows")
    
    # print "Original Route:"
    # print currRoute
    
    # store the task we are working with
    latestWaitingTask = currRoute[latestWaitingTaskIndex]
    # print "latest waiting task = route[" + str(latestWaitingTaskIndex) + " =", latestWaitingTask.id
    
    # store the new time window it is moving to
    tw = latestWaitingTask.timeWindows[day][assignedTWs[latestWaitingTaskIndex]]
    
    # print "LWT time windows on day:", tw
    
    # moving the latestWaitingTask to its next time window as early as possible within the new time window
    latestWaitingTask.endingTime = latestWaitingTask.duration + tw[0]
    
    currRoute.endingTimes[latestWaitingTaskIndex] = latestWaitingTask.duration + tw[0]
    
    # update the assigned time window for the task we are working with
    assignedTWs[latestWaitingTaskIndex] += 1
    
    # storing the surrounding tasks starts and ends
    nextTaskStart = tw[0]
    prevTaskEnd = tw[0] + latestWaitingTask.duration
    
    # Move all tasks before latestWaitingTask as late as possible 
    
    # print "before squidging earlier tasks"
    # print currRoute
    
    for t in range(latestWaitingTaskIndex - 1, -1, -1):
        task = currRoute[t]
        routeTWs = task.timeWindows[day]
        
        
        
        # for each time window in that route find the latest possible time window
        # that fits this task before the end of that time window and the start of the next task
        for tw in range(len(routeTWs)):
            timeWindow = routeTWs[tw]
            if timeWindow[0] + task.duration <= nextTaskStart:
                assignedTWs[t] = tw

                currRoute.endingTimes[t] = min(nextTaskStart, timeWindow[1])
                # print "   ending time in currRoute has been reset: ", currRoute.endingTimes[t]
            else:
                nextTaskStart = currRoute.endingTimes[t] - task.duration
                # print "\t\t\tAFTER ELSE nextTaskStart has been reset: ", nextTaskStart
                break
            
        nextTaskStart = currRoute.endingTimes[t] - task.duration
        # print " after FOR loop, nextTaskStart has been reset: ", nextTaskStart

    # print "after squidging starts"

    # print "before squidging later tasks"
    
    # Move all tasks after latestWaitingTask as early as possible
    for t in range(latestWaitingTaskIndex + 1, len(assignedTWs)):
        task = currRoute[t]
        routeTWs = task.timeWindows[day]
        
        # print " route[" + str(t) + "] = ", task.id
        # print " nextTaskStart", nextTaskStart
        
        for tw in range(len(routeTWs) - 1, -1, -1):
            timeWindow = routeTWs[tw]
            if timeWindow[1] - task.duration >= prevTaskEnd:
                assignedTWs[t] = tw
                
                # print "   reassigning assignedTWs: ", assignedTWs[t]
                # print nextTaskStart
                # print timeWindow
                
                currRoute.endingTimes[t] = max(prevTaskEnd, timeWindow[0]) + task.duration
            else:
                prevTaskEnd = currRoute.endingTimes[t]
                break
        prevTaskEnd = currRoute.endingTimes[t]
        if currRoute.endingTimes[t] - task.duration < currRoute.endingTimes[t - 1]:
            # print "Infeasible switch"
            # print "********** Exiting switchTimeWindows **********"
            return None
    
#     isRouteActuallyFeasible(currRoute, day, "After all squidging")
    # print "********** Exiting switchTimeWindows **********"
    return currRoute

'''
Given the ending time of currSolution, move all tasks to the latest possible
time without changing that ending time
@return: the dominant version of the schedule being passed in (squidging)
'''
def dominantRoute(currRoute, assignedTWs, dayIndex):
    # print "********** Entering dominantRoute **********"
    # print currRoute
    
    # put everything as late as possible within the assigned time window
    nextTaskStart = currRoute.endingTimes[-1] - currRoute[-1].duration
    # print "nextTaskStart:", nextTaskStart
    
    
    # goes through the current route backwards ignoring the last task
    for t in range(len(currRoute) - 2, -1, -1):
        
        task = currRoute[t]
        # print "task index", t, "id", task.id
        timeWindows = task.timeWindows[dayIndex]
        # print "time windows:", timeWindows
        
        # go through each time window for each task find latest time it could be 
        # scheduled given that the last task has not moved 
        for tw in range(assignedTWs[t], len(timeWindows)):
            timeWindow = timeWindows[tw]
            # print "checking tws[" + str(tw) + "]", timeWindow
            if timeWindow[0] + task.duration <= nextTaskStart:
                currRoute.endingTimes[t] = min(timeWindow[1], nextTaskStart)
                # print "assigned new tw:", assignedTWs[t], "to",
                assignedTWs[t] = tw
                # print assignedTWs[t]
            else:
                break
        nextTaskStart = currRoute.endingTimes[t] - task.duration
        # print "nextTaskStart:", nextTaskStart
    
    # print "********** Exiting dominantRoute **********"
    return currRoute

'''
This works with Schedule objects
@return: True if sol1 has more profit than sol2
'''
def isBetterSchedule(sched1, sched2):
    sum1 = sched1.getProfit()
    sum2 = sched2.getProfit()
    return sum1 > sum2

'''
@return: schedule object containing all of the routes and tasks from the original solution
'''
def createSchedule(solution):
    currSchedule = Objects.Schedule()
    # goes through each day in the solution 
    for d in range(len(solution)):
        day = solution[d]
        route = Objects.Route()
        # creates a copy of each task in that day and adds it to the new route
        for task in range(len(day)):
            newTask = copy.deepcopy(day[task])
            route.append(newTask, None)
        # the new route is added to the new schedule
        currSchedule.append(route)
    return currSchedule



def getRouteDuration(currRoute):
    # TODO: put this in Object.Route instead 
    routeDuration = 0
    # for each task in the route, calculate the duration by traveling time and the duration of the task
    # add the total duration calculation to the overall routeDuration 
    for t in range(len(currRoute)):
        task = currRoute[t]   
        travelTime = helperFunctions.getDistanceBetweenTasks(task, currRoute[t - 1])
        taskDuration = task.duration + travelTime
        routeDuration += taskDuration
    
    return routeDuration

'''
@return: the length of a schedule from the start of the first 
    route to the end of the last
'''
def getScheduleDuration(taskList, currSchedule):
#     print "************* Entering getScheduleDuration **************"
    sum = 0
    
    feasSched = copy.deepcopy(currSchedule)
    
    feasSched = isFeasible(taskList, feasSched)
    
    if feasSched != None:
        for route in feasSched:
            sum += getRouteDuration(route)
#         "************* Exiting getScheduleDuration **************"
        return sum
    
    for route in currSchedule:
        sum += getRouteDuration(route)
#     "************* Exiting getScheduleDuration **************"
    return sum

'''
@return: total distance of a solution
'''
def calcTotalDistance(currSolution):
    totalDistance = 0
    for r in range(len(currSolution)):
        route = currSolution[r]
        routeTravelTime = 0
        for t in range(len(route)):
            task = route[t]
            routeTravelTime += helperFunctions.getDistanceBetweenTasks(task, route[t - 1])
        totalDistance += routeTravelTime
        
    return totalDistance
    
# take the last tasks ending time - first tasks ending time + first tasks duration 
def getMinRouteDuration(currRoute): 
    
    totalDuration = currRoute.endingTimes[-1] - currRoute.endingTimes[0] + currRoute.taskList[0].duration
    return totalDuration    


def updatePrevUnplanned(task):
    if task in prevUnplanned:
        prevUnplanned.remove(task)
        prevUnplanned.append(task)


def printUnplanned():
    print "unplanned tsks: (",
    for task in unplannedTasks:
        print str(task) + ", "
    print ")"

def printSolution(sol):
    print "["
    for route in sol:
        for task in route:
            print str(task) + ", "
    print "]"
         
def unplannedIDs():
    result = []
    for task in unplannedTasks:
        result.append(task.id)
    return result
         
         
def scheduleIDs(sched):
    result = []
    for route in sched:
        for task in route:
            result.append(task.id)
    return result


def isUnplannedWrong(currSchedule):
    if currSchedule == None:
        return
    ids = unplannedIDs()
    for route in currSchedule:
        for task in route:
            if task.id in ids:
                print "BAD"
                exit(1)

def findNoneRoutes(currSchedule):
    if currSchedule == None:
        return
    for r in currSchedule:
        if (r == None):
            print "IT WAS NONE"
            exit(1)

def isRouteActuallyFeasible(currRoute, routeIndex, codeLocation):
    if not checkForOverlappingTasks(currRoute) or not checkForProperTaskScheduling(currRoute, routeIndex):
        print codeLocation
        exit()

#checking to see if tasks that have been scheduled are overlapping        
def checkForOverlappingTasks(currRoute):
    if len(currRoute) == 0:
        return True
    task = currRoute[0]
    if currRoute.endingTimes[0] == None:
        return True
    startTime = currRoute.endingTimes[0] - task.duration
    lastEndingTime = currRoute.endingTimes[0]
    for t in range(1, len(currRoute)):
        task = currRoute[t]
        startTime = currRoute.endingTimes[t] - task.duration
        if startTime < lastEndingTime:
            print "Error in route"
            print currRoute
            for t in range(1, len(currRoute)):
                prevTask = currRoute[t - 1]
                task = currRoute[t]
                
            print "task", t, "overlaps task\a", t - 1
            return False
        lastEndingTime = currRoute.endingTimes[t] - task.duration
    return True

#checks to make sure that all taska are scheduled within a time window        
def checkForProperTaskScheduling(currRoute, routeIndex):
    for t in range(len(currRoute)): 
        task = currRoute[t]
        taskEndingTime = currRoute.endingTimes[t]
        
        # if an ending time has been set for the task --> we need not check to see if task is 
        # scheduled within its time window if an ending time has not been set. 
        if taskEndingTime != None: 
            #calculate the start time
            taskStartTime = taskEndingTime - task.duration
            foundFeasibleTW = False
            
            # go through all the time windows for the task within a given time window
            # if we find a tw start time that is less than the taskStartTime and a 
            # tw ending time that is greater than or equal to the task end time then 
            # set bool value to true
            for tw in task.timeWindows[routeIndex]:
                if tw[0] <= taskStartTime and tw[1] >= taskEndingTime:
                    foundFeasibleTW = True
                
            # if we have made it through all the tws but haven't found a feasible one, 
            # indicate that there is an error 
            if foundFeasibleTW == False: 
                print "******** Error in route ********"
                print "task", task.id, "is not scheduled within its available TWs"
                print currRoute 
                print "task start time: ", taskStartTime
                print "task ending time: ", taskEndingTime
                print "*********************************"
                return False
    return True

'''
Function so the GUI can display the time you may have to wait
'''
def getStoppingCondition():
    return stoppingCondition
    
def changedTimeWindowsInSchedule(route, r, taskList):
    for t in range(len(route)):
        task = route[t]
        for tw in range(len(task.timeWindows[r])):
            timeWindow = task.timeWindows[r][tw]
            taskListTW = taskList[task.id].timeWindows[r][tw]
            if timeWindow[0] != taskListTW[0] or timeWindow[1] != taskListTW[1]:
                print "ERROR"
                print route
                print "Error: task", task.id, "timewindow", timeWindow, "does not match", taskListTW
                exit()
            
'''
Tries to add the current schedule information to the global list of schedSteps
used by the visualizer.
@param stringInfo: A string describing the step of the algorithm which just completed
@param schedOrRoute: The schedule or route object being added to the list
@param routeIndex: The index of the route in the schedule, or None if schedOrRoute
    is a full schedule
'''
def appendToSchedSteps(stringInfo, schedOrRoute, routeIndex = None):
    try:
        schedSteps.append([stringInfo, copy.deepcopy(schedOrRoute), routeIndex])
    except NameError:
        pass
            
def main():
    # print "********** Main **********"
    stoppingCondition = float(sys.argv[2])
    #run vns on file specified in user input
    f = sys.argv[1]
    f = os.path.realpath(f)
    
    result = solve(f, stoppingCondition)
    print
    print result[0]
    print
    
    
    #return result

if __name__ == "__main__":
    main()