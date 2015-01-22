# Comps 2014
# Larkin Flodin, Avery Johnson, Maraki Ketema, 
# Abby Lewis, Will Schifeling, and  Alex Trautman

import greedyByPresentChoice
import greedyByOrder
import createTasksFromCsv
import helperFunctions
import Objects
import time
import math
import random
import copy
import csv
from collections import deque
#from bruteForce import runBruteForceAlg

global timeLimit
timeLimit = 5000

random.seed(211680280677)

'''
@return: an ordering of tasks
'''
def solve(csvFile):
    # Get a greedy algorithm to then modify with VNS
    taskList = createTasksFromCsv.getTaskList(csvFile)
    helperFunctions.preprocessTimeWindows(taskList)

#     greedyByPrioritySol = greedyByOrder.runGreedyByOrder(csvFile, greedyByOrder.orderByPriority)
#     greedyByDeadlineSol = greedyByOrder.runGreedyByOrder(csvFile, greedyByOrder.orderOptionalByDeadline)
#     greedyByPresentChoiceSol = greedyByPresentChoice.runGreedyByPresentChoice(csvFile)
#     solutionList = [greedyByPrioritySol, greedyByDeadlineSol, greedyByPresentChoiceSol]
#     bestGreedy = max(solutionList, key = lambda schedule : schedule.getProfit())
#     bestGreedy = min(solutionList, key = lambda schedule : schedule.getProfit())
    bestGreedy = greedyByOrder.runGreedyByOrder(csvFile, greedyByOrder.orderByPriority)
    
    print bestGreedy
    assert(isFeasible(taskList, bestGreedy))

    print bestGreedy

#     brute = runBruteForceAlg(csvFile)
    
    # brute = runBruteForceAlg(csvFile)
    
    modTasks = bestGreedy[:]
    currSchedule = createSchedule(copy.deepcopy(bestGreedy))
    # Modify the greedy algorithm
    currSchedule = vns(taskList, currSchedule)
    assert(isFeasible(taskList, currSchedule))
    
#     print 'greedy solution'
#     print bestGreedy
# 
#     print 'vns solution'
#     print currSchedule
    
    '''
    print 'brute force solution'
    printSolution(brute)
    '''

     
#     print "brute journey"
# #     helperFunctions.printScheduleJourney(brute)
# 
#     print "greedy journey"
# #     helperFunctions.printScheduleJourney(greedySol)
#     

    print "vns journey"
    helperFunctions.printScheduleJourney(currSchedule)
    
    
    print "Profit of Greedy Schedule is: "
    print bestGreedy.getProfit()
    print "Profit of VNS Schedule is: "
    print currSchedule.getProfit()
    

#     writeTasks("testReturn.csv", currSchedule)
    return currSchedule


'''
@return: best schedule found in time limit
'''
def vns(taskList, currSchedule):
    
#     print "********** Entering VNS **********"
#     print "initial solution: "
#     print currSchedule
    
    global unplannedTasks
    global prevUnplanned
    
    unplannedTasks = deque(taskList[:])
   
   
    for day in currSchedule:
        for task in day:
            unplannedTasks.remove(task)
    
    # Number of seconds VNS is allowed to run
    stoppingCondition = 60
    
    # Number of neighborhood structures
    nHoodMax = 17
    
    # Number of iterations since last bestSolution update
    numIterations = 0
    
    currSchedule = isFeasible(taskList, currSchedule)
    if currSchedule == None:
        print "Your incumbent solution is infeasible, try again"
        exit(1)
    bestSchedule = currSchedule
    
    initTime = time.time()
    
    iterCount = 0
    
    # until the stopping condition is met
    while time.time() - initTime < stoppingCondition:
        # If we have gone through all neighborhood structures, start again
        nHood = 1
        while nHood < nHoodMax and time.time() - initTime < stoppingCondition:
            currSchedule = copy.deepcopy(currSchedule)
            currSchedule.resetEndingTimes()
            prevUnplanned = copy.deepcopy(unplannedTasks)
            
            iterCount += 1
            
            shakeSolution = shaking(currSchedule, nHood)
            iterSolution = iterativeImprovement(taskList, shakeSolution, nHood)

            # make sure the modified solution is still feasible. 
            # If it is not, try again
            # If it is, and it is a better solution, update bestSolution
            feasibleSchedule = isFeasible(taskList, iterSolution)
            
            # if feasible and better
            #     accept it as the new solution, reset nHood of numIterations
            
            if (feasibleSchedule != None):

                # If our solution is better than the current solution, update.
                if isBetterSchedule(feasibleSchedule, currSchedule):
                    currSchedule = feasibleSchedule
                    nHood = 1
                # Otherwise, increment nHood
                else:
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
                        currSchedule = feasibleSchedule
                        nHood = 1
                        unplannedTasks = prevUnplanned
                        
                    # Criteria for nHoods 1-8:
                    # If the new solution is not more than .5% longer (distance), accept
                    elif calcTotalDistance(iterSolution) >= .995 * calcTotalDistance(currSchedule):
                        currSchedule = feasibleSchedule
                        unplannedTasks = prevUnplanned
                else:
                    numIterations += 1 
                    unplannedTasks = prevUnplanned
            else:
                numIterations += 1
                unplannedTasks = prevUnplanned
                nHood += 1
                
