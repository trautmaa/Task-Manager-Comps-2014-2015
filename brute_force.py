# Comps 2014
# Larkin Flodin, Avery Johnson, Maraki Keteman, 
# Abby Lewis, Will Schifeling, and  Alex Trauman

import itertools
from create_tasks_from_csv import *
from write_to_csv import *
from helper_functions import *

task_features = ['x_coord', 'y_coord', 'release_time', 'duration', 'deadline']


'''
A function given a list of task objects and all the potential ways
to order the tasks will create a schedule for each ordering
and output one of the schedules with the most tasks scheduled.
'''
def find_maximal_schedule(object_list, task_orderings):
    max_schedule = []
    for task_ordering in task_orderings:
        new_schedule = create_schedule(task_ordering, object_list)
        if len(new_schedule) > len(max_schedule):
            max_schedule = new_schedule
    return max_schedule


'''
a function that returns all potential orderings of tasks as a list.
It just takes a number of how many elements you want to be permutated.
'''
def get_all_permutations(length_of_perms):
    permutations = [i for i in range(length_of_perms)]
    permutations = list(itertools.permutations(permutations, length_of_perms))
    return permutations


'''
a function that will run our brute force algorithm to find one of the
best schedules.
'''
def run_brute_force_alg(n):
    written_csv  = write_n_tasks(n, 'my.csv')
    object_list = get_object_list(written_csv)
    task_orderings = get_all_permutations(len(object_list))
    best_schedule = find_maximal_schedule(object_list, task_orderings)
    print_schedule(best_schedule)

def main():
    run_brute_force_alg(10)


if __name__ == '__main__':
    main()
    
    
    