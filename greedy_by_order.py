# Comps 2014
# Larkin Flodin, Avery Johnson, Maraki Keteman, 
# Abby Lewis, Will Schifeling, and  Alex Trauman

import itertools
from create_tasks_from_csv import *
from helper_functions import *
from brute_force import *


'''
A function that will create a schedule based on just ordering
all tasks by their release time or deadline and then outputting that 
schedule.
'''
def run_greedy_by_order(csv_file, method):
    task_list = get_task_list(csv_file)
    if method == "deadline":
        task_list = order_by_deadline(task_list)
    if method == "release":
        task_list = order_by_release(task_list)
    ordering = [i for i in range(len(task_list))]
    best_schedule = create_schedule(ordering, task_list)
    print_schedule(best_schedule)
    print


def main():
    run_greedy_by_order("test.csv", "deadline")
    run_greedy_by_order("test.csv", "release")
    


if __name__ == '__main__':
    main()
    