#     print "********** Exiting VNS **********"
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
        
    elif nHood >= 8 and nHood < 12:
        newSchedule = optionalExchange1(currSchedule, nHood)
        
    else:
        newSchedule = optionalExchange2(currSchedule, nHood)
    
#     print "********** Exiting shaking **********"
    return newSchedule

'''
@param currSchedule: list (schedule) of lists (days/routes) of task objects
@return: modified schedule
'''
def crossExchange(currSchedule, nHood):
#     print "********** Entering crossExchange **********"
        
    if len(currSchedule) <= 1:
#         print "Not doing cross exchange"
#         print "********** Exiting crossExchange **********"
        return currSchedule
    
    # choose two distinct random days
    day1 = random.randint(0, len(currSchedule)-1)
    day2 = random.randint(0, len(currSchedule)-1)
    while (day1 == day2):
        day2 = random.randint(0, len(currSchedule)-1)
        
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
    routeSegment1 = getRouteSegment(currSchedule, day1, day2, route1Len)
    routeSegment2 = getRouteSegment(currSchedule, day1, day2, route2Len)

    route1Start, route1End = routeSegment1[0], routeSegment1[1]
    route2Start, route2End = routeSegment2[0], routeSegment2[1]

    # setting route and  new day to be what they should be
    route1 = currSchedule[day1][route1Start : route1End]
    newDay1 = Objects.Route()
    tasks1 = currSchedule[day1][:route1Start] + currSchedule[day1][route1End:]
    newDay1.setTaskList(tasks1, [None] * len(tasks1))
    
    
    # starting index of the sub-route we will be removing
    route2 = currSchedule[day2][route2Start:route2End]
    newDay2 = Objects.Route()
    tasks2 = currSchedule[day2][:route2Start] + route1 + currSchedule[day2][route2End:]
    newDay2.setTaskList(tasks2, [None] * len(tasks2))
    
    for task in route2:
        unplannedTasks.append(task)
    
    # remove route1 from day1, remove route2 from day2, insert route1 into day2 where route2 was
    currSchedule[day1] = newDay1
    currSchedule[day2] = newDay2
    
#     print "********** Exiting crossExchange **********"
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
        
        if(len(origRoute[n].timeWindows[newDay]) > 0):
            if n - currRouteStart == segmentLength - 1:
                possRoutes.append(currRouteStart)
                currRouteStart += 1
        
        # move on to the next route if previous conditional statement was no satisfied 
        else:
            currRouteStart = n + 1
        n += 1
    
    # if we found a viable route, choose a random one 
    if len(possRoutes) > 1:
        route1Start = possRoutes[random.randint(0, len(possRoutes)-1)]
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
    
    #select the number of tasks to remove and add from unplanned according to nHood Index
    numToRemove = nHood - 9
    numToAdd = 1
    if nHood == 12:
        numToRemove = 0
        numToAdd = 2

    # pick a random day and starting time to exchange customers
    day = random.randint(0, len(currSchedule) - 1)
    
    pos = random.randint(0, len(currSchedule[day]))
    
    if numToRemove > 0:
        # using the numToRemove and numToAdd values, add and remove however many customers you need to
        for task in currSchedule[day][pos:pos + numToRemove]:
            if task.required == 0:
                unplannedTasks.append(task)
        newDay = currSchedule[day][:pos] + currSchedule[day][pos + numToRemove:]
        
    else:
        newDay = currSchedule[day][:]

    # selecting which unplanned tasks to add
    addingTasks = []
    for t in range(numToAdd):
        if len(unplannedTasks) > 0:
            popped = unplannedTasks.popleft()
            addingTasks.append(popped)
            updatePrevUnplanned(popped)
          
    # adding new tasks to day 
    newDay = newDay[:pos] + addingTasks + newDay[pos:]
    
    newRoute = Objects.Route()
    
    for task in newDay:
        newRoute.append(task, None)
    
     # replace the chosen days with the updated days   
    currSchedule[day] = newRoute
    
