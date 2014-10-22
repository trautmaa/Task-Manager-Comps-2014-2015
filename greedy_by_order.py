# Comps 2014
# Larkin Flodin, Avery Johnson, Maraki Keteman, 
# Abby Lewis, Will Schifeling, and  Alex Trauman

import itertools
from create_tasks_from_csv import *
from write_to_csv import *
from helper_functions import *
from brute_force import *


'''
A function that will create a schedule based on just ordering
all tasks by their release time or deadline and then outputting that 
schedule.
'''
def run_greedy_by_order(n, method):
    written_csv  = write_n_tasks(n, 'my.csv')
    object_list = get_object_list(written_csv)
    if method == "deadline":
        object_list = order_by_deadline(object_list)
    if method == "release":
        object_list = order_by_release(object_list)
    ordering = [i for i in range(len(object_list))]
    best_schedule = create_schedule(ordering, object_list)
    print_schedule(best_schedule)
    print


def main():
    run_greedy_by_order(10, "deadline")
    run_greedy_by_order(10, "release")
    


if __name__ == '__main__':
    main()
    
