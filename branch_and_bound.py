# Comps 2014
# Larkin Flodin, Avery Johnson, Maraki Keteman, 
# Abby Lewis, Will Schifeling, and  Alex Trautman


from helper_functions import *

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

def choose_better_node(node_a, node_b):
    if len(node_a.schedule) > len(node_b.schedule):
        return node_a
    return node_b

def choose_best_node(list_of_nodes):
    best_node = list_of_nodes[0]
    for node in list_of_nodes:
        if len(node.schedule) > len(best_node.schedule):
            best_node = node
    return best_node

def dfs(node, upper_bound_node):
    if len(node.tasks_to_search) == 0:
        return choose_better_node(node, upper_bound_node)
    elif compute_lower_bound() >= len(upper_bound_node.schedule):
        return upper_bound_node
    else:
        node_list = []
        nodes_to_search = create_nodes_to_search(node):
        for search_node in nodes_to_search:
            node_list.append(dfs(search_node, upper_bound_node))
        return choose_best_node(node_list)
        
    


def main():
    node = Node()


if __name__ == "__main__":
    main()