#     print
#     print currSchedule
#     printUnplanned()
#     print "********** Exiting optExchange1 **********"
    return currSchedule

'''
Removes tasks from a random day/position and adds removed tasks to unplanned tasks. 
@return: modified solution
'''
def optionalExchange2(currSchedule, nHood):
#     print "********** Entering optExchange2 **********"

    # calculate number to remove (nHood-12)
    numToRemove = nHood - 12
    # pick a random day and position
    
    # pick a random day and starting time to exchange customers
    day = random.randint(0, len(currSchedule) - 1)
    pos = random.randint(0, len(currSchedule[day]))
    
    # using the numToRemove and numToAdd values, add and remove however many customers you need to
    for task in currSchedule[day][pos:pos + numToRemove]:
        if task.required == 0:
            unplannedTasks.append(task)

    newDay = currSchedule[day][:pos] + currSchedule[day][pos + numToRemove:]

    newRoute = Objects.Route()
    for task in newDay:
        newRoute.append(task, None)

    currSchedule[day] = newRoute
#     print "********** Exiting optExchange2 **********"
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
    return newSchedule  
'''
@return: solution that has been modified by 3-Opt
'''
def threeOPT(taskList, currSchedule):
#     print "********** Entering threeOPT **********"
    
    currSchedule = copy.deepcopy(currSchedule)
    # pick a random day to optimize
    day = random.randint(0, len(currSchedule)-1)
    currRoute = currSchedule[day]
    currLength = len(currRoute)

    # 2
    if currLength > 3:
        maxM = math.factorial(currLength) / (6 * math.factorial(currLength - 3))
    else:
        return currSchedule
    
    for k in range(len(currRoute) - 2):
        topRange = min(k + 4, currLength - 2)
        for j in range(k + 1, topRange):
            route, currFeasibility = isRouteFeasible(currRoute, day)
            newRoute = switchChains(k, j, currRoute)
            newLength = len(newRoute)
            route, newFeasibility = isRouteFeasible(currRoute, day)
            if currLength >= newLength and newFeasibility <= currFeasibility:
                if newLength < currLength or newFeasibility < currFeasibility:
                    currSchedule[day] = newRoute
#                     print "********** Exiting threeOPT ***************"       
                    return currSchedule

#     print currSchedule
#     print "********** Exiting threeOPT ***************"       
    return currSchedule

def switchChains(k, j, currRoute):
    newRoute = copy.deepcopy(currRoute)
    chain1 = newRoute[0:k+1]
    chain2 = newRoute[k+1:j+1]
    chain3 = newRoute[j+1:len(currRoute)]
    newTaskList = chain1 + chain3 + chain2
    newRoute.setTaskList(newTaskList, [None]*len(newTaskList))
    return newRoute

