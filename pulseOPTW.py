# Comps 2014
# Larkin Flodin, Avery Johnson, Maraki Ketema, 
# Abby Lewis, Will Schifeling, and  Alex Trautman
import functools

'''
Find the paper on the drive: Ants>Duque,...
Ants are actually called Pulses now
For info on bounds, look at Ants>Lasagna
'''

'''
To do :
figure out 
    - parallel python
    -MULTIPLE DAYS: set time limit to be timeLimit * numDays (len of any tasks tws)
'''

'''
Global variables needed(?):
-array of visited nodes (172)
-primal bound information
'''

import multiprocessing
import helperFunctions, copy, sys, time
import createTasksFromCsv, collections
from createTests import dayLength

def solve(csvFile):
    global timeLimit, taskList, delta, tShoe, reducedBoundsMatrix, timeElapsed
    
    global initTime
    initTime = time.time()
    
    timeElapsed = [initTime]
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
    
    primalBound = manager.list([0])
    
    elapsedTime = manager.list([initTime])
    
    #initialize our list of all nodes
    taskList = createTasksFromCsv.getTaskList(csvFile)
    
    timeLimit = helperFunctions.getLatestDeadline(taskList)
    print "timeLimit:", timeLimit
    
    allNodes = [x.id for x in taskList]
#     allNodes.sort(key= lambda x: taskList[x].deadline)
    allNodes = manager.list(allNodes)
    
    #2-dimensional list with first index value as tao (currentTime), second index value as node
    reducedBoundsMatrix = {}
    
    #we can mess with this as we see fit. Make delta larger to speed things up. Make it smaller to have more values.
    #delta = timeLimit/10, tShoe = timeLimit/10 make us reach maximum recursion depth

    # will hold tShoe and delta    
    
    delta = 10
    # AVERY: hmmmm
    if stoppingTime > 10000:
        tShoe = 6*timeLimit / 8
    else:
        tShoe = timeLimit
    print "tShoe", tShoe
    boundsInfo = [delta, tShoe]
    defineBounds(boundsInfo, taskList, primalBound, allNodes)
    bestPaths = []
    
    '''
    Creates a pool of worker threads. Automatically set to the number of
    cores in the machine, but you can set that differently with an int argument.
    
    '''
    pool = multiprocessing.Pool(len(allNodes))
    
    '''
    This is a partial function, which means it creates an in-between function that
    has some set arguments. You can then call it later with the remaining arguments
    We use this here so that we can use the map function of the thread pool later
    '''
    partialPulse = functools.partial(pulse, primalBound, [0], allNodes)
    
    '''
    Calling map on the thread pool with our partial pulse function with added
    node args.
    '''
#     bestPaths = pool.map(partialPulse, allNodes)
    bestPaths = map(partialPulse, allNodes)

    print bestPaths
    bestSched = max(bestPaths, key = lambda x: getProfit(x))
    
    bestProfit = getProfit(bestSched)
    print bestSched
    
    # you have to call this on threads so they stop
    pool.close()
    
    # you have to call this on threads after you've closed them 
    # (read documentation)
    pool.join()
    
#     bestSched = helperFunctions.createOptimalSchedule(taskList, bestSched[1:])
    
    print "Wow you made it"
    print "best schedule\n", bestSched
    print "profit", bestProfit
    print "primal bound", primalBound
    return bestSched[1:]
    

