from greedy_by_order import *
from create_tasks_from_csv import *
from helper_functions import *
import time


'''
@return: an ordering of tasks
'''
def solve(csvFile):
    #Get a greedy algorithm to then modify with VNS
    taskList = get_task_list(csvFile)
    modTasks = run_greedy_by_order(csvFile, order_by_deadline)
    
    #Modify the greedy algorithm
    modTasks = vns(taskList, modTasks)
    
    return create_schedule(modTasks, taskList)

'''
@return: modified solution
'''

###### AVERY AND ABBY CHECK THIS SHIT OUT WHEN YOU'RE AWAKE
def vns(taskList, currSolution):
    
    #Number of seconds VNS is allowed to run
    stoppingCondition = 300
    
    #Number of neighborhood structures
    nHoodMax = 17
    
    #Number of iterations since last solution update
    numIterations = 0
    
    bestSolution = currSolution
    initTime = time.time()
    
    #until the stopping condition is met
    while time.time() - initTime > 0:
        #If we have gone through all neighborhood structures,
        #start again
        nHood = 1
        while nHood < nHoodMax:
            shakeSolution = shaking(currSolution, nHood)
            iterSolution = iterativeImprovement(taskList, currSolution, nHoodIndex)
            
            #make sure the modified solution is still feasible. 
            # If it is not, try again
            # If it is, and it is a better solution, update bestSolution
            feasibleSolution = isFeasible(taskList, iterSolution)
            if feasibleSolution == None:
                feasible = False
            else:
                feasible = True
                iterSolution = feasibleSolution
            if feasible and isBetter(iterSolution, currSolution):
                currSolution = iterSolution
                k = 1
                if isBetter(currSolution, bestSolution):
                    bestSolution  = currSolution
                    numIterations = 0
                    
                #After 8000 iterations without improvement, accept a slightly worse solution
                elif numIterations > 8000:
                    numIterations = 0
                    if nHood > 8:
                        currSolution = iterSolution
                        nHood = 1
                    elif calcDistance(iterSolution) >= .995*calcDistance(currSolution):
                        currSolution = iterSolution                    
                    elif nHood == nHoodMax:
                        nHood = 1
                        numIterations += 1
                    else:
                        nHood += 1
                        numIterations += 1  
    return currSolution

'''
@return: total distance of a solution
'''
def calcDistance(currSolution):
    return 0

'''
@return: modified solution
'''
def shaking(currSolution, nHoodIndex):
    #Based on the neighborhood perform a different operation
    if nHoodIndex <= 8:
        newSolution = crossExchange(currSolution, nHoodIndex)
    elif nHoodIndex > 8 and nHoodIndex <= 12:
        newSolution = optionalExchange1(currSolution, nHoodIndex)
    else:
        newSolution = optionalExchange2(currSolution, nHoodIndex)
    return currSolution

'''
@return: modified solution
'''
def optionalExchange1(currSolution, nHoodIndex):
    return currSolution

'''
@return: modified solution
'''
def optionalExchange2(currSolution, nHoodIndex):
    return currSolution

'''
@return: modified solution
'''
def crossExchange(currSolution, nHoodIndex):
    return currSolution

'''
@return: modified solution
'''
def iterativeImprovement(taskList, currSolution, nHoodIndex):
    return currSolution

'''
@return: True if sol1 has more profit than sol2
'''
def isBetter(sol1, sol2):
    return True

'''
@return: solution if currSolution is feasible
'''
def isFeasible(taskList, currSolution):
    return True

'''
@return: Graph with modified release times
'''
def tightenReleaseTimes(taskList, currSolution):
    return G

'''
@return: Graph with modified deadlines
'''
def tightenDeadlines(taskList, currSolution):
    return G

'''
@return: shortest duration of this schedule ordering
'''
def minRoute(taskList, currSolution):
    return 0

def calcDominantSolution(taskList, currSolution):
    return currSolution