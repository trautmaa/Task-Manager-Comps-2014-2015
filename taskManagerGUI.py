# Comps 2014
# Larkin Flodin, Avery Johnson, Maraki Ketema, 
# Abby Lewis, Will Schifeling, and  Alex Trautman

'''
To do:

Label days
Make it clearer what the ghost time windows are
Add a menu to choose algorithm and task input file, AND be able to manually input tasks

'''

'''
To run this properly, drag and drop the file onto processing-py, available at

https://github.com/jdf/processing.py
'''

import greedyByOrder, greedyByPresentChoice
from math import floor
from createTests import dayLength
import os


def setup():
    
    initialize()
    
    global buttonList, buttonRects, buttonFunctions
    #actually do math bro
    buttonRects = [[100, 100]]
    buttonFunctions = ["vns.py"]
    buttonList = len(buttonFunctions) * [False]  
    
    drawButtons()
    
    menuSetup()
    #calendarSetup()
    size(displayWidth, displayHeight)    

def draw():
    #FIX MEEEE
    if mousePressed == True:
        if mouseX >= 100 and mouseX <= 100+textWidth("vns.py"):
            if mouseY >= 100 and mouseY <= 100+100: #EEWWWWW
                clickedOkay[0] = True
    if clickedOkay[0]:
        drawCalendar()
    
    else:
        drawMenu()

def sketchFullScreen():
    return True

def drawMenu():
    drawButtons()

def drawCalendar():
    calendarSetup()

def initialize():
    
    global dayWidth, dayHeight, headerHeight, sideBarWidth, mapDimension, mapX, mapY, maxX, maxY
    global textX, textY, textDimensionX, textDimensionY, clickedOkay
    global taskRects, taskMapDots, dayRects, colorList, rectColors
    global schedule, minWidth, timeList, timeWindowRects, maxNumTimeWindows
    global blues, greens, oranges, yellows
    
    clickedOkay = [False]    
    
    #colors that fit our color scheme
    blues = [color(46, 75, 137), color(71, 98, 157), color(105, 130, 184),
                        color(150, 170, 213), color(200, 212, 238)]

    greens = [color(37, 108, 118), color(63, 131, 140), color(99, 160, 169),
               color(150, 198, 205), color(203, 231, 234)]
    
    oranges = [color(192, 123, 59), color(229, 162, 100), color(255, 199, 148),
                color(255, 219, 185), color(255, 237, 221)]
    
    yellows = [color(192, 147, 59), color(229, 185, 100), color(255, 219, 148),
                color(255, 231, 185), color(255, 243, 221)]
    
    #rainbow from which to create rectColors rainbow spectrum
    colorList = [color(255, 0, 0), color(255, 255, 0), color(0, 255, 0),\
                 color(0, 255, 255), color(0, 0, 255), color(255, 0, 255)]
    
    #what times we see on the sidebar
    timeList = [9, 10, 11, 12, 1, 2, 3, 4, 5, 6]
    
    
    smooth()
    background(blues[3])
    
    
def drawButton(x, y, buttonText, buttonHeight):
    pushStyle()
    noStroke()
    textSize(32)
    fill(yellows[4], alpha = 255)
    rect(x, y, 10 + textWidth(buttonText), buttonHeight, 7)
    fill(blues[0])
    text(buttonText, x + 5, y + 50)
    popStyle()

def drawButtons():
    for b in range(len(buttonList)):
        buttonRect = buttonRects[b]
        drawButton(buttonRect[0], buttonRect[1], buttonFunctions[b], 100)

def menuSetup():
    pass

def calendarSetup():
    
    #initialize global lists to empty
    taskRects = []
    timeWindowRects = []
    rectColors = []
    taskMapDots = []
    dayRects = []
    
    #do stuff so that we can call different algorithms depending on user's selection
    vns = pwd("vns.py")
    file = pwd("newTest.csv")
    print os.system("python " + vns + " " + file)
    
    csvFile = pwd("newTest.csv")
    
    #vns schedule:
#     schedule, useless = vns.solve(csvFile)
    schedule = greedyByOrder.runGreedyByOrder(csvFile, greedyByOrder.orderByPriority)
    greedyByPrioritySol = greedyByOrder.runGreedyByOrder(csvFile, greedyByOrder.orderByPriority)
    greedyByDeadlineSol = greedyByOrder.runGreedyByOrder(csvFile, greedyByOrder.orderOptionalByDeadline)
    greedyByPresentChoiceSol = greedyByPresentChoice.runGreedyByPresentChoice(csvFile)
    solutionList = [greedyByPrioritySol, greedyByDeadlineSol, greedyByPresentChoiceSol]
    bestGreedy = max(solutionList, key = lambda schedule : schedule.getProfit())
 
    schedule = bestGreedy
    print schedule
    #Globals for reference later
    
    setupScreen()

