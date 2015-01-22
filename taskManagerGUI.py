# Comps 2014
# Larkin Flodin, Avery Johnson, Maraki Ketema, 
# Abby Lewis, Will Schifeling, and  Alex Trautman


'''
To run this properly, drag and drop the file onto processing-py, available at

https://github.com/jdf/processing.py
'''
import vns, greedyByOrder, greedyByPresentChoice



def setup():
    #PLEASE LINK DAYLENGTH TO SCHEDULE SET DAY LENGTH
    global dayLength
    dayLength = float(100)
    
    global taskRects, taskMapDots, dayRects
    
    taskRects = []
    taskMapDots = []
    dayRects = []
    
    global schedule
#     schedule = [[]]*5
    csvFile = pwd("test50.csv")
    #vns schedule:
    #schedule = vns.solve(pwd("test50.csv"))
    schedule = greedyByOrder.runGreedyByOrder(csvFile, greedyByOrder.orderByPriority)
    greedyByPrioritySol = greedyByOrder.runGreedyByOrder(csvFile, greedyByOrder.orderByPriority)
    greedyByDeadlineSol = greedyByOrder.runGreedyByOrder(csvFile, greedyByOrder.orderOptionalByDeadline)
    greedyByPresentChoiceSol = greedyByPresentChoice.runGreedyByPresentChoice(csvFile)
    solutionList = [greedyByPrioritySol, greedyByDeadlineSol, greedyByPresentChoiceSol]
    bestGreedy = max(solutionList, key = lambda schedule : schedule.getProfit())

    schedule = bestGreedy
    print schedule
    #Globals for reference later
    global dayWidth, dayHeight, headerHeight, sideBarWidth, boxDimension, boxX, boxY, maxX, maxY
    headerHeight = 50
    sideBarWidth = 75
    dayWidth = min(200, (displayWidth - sideBarWidth)/len(schedule))
    
    w = len(schedule) * dayWidth + sideBarWidth
    h = min(900, displayHeight)
    dayHeight = h/2 - headerHeight

    boxDimension = displayHeight - dayHeight - 200 - headerHeight
    boxX = w/2 - boxDimension/2
    boxY = dayHeight + headerHeight + ((h - (dayHeight + headerHeight) - boxDimension)/2)

    maxX = 0
    maxY = 0
    for day in range(len(schedule)):
        for t in range(len(schedule[day])):
            task = schedule[day][t]
            taskX = task.x
            taskY = task.y
            if taskX > maxX:
                maxX = taskX
            if taskY > maxY:
                maxY = taskY
    
    size(w, h)
    
    setupScreen()


def draw():
    whichTask = -1
    whichDay = -1
    whichTask, whichDay = update(mouseX, mouseY, whichTask, whichDay)
    drawScreen()
    highlight(whichTask, whichDay)
    
    
    
#Updating our global values whichDay and whichTask, telling us which day and which task (if any) need to be highlighted
def update(x, y, whichTask, whichDay):
    for d in range(len(dayRects)):
        day = dayRects[d]
        if x >= day[0] and x <= day[0] + day[2] and y >= day[1] and y <= day[1] + day[3]:
            whichDay = d
            break
    if whichDay == -1:
        return -1, -1
    for t in range(len(taskRects[whichDay])):
        task = taskRects[whichDay][t]
        if x >= task[0] and x <= task[0] + task[2] and y >= task[1] and y <= task[1] + task[3]:
            
            whichTask = t
            return whichTask, whichDay
    return -1, whichDay

#Highlight the correct day and task
def highlight(whichTask, whichDay):
    
    #empty the taskRects list
    for i in range(len(taskRects)):
        taskRects.pop()
    
    for i in range(len(taskMapDots)):
        taskMapDots.pop()
    
    #redraw all the tasks
    for d in range(len(schedule)):
        day = schedule[d]
        drawTasks(day, sideBarWidth + (d * dayWidth))

    #redraw all the lines and times
    for i in range(10, 110, 10):
        y = headerHeight + (i/100.0) * dayHeight
        strokeWeight(1)
        stroke(0, 0, 0, 50)
        #text(str(i), 0, y)
        line(sideBarWidth, int(y), width, int(y))
        
    if whichDay != -1 and whichTask != -1:
        #highlight the current task
        fill(175,200,230, 200)
        task = taskRects[whichDay][whichTask]
        rect(task[0], task[1], task[2], task[3])

