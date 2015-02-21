# Comps 2014
# Larkin Flodin, Avery Johnson, Maraki Ketema, 
# Abby Lewis, Will Schifeling, and  Alex Trautman
import functools

'''
Find the paper on the drive: Ants>Duque,...
Ants are actually called Pulses now
For info on bounds, look at Ants>Lasagna

Multiprocessing tutorial:
    http://chriskiehl.com/article/parallelism-in-one-line/

'''

'''
To do:
- speed up defineBounds somehow (use bounds?)
'''

import multiprocessing
import helperFunctions, copy, sys, time
import createTasksFromCsv, collections
from createTests import dayLength

def solve(csvFile):
    global timeLimit, taskList, delta, tShoe
    global startTime
    
    startTime = time.time()
    
    '''
    The primal bound holds the priority of best possible schedule we have found so far.
    Initialize it to 0. If we find a feasible path with a higher priority (score), 
    then we update the primal bound.
    
    A multiprocessing manager does all the locking work for you. When you pass it into
    a function and the function accesses the managed resource, it is accessed as a proxy,
    and the manager makes sure all threads get the updated value. It works with python objects,
    which is why it is a list.
    '''
    manager = multiprocessing.Manager()
    
    #initialize our list of all nodes
    taskList = createTasksFromCsv.getTaskList(csvFile)
    
    primalBound = manager.list([0, 0, 0, 0, 0] + [0, 0, 0, 0])
    
    timeLimit = helperFunctions.getLatestDeadline(taskList)
    print "timeLimit:", timeLimit
    
    allNodes = [x.id for x in taskList]
    allNodes = manager.list(allNodes)
    
    #2-dimensional list with first index value as tao (currentTime), second index value as node
    
    #we can mess with this as we see fit. Make delta larger to speed things up. Make it smaller to have more values.
    #delta = timeLimit/10, tShoe = timeLimit/10 make us reach maximum recursion depth

    delta = max(10, (timeLimit/dayLength * 3))
    
    
    tShoe = 9 * timeLimit / 13
    print "tShoe", tShoe
    boundsInfo = [delta, tShoe]
    defineBounds(boundsInfo, primalBound, allNodes)
    bestPaths = []
    
    
    order = reducedBoundsMatrix[min(reducedBoundsMatrix.keys())]
    if float("inf") in order:
        otherKeys = reducedBoundsMatrix.keys()
        otherKeys.remove(min(reducedBoundsMatrix.keys()))
        order = reducedBoundsMatrix[min(otherKeys)]
    print order
    allNodes = sorted(allNodes, key = lambda x: order[x])
    print allNodes
    print "setting primal bound to ", max(order), " initially"
    primalBound[0] = max(order)
    
    '''
    Creates a pool of worker threads. Automatically set to the number of
    cores in the machine, but you can set that differently with an int argument.
    
    '''
    pool = multiprocessing.Pool(len(allNodes)/2 + 1)
    
    '''
    This is a partial function, which means it creates an in-between function that
    has some set arguments. You can then call it later with the remaining arguments
    We use this here so that we can use the map function of the thread pool later
    '''
    partialPulse = functools.partial(pulse, primalBound, [0], allNodes, allNodes[:], 0)
    
    '''
    Calling map on the thread pool with our partial pulse function with added
    node args.
    '''
    #Uncomment the following line for parallel
    bestPaths = pool.map(partialPulse, allNodes)
    
    #Uncomment the following line for sequential
#     bestPaths = map(partialPulse, allNodes)

    print bestPaths
    bestSched = max(bestPaths, key = lambda x: getProfit(x))
    
    bestProfit = getProfit(bestSched)
    print bestSched
    
    # you have to call this on threads so they stop
    pool.close()
    
    # you have to call this on threads after you've closed them 
    # (read documentation)
    pool.join()
    
    bestSched = helperFunctions.createOptimalSchedule(taskList, bestSched[1:])
    
    print "Wow you made it"
    print "best schedule\n", bestSched
    print "profit", bestProfit
    print "primal bound", primalBound
    return bestSched
    