def setColors():
    for d in range(len(schedule)):
        
        scaleFactor = float(d+1)/float(len(schedule)) * (len(colorList) - 1)
        baseColor = int(floor(scaleFactor))
        percentBetweenColors = scaleFactor - baseColor
        #find new r, g and b where its scaled according to the percentBetweenColors
        oldC = [red(colorList[baseColor - 1]), green(colorList[baseColor - 1]), blue(colorList[baseColor - 1])]
        oldNextC = [red(colorList[baseColor]), green(colorList[baseColor]), blue(colorList[baseColor])] 
        
        
        newC = [abs(oldC[c] - oldNextC[c]) for c in range(len(oldC))]
        
        for c in range(len(newC)):
            if oldC[c] == 0:
                newC[c] = oldC[c] + (oldNextC[c] - oldC[c]) * percentBetweenColors
            else:
                newC[c] = oldC[c] - (oldC[c] - oldNextC[c]) * percentBetweenColors
        
        newColor = color(newC[0], newC[1], newC[2])
        
        
#         newColor = blendColor(colorList[baseColor-1],colorList[baseColor],0)
        #newColor = blendColor(colorList[baseColor-1]*percentBetweenColors,colorList[baseColor],BLEND)
        rectColors.append(newColor)


def calendarDraw():
    #NEED TO CALL setupScreen() IF IT IS THE FIRST TIME
    calendarDrawInit()
    whichTask = -1
    whichDay = -1
    whichTask, whichDay = update(mouseX, mouseY, whichTask, whichDay)
    drawScreen()
    drawMap(whichDay, whichTask)
    drawTextBox(whichDay, whichTask)
    highlight(whichTask, whichDay)

def calendarDrawInit():
    headerHeight = 50
    sideBarWidth = 75
    dayWidth = min(200, (displayWidth - sideBarWidth)/len(schedule))

    #Set global minimum screen width
    minWidth = 1000
        
    w = max(len(schedule) * dayWidth + sideBarWidth, minWidth)
    h = min(900, displayHeight)
    dayHeight = h/2 - headerHeight


    #Set dimension and coordinates for map and text box
    mapDimension = h - dayHeight - 2 * headerHeight
    
    textDimensionX = mapDimension
    textDimensionY = mapDimension / 2
    
    mapX = (w - mapDimension - textDimensionX) * 2 / 3 + textDimensionX
    mapY = dayHeight + headerHeight + ((h - (dayHeight + headerHeight) - mapDimension)/2)

    #set X and Y for our text box
    textX = (w - mapDimension - textDimensionX) * 1/3
    textY = mapY + mapDimension * 1 / 16


    #populate the rectColors list with some rainbow colors
    setColors()

    #determine maximum coordinate values
    maxX = 0
    maxY = 0
    maxNumTimeWindows = 0
    for day in range(len(schedule)):
        for t in range(len(schedule[day])):
            task = schedule[day][t]
            taskX = task.x
            taskY = task.y
            if taskX > maxX:
                maxX = taskX
            if taskY > maxY:
                maxY = taskY
            
            #get maxNumTimeWindows so we can make ghost time windows appropriate width in highlight()
            for j in range(len(schedule[day][t].timeWindows)):
                if len(schedule[day][t].timeWindows[j]) > maxNumTimeWindows:
                    maxNumTimeWindows = len(schedule[day][t].timeWindows[j])
                
    

    
    
