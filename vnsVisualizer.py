import vns, Objects

# PROCESSING DELETE
def setup():
    
    size(displayWidth, displayHeight - 100)
    
    global sideBarWidth, headerHeight, schedSteps, currStep, sched
    
    sched = []
    
    sideBarWidth = 75
    headerHeight = 30
    currStep = [-1]
        
    currSchedule, schedSteps = vns.solve(pwd("test50.csv"))
    

# PROCESSING DELETE
def draw():
    if len(sched) == 0:
        currStep[0] = 0
        sched.append(schedSteps[currStep[0]])
    
    if keyPressed and keyCode == RIGHT:
        currStep[0] += 1
        newSched = schedSteps[currStep[0]]
        if isinstance(newSched[1], Objects.Route):
            routeIndex = newSched[2]
            sched[0][1][routeIndex] = newSched[1]
        else:
            sched.pop()
            sched.append(newSched)
        
        drawRoute()
        
    

# maybe have global step variable.
# Every time a new step happens in vns, increment it
# In draw, wait

# PROCESSING DELETE
def drawRoute():

    fill(255, 255, 255, 255)
    rect(0, 0, width, headerHeight)

    
    # width of the screen minus the side bar with divided by the number of routes in the schedule
    currSchedule = sched[0][1]

    stringInfo = sched[0][0]
    
    routeWidth = (width - sideBarWidth) / len(currSchedule)
    fill(255)
    stroke(150)
    for x in range(sideBarWidth, width, routeWidth):
        rect(x, headerHeight, routeWidth, height - headerHeight)
        routeIndex = (x - sideBarWidth) / routeWidth
        if routeIndex < len(currSchedule):
            drawRouteTimeWindows(x, currSchedule[routeIndex], routeWidth, routeIndex)
    print stringInfo
    
    fill(0, 0, 0, 255)
    text(stringInfo, width/2 - 200, 10, 400, headerHeight)
    


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
