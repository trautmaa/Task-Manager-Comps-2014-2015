# Comps 2014
# Larkin Flodin, Avery Johnson, Maraki Ketema, 
# Abby Lewis, Will Schifeling, and  Alex Trautman

from greedy_by_order import *
from create_tasks_from_csv import *
from helper_functions import *
from Objects import *
import time
import math
import random


global timeLimit
timeLimit = 8


'''
@return: an ordering of tasks
'''
def solve(csvFile):
    #Get a greedy algorithm to then modify with VNS
    taskList = get_task_list(csvFile)
    modTasks = run_greedy_by_order(csvFile, order_by_deadline)
    
    #Modify the greedy algorithm
    modTasks = vns(taskList, modTasks)
    
    return create_schedule(modTasks, taskList)

'''
@return: modified solution
'''

def vns(taskList, currSolution):
    
    global unplannedTasks
    unplannedTasks = deque(taskList[:])
    
    for day in currSolution:
        for task in day:
            unplannedTasks.remove(task)
    
    #Number of seconds VNS is allowed to run
    stoppingCondition = 300
    
    #Number of neighborhood structures
    nHoodMax = 17
    
    #Number of iterations since last bestSolution update
    numIterations = 0
    
    bestSolution = currSolution
    initTime = time.time()
    
    #until the stopping condition is met
    while time.time() - initTime > 0:
        #If we have gone through all neighborhood structures,
        #start again
        nHood = 1
        while nHood < nHoodMax:
            shakeSolution = shaking(currSolution, nHood)
            iterSolution = iterativeImprovement(taskList, shakeSolution, nHoodIndex)
            
            #make sure the modified solution is still feasible. 
            # If it is not, try again
            # If it is, and it is a better solution, update bestSolution
            feasibleSolution = isFeasible(taskList, iterSolution)
            if feasibleSolution == None:
                feasible = False
            else:
                feasible = True
                iterSolution = feasibleSolution
            
            #if feasible and better
            #     accept it as the new solution, reset nHood of numIterations
            
            if feasible:
                #If our solution is better than the current solution, update.
                if isBetter(iterSolution, currSolution):
                    currSolution = iterSolution
                    nHood = 1
                #Otherwise, increment nHood
                else:
                    nHood += 1
                
                #If our solution is better than the best solution so far, update.
                if isBetter(iterSolution, bestSolution):
                    bestSolution = iterSolution
                    numIterations = 0
                    
            #If we have gone 8000 iterations with no improvement to bestSolution
            # If criteria for selection are true, select a new currSolution
            elif numIterations > 8000:
                numIterations = 0
                
                if nHood > 8:
                    currSolution = iterSolution
                    nHood = 1
                #Criteria for nHoods 1-8:
                # If the new solution is not more than .5% longer (distance), accept
                elif calcTotalDistance(iterSolution) >= .995*calcTotalDistance(currSolution):
                    currSolution = iterSolution
            else:
                numIterations += 1
    return bestSolution


'''
@return: modified solution
'''
def shaking(currSolution, nHoodIndex):
    #Based on the neighborhood perform a different operation
    if nHoodIndex <= 8:
        newSolution = crossExchange(currSolution, nHoodIndex)
    elif nHoodIndex > 8 and nHoodIndex <= 12:
        newSolution = optionalExchange1(currSolution, nHoodIndex)
    else:
        newSolution = optionalExchange2(currSolution, nHoodIndex)
    return newSolution