'''
@return: solution that has been modified by 3-Opt
'''
def bestInsertion(taskList, currSchedule):
#     print "********** Entering bestInsertion **********"

    # Sequentially consider tasks from unplannedTasks
    # For each day, if that task:
        # has a time window in that day
        # and the duration of that day + that task's duration <= timeLimit
    # find the additional distance of adding that task in that location
    # if that is smaller than the smallest so far, update smallest
    
    # otherwise, enqueue it and go to the next task

    tasksSinceLastInsertion = 0
    # while we have not explored all of the unplanned tasks
    while tasksSinceLastInsertion < len(unplannedTasks):
        
        # shortestDistance set to infinity 
        shortestDistance = float("inf")
        # keeps track of the day and position within the day at which to insert task
        insertLocation = (0, 0)
        
        # bool that keeps track of whether a give task is valid 
        isValid = False
        
        currTask = unplannedTasks.popleft()
        updatePrevUnplanned(currTask)

        # looping through each day in the current solution list 
        for day in range(len(currSchedule)):
            
            # if the duration of the task under consideration added to the current day 
            # is less than the time limit then accept it as valid
            if len(currTask.timeWindows[day]) > 0 and \
            getRouteDuration(currSchedule[day]) + currTask.duration < timeLimit:
                isValid = True
                
                # for each position within the day 
                for pos in range(len(currSchedule[day]) - 1):
                    
                    task1 = currSchedule[day][pos]
                    task2 = currSchedule[day][pos + 1]
                   
                    # calculates what the distance would be if the task under consideration were to be added between task1 and task2
                    addedDist = helperFunctions.getDistanceBetweenTasks(task1, currTask) + \
                    helperFunctions.getDistanceBetweenTasks(currTask, task2) - \
                    helperFunctions.getDistanceBetweenTasks(task1, task2)
                    
                    # if the calculated distance is less than the shortestDistance value then reset shortestDistance and save the day and pos
                    if addedDist < shortestDistance:
                        shortestDistance = addedDist
                        insertLocation = (day, pos)
    
        # adding the 'valid' task to the day at the specified position 
        if isValid:
            newRoute = Objects.Route()
            day = insertLocation[0]
            pos = insertLocation[1]
            newRoute.taskList = currSchedule[day][:pos]
            newRoute.endingTimes = [None] * len(newRoute.taskList)
            newRoute.append(currTask, None)
            for t in currSchedule[day][pos:]:
                newRoute.append(t, None)
            currSchedule[day] = newRoute
            tasksSinceLastInsertion = 0
        
        # if not valid then increment and add the task that was being evaluated back into the unplannedTasks list     
        else:
            tasksSinceLastInsertion += 1
            unplannedTasks.append(currTask)
    
    # after all that, add the task to the solution in the time with smallest added distance.
#     print "********** Exiting bestInsertion **********"
    return currSchedule

def isFeasible(taskList, currSchedule):
#     print "********** Entering isFeasible **********"
    currSchedule = copy.deepcopy(currSchedule)
    newSchedule = copy.deepcopy(currSchedule)
    for r in range(len(currSchedule)):
        newRoute, infeas = isRouteFeasible(currSchedule[r], r)
        if infeas > 0 or newRoute == None:
#             print "********** Exiting isFeasible **********"
            return None
        else:
            newSchedule[r] = newRoute
#     print "********** Exiting isFeasible **********"
    newSchedule = minRoute(taskList, newSchedule)
    return newSchedule

def isRouteFeasible(currRoute, routeIndex):
#     print "********** Entering isRouteFeasible **********"
    currRoute = copy.deepcopy(currRoute)
    
    
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
            
    oldRoute = copy.deepcopy(currRoute)
        
    currRoute = tightenTWStarts(currRoute, routeIndex)
    currRoute = tightenTWEnds(currRoute, routeIndex)

    
    if currRoute != None:
#         print "********** Exiting isRouteFeasible1 **********"
        return currRoute, 0
    
    infeas = 0
    currRoute = oldRoute
    lastTaskEnd = currRoute[0].releaseTime
    
    
    # find proper time window for this task (after end of last task)
    # if not available, add all of duration to infeas
    # if available but it doesn't fit, put the task as early as possible within tw,
    # add any duration spent outside of tw to infeas
    
    for t in range(len(currRoute)):
        task = currRoute[t]
        timeWindows = task.timeWindows[routeIndex]
        selectedTW = None
        for i in range(len(timeWindows)):
            tw = timeWindows[i]
            if tw[1] > lastTaskEnd:
                selectedTW = tw
                break
        if selectedTW == None:
            infeas += task.duration
            lastTaskEnd = lastTaskEnd + task.duration
        else:
            if max(lastTaskEnd, selectedTW[0]) + task.duration > selectedTW[1]:
                infeas +=  max(lastTaskEnd, selectedTW[0]) + task.duration - selectedTW[1]
            lastTaskEnd = max(lastTaskEnd, selectedTW[0]) + task.duration


#     print "********** Exiting isRouteFeasible2 **********"
    return None, infeas
                    

