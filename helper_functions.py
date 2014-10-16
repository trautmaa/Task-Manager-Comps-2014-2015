# Comps 2014
# Larkin Flodin, Avery Johnson, Maraki Keteman, 
# Abby Lewis, Will Schifeling, and  Alex Trauman


def get_distance(task_a, task_b):
    return ((task_a.x - task_b.x)**2 + (task_a.y - task_b.y)**2)**0.5

def get_starting_time_of_next_task(finishing_time, prev_task, next_task):
    distance = get_distance(prev_task, next_task)
    starting_time = max((finishing_time + distance), next_task.release_time)
    return starting_time


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

