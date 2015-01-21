# Comps 2014
# Larkin Flodin, Avery Johnson, Maraki Ketema, 
# Abby Lewis, Will Schifeling, and  Alex Trautman


'''
To run this properly, drag and drop the file onto processing-py, available at

https://github.com/jdf/processing.py
'''
import vns,greedyByOrder, greedyByPresentChoice



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
#     schedule = vns.solve(pwd("test50.csv"))
    csvFile = pwd("test50.csv")
    greedyByPrioritySol = greedyByOrder.runGreedyByOrder(csvFile, greedyByOrder.orderByPriority)
    greedyByDeadlineSol = greedyByOrder.runGreedyByOrder(csvFile, greedyByOrder.orderOptionalByDeadline)
    greedyByPresentChoiceSol = greedyByPresentChoice.runGreedyByPresentChoice(csvFile)
    solutionList = [greedyByPrioritySol, greedyByDeadlineSol, greedyByPresentChoiceSol]
    bestGreedy = max(solutionList, key = lambda schedule : schedule.getProfit())

    schedule = bestGreedy

    #Globals for reference later
    global dayWidth, dayHeight, headerHeight, sideBarWidth
    headerHeight = 50
    sideBarWidth = 75
    dayWidth = min(200, (displayWidth - sideBarWidth)/len(schedule))
    
    w = len(schedule) * dayWidth + sideBarWidth
    h = min(900, displayHeight)
    dayHeight = h/2 - headerHeight
    size(w, h)
    
    setupScreen()


def draw():
    whichTask = -1
    whichDay = -1
    whichTask, whichDay = update(mouseX, mouseY, whichTask, whichDay)
    print whichDay, whichTask
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
    
    #redraw all the tasks
    for d in range(len(schedule)):
        day = schedule[d]
        drawTasks(day, sideBarWidth + (d * dayWidth))

    if whichDay != -1 and whichTask != -1:
        #highlight the current task
        fill(175,200,230)
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
    
    textSize(15)
    fill(10,10,25)
    for i in range(10, 110, 10):
        y = headerHeight + (i/100.0) * dayHeight
        strokeWeight(1)
        stroke(0, 0, 0, 50)
        text(str(i), 0, y)
        line(sideBarWidth, int(y), width, int(y))
    
    popStyle()

def drawDays():
    pushStyle()
    
    #Lines differentiating the days in the schedule
    stroke(200)
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
    
    for t in range(len(route)):
        task = route[t]
        
        dayNum = int(route.endingTimes[t] - task.duration)/int(dayLength)
        startTime = ((float(route.endingTimes[t] - task.duration)/float(dayLength)) - dayNum) * dayHeight
        
        fill(175,200,230, 50)
        
        dayToAdd.append([leftX, headerHeight + startTime, dayWidth, (float(task.duration)/float(dayLength)) * dayHeight])
        
        rect(leftX, headerHeight + startTime, dayWidth, (float(task.duration)/float(dayLength)) * dayHeight )
        
    taskRects.append(dayToAdd)
    
    popStyle()