'''
Recursively generate every possible path starting with starting path and going 
to every unvisited node.

This function is called in separate threads by our main function.

@param: node, current score, current time, and current path
@ return: nothing
'''
def pulse(pBound, currPath, allNodes, unvisitedNodes, profit, node, definingBounds = [False]):
#     if definingBounds[0]:
#         print "entering pulse trying to add"
#         print node, "to "
#         print currPath
    
    processName = multiprocessing.current_process().name
    # making set of unvisited nodes by subtracting the intersection of all nodes with the 
    # nodes in the current path and node under consideration
    if (definingBounds[0] and time.time() - startTime > boundsStoppingTime) or (time.time() - startTime > stoppingTime):
        return currPath
    
    result = []
    resultProfits = []
    
    # checking if it's work considering this new path...could it possibly be optimal
    
    newProposedEndingTime = isFeasible(node, currPath, definingBounds)
        
    if newProposedEndingTime != None:
        isValid = doTests(node, currPath, pBound, unvisitedNodes, definingBounds, newProposedEndingTime)
    
    if newProposedEndingTime != None and False not in isValid:
        unvisitedNodes.remove(node)
        newPath = currPath[:] + [node]
        # if it is a candidate for optimality pulse is called recursively, 
        # on the same thread...i.e keep going down the branch
        newPath[0] = newProposedEndingTime
        
        newProfit = profit + taskList[node].priority
        
        if not definingBounds[0] and newProfit >= pBound[0]:
            result.append(newPath)
            resultProfits.append(newProfit)
            if newProfit > pBound[0] and not definingBounds[0]:
                print "%s RESETTING0 PRIMAL BOUND from %d to %d" %(multiprocessing.current_process().name, pBound[0], newProfit)
                print newPath
                pBound[0] = newProfit
        elif definingBounds[0] and newProfit >= definingBounds[3]:
            result.append(newPath)
            resultProfits.append(newProfit)
            if newProfit > definingBounds[3]:
                definingBounds[3] = newProfit
#         else:
        for newNode in unvisitedNodes:
            # new time is the current time plus the distance between current node and new node
            
            res = pulse(pBound, newPath, allNodes, unvisitedNodes[:], newProfit, newNode, definingBounds)
            result.append(res)
            resultProfits.append(getProfit(res))          
            
#     elif definingBounds[0]:
#         print "PRUNING"
#         print currPath, " + ", node
#         print "newEndingTIme", newProposedEndingTime
#         if newProposedEndingTime != None:
#             print "withinBounds", isValid[0]
#             print "cannotDetour", isValid[1]
#             print "notDominated", isValid[2]
#         print "profit", profit
#         print
    
    if len(result) == 0:
#         pBound[5 + len(currPath) - 2] += time.time() - pulseStart
        return []
    
    bestProfit = resultProfits[0]
    best = result[0]
    
    for p in range(1, len(resultProfits)):
        if resultProfits[p] > bestProfit:
            bestProfit = resultProfits[p]
            best = result[p]
#     best = max(result, key = lambda x: resultProfits[x])
    if not definingBounds[0] and bestProfit > pBound[0]:
        print "%s RESETTING1 PRIMAL BOUND from %d to %d" %(multiprocessing.current_process().name, pBound[0], getProfit(best))
        print best#, "\a"
        pBound[0] = getProfit(best)
        print "TIMES", ["%.3f" %(x) for x in pBound]
    elif definingBounds[0] and bestProfit >= definingBounds[3]:
            result.append(newPath)
            resultProfits.append(newProfit)
            if newProfit > definingBounds[3]:
                definingBounds[3] = newProfit
    return best


