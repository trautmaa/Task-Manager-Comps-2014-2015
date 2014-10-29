# Comps 2014
# Larkin Flodin, Avery Johnson, Maraki Keteman, 
# Abby Lewis, Will Schifeling, and  Alex Trautman


from helper_functions import *
from create_tasks_from_csv import get_task_list

class Node(object):
    def __init__(self):
        self.children = []
        self.parent = []
        self.schedule = None
        self.searched = 0
        self.tasks_to_search = None

    def add_child(self, child):
        self.children.append(child)

    def add_parent(self, parent):
        self.parent.append(child)

    def set_schedule(self, schedule):
        self.schedule = schedule

    def mark_searched(self):
        self.searched = 1

    def set_tasks_to_search(self, tasks_to_search):
        self.tasks_to_search = tasks_to_search

def compute_lower_bound():
    return 10000 # To be changed

'''
Returns node with longer schedule
'''
def choose_better_node(node_a, node_b):
    if len(node_a.schedule) > len(node_b.schedule):
        return node_a
    return node_b

'''
Returns the node with the longest schedule in the list
'''
def choose_best_node(list_of_nodes):
    best_node = list_of_nodes[0]
    for node in list_of_nodes:
        if len(node.schedule) > len(best_node.schedule):
            best_node = node
    return best_node

'''
Needs to be implemented
'''
def create_nodes_to_search(node):
    pass

'''
If the given node has no more tasks_to_search, then return the better of node and upper_bound_node
If the lower bound is larger than (or equal to) the schedule of the upper_bound_node, then return the upper_bound_node
Otherwise, populate the node_list with all the children of all the nodes_to_search
'''
def dfs(node, upper_bound_node):
    if len(node.tasks_to_search) == 0:
        return choose_better_node(node, upper_bound_node)
    elif compute_lower_bound() >= len(upper_bound_node.schedule):
        return upper_bound_node
    else:
        node_list = []
        nodes_to_search = create_nodes_to_search(node)
        for search_node in nodes_to_search:
            node_list.append(dfs(search_node, upper_bound_node))
        return choose_best_node(node_list)
        

'''
Uses create_tasks_from_csv file to get a task_list
Next, populates a tree with height equal to the number of these tasks. 
Branching left means including the task on time,
branching right means including the task after all that we want to be on time.

Takes a filename as input
'''
def make_a_binary_tree(file_name):
    task_list = get_task_list(file_name)
    Head = Node()
    set_up_node(task_list, Head)
    
#    ChildOne = Node()
#    ChildTwo = Node()
#    ChildOne.parent = Head
#    ChildTwo.parent = Head
    
'''
set_up_node takes as parameters a task_list and a parent
It makes a node with parent parent.
For children, it assigns one to include the first task in task_list and one to exclude the first task in task_list
'''
def set_up_node(task_list, parent):
    if len(task_list) > 1: #there is more than one task left to think about
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
    file_name = "test.csv"
    node = Node()
    make_a_binary_tree(file_name)


if __name__ == "__main__":
    main()