'''
@param currSolution: list (schedule) of lists (days/routes) of task objects
@return: modified solution
'''
def crossExchange(currSolution, nHoodIndex):
    
    if(len(currSolution) <= 1):
        return currSolution
    # choose two distinct random days
    day1 = random.randint(0, len(currSolution))
    day2 = random.randint(0, len(currSolution))
    while (day1 == day2):
        day2 = random.randint(0,len(currSolution))
        
    # find the length of the routes to be exchanged:
    len1 = len(currSolution[day1])
    len2 = len(currSolution[day2])
    
    # for route1 (removed and inserted)
    route1Len = random.randint(1, min(len1, nHoodIndex))
    # for route2 (replaced by route1)
    route2Len = random.randint(0, min(len2, nHoodIndex))
    
    n = 0
    # whole route for day one
    origRoute1 = currSolution[day1]
    #list of possible start indices for routes in day 1 of valid length s.t each task has a time window in day 2 
    possRouteStarts = []
    #start index of the current route we are looking at 
    currRouteStart = 0
    #start index of the longest route
    longestRouteStart = 0
    #length of longest route 
    longestRouteLen = 0
    
    # route1: choose random segment w/ customers who have a valid time window in day2
    # if there is no such route, choose the longest route.
    while n < len(origRoute1):
        
        # checking to see if the current route is longer than longest route, if it is update 
        #longest route start and length
        if (n - currRouteStart) > len(longestRoute):
            longestRouteStart = currRouteStart
            longestRouteLen = n - currRouteStart
        
        #if task(n) has a valid time window in day 2, check to see if the route from curr start to n is 
        # long enough, if so add it to possible list of routes
        if(len(origRoute1[n].time_windows[day2]) > 0):
            if n - currRouteStart == route1Len - 1:
                possRoutes.append(currRouteStart)
                currRouteStart += 1
        
        #move on to the next route if previous conditional statement was no satisfied 
        else:
            currRouteStart = n + 1
        n+=1
    
    #if we found a viable route, choose a random one 
    if len(possRoutes) > 0:
        route1Start = possRoutes[random.randint(len(possRouteStarts))]

    # otherwise choose longest 
    else:
        route1Start = longestRouteIndex
        route1Len = longestRouteLen

    #setting route and  new day to be what they should be
    route1 = currSolution[day1][route1Start : route1Start + route1Len]
    newDay1 = currSolution[day1][:route1Start] + currSolution[day1][route1Start + route1Len:]
    
    
    #starting index of the sub-route we will be removing
    route2Start = random.randint(0, len2 - route2Len + 1)
    route2 = currSolution[day2][route2Start:route2Start + route2Len]
    newDay2 = currSolution[day2][:route2Start] + route1 + currSolution[day2][route2Start + route2Len:]
    
    for task in route2:
        unplannedTasks.append(task)
    
    # remove route1 from day1, remove route2 from day2, insert route1 into day2 where route2 was
    currSolution[day1] = newDay1
    currSolution[day2] = newDay2
    return currSolution

'''
@return: modified solution
'''
def optionalExchange1(currSolution, nHoodIndex):
    # set p and q according to nHood Index
    numToRemove = nHoodIndex - 9
    numToAdd = 1
    if nHoodIndex == 12:
        numToRemove= 0
        numToAdd = 2
    
    # pick a random day and starting time to exchange customers
    day = random.randint(0, len(currSolution))
    pos = random.randint(0, len(currSolution[day]))
    
    # using the numToRemove and numToAdd values, add and remove however many customers you need to
    for task in currSolution[day][pos:pos+ numToRemove]:
        unplannedTasks.append(task)
    newDay = currSolution[day][:pos] + currSolution[day][:pos + numToRemove]
    
    #selecting which unplanned tasks to add
    addingTasks = []
    for t in range(numToAdd):
        addingTasks.append(unplannedTasks.popleft())
    
    #adding new tasks to day 
    newDay = newDay[:pos] + addingTasks + newDay[pos:]
 
     # replace the chosen days with the updated days   
    currSolution[day] = newDay
    
    return currSolution

'''
@return: modified solution
'''
def optionalExchange2(currSolution, nHoodIndex):
    # calculate number to remove (nHoodIndex-12)
    numToRemove = nHoodIndex - 12
    # pick a random day and position
    
    # pick a random day and starting time to exchange customers
    day = random.randint(0, len(currSolution))
    pos = random.randint(0, len(currSolution[day]))
    
    # using the numToRemove and numToAdd values, add and remove however many customers you need to
    for task in currSolution[day][pos:pos+ numToRemove]:
        unplannedTasks.append(task)
    newDay = currSolution[day][:pos] + currSolution[day][:pos + numToRemove]
    
    currSolution[day] = newDay
    
    return currSolution


'''
@return: modified solution
'''
def iterativeImprovement(taskList, currSolution, nHoodIndex):
    #If nHoodIndex< 13: do 3-OPT
    if nHoodIndex < 13:
        #only currSolution because we believe edges are being removed and inserted within the solution
        newSolution = threeOPT(currSolution)
    #Otherwise: Best Insertion
    else:
        newSolution = bestInsertion(taskList, currSolution)
    return currSolution
