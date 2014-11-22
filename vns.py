# Comps 2014
# Larkin Flodin, Avery Johnson, Maraki Ketema, 
# Abby Lewis, Will Schifeling, and  Alex Trautman

import greedy_by_order
import create_tasks_from_csv
import helper_functions
import Objects
import time
import math
import random
from collections import deque
from brute_force import run_brute_force_alg
from matplotlib.testing.jpl_units import day

global timeLimit
timeLimit = 5000

'''
@return: an ordering of tasks
'''
def solve(csvFile):
    #Get a greedy algorithm to then modify with VNS
    taskList = create_tasks_from_csv.get_task_list(csvFile)
    modTasks = greedy_by_order.run_greedy_by_order(csvFile, greedy_by_order.order_by_deadline)
#     brute = run_brute_force_alg(csvFile)
    
    greedysol = modTasks

    #Modify the greedy algorithm
    modTasks = vns(taskList, modTasks)
    
    print '################ FINAL SOLUTION from VNS #############'
    print modTasks
    print '#############################'
    print 'greedy solution'
    printSolution(greedysol)
#     print 'brute force solution'
#     printSolution(brute)

    return modTasks


'''
@return: best schedule found in time limit
'''
def vns(taskList, currSolution):
    
#     print "********** Entering VNS **********"
#     print "initial solution: "
#     printSolution(currSolution)

    
    global unplannedTasks
    unplannedTasks = deque(taskList[:])
   
    for day in currSolution:
        for task in day:
            unplannedTasks.remove(task)
    
    # Number of seconds VNS is allowed to run
    stoppingCondition = 60
    
    # Number of neighborhood structures
    nHoodMax = 17
    
    # Number of iterations since last bestSolution update
    numIterations = 0
    
    bestSolution = currSolution
    currSchedule = isFeasible(taskList, currSolution)
    bestSchedule = currSchedule
    
    initTime = time.time()
    
    iterCount = 0
    
    # until the stopping condition is met
    while time.time() - initTime < stoppingCondition:
        # If we have gone through all neighborhood structures, start again
        nHood = 1
        while nHood < nHoodMax and time.time() - initTime < stoppingCondition:
            print iterCount, "VNS loops so far with numIterations", numIterations, "nHood:", nHood
            iterCount += 1
            shakeSolution = shaking(currSolution, nHood)
            
            iterSolution = iterativeImprovement(taskList, shakeSolution, nHood)

            #make sure the modified solution is still feasible. 
            # If it is not, try again
            # If it is, and it is a better solution, update bestSolution
            feasibleSchedule = isFeasible(taskList, iterSolution)
            if feasibleSchedule == None:
                feasible = False
            else:
                feasible = True
            
            #if feasible and better
            #     accept it as the new solution, reset nHood of numIterations
            
            if feasible:
                #If our solution is better than the current solution, update.
                if isBetterSchedule(feasibleSchedule, currSchedule):
                    currSolution = iterSolution
                    currSchedule = feasibleSchedule
                    nHood = 1
                #Otherwise, increment nHood
                else:
                    nHood += 1
                
                #If our solution is better than the best solution so far, update.
                if isBetterSchedule(feasibleSchedule, bestSchedule):
                    bestSolution = iterSolution
                    bestSchedule = feasibleSchedule
                    numIterations = 0
                    
                #If we have gone 8000 iterations with no improvement to bestSolution
                # If criteria for selection are true, select a new currSolution
                elif numIterations > 8000:
                    numIterations = 0
                    
                    if nHood > 8:
                        currSolution = iterSolution
                        currSchedule = feasibleSchedule
                        nHood = 1
                    #Criteria for nHoods 1-8:
                    # If the new solution is not more than .5% longer (distance), accept
                    elif calcTotalDistance(iterSolution) >= .995*calcTotalDistance(currSolution):
                        currSolution = iterSolution
                        currSchedule = feasibleSchedule
                else:
                    numIterations += 1 
            else:
                numIterations += 1
                
#     print "********** Exiting VNS **********"
    return bestSchedule


'''
@return: modified solution
'''
def shaking(currSolution, nHood):
#     print "********** Entering shaking **********"
    
    #Based on the neighborhood perform a different operation
    if nHood < 8:
        newSolution = crossExchange(currSolution, nHood)
        
    elif nHood >= 8 and nHood < 12:
        newSolution = optionalExchange1(currSolution, nHood)
        
    else:
        newSolution = optionalExchange2(currSolution, nHood)
        