#Updating our global values whichDay and whichTask, telling us which day and which task (if any) need to be highlighted
def update(x, y, whichTask, whichDay):
    
    #if cursor is in the map
    if x >= mapX and x <= mapX + mapDimension and y >= mapY and y <= mapY + mapDimension:
        coordPlay = 7
        matchingCoordsX = []
        for d in range(len(taskMapDots)):
            for t in range(len(taskMapDots[d])):
                coordinates = taskMapDots[d][t]
                if x >= (coordinates[0] - coordPlay) and x <= (coordinates[0] + coordPlay):
                    if (y >= coordinates[1] - coordPlay) and y <= (coordinates[1] + coordPlay):
                        #if x and y are within the coordinate bounds, return the task # and day #
                        return t, d
                            
    #else cursor could be on the schedule
    #find out which day
    for d in range(len(dayRects)):
        day = dayRects[d]
        if x >= day[0] and x <= day[0] + day[2] and y >= day[1] and y <= day[1] + day[3]:
            whichDay = d
            break
    if whichDay == -1:
        return -1, -1
    #find out which task
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
    
    #empty the taskMapDots list
    for i in range(len(taskMapDots)):
        taskMapDots.pop()
    
    #empty the timeWindowRects list
    for i in range(len(timeWindowRects)):
    	timeWindowRects.pop()
    
    #redraw all the tasks
    for d in range(len(schedule)):
        day = schedule[d]
        drawTasks(day, sideBarWidth + (d * dayWidth))

    #redraw all the window's lines and times
    for i in range(10, 110, 10):
        y = headerHeight + (i/100.0) * dayHeight
        strokeWeight(1)
        stroke(0, 0, 0, 50)
        #text(str(i), 0, y)
        line(sideBarWidth, int(y), sideBarWidth + (dayWidth * len(schedule)), int(y))
        
    if whichDay != -1 and whichTask != -1:
        #highlight the current task's rectangle
        fill(175,200,230, 200)
        task = taskRects[whichDay][whichTask]
        fill(rectColors[whichDay], 125)
        rect(task[0], task[1], task[2], task[3])
        
        #make its time window ghosts appear
        timeWindows = timeWindowRects[whichDay][whichTask]
        fill(rectColors[whichDay], 50)
        for i in range(len(timeWindows)):
            rect(timeWindows[i][0], timeWindows[i][1], timeWindows[i][2], timeWindows[i][3])
        
        #add task information to text box
        textSize(20)
        fill(blues[3])
        textItemsList = []
        task = schedule[whichDay][whichTask]
        textStr = ""
        textStr = textStr + "ID: " + str(task.id) + "\n"
        textStr = textStr + "Release Time: " + str(task.releaseTime) + "\n"
        textStr = textStr + "X Coordinate: " + str(task.x) + "\n"
        textStr = textStr + "Y Coordinate: " + str(task.y) + "\n"
        textStr = textStr + "Start Time: " + str(schedule[whichDay].endingTimes[whichTask] - task.duration) + "\n"
        
        
        text(textStr, textX + textDimensionX / 100, textY + textDimensionY / 10)
        
    
    if whichDay != -1:
        drawDayMap(whichDay)
    

def drawScreen():
    pushStyle()
    noStroke()
    
    drawSchedule()
    
    drawDays()
    
    popStyle()

#draw schedule...
def drawSchedule():
    fill(255,255,255)
    rect(sideBarWidth, headerHeight, dayWidth * len(schedule), dayHeight)

#A function to set up the preliminary style details for the given schedule
def setupScreen():
    pushStyle()
    
    noStroke()
    
    
    drawSchedule()
    
    drawDays()
    
    #Header
    fill(blues[1])
    rect(0,0, width, headerHeight)

    #Sidebar
    fill(blues[0]) 
    rect(0, headerHeight, sideBarWidth, dayHeight)
    
    #Add times to the sidebar
    textSize(15)
    fill(240,240,240)
    for i in range(10, 110, 10):
        y = (headerHeight + ((i/100.0 - .07) * dayHeight))
        strokeWeight(2)
        stroke(0, 0, 0, 50)
        timeText = "%d:%02d" % (timeList[i/10 - 1], 00)
        text(timeText, 0, y)

        #limit line width to width of days
        line(sideBarWidth, int(y), sideBarWidth + (dayWidth * len(schedule)), int(y))
    
    
    
    popStyle()

