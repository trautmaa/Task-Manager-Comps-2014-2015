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
Given a csv file, it will read tasks into a list before they are to be converted into a class.
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

def get_distance(point_a, point_b):
    return ((point_a[0] - point_b)**2 + (point_a[0] - point_b[0])**2)**0.5

def convert_dist_to_time(distance, factor):
    return distance*factor

def get_all_permuations(length_of_perms):
    permutations = [i for i in range(length_of_perms)]
    permutations = list(itertools.permutations(permutations, length_of_perms))
    return permutations

def main():
    with open('my.csv', 'wb') as f:
        writer = csv.writer(f)
        writer.writerow(task_features)
        for i in range(10):
            writer.writerow(generate_task(5, 5, 10, 2, 2))
    
    tasks = read_in_task('my.csv')#tasks is list of tuples

    #Testing the class:
    object_list = make_objects(tasks) # object_list gets objects populated with info from tasks
    print object_list[4].deadline # should print the deadline for the 5th task in the list


#Class definition
#Task is a class that contains five variables
class Task(object):
    def setX(self, x):#x coordinate
    	self.x = x
    def setY(self, y):#y coordinate
    	self.y = y
    def set_release_time(self, r):#release time
    	self.release_time = r
    def set_duration(self, dur):#duration
    	self.duration = dur
    def set_deadline(self, dead):#deadline
    	self.deadline = dead




if __name__ == '__main__':
    main()
    
    
    