def doTests(node, currPath, pBound, unvisitedNodes, definingBounds, newProposedEndingTime):
    
    if newProposedEndingTime != None:
        withinBounds = inBounds(node, currPath, pBound, definingBounds)
        if withinBounds:
            cannotDetour = noDetour(node, currPath, unvisitedNodes, newProposedEndingTime, definingBounds)
            if cannotDetour and not definingBounds[0]:
                notDominated = notSoftDominated(node, newProposedEndingTime, currPath)
            else:
                notDominated = definingBounds[0]
        else:
            cannotDetour = False
            notDominated = False
            
    else:
        withinBounds = False
        cannotDetour = False
        notDominated = False
    
    return [withinBounds, cannotDetour, notDominated]
    
'''
isFeasible() returns a proposed new ending time: this is the earliest possible
time that we could allow the passed in task to begin 

@param node: a number between 0 and number of tasks - 1
@param currPath: a list: the 0th index is an ending time, and the following entries are numbers referring to tasks

taskList[currPath[1]] is the task object for the first scheduled task
'''
def isFeasible(node, currPath, definingBounds):
    task = taskList[node]
    routeIndex = int(currPath[0]) / dayLength

    noEndingTime = currPath[1:]
    
    if not definingBounds[0]:
        for r in range(len(task.dependencyTasks)):
            releaseTask = int(task.dependencyTasks[r])
            if releaseTask not in noEndingTime:
                return None
    
    #limit is the earliest we could reach node and begin proposed task
    limit = currPath[0]
    if len(currPath) > 2:
        dist = helperFunctions.getDistanceBetweenTasks(taskList[currPath[-1]], taskList[node])
        if int(limit + dist)/dayLength == int(limit)/dayLength:
            limit += dist
    
    #return a proposedEnd based on the earliest we can schedule the node, considering its time windows
    for d in range(routeIndex - 1, len(task.timeWindows)):
        for tw in range(len(task.timeWindows[d])):

            timeWindow = task.timeWindows[d][tw]
            proposedEnd = max(timeWindow[0], limit) + task.duration
            
            #if we could fit the task in its time window after the earliest possible starting time
            if timeWindow[1] - task.duration >= limit and proposedEnd <= timeLimit:
                return proposedEnd
    
    #if it's not possible to schedule the task (visit the node) then it's not feasible
    return None

'''
checks a few different orders to make sure that this ordering is worth further
exploration.

@param node, newProposedEndingTime, currPath
@return boolean
'''
def notSoftDominated(node, newProposedEndingTime, currPath):
    
    '''
    New optimization:
    get ending time of currently scheduled path:
    - swapping v_m and v_0 => [et]
    - swapping v_m => [et, v_1]
    - swapping v_m => [et, v_1, v_2] etc.
    schedule node
    schedule remaining nodes
    If ending time of new path is better, return False
    Otherwise, currPath += next node
    '''
 
#     endingTime = 0
#     path = [0]
#     for swapNodeIndex in range(len(currPath)): #O(n)        `|
#         #schedule nodes up to swap node        `|            |- O(n^2*tw)
#         #schedule swapped node                  |-O(n*tw)    |
#         #schedule nodes after swapped node     _|           _|
#         for n in range(swapNodeIndex):
#             newEndingTime = 
#         
#         pass
#          
#     
    
    
    #look at each new ordering
    for nodeToSwap in range(1, len(currPath)):
        tempPath = currPath[:] + [node]
        tempPath[-1], tempPath[nodeToSwap] = tempPath[nodeToSwap], tempPath[-1]
#         print "checking tempPath", tempPath
        #schedule tasks and determine the soonest possible ending time
        newTime = scheduleASAP(tempPath)
        
        #if this tempPath's time is an improvement over currPath's time, prune
        if newTime != None:
            if newTime[0] < currPath[0]:
                return False
    return True


'''
inBounds checks our pre-created matrix from define bounds to see if the path is
worth further exploration
'''
def inBounds(node, path, pBound, definingBounds):
    
