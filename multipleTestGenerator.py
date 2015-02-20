# Comps 2014
# Larkin Flodin, Avery Johnson, Maraki Ketema, 
# Abby Lewis, Will Schifeling, and  Alex Trautman

import createTests
import os

'''
These are the baseline parameters. Individual functions will change these, create a test,
then change them back, to avoid having to type all the parameters to writeNTasks
a million times.
'''
dayLength = 1440
numberOfTasks = 64
xRange = 60
yRange = 60
releaseTimeRange = 0
durationMin = 1
durationMax = 120
deadlineRange = 1440 * 3
priorityRange = 10
numberRequired = 8
numDays = 3
maxTaskTimeWindows = 2
numberDependencies = 0
numberConsistent = 0

'''
Creates a test with baseline parameters. See
https://docs.google.com/a/carleton.edu/document/d/18T8vBWkGwU1XW6XSNElvy18muNcUZbKYWpDTg-EXb_Y/edit

@param fileName: the path of the file to create the test at
'''
def createBaselineTest(fileName):
	createTestWithGlobals(fileName)

def createTaskNumberTest(fileName, numTasks):
	global numberRequired
	global numberOfTasks
	oldNumTasks = numberOfTasks
	oldNumRequired = numberRequired
	numberRequired = int(numTasks * .125)
	numberOfTasks = numTasks
	createTestWithGlobals(fileName)
	numberOfTasks = oldNumTasks
	numberRequired = oldNumRequired

def createDayNumberTest(fileName, numberOfDays):
	global numDays
	oldNumDays = numDays
	numDays = numberOfDays
	createTestWithGlobals(fileName)
	numDays = oldNumDays

def createMaxTimeWindowsTest(fileName, numberWindows):
	global maxTaskTimeWindows
	oldNumWindows = maxTaskTimeWindows
	maxTaskTimeWindows = numberWindows
	createTestWithGlobals(fileName)
	maxTaskTimeWindows = oldNumWindows

def createNumberRequiredTest(fileName, numRequired):
	global numberRequired
	oldNumberRequired = numberRequired
	numberRequired = numRequired
	createTestWithGlobals(fileName)
	numberRequired = oldNumberRequired

def createPriorityTest(fileName, maxPriority):
	global priorityRange
	oldPriorityRange = priorityRange
	priorityRange = maxPriority
	createTestWithGlobals(fileName)
	priorityRange = oldPriorityRange

def createLocationTest(fileName, xValue, yValue):
	global xRange
	global yRange
	oldX = xRange
	oldY = yRange
	xRange = xValue
	yRange = yValue
	createTestWithGlobals(fileName)
	xRange = oldX
	yRange = oldY

def createDurationTest(fileName, minDur, maxDur):
	global durationMin
	global durationMax
	oldMinDur = durationMin
	oldMaxDur = durationMax
	durationMin = minDur
	durationMax = maxDur
	createTestWithGlobals(fileName)
	durationMax = oldMaxDur
	durationMin = oldMinDur

def createConsistentTest(fileName, numConsistent):
	global numberConsistent
	oldNumConsistent = numberConsistent
	numberConsistent = numConsistent
	createTestWithGlobals(fileName)
	numberConsistent = oldNumConsistent

def createReleaseTasksTest(fileName, numRelease):
	global numberDependencies
	oldNumRelease = numberDependencies
	numberDependencies = numRelease
	createTestWithGlobals(fileName)
	numberDependencies = oldNumRelease

'''
Creates a test given the current global parameter settings. These must be set
before calling this function, and should be reset afterwards.

@param fileName: the path of the file to create the test at
'''
def createTestWithGlobals(fileName):
	createTests.writeNTasks(dayLength, numberOfTasks, xRange, yRange, releaseTimeRange,
        durationMin, durationMax, deadlineRange, priorityRange, numberRequired,
        numDays, maxTaskTimeWindows, numberDependencies, numberConsistent, fileName)

'''
Takes a string representing the category of the test, and a number to be appended at the end,
and returns a string that is a path in the test folder to a file like:
"test_testTypeString_number.csv"
'''
def makeFilePath(testTypeString, number):
	return str(os.getcwd()) + "/Test Generation Folder/test_" + testTypeString + "_" + str(number) + ".csv"

def main():
	for i in range(10):
		createBaselineTest(makeFilePath("baseline", i))

		createTaskNumberTest(makeFilePath("sixteenTask", i), 16)
		createTaskNumberTest(makeFilePath("thirtyTwoTask", i), 32)
		# 64 is baseline
		createTaskNumberTest(makeFilePath("oneTwentyEightTask", i), 128)
		createTaskNumberTest(makeFilePath("twoFiftySixTask", i), 256)
 
		createDayNumberTest(makeFilePath("oneDay", i), 1)
		# 3 is baseline
		createDayNumberTest(makeFilePath("fiveDay", i), 5)
		createDayNumberTest(makeFilePath("sevenDay", i), 7)
 
		createMaxTimeWindowsTest(makeFilePath("oneWindow", i), 1)
		# 2 is baseline
		createMaxTimeWindowsTest(makeFilePath("threeWindow", i), 3)
 
		createNumberRequiredTest(makeFilePath("zeroRequired", i), 0)
		# 8 is baseline
		createNumberRequiredTest(makeFilePath("sixteenRequired", i), 16)
		createNumberRequiredTest(makeFilePath("thirtyTwoRequired", i), 32)
 
		createPriorityTest(makeFilePath("onePriority", i), 1)
		# 10 is baseline
		createPriorityTest(makeFilePath("oneHundredPriority", i), 100)
 
		createLocationTest(makeFilePath("thirtyLocation", i), 30, 30)
		# 60, 60 is baseline
		createLocationTest(makeFilePath("oneHundredTwentyLocation", i), 120, 120)
		createLocationTest(makeFilePath("twoHundredFortyLocation", i), 240, 240)
 
		createDurationTest(makeFilePath("sixtyDuration", i), 1, 60)
		# 1, 120 is baseline
		createDurationTest(makeFilePath("twoHundredFortyDuration", i), 1, 240)
		createDurationTest(makeFilePath("threeHundredSixtyDuration", i), 1, 360)
 
		# 0 is baseline
		createConsistentTest(makeFilePath("thirtyTwoConsistent", i), 32)
		createConsistentTest(makeFilePath("sixtyFourConsistent", i), 64)
 
		# 0 is baseline
		createReleaseTasksTest(makeFilePath("sixteenDependencies", i), 16)
		createReleaseTasksTest(makeFilePath("thirtyTwoDependencies", i), 32)


if __name__ == '__main__':
	main()