#     print "********** Exiting shaking **********"
    return newSolution

'''
@param currSolution: list (schedule) of lists (days/routes) of task objects
@return: modified solution
'''
def crossExchange(currSolution, nHood):
#     print "********** Entering crossExchange **********"
    
    #NOTE TO AVERY: MAKE SURE EXCHANGE
    
    if len(currSolution) <= 1:
#         print "Not doing cross exchange"
#         print "********** Exiting crossExchange **********"
        return currSolution
    
    # choose two distinct random days
    day1 = random.randint(0, len(currSolution))
    day2 = random.randint(0, len(currSolution))
    while (day1 == day2):
        day2 = random.randint(0,len(currSolution))
        
    # find the length of the routes:
    len1 = len(currSolution[day1])
    len2 = len(currSolution[day2])
    
    # for route1 (removed and inserted)
    route1Len = random.randint(1, min(len1, nHood))
    # for route2 (replaced by route1)
    route2Len = random.randint(0, min(len2, nHood))
    
    
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
    
#     print "********** Exiting crossExchange **********"
    return currSolution

'''
@return: modified solution
'''
def optionalExchange1(currSolution, nHood):
#     print "********** Entering optExchange1**********"
    
    # set p and q according to nHood Index
    numToRemove = nHood - 9
    numToAdd = 1
    if nHood == 12:
        numToRemove= 0
        numToAdd = 2

    # pick a random day and starting time to exchange customers
    day = random.randint(0, len(currSolution)-1)
    
    pos = random.randint(0, len(currSolution[day]))
    
    if numToRemove > 0:
        # using the numToRemove and numToAdd values, add and remove however many customers you need to
        for task in currSolution[day][pos:pos + numToRemove]:
            unplannedTasks.append(task)
        newDay = currSolution[day][:pos] + currSolution[day][pos + numToRemove:]
        
    else:
        newDay = currSolution[day][:]

    #selecting which unplanned tasks to add
    addingTasks = []
    for t in range(numToAdd):
        if len(unplannedTasks)>0:
            addingTasks.append(unplannedTasks.popleft())
          
    #adding new tasks to day 
    newDay = newDay[:pos] + addingTasks + newDay[pos:]
    
     # replace the chosen days with the updated days   
    currSolution[day] = newDay


#     print "********** Exiting optExchange1 **********"
    return currSolution

'''
@return: modified solution
'''
def optionalExchange2(currSolution, nHood):
#     print "********** Entering optExchange2 **********"
    
    # calculate number to remove (nHood-12)
    numToRemove = nHood - 12
    # pick a random day and position
    
    # pick a random day and starting time to exchange customers
    day = random.randint(0, len(currSolution)-1)
    pos = random.randint(0, len(currSolution[day]))
    
    # using the numToRemove and numToAdd values, add and remove however many customers you need to
    for task in currSolution[day][pos:pos+ numToRemove]:
        unplannedTasks.append(task)

    newDay = currSolution[day][:pos] + currSolution[day][pos + numToRemove:]

    currSolution[day] = newDay
    
#     print "********** Exiting optExchange2 **********"
    return currSolution


'''
@return: modified solution
'''
def iterativeImprovement(taskList, currSolution, nHood):
#     print "********** Entering iterativeImprovement **********"
    
    #If nHood< 13: do 3-OPT
    if nHood < 13:
        #only currSolution because we believe edges are being removed and inserted within the solution
        newSolution = threeOPT(currSolution)

    #Otherwise: Best Insertion
    else:
        newSolution = bestInsertion(taskList, currSolution)
   
#     print "********** Exiting iterativeImprovement **********"
    return newSolution
'''
@return: solution that has been modified by 3-Opt
'''
def threeOPT(currSolution):
#     print "********** Entering threeOPT **********"
    
    #MUST ASSUME START AND END ARE CONNECTED?
    duration = getDuration(currSolution)
    improvement = False
    #CHECK DEPENDING ON HOW WE STORE SCHEDULES
    
    #CHANGE THIS
    scheduleLength = len(currSolution)
    #2
    
    if scheduleLength >= 3:
        
        maxM = math.factorial(scheduleLength)/(6*math.factorial(scheduleLength-3))
    else:
        return currSolution
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
#     print "********** Exiting threeOPT **********"
    return currSolution



