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
    schedule = []
    starting_time = 0
    unable_to_include = set()
    while len(unable_to_include) != len(object_list):
        next_task, finishing_time = get_next_task(starting_time, object_list, \
                                                  unable_to_include, method)
        if next_task == False:
            return schedule
        else:
            schedule.append(next_task):
            unable_to_include = add_unincludable_tasks(unable_to_include, next_task, \
                                                       finishing_time)
    return schedule

def get_next_task(starting_time, object_list, unable_to_include, method):
    

def main():
    run_greedy_by_present_choice(10, "finish_time")
    run_greedy_by_choice(10, "start_time")
    


if __name__ == '__main__':
    main()
