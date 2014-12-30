# Comps 2014
# Larkin Flodin, Avery Johnson, Maraki Ketema, 
# Abby Lewis, Will Schifeling, and  Alex Trautman

import itertools

import createTasksFromCsv
import helperFunctions

'''
A function that prints the result of runGreedyByOrder
in a more detailed format.
'''
def printGreedyByOrder(csvFile, orderFunction):
	print runGreedyByOrder(csvFile, orderFunction)
	print	
	
'''
A function that will create a schedule based on just ordering
all tasks by their release time or deadline and then outputting that 
schedule.
'''
def runGreedyByOrder(csvFile, orderFunction):
    taskList = createTasksFromCsv.getTaskList(csvFile)
    taskList = orderFunction(taskList)
    ordering = [i for i in range(len(taskList))]
    bestSchedule = helperFunctions.createSchedule(ordering, taskList)
    return bestSchedule

def main():
    print
    printGreedyByOrder("test.csv", helperFunctions.orderByRelease)
    printGreedyByOrder("test.csv", helperFunctions.orderByDeadline)
    


if __name__ == '__main__':
    main()
    
