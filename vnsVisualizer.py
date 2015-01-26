import vns, Objects

# PROCESSING DELETE
def setup():
    
    size(displayWidth, displayHeight - 100)
    
    global sideBarWidth, headerHeight, schedSteps, currStep, sched
    
    global dayColor, twColor, headerColor, sideBarColor, textColor
    
    blues = [color(46, 75, 137), color(71, 98, 157), color(105, 130, 184),
             color(150, 170, 213), color(200, 212, 238)]
    
    greens = [color(37, 108, 118), color(63, 131, 140), color(99, 160, 169),
              color(150, 198, 205), color(203, 231, 234)]
    
    oranges = [color(192, 123, 59), color(229, 162, 100), color(255, 199, 148),
               color(255, 219, 185), color(255, 237, 221)]
    
    yellows = [color(192, 147, 59), color(229, 185, 100), color(255, 219, 148),
               color(255, 231, 185), color(255, 243, 221)]
    
    
    dayColor = yellows[-1]
    twColor = blues[2]
    sideBarColor = blues[0]
    headerColor = blues[1]
    
    textColor = oranges[-1]
    
    sched = []
    
    sideBarWidth = 75
    headerHeight = 30
    currStep = [-1]
        
    currSchedule, schedSteps = vns.solve(pwd("test50.csv"))
    fill(sideBarColor, 255)
    noStroke()
    rect(0, headerHeight, sideBarWidth, height-headerHeight)
    
    frameRate(5)
    

def draw():
    if len(sched) == 0:
        currStep[0] = 0
        sched.append(schedSteps[currStep[0]])
        drawRoute()
    
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
    pushStyle()
    
    fill(headerColor, 255)
    rect(0, 0, width, headerHeight)

    
    # width of the screen minus the side bar with divided by the number of routes in the schedule
    currSchedule = sched[0][1]

    stringInfo = sched[0][0]
    
    routeWidth = (width - sideBarWidth) / len(currSchedule)
    fill(dayColor, 255)
    stroke(150)
    for x in range(sideBarWidth, width, routeWidth):
        rect(x, headerHeight, routeWidth, height - headerHeight)
        routeIndex = (x - sideBarWidth) / routeWidth
        if routeIndex < len(currSchedule):
            drawRouteTimeWindows(x, currSchedule[routeIndex], routeWidth, routeIndex)
    print stringInfo
    
    fill(textColor, 255)
    text(stringInfo, width/2 - 200, 10, 400, headerHeight)
    popStyle()
    


# PROCESSING DELETE
def drawRouteTimeWindows(routeX, route, routeWidth, routeIndex):
    pushStyle()
    stroke(50)
    fill(twColor, 150)
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
