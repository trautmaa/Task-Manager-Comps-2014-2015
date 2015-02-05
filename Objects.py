# Comps 2014
# Larkin Flodin, Avery Johnson, Maraki Ketema, 
# Abby Lewis, Will Schifeling, and  Alex Trautman

'''
A class to represent how many different locations there are for each task
'''
class Category:
    def __init__(self):
        self.categoryList = []
        
    def __init__(self, taskList):
        self.categoryList = taskList
            
    def addToList(self, task):
        self.categoryList.append(task)

'''
Task is a class that contains seven variables:
task.x is the task's x coordinate.
task.y is the task's y coordinate.
task.releaseTime is the task's release time.
task.duration is the task's duration.
task.deadline is the task's deadline.
task.priority is the task's priority
task.required represents whether the task is required
'''    
class Task:
    def __init__(self, id):
        self.id = id
        pass
    
    def setX(self, x):
        self.x = float(x)

    def setY(self, y):
        self.y = float(y)
        
    def setReleaseTime(self, r):
        self.releaseTime = float(r)

    def setDuration(self, dur):
        self.duration = float(dur)

    def setDeadline(self, dead):
        self.deadline = float(dead)
        
    def setPriority(self, priority):
        self.priority = float(priority)
        
    def setRequired(self, required):
        self.required = required
        
    #   This is a list of task IDs that this task would be dependent on.  
    #   Ie, this task cannot be completed until all dependent tasks have been completed.    
    def setTaskDependency(self, taskIds):
        self.dependencyTasks = taskIds
    
    #   This is a list of days. Each day has a list of time windows
    #   they will come in as a string: "[[(twStart1, twEnd1),(twStart2, twEnd2)], [day2..], etc.]
    #   do a regex to read it in. List of lists (days) of tuples (tw starts and ends)
    def setTimeWindows(self, timeWindows):
        self.timeWindows = timeWindows
        
    def getProfit(self):
        return self.priority
    
    def getNumTimeWindows(self):
        numWindows = 0
        for day in self.timeWindows:
            for window in day:
                numWindows += 1
        return numWindows


    def __str__(self):
        stringRepresentation = "(ID: " + str(self.id) + ", Location: (" + str(self.x) + ", "\
        + str(self.y) + "), Release Time: " + str(self.releaseTime) \
        + ", Duration: " + str(self.duration) + ", Deadline: " \
        + str(self.deadline) + ", Priority: " + str(self.priority) + ", Required: " + str(self.required)\
        + ", Tasks Depended On: " + str(self.dependencyTasks)\
        + ", Time Windows: ["
        
        for day in self.timeWindows:
            for tw in day:
                stringRepresentation = stringRepresentation + "(" + str(tw[0]) + ", "  + str(tw[1]) + "), "
        stringRepresentation += "])" 
        
        return stringRepresentation
    
    def __eq__(self, other):
        return isinstance(other, Task) and self.id == other.id
    
    def __ne__(self, other):
        return not (isinstance(other, Task) and self.id == other.id)
    
'''
 A class to hold the schedule for an individual day
'''   
class Route:
    def __init__(self, taskList = None, endingTimes = None):
        if taskList is None: self.taskList = []
        if endingTimes is None: self.endingTimes = []
        
    def setTaskList(self, taskList, endingTimes):
        self.taskList = taskList
        self.endingTimes = endingTimes
    
    def append(self, task, endingTime):
        self.taskList.append(task)
        self.endingTimes.append(endingTime)
    
    def addToTaskList(self, task, endingTime, index):
        self.taskList[index] = task
        self.endingTimes[index] = endingTime
    
    def getTask(self, index):
        return self.taskList[index]
    
    def getEndingTime(self, index):
        return self.endingTimes[index]
    
    def removeSegment(self, startIndex, endIndex):
        self.taskList = self.taskList[:startIndex] + self.taskList[endIndex:]
        self.endingTimes = self.endingTimes[:startIndex] + self.endingTimes[endIndex:]
    
    def resetEndingTimes(self):
        self.endingTimes = [None] * len(self.taskList)
    
    def __getitem__(self, index):
        return self.taskList[index]
    
    def __setitem__(self, index, task):
        self.taskList[index] = task
    
    def __len__(self):
        return len(self.taskList)
    
    def __str__(self):
        result = "["
        for task in range(len(self.taskList)):
            result = str(result) + "(task: " + str(self.taskList[task]) + ", ending at: " + str(self.endingTimes[task]) + ")\n"
        return result + "]"

'''
 A class to hold the routes for an individual day, representing the entire schedule
'''  
class Schedule:
    def __init__(self):
        self.routeList = []
        
    def append(self, route):
        self.routeList.append(route)
    
    def getRoute(self, index):
        return self.routeList[index]
    
    def getProfit(self):
        profit = 0
        for route in self.routeList:
            for task in route.taskList:
                if task != None:
                    profit += task.getProfit()
        return profit
    
    def resetEndingTimes(self):
        for route in self.routeList:
            route.resetEndingTimes()
    
    def __getitem__(self, index):
        return self.routeList[index]
    
    def __setitem__(self, index, route):
        self.routeList[index] = route
    
    def __str__(self):
        result = "["
        for route in range(len(self.routeList)):
            result = result + str(self.routeList[route]) + "\n"
        result = result + "]"
        return result
    
    def __len__(self):
        return len(self.routeList)
        
    
    
