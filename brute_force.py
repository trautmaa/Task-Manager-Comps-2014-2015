# Comps 2014
# Larkin Flodin, Avery Johnson, Maraki Keteman, 
# Abby Lewis, Will Schifeling, and  Alex Trauman

import csv
import random
import itertools
import math
from create_tasks_from_csv import *
from write_to_csv import *

task_features = ['x_coord', 'y_coord', 'release_time', 'duration', 'deadline']


def get_distance(task_a, task_b):
    return ((task_a.x - task_b.x)**2 + (task_a.y - task_b.y)**2)**0.5

'''
A function given a list of objects and all the potential ways
to order the tasks will output one of the schedules with the 
most tasks scheduled.
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
            includable, ending_time = includable_task(ending_time, last_included_task, object_list[task_ordering[i]])
            if includable:
                last_included_task = object_list[task_ordering[i]]
                schedule.append(last_included_task)
                
                
    return schedule

def print_schedule(schedule):
    finishing_time = 0
    for i in range(len(schedule)):
        if i == 0:
            finishing_time = schedule[i].release_time + schedule[i].duration
            print "Task", i+1, "will start at", schedule[i].release_time, "and finish at", finishing_time, \
                "becuase it must start after", schedule[i].release_time, "and must finish before", schedule[i].deadline
        else:
            starting_time = get_starting_time_of_next_task(finishing_time, schedule[i-1], schedule[i])
            finishing_time = starting_time + schedule[i].duration
            print "Task", i+1, "will start at", starting_time, "and finish at", finishing_time, \
                "becuase it must start after", schedule[i].release_time, "and must finish before", schedule[i].deadline
        


    
def get_starting_time_of_next_task(finishing_time, prev_task, next_task):
    distance = get_distance(prev_task, next_task)
    starting_time = max((finishing_time + distance), next_task.release_time)
    return starting_time

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
a function that returns all potential orderings of tasks.
'''

def get_all_permutations(length_of_perms):
    permutations = [i for i in range(length_of_perms)]
    permutations = list(itertools.permutations(permutations, length_of_perms))
    return permutations




def main():
    written_csv  = write_n_tasks(10, 'my.csv')
    object_list = get_object_list(written_csv)
    task_orderings = get_all_permutations(len(object_list))
    best_schedule = find_maximal_schedule(object_list, task_orderings)
    print_schedule(best_schedule)





if __name__ == '__main__':
    main()
    
    
    
