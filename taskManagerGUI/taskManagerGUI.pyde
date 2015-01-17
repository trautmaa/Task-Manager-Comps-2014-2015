
#import vns

def setup():
    schedule = [[None]]*5
        
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
    
    #Lines differentiating the days in the schedule
    stroke(200)
    for d in range(1,len(schedule)):
        line(dayWidth * d + sideBarWidth, headerHeight, dayWidth * d+ sideBarWidth, dayHeight+headerHeight)
        
        
    
    popStyle()

def drawDays(schedule):
    pushStyle()

    popStyle()

def drawTasks(route):
    pass
