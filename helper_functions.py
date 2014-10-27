# Comps 2014
# Larkin Flodin, Avery Johnson, Maraki Keteman, 
# Abby Lewis, Will Schifeling, and  Alex Trauman

'''
A function given two task objects will return the euclidean distance
between them. I should check if **.5 is faster than math.sqrt()?
'''
def get_distance_between_tasks(task_a, task_b):
    return ((task_a.x - task_b.x)**2 + (task_a.y - task_b.y)**2)**0.5

'''
A function that returns the distance between 2 tuple coordinates.
'''
def get_distance_between_coords(location_a, location_b):
    return ((location_a[0] - location_b[0])**2 + (location_a[1] - location_b[1])**2)**0.5

'''
A function that returns a tuple of a task's coordinates.
'''
def get_coords(task):
    return (task.x, task.y)

'''
A function given a task, the present location and the present time
returns True if it is finishable (before the task's deadline) along 
with the finishing time and False if not, and the present time.
'''
def is_finishable_task(task, present_location, present_time):
    distance = get_distance_between_coords(get_coords(task), present_location)
    starting_time = max(task.release_time, (present_time + distance))
    finishing_time = starting_time + task.duration
    if finishing_time <= task.deadline:
        return True, finishing_time
    return False, present_time


'''
A function that given an ordering of tasks and a list of objects
will output the schedule that can be created from that ordering.
'''
def create_schedule(task_ordering, task_list):
    last_location = (2.5, 2.5)
    ending_time = 0
    schedule = []
    for i in range(len(task_ordering)):
        task = task_list[task_ordering[i]]
        includable, ending_time = is_finishable_task(task, last_location, 
                                                     ending_time)
        if includable:
            last_location = get_coords(task)
            schedule.append(task)
    return schedule
    
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

def order_by_method(tasks_list, method):
    if method == "start_time":
        return order_by_release(tasks_list)
    else:
        return order_by_deadline(tasks_list)

def get_ending_time(present_location, present_time, task):
    distance = get_distance_between_coords(present_location, present_location)
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
A function will print out the schedule in a semi-readable fashion.
'''
def print_schedule(schedule):
    finishing_time = 0
    for i in range(len(schedule)):
        if i == 0:
            finishing_time = schedule[i].release_time + schedule[i].duration
            print "Task", i+1, "will start at", schedule[i].release_time,\
                "and finish at", finishing_time, "becuase it must start after",\
                schedule[i].release_time, "and must finish before", schedule[i].deadline
        else:
            starting_time = get_starting_time_of_next_task(finishing_time, get_coords(schedule[i-1]), 
                                                           get_coords(schedule[i]), schedule[i].release_time)
            finishing_time = starting_time + schedule[i].duration
            print "Task", i+1, "will start at", starting_time, "and finish at",\
                finishing_time, "becuase it must start after", schedule[i].release_time,\
                "and must finish before", schedule[i].deadline

