# Comps 2014
# Larkin Flodin, Avery Johnson, Maraki Ketema, 
# Abby Lewis, Will Schifeling, and  Alex Trautman


'''
Find the paper on the drive: Ants>Duque,...
Ants are actually called Pulses now
'''
'''
To do :
figure out 
    - parallel python
'''
'''
Global variables needed(?):
-array of visited nodes (172)
-primal bound information

'''

import helperFunctions, copy
import createTasksFromCsv, collections
from createTests import dayLength


def solve(csvFile):
    global allNodes, taskList, reducedBoundsMatrix
    global  delta, tShoe, primalBound
    
    #initialize the primalBound
    primalBound = float("inf")
    
    #initialize our list of all nodes
    taskList = createTasksFromCsv.getTaskList(csvFile)
    allNodes = [x.id for x in taskList]
    
    #2-dimensional list with first index value as tao (currentTime), second index value as node
    reducedBoundsMatrix = collections.defaultdict(list)
    
    #we can mess with this as we see fit. Make delta larger to speed things up. Make it smaller to have more values.
    #delta = dayLength/10, tShoe = dayLength/10 make us reach maximum recursion depth
    delta = dayLength/3
    tShoe = dayLength/4

    defineBounds(tShoe, delta, taskList)

    
    bestPaths = []
    for node in taskList:
        bestPaths.append(pulse(node.id, 0, 0, [0]))
        
    print "Wow you made it"
    print "best schedule\n", max(bestPaths, key = lambda x: getProfit(x))

'''
Recursively generate every possible path starting with starting path and going to every unvisited node...
This function is called in separate threads by our main function..

@param: node, current score, current time, and current path
@ return: nothing
'''
def pulse(node, currScore, currTime, currPath):
    # making set of unvisited nodes by subtracting the intersection of all nodes with the 
    # nodes in the current path and node under consideration
    unvisitedNodes = copy.deepcopy(allNodes)
    for n in range(1, len(currPath)):
        unvisitedNodes.remove(currPath[n].id)
    result = []
    assert(node not in currPath[1:])
    assert(currScore >= 0 and currTime >= 0)
    # checking if it's work considering this new path...could it possibly be optimal
    newProposedEndingTime = isFeasible(node, currPath)
    print "newProposedEndingTime: ", newProposedEndingTime
    print "inBounds? ", inBounds(node, currTime, currPath)
    if newProposedEndingTime != None and inBounds(node, currTime, currPath) \
      and notSoftDominated(node, newProposedEndingTime, currPath):
        
        newPath = currPath[:] + [node]
        newScore = currScore + taskList[node].priority
        # if it is a candidate for optimality pulse is called recursively, 
        # on the same thread...i.e keep going down the branch
        for newNode in unvisitedNodes:
            newPath = copy.deepcopy(currPath)
            # new time is the current time plus the distance between current node and new node 
            newTime = currTime + helperFunctions.getDistanceBetweenTasks(taskList[node], taskList[newNode])
            result = result + pulse(newNode, newScore, newTime, newPath)
    if len(result) == 0:
        return []
    return max(result, key = lambda x: getProfit(x))
                    


'''
isFeasible() returns a proposed new ending time: this is the earliest possible time that we could allow the passed in task to begin
node is a number between 0 and number of tasks - 1
currPath is a list: the 0th index is an ending time, and the following entries are numbers referring to tasks
taskList[currPath[1]] is the task object for the first scheduled task
'''
def isFeasible(node, currPath):
    task = taskList[node]
    routeIndex = int(currPath[0]) / dayLength
    
    #limit is the earliest we could reach node and begin proposed task
    limit = currPath[0] + helperFunctions.getDistanceBetweenTasks(taskList[currPath[-1]], taskList[node])
    
    #return a proposedEnd based on the earliest we can schedule the node, considering its time windows
    for tw in range(len(task.timeWindows[routeIndex])):

        timeWindow = task.timeWindows[tw][routeIndex]
        proposedEnd = max(timeWindow[0], limit) + task.duration
        
        #if we could fit the task in its time window after the earliest possible starting time
        #and if the task would not then go over a day division...
        if timeWindow[1] - task.duration >= limit and proposedEnd < (routeIndex + 1) * dayLength:
            return proposedEnd
            
    #if it's not possible to schedule the task (visit the node) then it's not feasible
    return None

'''
checks a few different orders to make sure that this ordering is worth further exploration
@param node, newProposedEndingTime, currPath
@return boolean
'''
def notSoftDominated(node, newProposedEndingTime, currPath):
    #look at each new ordering
    for nodeToSwap in range(1, len(currPath)):
        tempPath = currPath[:]
        tempPath[-1], tempPath[nodeToSwap] = tempPath[nodeToSwap], tempPath[-1]
        
        #schedule tasks and determine the soonest possible ending time
        newTime = scheduleASAP(tempPath)
        
        #if this tempPath's time is an improvement over currPath's time, prune
        if newTime != None:
            if newTime < currTime:
                return False
    return True


'''
inBounds checks our pre-created matrix from define bounds to see if the path is worth further exploration
'''
def inBounds(node, currTime, path):
    if currTime not in reducedBoundsMatrix:
        return True
    
    #round down taoValue so it is consistent with our matrix indices and we may compare
    taoValue = currTime - currTime % delta
    if reducedBoundsMatrix[taoValue][node] + scheduleASAP(path)[1] >= primalBound:
        return False
    return True
    
    

'''
define bounds function defines a matrix of values of the least amount of time it would take to complete the schedule
from a given node to the end within a time limit of the day length minus the length of the path so far (round up? round down?)
@param tShoe: the lowest time value we will explore in our matrix. We don't go lower than tShoe because we don't want to fully solve
the problem at this point. 
@param delta: the length of the time steps
tHat is just the dayLength
'''
def defineBounds(tShoe, delta, taskList):
    currentLimit = dayLength
    
    #go through each value of tao AKA currentTime until we reach our stopping condition
    while currentLimit > tShoe:        
        #decrement
        
        currentLimit -= delta
        reducedBoundsMatrix[currentLimit] = ([0] * len(taskList))
        
        for task in taskList:
            path = [0]
            path += pulse(task.id, 0, currentLimit, path)
            
            #add a cost value to our global reducedBoundsMatrix
            if path == []:
                reducedBoundsMatrix[currentLimit][task.id] = float("inf")
            else:
                print reducedBoundsMatrix
                print reducedBoundsMatrix[currentLimit]
                print len(reducedBoundsMatrix[currentLimit])
                print task.id
                reducedBoundsMatrix[currentLimit][task.id] = scheduleASAP(path)[1] #this is the duration
                print "duration: ", scheduleASAP(path)[1]
                print "path", path
    return reducedBoundsMatrix            
    

'''
returns a new path with the lowest possible ending time, as well as a duration
@param path: a list of task ids in order that they're scheduled. the first index is the ending time of the path
'''
def scheduleASAP(path):
    currentTime = 0
    dayIndex = 0
    if len(path) < 2:
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
        dayIndex = int(currentTime)/100
        task = path[t]
        setTime = False
        # find the next possible time window to schedule node in in this day or any later days... 
        for day in range(dayIndex, len(task.timeWindows)):
            for tw in range(len(task.timeWindows[day])):
                
                #if task can be scheduled in this time window..
                timeWindow = task.timeWindows[day][tw]
                travelTime = helperFunctions.getDistanceBetweenTasks(path[t-1], path[t])
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

def main():
    solve("newTest.csv")

    
if __name__ == '__main__':
    main()