#     if definingBounds[0]:
#         return True
    
    currTime = path[0]
    #round down taoValue so it is consistent with our matrix indices and we may compare
    taoValue = getTao(reducedBoundsMatrix.keys(), currTime)
    if taoValue == -1:
#         print "TaoValue %d not found" %(taoValue)
#         print "*********** exiting inBounds ***********"
        return True
    
    pathScore = reducedBoundsMatrix[taoValue][node] + getProfit(path + [node])
    
#     print "*********** exiting inBounds ***********"
    if not definingBounds[0] and pathScore <= pBound[0]:
        return False
    
    if definingBounds[0]:
        if pathScore <= definingBounds[3]:
            return False
    return True


'''
OPTIMIZE THIS
'''
def getTao(reducedBoundsKeys, currTime):
    if len(reducedBoundsKeys) == 0:
        return -1
    reducedBoundsKeys.sort()
    if currTime < reducedBoundsKeys[0]:
        return -1
    else:
        for k in range(len(reducedBoundsKeys)):
            if reducedBoundsKeys[k] == currTime:
                return reducedBoundsKeys[k]
            elif reducedBoundsKeys[k] > currTime:
                return reducedBoundsKeys[k-1]
    return reducedBoundsKeys[-1]


def noDetour(node, origPath, unvisitedNodes, proposedEnd, definingBounds):
    '''
    For each unvisited node, try to insert it between the end of origPath and node.
    If the endingTime of scheduleASAP is the same, return False
    '''
    origPathEnd = origPath[0]

    unvisitedNodes = unvisitedNodes[:]
    unvisitedNodes.remove(node)
    
    if proposedEnd == None:
        return False

    for newNode in unvisitedNodes:
        newPathEnd = isFeasible(newNode, origPath, definingBounds)
        newPath = origPath + [newNode]
        
        if newPathEnd == None:
            continue
        
        newPath[0] = newPathEnd
        newPathEnd = isFeasible(node, newPath, definingBounds)
        
        if newPathEnd == proposedEnd:
#             print "Detour:"
#             print newPath, " not ", node
            return False
    return True
    
    

'''
define bounds function defines a matrix of values of the least amount of time 
it would take to complete the schedule from a given node to the end within a 
time limit of the day length minus the length of the path so far (round up? 
round down?)

@param tShoe: the lowest time value we will explore in our matrix. We don't go
lower than tShoe because we don't want to fully solve the problem yet.

@param delta: the length of the time steps
'''
def defineBounds(boundsInfo, pBound, allNodes):
#     timerStart = time.time()
    
    print "*********** entering defineBounds ***********"
    timeElapsed = timeLimit
    checkingBounds = [True]
    
    global reducedBoundsMatrix
    reducedBoundsMatrix = multiprocessing.Manager().dict()

    #go through each value of tao AKA currentTime until we reach the lower time limit
    while timeElapsed - boundsInfo[0] >= boundsInfo[1]:        
        #decrement
        timeElapsed = timeElapsed - boundsInfo[0]
        
        # resetting delta to be higher as we go back in the graph
        # This makes it so we can go further back but still explore more
        # short solutions
        boundsInfo[0] = int(boundsInfo[0] * 1.1)
        print "Tao:", timeElapsed, "Delta: ", boundsInfo[0]
        
        nodeTimes = ([0] * len(allNodes))
        
        for n1 in allNodes:
#             print "defining bounds for", n1
            path = [timeElapsed]
            pathEndingTime = isFeasible(n1, path, [True])
            if pathEndingTime == None:
                nodeTimes[n1] = 0
            else:
                allOtherNodes = allNodes[:]
                allOtherNodes.remove(n1)
                foundPaths = []
                checkingBounds = [True, timeElapsed, n1, nodeTimes[n1]]
                
                for n2 in allNodes:
                    if n2 != n1:
                        newPath = [pathEndingTime]
                        foundPaths.append(pulse(pBound, newPath, allOtherNodes, allOtherNodes[:], 0, n2, definingBounds = checkingBounds))
                if time.time() - startTime > boundsStoppingTime:
                    for n in range(n1, len(nodeTimes)):
                        nodeTimes[n] = float("inf")
                    break
                bestScore = max([getProfit(x) for x in foundPaths])
                bestScore2 = checkingBounds[3]
                assert(bestScore == bestScore2)