'''
@return: modified schedule with tightened tw starts
'''
def tightenTWStarts(currRoute, routeIndex):
#     print "********** Entering tightenTWStarts **********"

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
                print "resetting tw start: no overlap"
                # set the beginning of that time window to be the minimum of the the ending time of task i's first time window
                # and the start of task i+1's first time window
#                 print "start of tw", tw[0][0], ", twNext", twNext[0][0], ", duration", task.duration
                print "old tw", tw
                tw[0] = (min(twNext[0][0], tw[0][1]) - task.duration, tw[0][1])
                print "new tw",tw
                
            # elif the duration of task i set at the beginning of its first tw overlaps any tws for the next task
            elif len(tw) > 0 and len(twNext) > 0 and task.duration + tw[0][0] > twNext[0][0]:
                print "resetting twNext starts: overlap"
                # reset the beginnings of all time windows to be as early as possible
                # after the end of task i (with i scheduled as early as possible)
                for w in range(len(twNext)):
                    print "start of tw", tw[0][0], "+ duration", task.duration, "=", tw[0][0] + task.duration
                    print "start of next task's tw", twNext[w][0]
                    twNext[w] = (max(tw[0][0] + task.duration, twNext[w][0]), twNext[w][1])
            
            task.timeWindows[routeIndex] = tw
            currRoute.taskList[taskIndex + 1].timeWindows[routeIndex] = twNext
            
            print "Incrementing task index from", taskIndex, "to", taskIndex + 1
            taskIndex += 1
    
                    
        print "routeIndex", routeIndex
        print "taskIndex + 1 = ", taskIndex + 1
        
        
        
        print "End of while:"
        print "End tw", tw
        print "tasks["+str(taskIndex)+"] =", currRoute.taskList[taskIndex].id, "tw:", twNext
        print 
        
    
    task =  currRoute.taskList[taskIndex]
    tw = task.timeWindows[routeIndex] 
    
    if taskIndex == len(currRoute) - 1 and len(currRoute.taskList[taskIndex].timeWindows[routeIndex]) > 0 and task.duration > tw[0][1] - tw[0][0]:
            # remove that task's first tw
            tw = tw[1:]
            task.timeWindows[routeIndex] = tw
    
    print "taskIndex", taskIndex
    print "len of taskList", len(currRoute.taskList) - 1  
    print "any empty TWListst", anyEmptyTWLists(currRoute, routeIndex)
    if taskIndex  < len(currRoute.taskList) - 1 or anyEmptyTWLists(currRoute, routeIndex):
        print "********** Exiting tightenTWStarts 2 **********"
        return None
    print "********** Exiting tightenTWStarts 3 **********"
    return currRoute

'''
@return: modified schedule with tightened tw ends
'''
def tightenTWEnds(currRoute, routeIndex):
    print "********** Entering tightenTWEnds **********"
    if currRoute == None:
        print "********** Exiting tightenTWEnds1 **********"
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
        
        print "route["+str(taskIndex) + "] =", task.id
        print "Initial tw =", tw
        print "prevTW =", twPrev
        
        # if duration of task i does not fit in its last tw or it can fit between the end of its second to last time w
        #  and the end of the previous task's last tw:
        
        if (task.duration > tw[-1][1] - tw[-1][0]) or (len(tw) > 1 and task.duration + tw[-2][0] < twPrev[-1][0]):
            print "\tRemoving last tw"
            print "tw before remove:", tw
            tw = tw[:-1]
            print "tw after remove:", tw
            task.timeWindows[routeIndex] = tw
            if len(tw) == 0:
                print "\tExiting on task:", taskIndex
                break
            
            task.timeWindows[routeIndex] = tw
            currRoute.taskList[taskIndex - 1].timeWindows[routeIndex] = twPrev
            
        else:
            # if duration of task i at the end of its last tw starts before the end of the previous task's last tw
            if len(tw)>0 and len(twPrev)>0 and tw[-1][1] - task.duration < twPrev[-1][1]:
                print "\tresetting tw end: no overlap"
                
                # set the end of that tw to be the maximum of the the starting time of task i's last time w
                # and the end of task i-1's last time w
                tw[-1] = (tw[-1][0], max(twPrev[-1][1], tw[-1][0] + task.duration))
            
            # if the duration of task i set at the end of its last tw overlaps any tws for the previous customer
            elif len(tw)>0 and len(twPrev)>0 and tw[-1][1] - task.duration < twPrev[-1][1]:
                print "\tresetting twPrev ends: overlap"
                # reset the endings of all time windows to be as late as possible
                # before the beginning of task i (with i scheduled as late as possible)
                for w in range(len(twPrev)):
                    print "\t\tend of tw", tw[-1][1], "- duration", task.duration, "=", tw[-1][1] - task.duration
                    print "\t\tend of next task's tw", twPrev[w][1]
                    twPrev[w] = (twPrev[w][0], min(tw[-1][1] - task.duration, twPrev[w][1]))
            
            task.timeWindows[routeIndex] = tw
            currRoute.taskList[taskIndex-1].timeWindows[routeIndex] = twPrev
            taskIndex -= 1
        
            
        
        print "End of while:"
        print tw
        print taskIndex, "prev task", twPrev
        print "actual task info:", task.timeWindows[routeIndex]
        print "actual prevTaskInfo: ", currRoute.taskList[taskIndex].timeWindows[routeIndex]
        print
    
    task = currRoute.taskList[taskIndex]
    tw = task.timeWindows[routeIndex]
    twIndex = 0
    
    if taskIndex == len(currRoute) - 1 and len(currRoute.taskList[taskIndex].timeWindows[routeIndex]) > 0 and task.duration > tw[0][1] - tw[0][0]:
           # remove that task's first tw
           tw = tw[1:]
           task.timeWindows[routeIndex] = tw
            
    for task in currRoute:
        print task.id, task.timeWindows[routeIndex]
    
    if taskIndex  > 0 or anyEmptyTWLists(currRoute, routeIndex):
        print "********** Exiting tightenTWEnds2 **********"
        return None
    
    print "********** Exiting tightenTWEnds3 **********"
    return currRoute

