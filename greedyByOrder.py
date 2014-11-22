# Comps 2014
# Larkin Flodin, Avery Johnson, Maraki Ketema, 
# Abby Lewis, Will Schifeling, and  Alex Trautman

import itertools

from createTasksFromCsv import *
from helperFunctions import *


'''
A function that prints the result of runGreedyByOrder
in a more detailed format.
'''
def printGreedyByOrder(csvFile, orderFunction):
	schedule = runGreedyByOrder(csvFile, orderFunction)
	printSchedule(schedule)
	print

'''
A function that will create a schedule based on just ordering
all tasks by their release time or deadline and then outputting that 
schedule.
'''
def runGreedyByOrder(csvFile, orderFunction):
    taskList = getTaskList(csvFile)
    taskList = orderFunction(taskList)
    ordering = [i for i in range(len(taskList))]
    bestSchedule = createSolution(ordering, taskList)
    return bestSchedule

def main():
    print
    printGreedyByOrder("test.csv", orderByRelease)
    printGreedyByOrder("test.csv", orderByDeadline)
    


if __name__ == '__main__':
    main()
    
