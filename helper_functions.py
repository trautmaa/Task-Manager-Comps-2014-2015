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
A function given the finishing time of the last task done along with that 
task itself and the next task will return the time you will be able to
start the next task.
'''
def get_starting_time_of_next_task(finishing_time, prev_task, next_task):
    distance = get_distance_between_tasks(prev_task, next_task)
    starting_time_of_next_task = max((finishing_time + distance), next_task.release_time)
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
            starting_time = get_starting_time_of_next_task(finishing_time, schedule[i-1], schedule[i])
            finishing_time = starting_time + schedule[i].duration
            print "Task", i+1, "will start at", starting_time, "and finish at",\
                finishing_time, "becuase it must start after", schedule[i].release_time,\
                "and must finish before", schedule[i].deadline