def anyEmptyTWLists(route, routeIndex):
    for t in range(len(route)):  
        task = route[t]
        if len(task.timeWindows[routeIndex]) < 1:
            print "THE TWS for task", task.id,"was EMPTY"
            return True
    return False

'''
@return: shortest duration of this schedule ordering
'''
def minRoute(taskList, currSchedule):
    print "********** Entering minRoute **********"
    bestSchedule = copy.deepcopy(currSchedule)
#     print currSchedule
    
    # Minimize each route
    for d in range(len(currSchedule)):
        day = currSchedule[d]
        
        print "start of minRouteLoop", d
        print day
        isRouteActuallyFeasible(day)
        
        if len(day) == 0:
            continue
        
        print "\nstart of minRoute"
        print day
        isRouteActuallyFeasible(day)
        
        # keep track of what tw index each task has been assigned
        assignedTWs = [0] * len(day)        
        
        
        # set the ending times for each task in the route by scheduling
        # all tasks as early as possible (start at the beginning of the
        # first time window. This is feasible because of preprocessing
        for t in range(len(day)):
            task = day[t]
            
            day.endingTimes[t] = task.duration + task.timeWindows[d][0][0]
            
#             print "new ending time:"
#             print task
#             print day.endingTimes[t]
#         print 
        # Find the dominant version of this route (shortest possible route
        # with this ending time.
        

        
        print "checking initRoute"
        isRouteActuallyFeasible(day)
        
        latestWaitingTask = getLatestWaitingTask(day)
        if latestWaitingTask == -1:
            bestSchedule[d] = day
            continue
        bestRoute = dominantRoute(day, assignedTWs, d)
        
        
        print " after dominantRoute 0"
        isRouteActuallyFeasible(bestRoute)
        
        latestWaitingTask = getLatestWaitingTask(bestRoute)
        
        
        # While this there are still tasks with waiting time and the latest
        # waiting task has time windows to switch to
        while latestWaitingTask > -1 and assignedTWs[latestWaitingTask] < len(day[latestWaitingTask].timeWindows[d]) - 1:
            
            # move the latest waiting task to its next time window.
            newRoute = switchTimeWindows(bestRoute, latestWaitingTask, d, assignedTWs)
            if newRoute == None:
                break
            # find the shortest route with that ending time
            newRoute = dominantRoute(newRoute, assignedTWs, d)
            
            # if it's better than the best so far, update the best.
            if(getMinRouteDuration(newRoute) < getMinRouteDuration(bestRoute)):
                bestRoute = newRoute
            latestWaitingTask = getLatestWaitingTask(newRoute)
            
        print "after dom and switch loop"
        isRouteActuallyFeasible(bestRoute)
        
        if bestRoute == None:
            print "WHAT"
            exit()
        
        # update the schedule to have this route
        bestSchedule[d] = bestRoute
    

    # Set bestSchedule tasks to be the original tasks from the tasklist
    # We do this to remove changes we made to time windows in the
    # preprocessing steps
    for r in range(len(bestSchedule)):
        for t in range(len(bestSchedule[r])):

            bestSchedule[r][t] = taskList[bestSchedule[r][t].id]
    print "********** Exiting minRoute **********"

    return bestSchedule



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
    print "********** Entering switchTimeWindows **********"

    currRoute = copy.deepcopy(currRoute)
    
    print "Beginning of switchTimeWindows"
    isRouteActuallyFeasible(currRoute)
    
    print "Original Route:"
    print currRoute
    
    #store the task we are working with
    latestWaitingTask = currRoute[latestWaitingTaskIndex]
    print "latest waiting task = route["+str(latestWaitingTaskIndex)+" =", latestWaitingTask.id
    
    # store the new time window it is moving to
    tw = latestWaitingTask.timeWindows[day][assignedTWs[latestWaitingTaskIndex]]
    
    print "LWT time windows on day:", tw
    
    #moving the latestWaitingTask to its next time window as early as possible within the new time window
    latestWaitingTask.endingTime = latestWaitingTask.duration + tw[0]
    
    currRoute.endingTimes[latestWaitingTaskIndex] = latestWaitingTask.duration + tw[0]
    
    # update the assigned time window for the task we are working with
    assignedTWs[latestWaitingTaskIndex] += 1
    
    #storing the surrounding tasks starts and ends
    nextTaskStart = tw[0]
    prevTaskEnd = tw[0] + latestWaitingTask.duration
    
    # Move all tasks before latestWaitingTask as late as possible 
    
    print "before squidging earlier tasks"
    print currRoute
    
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
                print "   ending time in currRoute has been reset: ", currRoute.endingTimes[t]
            else:
                nextTaskStart = currRoute.endingTimes[t] - task.duration
                print "\t\t\tAFTER ELSE nextTaskStart has been reset: ", nextTaskStart
                break
            
        nextTaskStart = currRoute.endingTimes[t] - task.duration
        print " after FOR loop, nextTaskStart has been reset: ", nextTaskStart

    print "after squidging starts"

    print "before squidging later tasks"
    
    # Move all tasks after latestWaitingTask as early as possible
    for t in range(latestWaitingTaskIndex + 1, len(assignedTWs)):
        task = currRoute[t]
        routeTWs = task.timeWindows[day]
        
        print " route["+str(t)+"] = ", task.id
        print " nextTaskStart", nextTaskStart
        
        for tw in range(len(routeTWs) - 1, -1, -1):
            timeWindow = routeTWs[tw]
            if timeWindow[1] - task.duration >= prevTaskEnd:
                assignedTWs[t] = tw
                
                print "   reassigning assignedTWs: ", assignedTWs[t]
                print nextTaskStart
                print timeWindow
                
                currRoute.endingTimes[t] = max(prevTaskEnd, timeWindow[0]) + task.duration
            else:
                prevTaskEnd = currRoute.endingTimes[t]
                break
        prevTaskEnd = currRoute.endingTimes[t]
        if currRoute.endingTimes[t] - task.duration < currRoute.endingTimes[t-1]:
            print "Infeasible switch"
            print "********** Exiting switchTimeWindows **********"
            return None
    
    print "after all squidging"
    print currRoute
    isRouteActuallyFeasible(currRoute)
    print "********** Exiting switchTimeWindows **********"
    return currRoute

