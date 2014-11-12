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

def vns(taskList, currSolution):
    
    #Number of seconds VNS is allowed to run
    stoppingCondition = 300
    
    #Number of neighborhood structures
    nHoodMax = 17
    
    #Number of iterations since last bestSolution update
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
            iterSolution = iterativeImprovement(taskList, shakeSolution, nHoodIndex)
            
            #make sure the modified solution is still feasible. 
            # If it is not, try again
            # If it is, and it is a better solution, update bestSolution
            feasibleSolution = isFeasible(taskList, iterSolution)
            if feasibleSolution == None:
                feasible = False
            else:
                feasible = True
                iterSolution = feasibleSolution
            
            #if feasible and better
            #     accept it as the new solution, reset nHood of numIterations
            
            if feasible:
                #If our solution is better than the current solution, update.
                if isBetter(iterSolution, currSolution):
                    currSolution = iterSolution
                    nHood = 1
                #Otherwise, increment nHood
                else:
                    nHood += 1
                
                #If our solution is better than the best solution so far, update.
                if isBetter(iterSolution, bestSolution):
                    bestSolution = iterSolution
                    numIterations = 0
                    
            #If we have gone 8000 iterations with no improvement to bestSolution
            # If criteria for selection are true, select a new currSolution
            elif numIterations > 8000:
                numIterations = 0
                
                if nHood > 8:
                    currSolution = iterSolution
                    nHood = 1
                #Criteria for nHoods 1-8:
                # If the new solution is not more than .5% longer (distance), accept
                elif calcDistance(iterSolution) >= .995*calcDistance(currSolution):
                    currSolution = iterSolution
            else:
                numIterations += 1
    return bestSolution

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
    return newSolution

'''
@return: modified solution
'''
def crossExchange(currSolution, nHoodIndex):
    # choose two distinct random days
    
    # find the length of the routes to be exchanged:
    #    for route1 (removed and inserted), length = rand(1, min(numberCustomers, nHoodIndex))
    #    for route2 (just removed), length = rand(0, min(numberCustomers, nHoodIndex))
    # route1: choose random segment w/ customers who have a valid time window in day2
    # route2: choose random segment
    # remove route1 from day1, remove route2 from day2, insert route1 into day2 where route2 was
    return currSolution

'''
@return: modified solution
'''
def optionalExchange1(currSolution, nHoodIndex):
    # set p and q according to nHood Index
    # pick a random day and starting time to exchange customers
    # using the p and q values, add and remove however many customers you need to
    # use the customerQueue to do this
    # replace the chosen days with the updated days
    return currSolution

'''
@return: modified solution
'''
def optionalExchange2(currSolution, nHoodIndex):
    # calculate number to remove (nHoodIndex-12)
    numRemove = nHoodIndex - 12
    # pick a random day and position
    # remove those number of customers starting at that point
    # update the chosen days
    return currSolution


'''
@return: modified solution
'''
def iterativeImprovement(taskList, currSolution, nHoodIndex):
    #If nHoodIndex< 13: do 3-OPT
    if nHoodIndex < 13:
        #only currSolution because we believe edges are being removed and inserted within the solution
        newSolution = threeOPT(currSolution)
    #Otherwise: Best Insertion
    else:
        newSolution = bestInsertion(taskList, currSolution)
    return currSolution
'''
@return: solution that has been modified by 3-Opt
'''
def threeOPT(currSolution):
    #MUST ASSUME START AND END ARE CONNECTED?
    duration = getDuration(currSolution)
    improvement = False
    #CHECK DEPENDING ON HOW WE STORE SCHEDULES
    scheduleLength = len(currSolution)
    #2
    while improvement == False:
        #5
        for n in range(1, scheduleLength):
            #8
            for k in range(1, scheduleLength - 3):
                #9
                for j in range(1, scheduleLength - 1):
                    #10
                    distance1 = dist(currSolution[k], currSolution[j+1]) + dist(currSolution[1], currSolution[j])
                    distance2 = dist(currSolution[1], currSolution[j+1]) + dist(currSolution[k], currSolution[j])
                    #11
                    distance3 = dist(currSolution[1], currSolution[scheduleLength]) + dist(currSolution[k], currSolution[k+1]) + dist(currSolution[j], currSolution[j+1])
                    #10
                    if  distance1 <= distance2:
                        d = distance1
                        #11
                        if d + dist(currSolution[k+1], currSolution[scheduleLength]) < distance3:
                            #16
                            # make newSchedule = [j+2....schedulelength, k+1, 1...k,j+1] 
                            #newDuration = check duration
                            if newDuration < duration:
                                newSolution = newSchedule
                                improvement = True
                                break
                    #10
                    else:
                        d = distance2
                        #11
                        if d + dist(currSolution[k+1], currSolution[scheduleLength]) < distance3:
                            #18
                            # make newSchedule = [j+2....schedulelength, k+1, k...1,j+1]
                            #newDuration = check duration
                            if newDuration < duration:
                                newSolution = newSchedule
                                improvement = True
                                break
    
    return newSolution

def getDuration(currSolution):
    return 0

'''
@return: solution that has been modified by 3-Opt
'''
def bestInsertion(taskList, currSolution):
    
    return currSolution


'''
@return: True if sol1 has more profit than sol2
'''
def isBetter(sol1, sol2):
    sum1 = 0 #sum profits in sol1 (number of tasks, right now)
    sum2 = 0 #sum profits in sol2
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


