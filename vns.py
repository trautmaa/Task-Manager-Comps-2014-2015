# Comps 2014
# Larkin Flodin, Avery Johnson, Maraki Ketema, 
# Abby Lewis, Will Schifeling, and  Alex Trautman


# Notes from Avery:
# -getScheduleDuration and getRouteDuration:
#    - run isFeasible. if it is feasible, get the duration of the squidged route
#    - otherwise, it is not feasible and it returns infinity (we cannot calculate
#        actual route duration. We could instead calculate all task duration + travel time
#        but I feel like that would be wrong. Let's talk.




import greedyByOrder
import createTasksFromCsv
import helperFunctions
import Objects
import time
import math
import random
import copy
from collections import deque
from bruteForce import runBruteForceAlg

global timeLimit
timeLimit = 5000

'''
@return: an ordering of tasks
'''
def solve(csvFile):
    # Get a greedy algorithm to then modify with VNS
    taskList = createTasksFromCsv.getTaskList(csvFile)
    helperFunctions.preprocessTimeWindows(taskList)
    greedySol = greedyByOrder.runGreedyByOrder(csvFile, greedyByOrder.orderByDeadline)
    
#     brute = runBruteForceAlg(csvFile)
    
    modTasks = greedySol[:]
    currSchedule = createSchedule(modTasks)
    # Modify the greedy algorithm
    currSchedule = vns(taskList, currSchedule)
    
    print 'greedy solution'
    printSolution(greedySol)
    
    print 'vns solution'
    print currSchedule
    
#     print 'brute force solution'
#     printSolution(brute)
     
#     print "brute journey"
#     helperFunctions.printJourney(brute)

    print "greedy journey"
    helperFunctions.printJourney(greedySol)
    print "vns journey"
    helperFunctions.printJourney(currSchedule)

    return currSchedule


'''
@return: best schedule found in time limit
'''
def vns(taskList, currSchedule):
    
#     print "********** Entering VNS **********"
#     print "initial solution: "
#     print currSchedule
    
    global unplannedTasks
    
    unplannedTasks = deque(taskList[:])
   
    for day in currSchedule:
        for task in day:
            unplannedTasks.remove(task)
    
    # Number of seconds VNS is allowed to run
    stoppingCondition = 5
    
    # Number of neighborhood structures
    nHoodMax = 17
    
    # Number of iterations since last bestSolution update
    numIterations = 0
    
    currSchedule = isFeasible(taskList, currSchedule)
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
            if feasibleSchedule == None:
                feasible = False
            else:
                feasible = True
            
            # if feasible and better
            #     accept it as the new solution, reset nHood of numIterations
            
            if feasible:
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
                # If criteria for selection are true, select a new currSolution
                elif numIterations > 8000:
                    numIterations = 0
                    
                    if nHood > 8:
                        currSchedule = feasibleSchedule
                        nHood = 1
                    # Criteria for nHoods 1-8:
                    # If the new solution is not more than .5% longer (distance), accept
                    elif calcTotalDistance(iterSolution) >= .995 * calcTotalDistance(currSolution):
                        currSchedule = feasibleSchedule
                else:
                    numIterations += 1 
            else:
                numIterations += 1
                unplannedTasks = prevUnplanned
                
#     print "********** Exiting VNS **********"
    return bestSchedule


'''
@return: modified solution
'''
def shaking(currSchedule, nHood):
#     print "********** Entering shaking **********"
#     print currSchedule
       
    currSchedule = copy.deepcopy(currSchedule)
    
    # Based on the neighborhood perform a different operation
    if nHood < 8:
        newSolution = crossExchange(currSchedule, nHood)
        
    elif nHood >= 8 and nHood < 12:
        newSolution = optionalExchange1(currSchedule, nHood)
        
    else:
        newSolution = optionalExchange2(currSchedule, nHood)
        
#     print "********** Exiting shaking **********"
    return newSolution

