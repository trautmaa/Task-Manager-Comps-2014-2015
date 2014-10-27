# Comps 2014
# Larkin Flodin, Avery Johnson, Maraki Keteman, 
# Abby Lewis, Will Schifeling, and  Alex Trauman

import itertools
from create_tasks_from_csv import *
from write_to_csv import *
from helper_functions import *
from brute_force import *

'''
A function that given a csv_file and the method, i.e. whether to
pick the next task based on when you can start it or when you can finish
it.  This algorithm just picks a schedule based on just doing what it can 
then moving on.
'''
def run_greedy_by_present_choice(csv_file, method):
    task_list = get_task_list(csv_file)
    schedule = select_schedule(task_list, method)
    print_schedule(schedule)
    print

'''
Refer to run_greedy_by_present_choice.
Given a method and a task list, returns a greedily selected schedule.
'''
def select_schedule(task_list, method):
    schedule, present_location, present_time = [], (2.5, 2.5), 0 #present_location is arbitrary.
    best_tasks = task_list
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

'''
A function that given a present time and location along with a tasks list, and
a method will return the next task that can be started or finished depending on the method.
'''
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
    run_greedy_by_present_choice("test.csv", "finish_time")
    run_greedy_by_present_choice("test.csv", "start_time")
    


if __name__ == '__main__':
    main()