#                 print "BEST SCORE FOR", n1, "is", bestScore
                nodeTimes[n1] = bestScore + taskList[n1].priority
            
        reducedBoundsMatrix[timeElapsed] = nodeTimes
        if time.time() - startTime > boundsStoppingTime:
            break
    print "*********** exiting defineBounds ********************************************"
    print "matrix"
    
    printMatrix()
#     for i in reducedBoundsMatrix.keys():
#         print "%d:" %(i), reducedBoundsMatrix[i]
    print "*****************************************************************************"
    return reducedBoundsMatrix            
    

def scheduleASAP(path, initTime = 0):
    '''
    returns a new path with the lowest possible ending time, as well as a duration
    
    @param path: a list of task ids in order that they're scheduled. the first 
    index is the ending time of the path
    '''
    currentTime = initTime
    dayIndex = 0
    if len(path) <= 1:
        return 0, 0
    
    task = taskList[path[1]]
    
    setTime = False
    #schedule the first task as early as possible
    t = 1
    for day in range(0, len(task.timeWindows)):
        for tw in range(len(task.timeWindows[day])):
            
            #if task can be scheduled in this time window..
            timeWindow = task.timeWindows[day][tw]
            if timeWindow[1] - task.duration >= currentTime:
                currentTime = max(timeWindow[0], currentTime) + task.duration
                schedStartTime = currentTime - task.duration
                setTime = True
                dayIndex = day
                break
        if setTime:
            break
    if not setTime:
        return None
    #schedule each task as early as possible and update currentTime
    for t in range(2, len(path)):
        task = taskList[path[t]]
        setTime = False
        # find the next possible time window to schedule node in in this day or any later days... 
        for day in range(dayIndex, len(task.timeWindows)):
            for tw in range(len(task.timeWindows[day])):
                
                #if task can be scheduled in this time window..
                timeWindow = task.timeWindows[day][tw]
                travelTime = helperFunctions.getDistanceBetweenTasks(taskList[path[t-1]], taskList[path[t]])
                if timeWindow[1] - task.duration >= currentTime + travelTime:
                    currentTime = max(timeWindow[0], currentTime + travelTime) + task.duration
                    setTime = True
                    dayIndex = day
                    break
            if setTime:
                break
        if not setTime:
            return None
    return currentTime, currentTime - schedStartTime

def getProfit(sched):
    tot = 0 
    if len(sched) == 0:
        return 0
    for t in range(1, len(sched)):
        tot += taskList[sched[t]].priority
    return tot

def printMatrix():
    keys = reducedBoundsMatrix.keys()
    keys.sort()
    print "\t",
    for task in taskList:
        print str(task.id) + "\t",
    print
    for k in keys:
        print str(k) + "\t",
        for n in reducedBoundsMatrix[k]:
            print str(n) + "\t",
        print

def setTimes(stopTime): ######THIS IS FOR ALGORITHM COMPARISON!!!!!
    global stoppingTime, startTime, boundsStoppingTime
    startTime = time.time()
    stoppingTime = stopTime
    boundsStoppingTime = (stoppingTime)/4

def main():
    startTime = time.time()
    testFile = sys.argv[1]
    if len(sys.argv) >= 3:
        setTimes(int(sys.argv[2]))
    else:
        setTimes(float("inf"))
    print "test file:", testFile, "stopping time:", stoppingTime,
    print "bounds stopping time:", boundsStoppingTime
    schedule = solve(testFile)
    
    helperFunctions.writeTasks("pulseSched.csv", schedule)

    
if __name__ == '__main__':
    main()
