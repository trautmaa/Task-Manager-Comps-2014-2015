# Comps 2014
# Larkin Flodin, Avery Johnson, Maraki Ketema, 
# Abby Lewis, Will Schifeling, and  Alex Trautman

from math import ceil
from Objects import *

'''
A function given two task objects will return the euclidean distance
between them. I should check if **.5 is faster than math.sqrt()?
'''
def get_distance_between_tasks(task_a, task_b):
    return get_distance_between_coords(get_coords(task_a), get_coords(task_b))

'''
A function that returns the distance between 2 tuple coordinates.
'''
def get_distance_between_coords(location_a, location_b):
    return ((location_a[0] - location_b[0]) ** 2 + (location_a[1] - location_b[1]) ** 2) ** 0.5

'''
A function that returns a tuple of a task's coordinates.
'''
def get_coords(task):
    return (task.x, task.y)

'''
A function which given a task, the present location and the present time
returns True if it is finishable (before the task's deadline) and False
if not, along with the time at which the task would complete.
'''
def is_finishable_task(task, present_location, present_time):
    finishing_time = get_ending_time(present_location, present_time, task)
    return (finishing_time <= task.deadline), finishing_time

'''
A function that given an ordering of tasks and a list of objects
will output the schedule that can be created from that ordering.
@return: a schedule object based on the earliest possible schedule
'''
def create_schedule(task_ordering, task_list):
    current_location = (0, 0)
    current_time = 0
    route = Route()
    for i in task_ordering:
        task = task_list[i] # task_ordering is a permutation
        includable, ending_time = is_finishable_task(
            task, current_location, current_time)
        if includable:
            current_location = get_coords(task)
            route.append(task, ending_time)
            current_time = ending_time
    schedule = Schedule()
    schedule.append(route)
    return route
    
'''
A function that given a bunch of tasks will order them by their
deadline from earliest to latest.
'''
def order_by_deadline(task_list):
    task_list = sorted(task_list, key=lambda task: task.deadline)
    return task_list

'''
A function that given a bunch of tasks will order them by their
release time from earliest to latest.
'''
def order_by_release(task_list):
    task_list = sorted(task_list, key=lambda task: task.release_time)
    return task_list

'''
A function that takes a list of tasks and a current location and 
orders the tasks with respect to the earliest time they could be started.
'''
def order_by_starting_time(task_list, current_location, current_time):
    task_list = sorted(task_list, key=lambda task:
        get_starting_time_of_next_task(
            current_time, current_location, get_coords(task), task.release_time))
    return task_list

'''
A function that takes a list of tasks and a current location and 
orders the tasks with respect to the earliest time they could be started.
'''
def order_by_ending_time(task_list, current_location, current_time):
    task_list = sorted(task_list, key=lambda task:
        get_ending_time(current_location, current_time, task))
    return task_list

'''
Takes the present location, the present time, and a task object,
and returns the earliest time at which that task could be completed.
'''
def get_ending_time(present_location, present_time, task):
    distance = get_distance_between_coords(present_location, get_coords(task))
    starting_time = max((present_time + distance), task.release_time)
    ending_time = starting_time + task.duration
    return ending_time

'''
A function given the finishing time of the last task done along with that 
task itself and the next task will return the time you will be able to
start the next task.
'''
def get_starting_time_of_next_task(finishing_time, present_location, next_location, release_time):
    distance = get_distance_between_coords(present_location, next_location)
    starting_time_of_next_task = max((finishing_time + distance), release_time)
    return starting_time_of_next_task


'''
A function that will print out the schedule in a semi-readable fashion.
'''
def print_schedule(schedule):
    current_time = 0
    last_location = (0, 0)
    for i, task in enumerate(schedule):
        starting_time = get_starting_time_of_next_task(
            current_time, last_location, get_coords(task), task.release_time)
        finishing_time = starting_time + task.duration
        if i == 0:
            print "Travel time is", get_distance_between_coords((0, 0), get_coords(task)),\
                "to travel from Start at (0, 0) to Task 1 at", get_coords(task)
            print "Task", i + 1, "will start at", starting_time,\
                "and finish at", finishing_time, "because it must start after",\
                task.release_time, "and must finish before", task.deadline
        else:
            print "Task", i + 1, "will start at", starting_time, "and finish at",\
                finishing_time, "because it must start after", task.release_time,\
                "and must finish before", task.deadline
        if i != (len(schedule) - 1):
            print "Travel time is", get_distance_between_tasks(task, schedule[i + 1]),\
                "to travel from Task", i + 1, "at", get_coords(task), "to Task", i + 2,\
                "at", get_coords(schedule[i + 1])
        current_time = finishing_time
        last_location = get_coords(task)

