# Comps 2014
# Larkin Flodin, Avery Johnson, Maraki Keteman, 
# Abby Lewis, Will Schifeling, and  Alex Trauman

import itertools
from create_tasks_from_csv import *
from write_to_csv import *
from helper_functions import *
from brute_force import *


def run_greedy_by_present_choice(n, method):
    written_csv  = write_n_tasks(n, 'my.csv')
    object_list = get_object_list(written_csv)
    schedule = select_schedule(object_list, method)
    print_schedule(schedule)

def select_schedule(object_list, method):
    schedule, present_location, present_time = [], (2.5, 2.5), 0
    best_tasks = object_list
    while len(best_tasks) != 0:
        best_tasks = get_next_task(present_time, present_location,
                                   best_tasks, method)
        if best_tasks:
            next_task = best_tasks[0]
            schedule.append(next_task)
            present_time = get_ending_time(present_location, present_time, next_task) 
            present_location = get_coords(next_task)
            del best_tasks[0]
            
    return schedule

def get_next_task(starting_time, starting_location, tasks_list, method):
    best_tasks = []
    for task in tasks_list:
        finishable, finishing_time = is_finishable_task(task, starting_location, starting_time)
        if finishable:
            best_tasks.append(task)
    if len(best_tasks) == 0:
        return best_tasks
    best_tasks = order_by_method(best_tasks, method)
    return best_tasks
    
    

def main():
    run_greedy_by_present_choice(10, "finish_time")
    run_greedy_by_present_choice(10, "start_time")
    


if __name__ == '__main__':
    main()