'''
@param currSolution: list (schedule) of lists (days/routes) of task objects
@return: modified solution
'''
def crossExchange(currSchedule, nHood):
#     print "********** Entering crossExchange **********"
        
    # NOTE TO AVERY: MAKE SURE EXCHANGE

    if len(currSchedule) <= 1:
#         print "Not doing cross exchange"
#         print "********** Exiting crossExchange **********"
        return currSchedule
    
    # choose two distinct random days
    day1 = random.randint(0, len(currSchedule))
    day2 = random.randint(0, len(currSchedule))
    while (day1 == day2):
        day2 = random.randint(0, len(currSchedule))
        
    # find the length of the routes:
    len1 = len(currSchedule[day1])
    len2 = len(currSchedule[day2])
    
    # for route1 (removed and inserted into day2)
    route1Len = random.randint(1, min(len1, nHood))
    # for route2 (removed and inserted into day1)
    route2Len = random.randint(0, min(len2, nHood))
    

    # setting route and  new day to be what they should be
    route1 = currSchedule[day1][route1Start : route1Start + route1Len]
    newDay1 = currSchedule[day1][:route1Start] + currSchedule[day1][route1Start + route1Len:]
    
    
    # starting index of the sub-route we will be removing
    route2Start = random.randint(0, len2 - route2Len + 1)
    route2 = currSchedule[day2][route2Start:route2Start + route2Len]
    newDay2 = currSchedule[day2][:route2Start] + route1 + currSchedule[day2][route2Start + route2Len:]
    
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
    # list of possible start indices for routes in day 1 of valid length s.t each task has a time window in day 2 
    possRouteStarts = []
    # start index of the current route we are looking at 
    currRouteStart = 0
    # start index of the longest route
    longestRouteStart = 0
    # length of longest route 
    longestRouteLen = 0
    
    # route1: choose random segment w/ customers who have a valid time window in newDay
    # if there is no such route, choose the longest route.
    while n < len(origRoute):
        
        # checking to see if the current route is longer than longest route, if it is update 
        # longest route start and length
        if (n - currRouteStart) > longestRouteLen:
            longestRouteStart = currRouteStart
            longestRouteLen = n - currRouteStart
        
        # if task(n) has a valid time window in day 2, check to see if the route from curr start to n is 
        # long enough, if so add it to possible list of routes
        if(len(origRoute1[n].timeWindows[newDay]) > 0):
            if n - currRouteStart == route1Len - 1:
                possRoutes.append(currRouteStart)
                currRouteStart += 1
        
        # move on to the next route if previous conditional statement was no satisfied 
        else:
            currRouteStart = n + 1
        n += 1
    
    # if we found a viable route, choose a random one 
    if len(possRoutes) > 0:
        route1Start = possRoutes[random.randint(len(possRouteStarts))]
    # otherwise choose longest 
    else:
        route1Start = longestRouteIndex
        route1Len = longestRouteLen
    
    return (route1Start, route1Start + route1Len)
    
    
'''
@return: modified schedule
'''
def optionalExchange1(currSchedule, nHood):
#     print "********** Entering optExchange1**********"

    # set p and q according to nHood Index
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
            unplannedTasks.append(task)
        newDay = currSchedule[day][:pos] + currSchedule[day][pos + numToRemove:]
        
    else:
        newDay = currSchedule[day][:]

    # selecting which unplanned tasks to add
    addingTasks = []
    for t in range(numToAdd):
        if len(unplannedTasks) > 0:
            addingTasks.append(unplannedTasks.popleft())
          
    # adding new tasks to day 
    newDay = newDay[:pos] + addingTasks + newDay[pos:]
    
    newRoute = Objects.Route()
    
    for task in newDay:
        newRoute.append(task, None)
    
     # replace the chosen days with the updated days   
    currSchedule[day] = newRoute
    
#     print "********** Exiting optExchange1 **********"
    return currSchedule