'''
@return: solution that has been modified by 3-Opt
'''
def bestInsertion(taskList, currSolution):
#     print "********** Entering bestInsertion **********"
    
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
                    addedDist = helper_functions.get_distance_between_tasks(task1, currTask) + \
                    helper_functions.get_distance_between_tasks(currTask, task2) - \
                    helper_functions.get_distance_between_tasks(task1, task2)
                    
                    #if the calculated distance is less than the shortestDistance value then reset shortestDistance and save the day and pos
                    if addedDist < shortestDistance:
                        shortestDistance = addedDist
                        insertLocation = (day, pos)
        
        #adding the 'valid' task to the day at the specified position 
        if isValid:
            day = insertLocation[0]
            pos = insertLocation[1]
            newSolution = currSolution[day][:pos]
            newSolution.append(currTask)
            currSolution[day] = newSolution + currSolution[day][pos:]
            tasksSinceLastInsertion = 0
        
        # if not valid then increment and add the task that was being evaluated back into the unplannedTasks list     
        else:
            tasksSinceLastInsertion += 1
            unplannedTasks.append(currTask)
    
    # after all that, add the task to the solution in the time with smallest added distance.

#     print "********** Exiting threeOPT **********"
    return currSolution


'''
This works with Schedule objects
@return: True if sol1 has more profit than sol2
'''
def isBetterSchedule(sched1, sched2):
    sum1 = sched1.getProfit()
    sum2 = sched2.getProfit()
    
    return sum1 > sum2

'''
@return: solution if currSolution is feasible
'''
def isFeasible(taskList, currSolution):
#     print "********** Entering isFeasible **********"
    
    #NOTE FROM AVERY: Does not yet take travel times into account!
    
    # pass in a list-solution
    # create a schedule object with DUPLICATE TASK OBJECTS for that list-solution
    # with no ending times in the routes yet
    currSchedule = Objects.Schedule()
    for day in currSolution:
        route = Objects.Route()
        for task in day:
            route.append(task.deepCopy(), None)
        currSchedule.append(route)
    
    # pass that into tightenTWStarts and tightenTWEnds. 
    # those functions will modify those tasks' time windows and return the modified schedule
    currSchedule = tightenTWStarts(taskList, currSchedule)
    currSchedule = tightenTWEnds(taskList, currSchedule)
    
    # If those terminate early and return None, the schedule is infeasible. Return None
    if currSchedule == None:
        return None
    
    # Otherwise, squidge to find the best schedule for this solution
    feasSol = minRoute(taskList, currSchedule)
    
#     print "********** Exiting isFeasible **********" 
    return feasSol

'''
@return: Graph with modified release times
'''
def tightenTWStarts(taskList, currSchedule):
    
    if currSchedule == None:
        return None
    for dayIndex in range(len(currSchedule)):
        custIndex = 0
        day = currSchedule[dayIndex]
        while custIndex < len(day) - 1 and len(day.task_list[custIndex].time_windows) > 0 :
            task = day.task_list[custIndex]
            tw = task.time_windows[dayIndex]
            twNext = day.task_list[custIndex+1].time_windows[dayIndex]
         # if duration of task i does not fit in its first tw or it can fit between the start of its second time window
         #  and the start of the next task's first tw:
            if task.duration > tw[0][1] - tw[0][0] or (len(tw) > 1 and task.duration + tw[1][0] < twNext[0][0]):
                #remove that task's first tw
                tw = tw[1:]
                
        # else if duration of task i at the beginning of its first tw ends before the start of the next task's first tw
            elif task.duration + tw[0][0] < twNext[0][0]:
                # set the beginning of that time window to be the minimum of the the ending time of task i's first time window
                # and the start of task i+1's first time window
                tw[0][0] = min(twNext[0][0], tw[0][1]) - task.duration

        # else if the duration of task i set at the beginning of its first tw overlaps any tws for the next customer
            elif task.duration + tw[0][0] > twNext[0][0]:
                # reset the beginnings of all time windows to be as early as possible
                # after the end of task i (with i scheduled as early as possible)
                for window in twNext:
                    window = (max(tw[0][0] + task.duration, window[0]), window[1])
            custIndex+= 1
        if custIndex == len(day) -1 and len(day.task_list[custIndex].time_windows) > 0 and task.duration > tw[0][1] - tw[0][0]:
            #remove that task's first tw
            tw = tw[1:]
            
        custIndex += 1
        
        if custIndex < len(day.task_list):
            return None

    return currSchedule

