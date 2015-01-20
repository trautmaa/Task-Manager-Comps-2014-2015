# Comps 2014
# Larkin Flodin, Avery Johnson, Maraki Ketema, 
# Abby Lewis, Will Schifeling, and  Alex Trautman


'''
To run this properly, drag and drop the file onto processing-py, available at

https://github.com/jdf/processing.py
'''
import vns

def setup():
    #PLEASE LINK DAYLENGTH TO SCHEDULE SET DAY LENGTH
    global dayLength
    dayLength = float(100)
    
    
#     schedule = [[]]*5
    schedule = vns.solve(pwd("test50.csv"))


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


def draw():
    pass

#A function to set up the preliminary style details for the given schedule
def setupScreen(schedule):
    pushStyle()
    noStroke()
    
    #Schedule
    fill(255,255,255)
    rect(sideBarWidth,headerHeight,width, dayHeight)
    
    drawDays(schedule)
    
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
        print "drawing line from", sideBarWidth, y, "to", width, y
        line(sideBarWidth, int(y), width, int(y))
    
    
    popStyle()

def drawDays(schedule):
    pushStyle()
    
    #Lines differentiating the days in the schedule
    stroke(200)
    for d in range(0,len(schedule)):
        print "Day number", d
        #new for loop index from 0
        dayX = dayWidth * d + sideBarWidth
        drawTasks(schedule[d], dayX)
        if(d > 0):
            line(dayX, headerHeight, dayX, dayHeight+headerHeight)


    popStyle()

def drawTasks(route, leftX):
    pushStyle()
    for t in range(len(route)):
        #THis is gonna fuck up on days later than day 1
        task = route[t]
        
        
        
        dayNum = int(route.endingTimes[t] - task.duration)/int(dayLength)
        startTime = ((float(route.endingTimes[t] - task.duration)/float(dayLength)) - dayNum) * dayHeight
        
        print "task id", task.id, "start", (startTime/dayHeight) * dayLength, "endTime", (route.endingTimes[t] - (dayNum*dayLength)),
        print "duration", task.duration
    
        fill(100,100,100)
        
        rect(leftX, headerHeight + startTime, dayWidth, (float(task.duration)/float(dayLength)) * dayHeight )
        
    popStyle()