def drawScreen():
    pushStyle()
    noStroke()
    
    #Schedule
    fill(255,255,255)
    rect(sideBarWidth,headerHeight,width, dayHeight)
    
    drawDays()
    
    popStyle()

#A function to set up the preliminary style details for the given schedule
def setupScreen():
    pushStyle()
    
    noStroke()
    
    #Schedule
    fill(255,255,255)
    rect(sideBarWidth,headerHeight,width, dayHeight)
    
    drawDays()
    
    #Header
    fill(175, 200, 175)
    rect(0,0, width, headerHeight)

    #Sidebar
    fill(175, 175, 200)
    rect(0, headerHeight, sideBarWidth, dayHeight)
    
    #Add times to the sidebar
    textSize(15)
    fill(10,10,25)
    for i in range(10, 110, 10):
        y = headerHeight + (i/100.0) * dayHeight
        strokeWeight(1)
        stroke(0, 0, 0, 50)
        text(str(i), 0, y)
        line(sideBarWidth, int(y), width, int(y))
    
    #Create Map box
    fill(255,255,255)
    rect(boxX, boxY, boxDimension, boxDimension)
    drawMap()
    popStyle()

def drawDays():
    pushStyle()
    
    #Lines differentiating the days in the schedule
    stroke(200)
    for i in range(len(taskRects)):
        taskRects.pop()

    for d in range(0,len(schedule)):
        #new for loop index from 0
        dayX = dayWidth * d + sideBarWidth
        drawTasks(schedule[d], dayX)
        
        dayRects.append([dayX, headerHeight, dayWidth, dayHeight])
        if(d > 0):
            
            line(dayX, headerHeight, dayX, dayHeight+headerHeight)

    popStyle()


#route is a day in the schedule
#leftX is the sidebarwidth + (dayNum * dayWidth)
def drawTasks(route, leftX):
    pushStyle()
    noStroke()
    
    dayToAdd = []
    mapLocationsToAdd = []
    for t in range(len(route)):
        task = route[t]
        
        dayNum = int(route.endingTimes[t] - task.duration)/int(dayLength)
        startTime = ((float(route.endingTimes[t] - task.duration)/float(dayLength)) - dayNum) * dayHeight
        
        fill(175,200,230, 50)
        
        #scale our coordinates to values within the box
        xToAdd = (float(task.x) / float(maxX) * (boxDimension - (float(boxDimension)/10.0)) + (boxX + float(boxDimension)/20.0))
        yToAdd = (float(task.y) / float(maxY) * (boxDimension - (boxDimension/10)) + (boxY + boxDimension/20))
        #print "taskX", task.x, "maxX", maxX, "xToAdd", xToAdd
        #print "taskX/maxX", float(task.x) / float(maxX)
        mapLocationsToAdd.append([xToAdd, yToAdd])
        
        
        dayToAdd.append([leftX, headerHeight + startTime, dayWidth, (float(task.duration)/float(dayLength)) * dayHeight])
        
        rect(leftX, headerHeight + startTime, dayWidth, (float(task.duration)/float(dayLength)) * dayHeight )
        
    taskRects.append(dayToAdd)
    taskMapDots.append(mapLocationsToAdd)
    
    popStyle()

    
    
def drawMap():
    pushStyle()
    fill(0,0,0)
    for day in range(len(taskMapDots)):
        for t in range(len(taskMapDots[day])):
            task = taskMapDots[day][t]
            print "task", task
            x = task[0]
            y = task[1]
            ellipse(x, y, 10, 10)
    
    
    
    popStyle()