def drawDays():
    pushStyle()
    
    #Lines differentiating the days in the schedule
    stroke(200)
    for i in range(len(taskRects)):
        taskRects.pop()

    for i in range(len(taskMapDots)):
    	taskMapDots.pop()

	for i in range(len(timeWindowRects)):
		timeWindowRects.pop()

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
    
    #get dayNum from leftX:
    dayNum = (leftX - sideBarWidth) / dayWidth
    
    timeWindowsToAdd = []
    dayToAdd = []
    mapLocationsToAdd = []
    for t in range(len(route)):
        task = route[t]
        
        #scale tasks so dimensions fit within day
        routeIndex = int(route.endingTimes[t] - task.duration)/int(dayLength)
        
        startTime = ((float(route.endingTimes[t] - task.duration)/float(dayLength)) - routeIndex) * dayHeight
        #set color of our unhighlighted tasks - depends on the day
        fill(rectColors[dayNum], 50)
        
        #for the MAP, scale our coordinates to values within the box
        xToAdd = (float(task.x) / float(maxX) * \
                  (mapDimension - (float(mapDimension)/10.0)) + (mapX + float(mapDimension)/20.0))
        yToAdd = (float(task.y) / float(maxY) * \
                  (mapDimension - (mapDimension/10)) + (mapY + mapDimension/20))

        #mapLocationsToAdd is a list of each task's coordinates
        mapLocationsToAdd.append([xToAdd, yToAdd])
        
        #dayToAdd is a list of each task's rectangle's dimensions for a given day
        dayToAdd.append([leftX, headerHeight + startTime, dayWidth, (float(task.duration)/float(dayLength)) * dayHeight])
        
        #draw the rectangle for each task
        rect(leftX, headerHeight + startTime, dayWidth, (float(task.duration)/float(dayLength)) * dayHeight )
        
        #initialize local helper list
        timeWindowsPerTask = []
        
        #populate the timeWindowRects list; draw these when task is highlighted
        for tw in range(len(task.timeWindows[dayNum])):
            twStart = task.timeWindows[dayNum][tw][0]
            twEnd = task.timeWindows[dayNum][tw][1]
            
            routeIndex = int(twStart) / int(dayLength)
            startTime = ((float(twStart) / float(dayLength)) - routeIndex) * dayHeight
            
            #numTimeWindowsForTask = len(task.timeWindows[dayNum])
            #widths = dayWidth/numTimeWindowsForTask
            widths = dayWidth/maxNumTimeWindows
            xStart = leftX + tw * widths
            
            #add rect dimensions for each time window            
            timeWindowsPerTask.append([xStart, headerHeight + startTime, widths, (float(twEnd - twStart)/float(dayLength)) * dayHeight])       	
       
       #add the timewindow rects for each task
        timeWindowsToAdd.append(timeWindowsPerTask)
          
    
    #taskRects is a list of lists of the task rectangle's dimensions
    timeWindowRects.append(timeWindowsToAdd)
    taskRects.append(dayToAdd)
    #taskMapDots is a list days, each of which is a list of coordinates of points on the map for that day
    taskMapDots.append(mapLocationsToAdd)

    popStyle()



#drawMap 
def drawMap(whichDay, whichTask):
    pushStyle()
    #Create Map box
    fill(255,255,255)
    rect(mapX, mapY, mapDimension, mapDimension)

    #draw the dots
    fill(0,0,0)
    for day in range(len(taskMapDots)):
        for t in range(len(taskMapDots[day])):
            strokeWeight(10)

        	#set the stroke depending on whichDay and whichTask are selected
            if day == whichDay:

            	#selected task gets a bigger dot
                if t == whichTask: 
                    stroke(rectColors[day])
                    strokeWeight(15)

                #non-selected task on a selected day gets a gray dot
                else:
                    stroke(rectColors[day], alpha = 100)
            
            #non-selected task on a non-selected day gets a lighter dot, on the rainbow spectrum
            else:
                stroke(rectColors[day], alpha = 40)
            
            #draw the dot
            task = taskMapDots[day][t]
            x = task[0]
            y = task[1]
            point(x, y)

    #if cursor is over a day, draw the lines connecting that day's tasks
    if whichDay != -1:
        drawDayMap(whichDay)
    popStyle()

#Function to draw the text box
def drawTextBox(whichDay, whichTask):
    pushStyle()
    
    #Create Text box
    fill(255,255,255)
    rect(textX, textY, textDimensionX, textDimensionY)
    
    
    
    popStyle()
    

#Function to draw the lines connecting the tasks you do on a certain day
def drawDayMap(whichDay):
    pushStyle()
    for t in range(len(taskMapDots[whichDay])-1):
        task = taskMapDots[whichDay][t]
        nextTask = taskMapDots[whichDay][t+1]

        #line dimensions
        x1 = task[0]
        y1 = task[1]
        x2 = nextTask[0]
        y2 = nextTask[1]

        #line settings
        strokeWeight(2)
        #stroke(50)
        #color the line depending on the day's color
        stroke(rectColors[whichDay], 50)
        
        #draw line
        line(x1, y1, x2, y2)
    popStyle()
    
