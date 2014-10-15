# Comps 2014
# Larkin Flodin, Avery Johnson, Maraki Keteman, 
# Abby Lewis, Will Schifeling, and  Alex Trauman
import csv
import random
import itertools
import math

task_features = ['x_coord', 'y_coord', 'release_time', 'duration', 'deadline']


'''
Generates a task as a list so that it may be written to a csv file.
'''
def generate_task(x_constraint, y_constraint, schedule_length, time_needed, extra_time):
    features = [x_constraint, y_constraint, schedule_length, time_needed, extra_time]
    task = []
    for feature in features:
        task.append(random.random()*feature)
    task[4] = task[2] + task[3] + task[4]
    if task[4] >100:
        task[4] = 100
    return task


'''
Given a csv file, it will read tasks into a list before they are to be converted into a class
so each task may then be turned into an object.
'''
def read_in_task(csv_file):
    tasks = []
    with open(csv_file, 'rb') as f:
        reader = csv.reader(f)
        for row in reader:
            tasks.append(row)
    return tasks[1:]


# make_objects() is a function which returns a list populated with the information 
# from the task_list input
# The function should still work if we add more columns to the .csv file (add another
# piece of information for each task)
def make_objects(task_list):
	object_list = []
	for i in range(len(task_list)): #i is each tuple
		newobject = Task()
		object_list.append(newobject)
		for j in range(len(task_list[i])): #j is xcoord, ycoord, release time, duration, deadline
			if (j % 5 == 0): #x coordinate value
				entry_we_want = task_list[i][j%5]
				object_list[i].setX(entry_we_want)
			if (j % 5 == 1): #y coordinate value
				entry_we_want = task_list[i][j%5]
				object_list[i].setY(entry_we_want)
			if (j % 5 == 2): #release time
				entry_we_want = task_list[i][j%5]
				object_list[i].set_release_time(entry_we_want)
			if (j % 5 == 3): #duration
				entry_we_want = task_list[i][j%5]
				object_list[i].set_duration(entry_we_want)
			if (j % 5 == 4): #deadline
				entry_we_want = task_list[i][j%5]
				object_list[i].set_deadline(entry_we_want)
	return object_list


def get_distance(task_a, task_b):
    return ((task_a.x - task_b.x)**2 + (task_a.y - task_b.y)**2)**0.5

'''
A function given a list of objects and all the potential ways
to order the tasks will output one of the schedules with the 
most tasks scheduled.
'''
def find_maximal_schedule(object_list, task_orderings):
    max_schedule = []
    for task_ordering in task_orderings:
        new_schedule = create_schedule(task_ordering, object_list)
        if len(new_schedule) > len(max_schedule):
            max_schedule = new_schedule
    return max_schedule
            
'''
A function that given an ordering of tasks and a list of objects
will output the schedule that can be created from that ordering.
'''
def create_schedule(task_ordering, object_list):
    last_included_task = object_list[task_ordering[0]]
    schedule = [last_included_task]
    ending_time = last_included_task.release_time + last_included_task.duration
    for i in range(len(task_ordering)):
        if i == 0:
            pass
        else:
            includable, ending_time = includable_task(ending_time, last_included_task, object_list[task_ordering[i]])
            if includable:
                last_included_task = object_list[task_ordering[i]]
                schedule.append(last_included_task)
                
                
    return schedule

def print_schedule(schedule):
    finishing_time = 0
    for i in range(len(schedule)):
        if i == 0:
            finishing_time = schedule[i].release_time + schedule[i].duration
            print "Task", i+1, "will start at", schedule[i].release_time, "and finish at", finishing_time, \
                "becuase it must start after", schedule[i].release_time, "and must finish before", schedule[i].deadline
        else:
            starting_time = get_starting_time_of_next_task(finishing_time, schedule[i-1], schedule[i])
            finishing_time = starting_time + schedule[i].duration
            print "Task", i+1, "will start at", starting_time, "and finish at", finishing_time, \
                "becuase it must start after", schedule[i].release_time, "and must finish before", schedule[i].deadline
        


    
def get_starting_time_of_next_task(finishing_time, prev_task, next_task):
    distance = get_distance(prev_task, next_task)
    starting_time = max((finishing_time + distance), next_task.release_time)
    return starting_time

'''
A function that given the finishing time of the last task done
and the previous task object and next task object will return
(true, the end time of finishing the next task) if the next task 
can be completed before it's deadline and (false, the finishing 
time of the task previously included) if the next_task cannot be finished.
'''
def includable_task(finishing_time, prev_task, next_task):
    starting_time = get_starting_time_of_next_task(finishing_time, prev_task, next_task)
    ending_time = (starting_time + next_task.duration)
    if ending_time <= next_task.deadline:
        return True, ending_time
    return False, finishing_time

'''
a function that returns all potential orderings of tasks.
'''
def get_all_permutations(length_of_perms):
    permutations = [i for i in range(length_of_perms)]
    permutations = list(itertools.permutations(permutations, length_of_perms))
    return permutations

def set_up_N_tasks():
    with open('my.csv', 'wb') as f:
        writer = csv.writer(f)
        writer.writerow(task_features)
        for i in range(10):
            writer.writerow(generate_task(5, 5, 10, 2, 2))
    
    tasks = read_in_task('my.csv')#tasks is list of tuples

    #Testing the class:
    object_list = make_objects(tasks) # object_list gets objects populated with info from tasks
    return object_list

def main():
    object_list = set_up_N_tasks()
    task_orderings = get_all_permutations(len(object_list))
    best_schedule = find_maximal_schedule(object_list, task_orderings)
    print_schedule(best_schedule)



#Class definition
#Task is a class that contains five variables
class Task(object):
    def setX(self, x):#x coordinate
    	self.x = float(x)
    def setY(self, y):#y coordinate
    	self.y = float(y)
    def set_release_time(self, r):#release time
    	self.release_time = float(r)
    def set_duration(self, dur):#duration
    	self.duration = float(dur)
    def set_deadline(self, dead):#deadline
    	self.deadline = float(dead)




if __name__ == '__main__':
    main()
    
    
    