'''
Recursively generate every possible path starting with starting path and going 
to every unvisited node.

This function is called in separate threads by our main function.

@param: node, current score, current time, and current path
@ return: nothing
'''
def pulse(pBound, currPath, allNodes, node, definingBounds = [False]):
#     print "entering pulse trying to add"
#     print node, "to "
#     print currPath
    
    processName = multiprocessing.current_process().name
    # making set of unvisited nodes by subtracting the intersection of all nodes with the 
    # nodes in the current path and node under consideration
    if time.time() - startTime > stoppingTime:
        return currPath
    
    currTime = currPath[0]
    
    unvisitedNodes = copy.deepcopy(allNodes)
    
    for n in range(1, len(currPath)):
        unvisitedNodes.remove(currPath[n])
    result = []
    
    assert(node not in currPath[1:])
    assert(currTime >= 0)
    
    # checking if it's work considering this new path...could it possibly be optimal
    
    newProposedEndingTime = isFeasible(node, currPath)
    withinBounds = inBounds(node, currPath, pBound)
    notDominated = notSoftDominated(node, newProposedEndingTime, currPath)
    cannotDetour = noDetour(node, currPath, unvisitedNodes)
    
    if (definingBounds[0] and newProposedEndingTime != None) or (newProposedEndingTime != None and withinBounds and notDominated and cannotDetour):
        unvisitedNodes.remove(node)
        newPath = currPath[:] + [node]
        # if it is a candidate for optimality pulse is called recursively, 
        # on the same thread...i.e keep going down the branch
        newPath[0] = newProposedEndingTime
        result.append(newPath)
        
        for newNode in unvisitedNodes:
            # new time is the current time plus the distance between current node and new node 
            newTime = isFeasible(newNode, newPath)
            if newTime == None:
#                 print " INFEASIBLE TO ADD ", newNode
                continue
            res = pulse(pBound, newPath, allNodes, newNode, definingBounds)
#             print "GOT RESULt", res
            result.append(res)
#     else:
#         print "failed"
#         print "newEndingTIme", newProposedEndingTime
#         print "withinBounds", withinBounds
#         print "notDominated", notDominated
#         print "cannotDetour", cannotDetour
    if len(result) == 0:
        return []
    
    best = max(result, key = lambda x: getProfit(x))
    if not definingBounds[0] and getProfit(best) > pBound[0]:
        print "%s RESETTING PRIMAL BOUND from %d to %d" %(multiprocessing.current_process().name, pBound[0], getProfit(best))
        print best, "\a"
        pBound[0] = getProfit(best)
    if len(best) > 27:
        print "thread: %s exiting at length %d with best" %(multiprocessing.current_process().name, len(best))
        print best
    return best
                    
'''
isFeasible() returns a proposed new ending time: this is the earliest possible
time that we could allow the passed in task to begin 

@param node: a number between 0 and number of tasks - 1
@param currPath: a list: the 0th index is an ending time, and the following entries are numbers referring to tasks

taskList[currPath[1]] is the task object for the first scheduled task
'''
def isFeasible(node, currPath):
    
    task = taskList[node]
    routeIndex = int(currPath[0]) / dayLength

    noEndingTime = currPath[1:]
    
    
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
    for d in range(len(task.timeWindows)):
        for tw in range(len(task.timeWindows[d])):

            timeWindow = task.timeWindows[d][tw]
            proposedEnd = max(timeWindow[0], limit) + task.duration
            
            #if we could fit the task in its time window after the earliest possible starting time
            if timeWindow[1] - task.duration >= limit and proposedEnd <= timeLimit:
                return proposedEnd
            
    #if it's not possible to schedule the task (visit the node) then it's not feasible
    return None

# def checkRelease(node, path):
#     noEndingTime = currPath[1:]
#     for r in range(len(task.dependencyTasks)):
#         releaseTask = task.dependencyTasks[r]
#         if releaseTask not in noEndingTime:
#             return None

'''
checks a few different orders to make sure that this ordering is worth further
exploration.

@param node, newProposedEndingTime, currPath
@return boolean
'''
def notSoftDominated(node, newProposedEndingTime, currPath):
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
def inBounds(node, path, pBound):
    currTime = path[0]
#     print "*********** entering inBounds ***********"
    taoValue = currTime - currTime % delta
    if taoValue not in reducedBoundsMatrix:
#         print "TaoValue %d not found" %(taoValue)
#         print "*********** exiting inBounds ***********"
        return True
    
    #round down taoValue so it is consistent with our matrix indices and we may compare
    pathScore = reducedBoundsMatrix[taoValue][node] + getProfit(path + [node])
    
#     print "*********** exiting inBounds ***********"
    if pathScore <= pBound[0]:
        return False
    return True


