# Comps 2014
# Larkin Flodin, Avery Johnson, Maraki Ketema, 
# Abby Lewis, Will Schifeling, and  Alex Trautman

import vns, Objects, copy
from createTests import dayLength

def setup():
    
    size(displayWidth, displayHeight - 100)
    
    global sideBarWidth, headerHeight, schedSteps, currStep, sched, keyPressed
    
    global dayColor, twColor, headerColor, sideBarColor, textColor, taskColor
    
    keyPressed = [False, False]
    
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
    taskColor = greens[0]
    
    
    sched = []
    
    sideBarWidth = 75
    headerHeight = 60
    currStep = [-1]
        
    currSchedule, schedSteps = vns.solve(pwd("averysImportantTestFile.csv"), 15)
    fill(sideBarColor, 255)
    noStroke()
    rect(0, headerHeight, sideBarWidth, height-headerHeight)
    
    

def draw():
    if len(sched) == 0:
        currStep[0] = 0
        sched.append(schedSteps[currStep[0]])
        drawRoute()
        return
    
    if keyPressed[0]:
        
        keyPressed[0] = False
        currStep[0] += 1
        newSched = schedSteps[currStep[0]]
        
        if isinstance(newSched[1], Objects.Route):
            routeIndex = newSched[2]
            sched[0] = copy.deepcopy(sched[0])
            if sched[0][1] != None:
                sched[0][1][routeIndex] = newSched[1]
            sched[0][0] = newSched[0]
            schedSteps[currStep[0]] = copy.deepcopy(sched[0])
        else:
            sched.pop()
            sched.append(newSched)
        
        
        drawRoute()
    elif keyPressed[1]:
        keyPressed[1] = False
        if currStep[0] > 0:
            currStep[0] -= 1
            newSched = schedSteps[currStep[0]]
            sched.pop()
            sched.append(newSched)
        drawRoute()
    
def keyPressed():
    if keyCode == RIGHT:
        keyPressed[0] = True
    elif keyCode == LEFT:
        keyPressed[1] = True
    

# maybe have global step variable.
# Every time a new step happens in vns, increment it
# In draw, wait

def drawRoute():
    pushStyle()
    
    fill(headerColor, 255)
    rect(0, 0, width, headerHeight)
    fill(dayColor)
    text("Task IDs", 5, headerHeight - 10)
    
    # width of the screen minus the side bar with divided by the number of routes in the schedule
    currSchedule = sched[0][1]

    stringInfo = sched[0][0]
    print currStep[0], stringInfo
    if currSchedule == None:
        fill(dayColor)
        rect(sideBarWidth, headerHeight, width - sideBarWidth, height - headerHeight)
        stringInfo = stringInfo + " IT WAS NONE"
    else:
        routeWidth = (width - sideBarWidth) / len(currSchedule)
        fill(dayColor, 255)
        stroke(150)
        for x in range(sideBarWidth, width, routeWidth):
            rect(x, headerHeight, routeWidth, height - headerHeight)
            routeIndex = (x - sideBarWidth) / routeWidth
            if routeIndex < len(currSchedule):
                drawRouteTimeWindows(x, currSchedule[routeIndex], routeWidth, routeIndex)
        
    
    fill(textColor, 255)
    text(stringInfo, width/2 - 200, 10, 400, headerHeight)
    popStyle()
    

def drawRouteTimeWindows(routeX, route, routeWidth, routeIndex):
    pushStyle()
    
    
    if len(route.endingTimes) > 0 and route.endingTimes[0] != None:
        ends = True
    else:
        ends = False
    
    scale = float(height - headerHeight) / dayLength
    
    for t in range(len(route)):
        
        task = route[t]
        
        
        taskWidth = routeWidth / len(route)
        taskX = routeX + t * taskWidth
        stroke(50, alpha = 100)
        strokeWeight(1)
        
        fill(textColor, 255)
        text(task.id, taskX + taskWidth/2 - 5 , 45) 
        
        for tw in range(len(task.timeWindows[routeIndex])):
            
            timeWindow = task.timeWindows[routeIndex][tw]
            
            twStart = (timeWindow[0] - routeIndex * dayLength) * scale
            twEnd = (timeWindow[1] - routeIndex * dayLength) * scale
            fill(twColor, 150)
            rect(taskX, headerHeight + twStart, taskWidth, twEnd - twStart)
            
        
        fill(taskColor, 50)
        noStroke()
        taskHeight = task.duration * scale
        if ends:
            taskEnd = (route.endingTimes[t] - routeIndex * dayLength) * scale
            rect(taskX, headerHeight + taskEnd - taskHeight, taskWidth, taskHeight)
        else:
            pass
    popStyle()