'''
@return: Graph with modified deadlines
'''
def tightenTWEnds(taskList, currSchedule):
    if currSchedule == None:
        return None
    
    for dayIndex in range(len(currSchedule)):
        custIndex = len(currSchedule[dayIndex].task_list) - 1
        day = currSchedule[dayIndex]

        while custIndex > 0 and len(day.task_list[custIndex].time_windows) > 0:
            task = day.task_list[custIndex]
            tw = task.time_windows[dayIndex]
            twPrev = day.task_list[custIndex-1].time_windows[dayIndex]
            # if duration of task i does not fit in its last tw or it can fit between the end of its second to last time window
            #  and the end of the previous task's last tw:
            if task.duration > tw[-1][1] - tw[-1][0] or (len(tw) > 1 and task.duration + tw[-2][0] < twPrev[-1][0]):
                # remove the last time window
                tw = tw[:-1] 

            # else if duration of task i at the end of its last tw starts before the end of the previous task's last tw
            elif tw[-1][1] - task.duration < twPrev[-1][1]:
                # set the end of that time window to be the maximum of the the starting time of task i's last time window
                # and the end of task i-1's last time window
                tw[-1] = (tw[-1][0], max(twPrev[-1][1], tw[-1][0] + task.duration))
             
            # else if the duration of task i set at the end of its last tw overlaps any tws for the previous customer
            elif tw[-1][1] - task.duration > twPrev[-1][1]:
                # reset the endings of all time windows to be as late as possible
                # before the beginning of task i (with i scheduled as late as possible)
                for window in twPrev:
                    window = (window[0], min(tw[-1][1] - task.duration, window[1]))

            custIndex -= 1
        if custIndex == 0 and len(day.task_list[custIndex].time_windows) > 0 and task.duration > tw[0][1] - tw[0][0]:
            #remove that task's first tw
            tw = tw[:-1]
            
        custIndex -= 1
        
        if custIndex > 0:
            return None
        
    return currSchedule

'''
@return: shortest duration of this schedule ordering
'''
def minRoute(taskList, currSolution):
    # tightenedSol = using the returned schedules from tighten functions, look at first task and first tw for that task and schedule it as early as possible
        # repeat for all tasks in order
    # currBestSol = calcDominantSolution(tasklist, tightenSol)
    # find the latest waiting customer and store 
    # while there is a waiting customer and while this is not the last time window for that customer
        # newSol = switchTimeWindows(solution, latest waiting customer)
        # newDomSol = calcDominantSolution(tasklist, newSol)
        # if getDuration(newDomSol) < getDuration(currBestSol)
            # currSol = domSol
        # update latest waiting customer
    #return currBestSol
    return currSolution

'''
@return: the index for the last task with waiting time in the route
'''
def getLatestWaitingTask(currSolution):
    return 0

'''
@return: the updated schedule after moving the latestWaitingTask to the next time window and updating the other tasks
'''
def switchTimeWindows(currSolution, latestWaitingTask):
    # move the task latestWaitingTask - 1 to the next time window as early as possible
    # moves all tasks before it as late as possible and all those after it as early as possible
    
    return currSolution

'''
@return: the dominant version of the schedule being passed in (squidging)
'''
def calcDominantSolution(taskList, currSolution):
    # given the ending time of currSolution, move all tasks to the latest possible time without changing that ending time
    return currSolution

def getDuration(currSolution):
    
    return 0

'''
@return: total distance of a solution
'''
def calcTotalDistance(currSolution):
    return 0


def printUnplanned():
    print "unplanned tasks: (",
    for task in unplannedTasks:
        print str(task) + ", "
    print ")"

def printSolution(sol):
    print "["
    for route in sol:
        for task in route:
            print str(task) + ", "
    print "]"
            
    

def main():
    print "********** Main **********"
    print solve("test.csv")
    
if __name__ == "__main__":
    main()
    