def noDetour(node, currPath, unvisitedNodes):
    '''
    For each unvisited node, try to insert it between the end of currPath and node.
    If the endingTime of scheduleASAP is the same, return False
    '''
    pathEnd = scheduleASAP(currPath + [node], currPath[0])
    if pathEnd == None:
        return False
    pathEnd = pathEnd[0]
    currPath = currPath[:]
    unvisitedNodes = unvisitedNodes[:]
    unvisitedNodes.remove(node)
    for newNode in unvisitedNodes:
        newSched = [pathEnd] + currPath[1:] + [newNode] + [node]
        newSchedEnd = scheduleASAP(newSched, currPath[0])
        if newSchedEnd != None and newSchedEnd[0] == pathEnd:
            return False
    return True
    
    

'''
define bounds function defines a matrix of values of the least amount of time 
it would take to complete the schedule from a given node to the end within a 
time limit of the day length minus the length of the path so far (round up? 
round down?)

@param tShoe: the lowest time value we will explore in our matrix. We don't go
lower than tShoe because we don't want to fully solve the problem yet.

@param delta: the length of the time steps tHat is just the timeLimit
'''
def defineBounds(boundsInfo, taskList, pBound, allNodes):
    
    print "*********** entering defineBounds ***********"
    remainingTime = len(taskList[0].timeWindows) * dayLength
    checkingBounds = multiprocessing.Manager().list([True])
    #go through each value of tao AKA currentTime until we reach the lower time limit
    while remainingTime - boundsInfo[0] >= boundsInfo[1]:        
        #decrement
        remainingTime = remainingTime - boundsInfo[0]
        
        print "Remaining time:", remainingTime
        reducedBoundsMatrix[remainingTime] = ([0] * len(taskList))
        
        for task in taskList:
            path = [remainingTime]
#             print "running pulse with"
#             print "taskid, path,",task.id, path
#             print "allNodes ", allNodes
            path = pulse(pBound, path, allNodes, task.id, definingBounds = checkingBounds)
#             print "path result", path
#             print
            #add a cost value to our global reducedBoundsMatrix
            if path == []:
                # There was no feasible path from this node with the remaining
                # time. Therefore the best possible additional profit from this
                # path is 0.
                reducedBoundsMatrix[remainingTime][task.id] = float("inf")
            else:
                reducedBoundsMatrix[remainingTime][task.id] = getProfit(path)
    print "*********** exiting defineBounds ********************************************"
    print "matrix"
    
    for i in reducedBoundsMatrix.keys():
        print "%d:" %(i), reducedBoundsMatrix[i]
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
    for day in range(dayIndex, len(task.timeWindows)):
        for tw in range(len(task.timeWindows[day])):
            
            #if task can be scheduled in this time window..
            timeWindow = task.timeWindows[day][tw]
            if timeWindow[1] - task.duration >= currentTime:
                currentTime = max(timeWindow[0], currentTime) + task.duration
                schedStartTime = currentTime - task.duration
                setTime = True
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
        for day in range(0, len(task.timeWindows)):
            for tw in range(len(task.timeWindows[day])):
                #if task can be scheduled in this time window..
                timeWindow = task.timeWindows[day][tw]
                travelTime = helperFunctions.getDistanceBetweenTasks(taskList[path[t-1]], taskList[path[t]])
                if timeWindow[1] - task.duration >= currentTime + travelTime:
                    currentTime = max(timeWindow[0], currentTime + travelTime) + task.duration
                    setTime = True
                    break
            if setTime:
                break
        if not setTime:
            return None
    return currentTime, currentTime - schedStartTime

def getProfit(sched):
    tot = 0 
    for t in range(1, len(sched)):
        tot += taskList[sched[t]].priority
    return tot

def setTimes(): ######THIS IS FOR ALGORITHM COMPARISON!!!!!
    global stoppingTime, startTime
    startTime = time.time()
    stoppingTime = float("inf")

def main():
    global stoppingTime, startTime
    startTime = time.time()
    testFile = sys.argv[1]
    if len(sys.argv) >= 3:
        stoppingTime = int(sys.argv[2])
    else:
        stoppingTime = float("inf")
    solve(testFile)

    
if __name__ == '__main__':
    main()