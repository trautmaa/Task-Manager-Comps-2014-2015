# Comps 2014
# Larkin Flodin, Avery Johnson, Maraki Keteman, 
# Abby Lewis, Will Schifeling, and  Alex Trautman

import itertools

from create_tasks_from_csv import *
from helper_functions import *

'''
A function that given a csv_file and the function used to determine which
task we want to do next, this algorithm makes a schedule by picking
one job at a time using a greedy rule that accounts for the current
location and time.
'''
def run_greedy_by_present_choice(csv_file, order_function):
    task_list = get_task_list(csv_file)
    schedule = select_schedule(task_list, order_function)
    print_schedule(schedule)
    print

'''
Refer to run_greedy_by_present_choice.
Given a method and a task list, returns a greedily selected schedule.
'''
def select_schedule(task_list, order_function):
    schedule, present_location, present_time = [], (0, 0), 0 # present_location is arbitrary.
    task = get_next_task(
        present_time, present_location, task_list, order_function)
    while (task != None):
        schedule.append(task)
        present_time = get_ending_time(present_location, present_time, task) 
        present_location = get_coords(task)
        del task_list[task_list.index(task)]
        task = get_next_task(
            present_time, present_location, task_list, order_function)            
    return schedule

'''
A function that given a present time and location along with a tasks list, and
a method that will return the next task that can be started or finished depending on the method.
'''
def get_next_task(starting_time, starting_location, remaining_tasks_list, order_function):
    finishable_tasks = []
    for task in remaining_tasks_list:
        finishable, ending_time = is_finishable_task(
            task, starting_location, starting_time)
        if finishable:
            finishable_tasks.append(task)
    if len(finishable_tasks) == 0:
        return None
    finishable_tasks = order_function(finishable_tasks, starting_location, starting_time)
    return finishable_tasks[0]
    
    

def main():
    run_greedy_by_present_choice("test.csv", order_by_starting_time)
    run_greedy_by_present_choice("test.csv", order_by_ending_time)
    


if __name__ == '__main__':
    main()
