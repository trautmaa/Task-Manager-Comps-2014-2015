# Comps 2014
# Larkin Flodin, Avery Johnson, Maraki Ketema, 
# Abby Lewis, Will Schifeling, and  Alex Trautman

from helperFunctions import *
from greedyByOrder import runGreedyByOrder
from greedyByPresentChoice import runGreedyByPresentChoice
from bruteForce import runBruteForceAlg
from writeToCsv import writeNTasks
# from taskManagerIntProg import runIntegerProgram
from time import time

fileName = "test.csv"
inputSize = 10

'''
Prints the total number of tasks the algorithm with a particular name
has scheduled, as well as the percentage of tasks it has scheduled.
'''
def printAlgResults(algName, totalTasks, possibleTasksCompleted, tasksCompleted, totalTime):
	print algName, "has scheduled", tasksCompleted, "out of", \
		possibleTasksCompleted, "or", \
		(100.0 * tasksCompleted / possibleTasksCompleted), \
		"percent of possible tasks."
	if (totalTime != None):
		print "This algorithm takes", (totalTime / (totalTasks / inputSize)), "seconds on average."

'''
Loops forever, repeatedly generating new inputs for the problem,
solving them with all algorithms, and periodically printing
updates on the aggregate numbers solved by each algorithm.
'''
def comparisonLoop():
	inputsSeen = 0
	totalTasksSeen = 0
	tasksCompletedBrute = 0
	tasksCompletedOrderDeadline = 0
	tasksCompletedOrderRelease = 0
	tasksCompletedChoiceStarting = 0
	tasksCompletedChoiceCompletion = 0

	tasksCompletedIntegerProgram = 0
	bruteForceTime = 0
	integerProgramTime = 0
	while True:
		inputsSeen += 1
		totalTasksSeen = inputsSeen * inputSize
# 		writeNTasks(inputSize, fileName)
		beforeTime = time()
		tasksCompletedBrute += len(runBruteForceAlg(fileName))
		bruteForceTime += time() - beforeTime
		beforeTime = time()
# 		tasksCompletedIntegerProgram += len(runIntegerProgram(fileName))
# 		integerProgramTime += time() - beforeTime
		tasksCompletedOrderRelease += len(runGreedyByOrder(fileName, orderByRelease))
		tasksCompletedOrderDeadline += len(runGreedyByOrder(fileName, orderByDeadline))
		tasksCompletedChoiceStarting += len(runGreedyByPresentChoice(fileName, orderByStartingTime))
		tasksCompletedChoiceCompletion += len(runGreedyByPresentChoice(fileName, orderByEndingTime))
		print inputsSeen, "inputs seen total, each of size", inputSize, "."
		printAlgResults(
			"Brute force", totalTasksSeen, tasksCompletedBrute, tasksCompletedBrute, bruteForceTime)
# 		printAlgResults(
# 			"Integer program", totalTasksSeen, tasksCompletedBrute, tasksCompletedIntegerProgram, integerProgramTime)
		printAlgResults(
			"Greedy by release date", totalTasksSeen, tasksCompletedBrute, tasksCompletedOrderRelease, None)
		printAlgResults(
			"Greedy by deadline", totalTasksSeen, tasksCompletedBrute, tasksCompletedOrderDeadline, None)
		printAlgResults(
			"Greedy by starting time", totalTasksSeen, tasksCompletedBrute, tasksCompletedChoiceStarting, None)
		printAlgResults(
			"Greedy by finish time", totalTasksSeen, tasksCompletedBrute, tasksCompletedChoiceCompletion, None)
		print
		if (tasksCompletedBrute != tasksCompletedIntegerProgram):
			print
			print "Integer program produced a non-optimal solution, halting comparison for debugging."
			print

def main():
	comparisonLoop()


if __name__ == '__main__':
	main()