'''
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
#     print isinstance(currSchedule[0], Objects.Route)   
    # If nHood< 13: do 3-OPT
    if nHood < 13:
        # only currSchedule because we believe edges are being removed and inserted within the solution
        newSolution = threeOPT(taskList, currSchedule)

    # Otherwise: Best Insertion
    else:
        newSolution = bestInsertion(taskList, currSchedule)
#     print isinstance(currSchedule[0], Objects.Route)   
#     print "********** Exiting iterativeImprovement **********"
    return newSolution
'''
@return: solution that has been modified by 3-Opt
'''
def threeOPT(taskList, currSchedule):
#     print "********** Entering threeOPT **********"
#     print isinstance(currSchedule[0], Objects.Route)       
#     printSolution(currSchedule)
    return currSchedule
    
    # MUST ASSUME START AND END ARE CONNECTED?
    
    # THIS IS NO LONGER GOING TO WORK BECAUSE IT IS SPECIFICALLY FOR ROUTES
    # WE ONLY KNOW ABOUT ROUTE DURATION ONCE WE'VE RUN ISFEASIBLE
    duration = getScheduleDuration(taskList, currSchedule)
    #duration = 1
    
    #ABBY CHANGE THIS FOR DEBUGGING
    improvement = False
    
    # CHANGE THIS
    # pick a random day to optimize
    day = random.randint(0, len(currSchedule) - 1)
    currRoute = currSchedule[day]
    routeLength = len(currRoute)
    print("routLength is " + str(routeLength))
    # 2
    
    
    if routeLength > 3:
        
        maxM = math.factorial(routeLength) / (6 * math.factorial(routeLength - 3))
        print(maxM)
    else:
        return currSchedule
    #ABBY CHANGE THIS FOR DEBUGGING
    m = 0
    #MAKE THIS AND and not OR??????????
    while improvement == False and m < maxM:

        # 5
        for n in range(0, routeLength -1):
            
            # 8
            for k in range(0, routeLength - 2):
        
                # 9 limiting the number of nodes that can move to 3
                topRange = min(k+4, routeLength - 2)
                
                for j in range(k + 1, topRange, 1):
                    #print(j)
                    # 10
                    distance1 = helperFunctions.getDistanceBetweenTasks(currRoute[k], currRoute[j + 1]) + helperFunctions.getDistanceBetweenTasks(currRoute[0], currRoute[j])
                    distance2 = helperFunctions.getDistanceBetweenTasks(currRoute[0], currRoute[j + 1]) + helperFunctions.getDistanceBetweenTasks(currRoute[k], currRoute[j])
                    # 11
                    distance3 = helperFunctions.getDistanceBetweenTasks(currRoute[0], currRoute[routeLength-1]) + helperFunctions.getDistanceBetweenTasks(currRoute[k], currRoute[k + 1]) + helperFunctions.getDistanceBetweenTasks(currRoute[j], currRoute[j + 1])
                    # 10
#                     print("distance1 is " + str(distance1))
#                     print("distance2 is " + str(distance2))
                    if  distance1 <= distance2:
                        d = distance1
                        print("Entered if")
#                         print("distance3 is " + str(distance3))
#                         print(d + helperFunctions.getDistanceBetweenTasks(currRoute[k + 1], currRoute[routeLength-1]))
                        # 11
                        if d + helperFunctions.getDistanceBetweenTasks(currRoute[k + 1], currRoute[routeLength-1]) < distance3:
                            # 16
                            print("entered second if")
                            # make newSchedule = [j+2....routeLength, k+1, 1...k,j+1] 
                            newRoute = Objects.Route()
                            
                            #CHECK THESE INDICES
                            for i in range(j+1, routeLength):
                                newRoute.append(currRoute[i], None)
                            newRoute.append(currRoute[k], None)
                            for l in range(0, k-1):
                                newRoute.append(currRoute[l], None)
                            newRoute.append(currRoute[j], None)
                            newSchedule = currSchedule
                            newSchedule[day] = newRoute
                            print("here?")
                            #printSolution(newSchedule)
                            
                            newDuration = getScheduleDuration(taskList, newRoute)
                            #newDuration = 0
                            if newDuration < duration:
                                print("got hereererere 1")
                                newSolution = newSchedule
                                improvement = True
                                break
                        #??????????????????
                        else:
                            print("entered else after if")
                            printSolution(currSchedule)
                            return currSchedule
                    # 10
                    else:
                        d = distance2
                        print("Entered else")
                        # 11
                        if d + helperFunctions.getDistanceBetweenTasks(currRoute[k + 1], currRoute[routeLength-1]) < distance3:
                            # 18
                            
                            # make newSchedule = [j+2....routeLength, k+1, k...1,j+1]
                           
                            newRoute = Objects.Route()
                            
                            #CHECK THESE INDICES
                            for i in range(j+1, routeLength):
                                newRoute.append(currRoute[i], None)
                            newRoute.append(currRoute[k], None)
                            for l in range(k-1, 0, -1):
                                newRoute.append(currRoute[l], None)
                            newRoute.append(currRoute[j], None)
                            newSchedule = currSchedule
                            newSchedule[day] = newRoute
                            print("here2?")
                            #printSolution(newSchedule)
                            
                            newDuration = getScheduleDuration(taskList, newRoute)
                            #newDuration = 0
                            if newDuration < duration:
                                print("got hereererere 2")
                                newSolution = newSchedule
                                improvement = True
                                break
                        else:
                            print("entered else after else")
                            printSolution(currSchedule)
                            return currSchedule
                if(improvement):
                    break
            if(improvement):
                    break
        m += 1
        
    print isinstance(currSchedule[0], Objects.Route)
    print("currSchedule")
    printSolution(currSchedule)  
    print("newSchedule")
    printSolution(newSolution) 
    print "********** Exiting threeOPT **********"
    return newSchedule



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
                   
                    # calculates what the distance would be if the task under consideration where to be added between task1 and task2
                    addedDist = helperFunctions.getDistanceBetweenTasks(task1, currTask) + \
                    helperFunctions.getDistanceBetweenTasks(currTask, task2) - \
                    helperFunctions.getDistanceBetweenTasks(task1, task2)
                    
                    # if the calculated distance is less than the shortestDistance value then reset shortestDistance and save the day and pos
                    if addedDist < shortestDistance:
                        shortestDistance = addedDist
                        insertLocation = (day, pos)
        
        # adding the 'valid' task to the day at the specified position 
        if isValid:
            newSolution = Objects.Route()
            day = insertLocation[0]
            pos = insertLocation[1]
            newSolution.taskList = currSchedule[day][:pos]
            newSolution.append(currTask, None)
            currSchedule[day] = newSolution + currSchedule[day][pos:]
            tasksSinceLastInsertion = 0
        
        # if not valid then increment and add the task that was being evaluated back into the unplannedTasks list     
        else:
            tasksSinceLastInsertion += 1
            unplannedTasks.append(currTask)
    
    # after all that, add the task to the solution in the time with smallest added distance.

#     print "********** Exiting bestInsertion **********"
    return currSchedule




'''
@return: solution if currSolution is feasible
'''
def isFeasible(taskList, currSchedule):
#     print "********** Entering isFeasible **********"
    
    # deepcopy currSchedule. We will be changing timewindows
    currSchedule = copy.deepcopy(currSchedule)
    
    
    # with no ending times in the routes yet
    for r in range(len(currSchedule)):
        route = currSchedule[r]
        
        # for each task except the first, add travel time from prev task to curr task
        # to the duration of task, then subtract that same time from each time window
        # start, and from release time.
        for t in range(1, len(route)):
            task = route[t]
            # include travel time in these duplicate tasks. (added to duration of task,
            # subtract from release time and time window starts)
            travelTime = helperFunctions.getDistanceBetweenTasks(task, route[t - 1])
            task.duration = task.duration + travelTime
            task.releaseTime = task.releaseTime - travelTime
            for tw in range(len(task.timeWindows[r])):
                oldTW = task.timeWindows[r][tw]
                newTW = (oldTW[0] - travelTime, oldTW[1])
                task.timeWindows[r][tw] = newTW
    
    
    # pass that into tightenTWStarts and tightenTWEnds. 
    # those functions will modify those tasks' time windows and return the modified schedule
    currSchedule = tightenTWStarts(currSchedule)
    currSchedule = tightenTWEnds(currSchedule)
    
    # If those terminate early and return None, the schedule is infeasible. Return None
    if currSchedule == None:
#         print "InFeasible Route"
#         print "********** Exiting isFeasible **********"
        return None
    
    
    # Otherwise, squidge to find the best schedule for this solution
    feasSol = minRoute(taskList, currSchedule)
    
#     print "********** Exiting isFeasible **********" 
    return feasSol
                

'''
@return: modified schedule with tightened tw starts
'''
def tightenTWStarts(currSchedule):
#     print "********** Entering tightenTWStarts **********"
    #AVERY THIS DOESN'T WORK RIGHT: TW STARTS NOT GETTING SET
#     print isinstance(currSchedule[0], Objects.Route)   
    if currSchedule == None:
        return None
    for d in range(len(currSchedule)):
        custIndex = 0
        day = currSchedule[d]
        task = day.taskList[custIndex]
        tw = task.timeWindows[d]
        while custIndex < len(day) - 1 and len(day.taskList[custIndex].timeWindows) > 0 :
            task = day.taskList[custIndex]
            tw = task.timeWindows[d]
            twNext = day.taskList[custIndex + 1].timeWindows[d]
            
         # if duration of task i does not fit in its first tw or it can fit between the start of its second time window
         #  and the start of the next task's first tw
            if task.duration > tw[0][1] - tw[0][0] or (len(tw) > 1 and task.duration + tw[1][0] < twNext[0][0]):
                # remove that task's first tw
                tw = tw[1:]
                if len(tw) == 0:
                    break
                
            elif task.duration + tw[0][0] < twNext[0][0]:
                # set the beginning of that time window to be the minimum of the the ending time of task i's first time window
                # and the start of task i+1's first time window
                tw[0] = (min(twNext[0][0], tw[0][1]) - task.duration, tw[0][1])

        # else if the duration of task i set at the beginning of its first tw overlaps any tws for the next customer
            elif task.duration + tw[0][0] > twNext[0][0]:
                # reset the beginnings of all time windows to be as early as possible
                # after the end of task i (with i scheduled as early as possible)
                for w in range(len(twNext)):
                    twNext[w] = (max(tw[0][0] + task.duration, twNext[w][0]), twNext[w][1])
            custIndex += 1
        #if this is the last customer and they still have time windows left,
        if custIndex == len(day) - 1 and len(day.taskList[custIndex].timeWindows) > 0 and task.duration > tw[0][1] - tw[0][0]:
                # remove that task's first tw
                tw = tw[1:]
            
        custIndex += 1
        
        if custIndex < len(day.taskList):
            return None
#     print "********** Exiting tightenTWStarts **********"
    return currSchedule

'''
@return: modified schedule with tightened tw ends
'''
def tightenTWEnds(currSchedule):
#     print "********** Entering tightenTWEnds **********"
    if currSchedule == None:
        return None
    
    for dayIndex in range(len(currSchedule)):
        custIndex = len(currSchedule[dayIndex].taskList) - 1
        day = currSchedule[dayIndex]
        task = day.taskList[custIndex]
        tw = task.timeWindows[dayIndex]
        while custIndex > 0 and len(day.taskList[custIndex].timeWindows) > 0:
            task = day.taskList[custIndex]
            tw = task.timeWindows[dayIndex]
            twPrev = day.taskList[custIndex - 1].timeWindows[dayIndex]
            # if duration of task i does not fit in its last tw or it can fit between the end of its second to last time w
            #  and the end of the previous task's last tw:
            if task.duration > tw[-1][1] - tw[-1][0] or (len(tw) > 1 and task.duration + tw[-2][0] < twPrev[-1][0]):
                # remove the last time w
                tw = tw[:-1]
                if len(tw) == 0:
                    break
            # else if duration of task i at the end of its last tw starts before the end of the previous task's last tw
            elif tw[-1][1] - task.duration < twPrev[-1][1]:
                # set the end of that time w to be the maximum of the the starting time of task i's last time w
                # and the end of task i-1's last time w
                tw[-1] = (tw[-1][0], max(twPrev[-1][1], tw[-1][0] + task.duration))
             
            # else if the duration of task i set at the end of its last tw overlaps any tws for the previous customer
            elif tw[-1][1] - task.duration > twPrev[-1][1]:
                # reset the endings of all time windows to be as late as possible
                # before the beginning of task i (with i scheduled as late as possible)
                for w in range(len(twPrev)):
                    twPrev[w] = (twPrev[w][0], min(tw[-1][1] - task.duration, twPrev[w][1]))

            custIndex -= 1
        if custIndex == 0 and len(day.taskList[custIndex].timeWindows) > 0:
            if task.duration > tw[0][1] - tw[0][0]:
                # remove that task's first tw
                tw = tw[:-1]
            
        custIndex -= 1
        
        if custIndex > 0:
            return None
    
#     print "********** Exiting tightenTWEnds **********"
    return currSchedule

'''
@return: shortest duration of this schedule ordering
'''
def minRoute(taskList, currSchedule):
#     print "********** Entering minRoute **********"
    #AVERY ENDING times are almost all the same. still wrong
    bestSchedule = copy.deepcopy(currSchedule)
    
#     print bestSchedule
    
    # Minimize each route
    for d in range(len(currSchedule)):
        day = currSchedule[d]
        
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
        bestRoute = dominantRoute(day, assignedTWs, d)
        latestWaitingTask = getLatestWaitingTask(bestRoute)
        
        # While this there are still tasks with waiting time and the latest
        # waiting task has time windows to switch to
        while latestWaitingTask > -1 and assignedTWs[latestWaitingTask] < len(day[latestWaitingTask].timeWindows[d]) - 1:
            # move the latest waiting task to its next time window.
            newRoute = switchTimeWindows(bestRoute, latestWaitingTask, d, assignedTWs)
            # find the shortest route with that ending time
            newRoute = dominantRoute(newRoute, assignedTWs, d)
            
            # if it's better than the best so far, update the best.
            if(getRouteDuration(newRoute) < getRouteDuration(bestRoute)):
                bestRoute = newRoute
            latestWaitingTask = getLatestWaitingTask(newRoute)
        # update the schedule to have this route
        bestSchedule[d] = bestRoute
    

    # Set bestSchedule tasks to be the original tasks from the tasklist
    # We do this to remove changes we made to time windows in the
    # preprocessing steps
    for r in range(len(bestSchedule)):
        for t in range(len(bestSchedule[r])):
            bestSchedule[r][t] = taskList[bestSchedule[r][t].id]
#     print bestSchedule
#     print "********** Exiting minRoute **********"
#     print
    return bestSchedule



'''
@return: the index for the last task with waiting time in the route
'''
def getLatestWaitingTask(currRoute):
    for task in range(len(currRoute) - 1, 0, -1):
        if currRoute.endingTimes[task] - currRoute[task].duration > currRoute.endingTimes[task - 1]:
            return task - 1
            #AVERY check: should this be task or task - 1?
    return -1

'''
@return: the updated schedule after moving the latestWaitingTask to the next time window and updating the other tasks
'''
def switchTimeWindows(currRoute, latestWaitingTaskIndex, day, assignedTWs):
#     print "********** Entering switchTimeWindows **********"
    
    #store the task we are working with
    latestWaitingTask = currRoute[latestWaitingTaskIndex]
    # store the new time window it is moving to
    tw = latestWaitingTask.timeWindows[day][assignedTWs[latestWaitingTaskIndex] + 1]
    
    #moving the latestWaitingTask to its next time window as early as possible within the new time window
    latestWaitingTask.endingTime = latestWaitingTask.duration + tw[0]
    
    # update the assigned time window for the task we are working with
    assignedTWs[latestWaitingTaskIndex] += 1
    
    #storing the surrounding tasks starts and ends
    nextTaskStart = tw[0]
    prevTaskEnd = tw[0] + latestWaitingTask.duration
    
    # Move all tasks before latestWaitingTask as late as possible 
    # from latest waiting task backwards
    for t in range(latestWaitingTaskIndex - 1, -1, -1):
        task = currRoute[t]
        routeTWs = task.timeWindows[day]
        # for each time window in that route find the latest possible time window
        # that fits this task before the end of that time window and the start of the next task
        for tw in range(len(routeTWs)):
            timeWindow = routeTWs[tw]
            if timeWindow[0] + task.duration <= nextTaskStart:
                assignedTWs[t] = tw
                task.endingTime = min(nextTaskStart, timeWindow[1])
            else:
                nextTaskStart = task.endingTime - task.duration
                break
            
    # Move all tasks after latestWaitingTask as early as possible
    # AVERY CHECK THIS
    for t in range(latestWaitingTaskIndex + 1, len(assignedTWs)):
        task = currRoute[t]
        routeTWs = task.timeWindows[day]
        # AVERY: DOES THIS GO BACKWARDS correctly?
        for tw in range(len(routeTWs) - 1, -1, -1):
            timeWindow = routeTWs[tw]
            if timeWindow[1] - task.duration >= prevTaskEnd:
                assignedTWs[t] = tw
                task.endingTime = max(prevTaskEnd, timeWindow[0]) + task.duration
            else:
                prevTaskEnd = task.endingTime
                break
                
    return currRoute

'''
Given the ending time of currSolution, move all tasks to the latest possible
time without changing that ending time

