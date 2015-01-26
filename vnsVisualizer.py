from vns import *

# PROCESSING DELETE
def setup():
    
    size(displayWidth, displayHeight - 100)
    
    global hasRun, sideBarWidth, headerHeight
    
    hasRun = []
    sideBarWidth = 75
    headerHeight = 30
    
    rect(0, 0, width, headerHeight)
    

# PROCESSING DELETE
def draw():
    if len(hasRun) == 0:
        currSchedule = solve(pwd("test50.csv"))
        hasRun.append(0)
        redraw(currSchedule)
    
# maybe have global step variable.
# Every time a new step happens in vns, increment it
# In draw, wait

# PROCESSING DELETE
def redraw(currSchedule):
    # width of the screen minus the side bar with divided by the number of routes in the schedule 
    routeWidth = (width - sideBarWidth) / len(currSchedule)
    fill(255)
    stroke(150)
    for x in range(sideBarWidth, width, routeWidth):
        rect(x, headerHeight, routeWidth, height - headerHeight)
        routeIndex = (x - sideBarWidth) / routeWidth
        if routeIndex < len(currSchedule):
            drawRouteTimeWindows(x, currSchedule[routeIndex], routeWidth, routeIndex)
    


# PROCESSING DELETE
def drawRouteTimeWindows(routeX, route, routeWidth, routeIndex):
    pushStyle()
    stroke(50)
    fill(50, 50, 50, 150)
    for t in range(len(route)):
        task = route[t]
        taskWidth = routeWidth / len(route)
        taskX = routeX + t * taskWidth
        
        for tw in range(len(task.timeWindows[routeIndex])):
            timeWindow = task.timeWindows[routeIndex][tw]
            scale = float(height - headerHeight) / 100.0
            twStart = (timeWindow[0] - routeIndex * 100) * scale
            twEnd = (timeWindow[1] - routeIndex * 100) * scale
            rect(taskX, headerHeight + twStart, taskWidth, twEnd - twStart)
    popStyle()
    
    
    
def doOneVNSStep(stepNum, currSchedule):
    
    
    pass