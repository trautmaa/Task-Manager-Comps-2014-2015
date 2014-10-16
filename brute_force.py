# Comps 2014
# Larkin Flodin, Avery Johnson, Maraki Keteman, 
# Abby Lewis, Will Schifeling, and  Alex Trauman

import csv
import random
import itertools
import math
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
A function that given an ordering of tasks and a list of objects
will output the schedule that can be created from that ordering.
'''
def create_schedule(task_ordering, object_list):
    last_included_task = object_list[task_ordering[0]]
    schedule = [last_included_task]
    ending_time = last_included_task.release_time + last_included_task.duration
    for i in range(len(task_ordering)):
        if i == 0:
            pass
        else:
            includable, ending_time = includable_task(ending_time, last_included_task, 
                                                      object_list[task_ordering[i]])
            if includable:
                last_included_task = object_list[task_ordering[i]]
                schedule.append(last_included_task)
                
    return schedule
    

'''
A function that given the finishing time of the last task done
and the previous task object and next task object will return
(true, the end time of finishing the next task) if the next task 
can be completed before it's deadline and (false, the finishing 
time of the task previously included) if the next_task cannot be finished.
'''
def includable_task(finishing_time, prev_task, next_task):
    starting_time = get_starting_time_of_next_task(finishing_time, prev_task, next_task)
    ending_time = (starting_time + next_task.duration)
    if ending_time <= next_task.deadline:
        return True, ending_time
    return False, finishing_time


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
    
    
    
