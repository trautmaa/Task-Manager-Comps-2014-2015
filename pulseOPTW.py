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
    - bounding
    - soft dominance
    - parallel python
'''
'''
Global variables needed(?):
-array of visited nodes (172)
-primal bound information

'''

import helperFunctions, copy

global allNodes


'''
Recursively generate every possible path starting with starting path and going to every unvisited node...
This function is called in separate threads by our main function..

@param: node, current score, current time, and current path
@ return: nothing
'''
def pulse(node, currScore, currTime, currPath):
    # making set of unvisited nodes by subtracting the intersection of all nodes with the 
    # nodes in the current path and node under consideration
    unvisitedNodes = allNodes - set(currPath) - node
    assert(node not in currPath)
    assert(currScore >= 0 and currTime >= 0)
    # checking if it's work considering this new path...could it possibly be optimal
    newProposedEndingTime = isFeasible(node, currPath)
    if newProposedEndingTime != None and inBounds(node, currScore, currTime) \
      and notSoftDominated(node, newProposedEndingTime, currPath):
        
        newPath = currPath.add(node)
        newScore = currScore + node.score()
        # if it is a candidate for optimality pulse is called recursively, 
        # on the same thread...i.e keep going down the branch
        for newNode in unvisitedNodes:
            newPath = copy.deepcopy(currPath)
            if noDetour(node, newNode, currPath, newProposedEndingTime):
                # new time is the current time plus the distance between current node and new node 
                newTime = currTime + helperFunctions.getDistanceBetweenTwoTasks(node, newNode)
                pulse(newNode, newScore, newTime, newPath)
'''
If there is a gap in the schedule 
'''

# def noDetour(node, newNode, currTime, currPath):
#     newSchedule scheduleASAP(newNode)
    #assert(isFeasible(newSchedule))
#     if the end of the last node in currPath + dist(last, new) >= start of next time window that could include newNode:
#         return True
#     for unvisitedNode in graph:
#         if it can fit between end of lastNode and start of newNode:
#             (there is a possible detour)
#             return False
#     return True
def noDetour(node, newNode, currTime, currPath):
    assert(isFeasible(newSchedule))

    return True


'''
isFeasible() returns a proposed new ending time: this is the earliest possible time that we could allow the passed in task to begin
node is a number between 0 and number of tasks - 1
currPath is a list: the 0th index is an ending time, and the following entries are numbers referring to tasks
taskList[currPath[1]] is the task object for the first scheduled task
'''
def isFeasible(node, currPath):
    task = taskList[node]
    routeIndex = int(currPath[0]) / 100
    
    #limit is the earliest we could reach node and begin proposed task
    limit = currPath[0] + helperFunctions.getDistanceBetweenTwoTasks(taskList[currPath[-1]], taskList[node])
    
    #return a proposedEnd based on the earliest we can schedule the node, considering its time windows
    for tw in range(len(task.timeWindows)):
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
    for taskToSwap in range(1, len(currPath)):
        tempPath = currPath[:]
        tempPath[-1], tempPath[taskToSwap] = tempPath[taskToSwap], tempPath[-1]
        
        #schedule tasks and determine the soonest possible ending time
        newTime = scheduleASAP(tempPath)
        
        #if this tempPath's time is an improvement over currPath's time, prune
        if newTime != None:
            if newTime < currTime:
                return False
    return True


def inBounds(node, currTime):
    return True
'''
def inBounds(node, currTime):
    Do this when you're smarter
'''

'''
returns a new path with the lowest possible ending time
'''
def scheduleASAP(path, node):
    currentTime = 0
    dayIndex = 0
    
    setTime = False
    #schedule the first task as early as possible
    t = 1
    for day in range(dayIndex, len(task.timeWindows)):
        for tw in range(len(task.timeWindows[day])):
            
            #if task can be scheduled in this time window..
            timeWindow = task.timeWindows[day][tw]
            if timeWindow[1] - task.duration >= currentTime:
                currentTime = max(timeWindow[0], currentTime) + task.duration
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
    return currentTime

def main():
    
    pulse(node, currScore, currTime, currPath)
    
    
    
if __name__ == '__main__':
    main()