@return: the dominant version of the schedule being passed in (squidging)
'''
def dominantRoute(currRoute, assignedTWs, dayIndex):
    #AVERY I believe the problem is here
    
    # put everything as late as possible within the assigned time window
    nextTaskStart = currRoute.endingTimes[-1] - currRoute[-1].duration
    
#     print nextTaskStart
    
    #goes through the current route backwards ignoring the last task
    for t in range(len(currRoute) - 2, -1, -1):
        task = currRoute[t]
        timeWindows = task.timeWindows[dayIndex]
        
        #go through each time window for each task find latest time it could be 
        #scheduled given that the last task has not moved 
        for tw in range(assignedTWs[t], len(timeWindows)):
            timeWindow = timeWindows[tw]
            if timeWindow[0] + task.duration <= nextTaskStart:
                currRoute.endingTimes[t] = min(timeWindow[1], nextTaskStart)
                assignedTWs[t] = tw
            else:
                nextTaskStart = currRoute.endingTimes[t] - task.duration
                break
    
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



'''
@return: the length of time from the start of the first task to the end of the last
'''
def getRouteDuration(currRoute):    
    # AVERY: put this in Object.Route instead
    # doesn't work if it's infeasible. If it is infeasible, I'm returning infinity
    if len(currRoute) == 0:
        return 0
    if currRoute.endingTimes[-1] == None or currRoute.endingTimes[0] == None:
        return float("inf")
    return currRoute.endingTimes[-1] - currRoute.endingTimes[0] + currRoute.taskList[0].duration

'''
@return: the length of a schedule from the start of the first 
    route to the end of the last
'''
def getScheduleDuration(taskList, currSchedule):
    sum = 0
    
    feasSched = copy.deepcopy(currSchedule)
    
    feasSched = isFeasible(taskList, feasSched)
    
    if feasSched != None:
        for route in feasSched:
            sum += getRouteDuration(route)
        return sum
    
    for route in currSchedule:
        sum += getRouteDuration(route)
    return sum

'''
@return: total distance of a solution
'''
def calcTotalDistance(currSolution):
    return 0


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
    

def main():
    print "********** Main **********"
    print solve("test.csv")
    
if __name__ == "__main__":
    main()
    


