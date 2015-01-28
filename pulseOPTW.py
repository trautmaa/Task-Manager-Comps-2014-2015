# Comps 2014
# Larkin Flodin, Avery Johnson, Maraki Ketema, 
# Abby Lewis, Will Schifeling, and  Alex Trautman


'''
Find the paper on the drive: Ants>Duque,...
Ants are actually called Pulses now
'''
'''
To do :
figure out 
    - bounding
    - soft dominance
    - parallel python
'''


'''
def pulse(node, currScore, currTime, currPath):
    if isFeasible(node, currTime) and inBounds(node, currScore, currTime) 
    and notSoftDominated(node, currTime, currPath):
        newPath = currPath.add(node)
        newScore = currScore + node.score
        for newNode in node.unvisitedNeighbors:
            if noDetour(node, newNode, currPath, currTime):
                newTime = currTime + dist(node, newNode)
                pulse(newNode, newScore, newTime, newPath)


    return currPath?????


def noDetour(currPath, newNode, graph):
    for each node in currPath:
        schedule as early as possible
    schedule newNode as early as possible
    
    if the end of the last node in currPath + dist(last, new)>= start of newNode:
        return True
    for unvisitedNode in graph:
        if it can fit between end of lastNode and start of newNode:
            (there is a possible detour)
            return False
    return True
    
def isFeasible(node, currTime, currPath):
    If currTime + node.duration > node deadline or node can't fit in tw or exceed time limit
    or we've already visited this node in the path:
        return False
    return True

def notSoftDominated():
    Do this when you're smarter

def inBounds(node, currTime):
    Do this when you're smarter
'''