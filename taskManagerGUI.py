# Comps 2014
# Larkin Flodin, Avery Johnson, Maraki Ketema, 
# Abby Lewis, Will Schifeling, and  Alex Trautman


'''
To run this properly, drag and drop the file onto processing-py, available at

https://github.com/jdf/processing.py
'''
import vns

def setup():
    
#     schedule = [[]]*5
    schedule = vns.solve(pwd("test11.csv"))

    print len(schedule)

    #Globals for reference later
    global dayWidth, dayHeight, headerHeight, sideBarWidth
    headerHeight = 50
    sideBarWidth = 75
    dayWidth = min(200, (displayWidth - sideBarWidth)/len(schedule))
    
    w = len(schedule) * dayWidth + sideBarWidth
    h = min(900, displayHeight)
    dayHeight = h/2 - headerHeight
    size(w, h)
    
    setupScreen(schedule)
    drawDays(schedule)
    

def draw():
    pass

#A function to set up the preliminary style details for the given schedule
def setupScreen(schedule):
    pushStyle()
    noStroke()
    
    #Header
    fill(175, 200, 175)
    rect(0,0, width, headerHeight)
    
    #Sidebar
    fill(175, 175, 200)
    rect(0, headerHeight, sideBarWidth, dayHeight)
    
    #Schedule
    fill(255,255,255)
    rect(sideBarWidth,headerHeight,width, dayHeight)
    
    popStyle()

def drawDays(schedule):
    pushStyle()
    
    #Lines differentiating the days in the schedule
    stroke(200)
    for d in range(1,len(schedule)):
        #new for loop index from 0
        line(dayX, headerHeight, dayX, dayHeight+headerHeight)

    #draw the tasks
    for d in range(len(schedule)):
        dayX = dayWidth * d + sideBarWidth
        drawTasks(schedule[d], dayX)

    popStyle()

def drawTasks(route, leftX):
    pushStyle()
    for t in range(len(route)):
        #THis is gonna fuck up on days later than day 1
        task = route[t]
        print task, route.endingTimes[t]
        startTime = ((route.endingTimes[t] - task.duration)/1000.0) * dayHeight
        print startTime
        
        fill(100,100,100)
        
        print leftX, headerHeight + startTime, dayWidth, task.duration
        rect(leftX, headerHeight + startTime, dayWidth, (task.duration/1000.0) * dayHeight )
        
    popStyle()