'''
Given the ending time of currSolution, move all tasks to the latest possible
time without changing that ending time

@return: the dominant version of the schedule being passed in (squidging)
'''
def   dominantRoute(currRoute, assignedTWs, dayIndex):
    print "********** Entering dominantRoute **********"
    print currRoute
    
    # put everything as late as possible within the assigned time window
    nextTaskStart = currRoute.endingTimes[-1] - currRoute[-1].duration
    print "nextTaskStart:", nextTaskStart
    
    
    #goes through the current route backwards ignoring the last task
    for t in range(len(currRoute) - 2, -1, -1):
        
        task = currRoute[t]
        print "task index", t, "id", task.id
        timeWindows = task.timeWindows[dayIndex]
        print "time windows:", timeWindows
        
        #go through each time window for each task find latest time it could be 
        #scheduled given that the last task has not moved 
        for tw in range(assignedTWs[t], len(timeWindows)):
            timeWindow = timeWindows[tw]
            print "checking tws["+str(tw)+"]", timeWindow
            if timeWindow[0] + task.duration <= nextTaskStart:
                currRoute.endingTimes[t] = min(timeWindow[1], nextTaskStart)
                print "assigned new tw:", assignedTWs[t], "to",
                assignedTWs[t] = tw
                print assignedTWs[t]
            else:
                break
        nextTaskStart = currRoute.endingTimes[t] - task.duration
        print "nextTaskStart:", nextTaskStart
    
    print "********** Exiting dominantRoute **********"
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
    #goes through each day in the solution 
    for d in range(len(solution)):
        day = solution[d]
        route = Objects.Route()
        #creates a copy of each task in that day and adds it to the new route
        for task in range(len(day)):
            newTask = copy.deepcopy(day[task])
            route.append(newTask, None)
        # the new route is added to the new schedule
        currSchedule.append(route)
    return currSchedule



