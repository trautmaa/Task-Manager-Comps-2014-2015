# Comps 2014
# Larkin Flodin, Avery Johnson, Maraki Ketema, 
# Abby Lewis, Will Schifeling, and  Alex Trautman


from helperFunctions import *
from createTasksFromCsv import getTaskList

class Node(object):
    def __init__(self):
        self.children = []
        self.parent = []
        self.schedule = None
        self.searched = 0
        self.tasksToSearch = None

    def addChild(self, child):
        self.children.append(child)

    def addParent(self, parent):
        self.parent.append(child)

    def setSchedule(self, schedule):
        self.schedule = schedule

    def markSearched(self):
        self.searched = 1

    def setTasksToSearch(self, tasksToSearch):
        self.tasksToSearch = tasksToSearch

def computeLowerBound():
    return 10000 # To be changed

'''
Returns node with longer schedule
'''
def chooseBetterNode(nodeA, nodeB):
    if len(nodeA.schedule) > len(nodeB.schedule):
        return nodeA
    return nodeB

'''
Returns the node with the longest schedule in the list
'''
def chooseBestNode(listOfNodes):
    bestNode = listOfNodes[0]
    for node in listOfNodes:
        if len(node.schedule) > len(bestNode.schedule):
            bestNode = node
    return bestNode

'''
Needs to be implemented
'''
def createNodesToSearch(node):
    pass

'''
If the given node has no more tasksToSearch, then return the better of node and upperBoundNode
If the lower bound is larger than (or equal to) the schedule of the upperBoundNode, then return the upperBoundNode
Otherwise, populate the nodeList with all the children of all the nodesToSearch
'''
def dfs(node, upperBoundNode):
    if len(node.tasksToSearch) == 0:
        return chooseBetterNode(node, upperBoundNode)
    elif computeLowerBound() >= len(upperBoundNode.schedule):
        return upperBoundNode
    else:
        nodeList = []
        nodesToSearch = createNodesToSearch(node)
        for searchNode in nodesToSearch:
            nodeList.append(dfs(searchNode, upperBoundNode))
        return chooseBestNode(nodeList)
        

'''
Uses createTasksFromCsv file to get a taskList
Next, populates a tree with height equal to the number of these tasks. 
Branching left means including the task on time,
branching right means including the task after all that we want to be on time.

Takes a filename as input
'''
def makeABinaryTree(fileName):
    taskList = getTaskList(fileName)
    Head = Node()
    setUpNode(taskList, Head)
    
#    ChildOne = Node()
#    ChildTwo = Node()
#    ChildOne.parent = Head
#    ChildTwo.parent = Head
    
'''
setUpNode takes as parameters a taskList and a parent
It makes a node with parent parent.
For children, it assigns one to include the first task in taskList and one to exclude the first task in taskList
'''
def setUpNode(taskList, parent):
    if len(taskList) > 1: #there is more than one task left to think about
        newNodeInclude = Node()
        newNodeExclude = Node()
        newNodeInclude.parent = parent
        newNodeExclude.parent = parent
        #Set each nodes identity to be "Task ___ was included" or "Task ___ was not included"
        #Now, call recursively

    else: #just return the two leaves, for this is the last task to think about
        newNodeInclude = Node()
        newNodeExclude = Node()
        newNodeInclude.parent = parent
        newNodeExclude.parent = parent
        #Set each nodes identity to be "Task ___ was included" or "Task ___ was not included"

'''
Tries to build a tree from the tasks in test.csv
'''
def main():
    fileName = "test.csv"
    node = Node()
    makeABinaryTree(fileName)


if __name__ == "__main__":
    main()
