# Comps 2014
# Larkin Flodin, Avery Johnson, Maraki Ketema, 
# Abby Lewis, Will Schifeling, and  Alex Trautman

import itertools

from create_tasks_from_csv import *
from helper_functions import *


'''
A function that prints the result of run_greedy_by_order
in a more detailed format.
'''
def print_greedy_by_order(csv_file, order_function):
	schedule = run_greedy_by_order(csv_file, order_function)
	print_schedule(schedule)
	print

'''
A function that will create a schedule based on just ordering
all tasks by their release time or deadline and then outputting that 
schedule.
'''
def run_greedy_by_order(csv_file, order_function):
    task_list = get_task_list(csv_file)
    task_list = order_function(task_list)
    ordering = [i for i in range(len(task_list))]
    best_schedule = create_schedule(ordering, task_list)
    return best_schedule

def main():
    print
    print_greedy_by_order("test.csv", order_by_release)
    print_greedy_by_order("test.csv", order_by_deadline)
    


if __name__ == '__main__':
    main()
    