def getRouteDuration(currRoute):
    # TODO: put this in Object.Route instead 
#     if currRoute.endingTimes[-1] == None or currRoute.endingTimes[0] == None:
#         return None
    
    routeDuration = 0
    # for each task in the route, calculate the duration by traveling time and the duration of the task
    # add the total duration calculation to the overall routeDuration 
    for t in range(len(currRoute)):
        task = currRoute[t]   
        travelTime = helperFunctions.getDistanceBetweenTasks(task, currRoute[t - 1])
        taskDuration = task.duration + travelTime
        routeDuration += taskDuration
    
    return routeDuration
#     return currRoute.endingTimes[-1] - currRoute.endingTimes[0] + currRoute.taskList[0].duration

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
    
#take the last tasks ending time - first tasks ending time + first tasks duration 
def getMinRouteDuration(currRoute): 
    
    totalDuration = currRoute.endingTimes[-1]- currRoute.endingTimes[0] + currRoute.taskList[0].duration
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

def isRouteActuallyFeasible(currRoute):
    if len(currRoute) == 0:
        return
    task = currRoute[0]
    if currRoute.endingTimes[0] == None:
        return
    startTime = currRoute.endingTimes[0] - task.duration
    lastEndingTime = currRoute.endingTimes[0]
    for t in range(1, len(currRoute)):
        task = currRoute[t]
        startTime = currRoute.endingTimes[t] - task.duration
        if startTime < lastEndingTime:
            print "Error in route"
            print currRoute
            for t in range(1, len(currRoute)):
                prevTask = currRoute[t-1]
                task = currRoute[t]
                
            print "task", t, "overlaps task\a", t-1
            exit()
        lastEndingTime = currRoute.endingTimes[t] - task.duration
        
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
A function that will write n tasks to a csv file.  It uses
generateTask to create the task to write. Right now the
constraints for generateTask are hard coded but that can 
be changed.  The name of the csv file is returned.
'''
def writeTasks(csvFile, schedule):
    taskList = []
    taskFeatures = ['xCoord', 'yCoord', 'releaseTime', 'duration', 'deadline', 'priority', 'required', 'timeWindows']
    with open(csvFile, 'wb') as f:
        writer = csv.writer(f)
        writer.writerow(taskFeatures)
        for i in range(len(schedule)):
            for j in range(len(schedule[i])):
                task = []
                task.append(schedule[i][j].x)
                task.append(schedule[i][j].y)
                task.append(schedule[i][j].releaseTime)
                task.append(schedule[i][j].duration)
                task.append(schedule[i][j].deadline)
                task.append(schedule[i][j].priority)
                task.append(schedule[i][j].required)
                task.append(schedule[i][j].timeWindows)
                taskList.append(task)
            taskList.append([])
        print "taskList", taskList
        #for taskList in schedule:
         #   writer.writerow(taskList)
        for task in taskList:
            writer.writerow(task)
    return csvFile
            
            
def main():
    print "********** Main **********"
    result = solve("test1000.csv")
    print result
    
    
    return result

if __name__ == "__main__":
    main()