'''
@return: solution that has been modified by 3-Opt
'''
def threeOPT(currSolution):
    #MUST ASSUME START AND END ARE CONNECTED?
    duration = getDuration(currSolution)
    improvement = False
    #CHECK DEPENDING ON HOW WE STORE SCHEDULES
    scheduleLength = len(currSolution)
    #2
    maxM = math.factorial(scheduleLength)/(6*math.factorial(scheduleLength-3))
    m = 0
    while improvement == False or m <= maxM:
        #5
        for n in range(0, scheduleLength):
            #8
            for k in range(0, scheduleLength - 3):
                #9 limiting the number of nodes that can move to 3
                for j in range(k+1, min(k + 4, scheduleLength-1)):
                    #10
                    distance1 = dist(currSolution[k], currSolution[j+1]) + dist(currSolution[1], currSolution[j])
                    distance2 = dist(currSolution[1], currSolution[j+1]) + dist(currSolution[k], currSolution[j])
                    #11
                    distance3 = dist(currSolution[1], currSolution[scheduleLength]) + dist(currSolution[k], currSolution[k+1]) + dist(currSolution[j], currSolution[j+1])
                    #10
                    if  distance1 <= distance2:
                        d = distance1
                        #11
                        if d + dist(currSolution[k+1], currSolution[scheduleLength]) < distance3:
                            #16
                            # make newSchedule = [j+2....schedulelength, k+1, 1...k,j+1] 
                            #newDuration = check duration
                            if newDuration < duration:
                                newSolution = newSchedule
                                improvement = True
                                break
                    #10
                    else:
                        d = distance2
                        #11
                        if d + dist(currSolution[k+1], currSolution[scheduleLength]) < distance3:
                            #18
                            # make newSchedule = [j+2....schedulelength, k+1, k...1,j+1]
                            #newDuration = check duration
                            if newDuration < duration:
                                newSolution = newSchedule
                                improvement = True
                                break
                if(improvement):
                    break
            if(improvement):
                    break
        m+=1
    
    return newSolution



'''
@return: solution that has been modified by 3-Opt
'''
def bestInsertion(taskList, currSolution):
    # Sequentially consider tasks from unplannedTasks
    # For each day, if that task:
        # has a time window in that day
        # and the duration of that day + that task's duration <= timeLimit
    # find the additional distance of adding that task in that location
    # if that is smaller than the smallest so far, update smallest
    
    #otherwise, enqueue it and go to the next task

    tasksSinceLastInsertion = 0
    
    # while we have not explored all of the unplanned tasks
    while tasksSinceLastInsertion < len(unplannedTasks):
        
        # shortestDistance set to infinity 
        shortestDistance = float("inf")
        # keeps track of the day and position within the day at which to insert task
        insertLocation = (0, 0)
        
        #bool that keeps track of whether a give task is valid 
        isValid = False
    
        currTask = unplannedTasks.popleft()
        
        #looping through each day in the current solution list 
        for day in range(len(currSolution)):
            
            #if the duration of the task under consideration added to the current day is less than the time limit then accept it as
            # valid  
            if len(currTask.time_windows[day]) > 0 and getDuration(currSolution[day]) + currTask.duration < timeLimit:
                isValid = True
                
                #for each position within the day 
                for pos in range(len(currSolution[day])-1):
                    
                    task1 = currSolution[day][pos]
                    task2 = currSolution[day][pos + 1]
                   
                    #calculates what the distance would be if the task under consideration where to be added between task1 and task2
                    addedDist = calcDistance(task1, currTask) + calcDistance(currTask, task2) - calcDistance(task1, task2)
                    
                    #if the calculated distance is less than the shortestDistance value then reset shortestDistance and save the day and pos
                    if addedDist < shortestDistance:
                        shortestDistance = addedDist
                        insertLocation = (day, pos)
        
        #adding the 'valid' task to the day at the specified position 
        if isValid:
            currSolution[day] = currSolution[day][:pos].append(currTask) + currSolution[day][pos:]
            tasksSinceLastInsertion = 0
        
        # if not valid then increment and add the task that was being evaluated back into the unplannedTasks list     
        else:
            tasksSinceLastInsertion += 1
            unplannedTasks.append(currTask)
                        
                
    
    
    
    # after all that, add the task to the solution in the time with smallest added distance.
        
    return currSolution


'''
@return: True if sol1 has more profit than sol2
'''
def isBetter(sol1, sol2):
    sum1 = 0 #sum profits in sol1 (number of tasks, right now)
    sum2 = 0 #sum profits in sol2
    return True

'''
@return: solution if currSolution is feasible
'''
def isFeasible(taskList, currSolution):
    return True

'''
@return: Graph with modified release times
'''
def tightenReleaseTimes(taskList, currSolution):
    return G

'''
@return: Graph with modified deadlines
'''
def tightenDeadlines(taskList, currSolution):
    return G

'''
@return: shortest duration of this schedule ordering
'''
def minRoute(taskList, currSolution):
    return 0

def calcDominantSolution(taskList, currSolution):
    return currSolution

def getDuration(currSolution):
    return 0

'''
@return: total distance of a solution
'''
def calcTotalDistance(currSolution):
    return 0

'''
@return: distance between two tasks
'''
def calcDistance(task1, task2):
    return 0

