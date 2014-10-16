# Comps 2014
# Larkin Flodin, Avery Johnson, Maraki Keteman, 
# Abby Lewis, Will Schifeling, and  Alex Trauman

import csv

'''
Task is a class that contains five variables:
task.x is the task's x coordinate.
task.y is the task's y coordinate.
task.release_time is the task's release time.
task.duration is the task's duration.
task.deadline is the task's deadline.
'''
class Task(object):
    
    def setX(self, x):
    	self.x = float(x)

    def setY(self, y):
    	self.y = float(y)

    def set_release_time(self, r):
    	self.release_time = float(r)

    def set_duration(self, dur):
    	self.duration = float(dur)

    def set_deadline(self, dead):
    	self.deadline = float(dead)


'''
Given a csv file, this function will call the read_in_task
function to retrieve the tasks and with those will call 
make_objects that returns a list of task objects, which
is then returned.
'''
def get_object_list(csv_file):
    tasks_from_csv = read_in_task(csv_file)
    object_list = make_objects(tasks_from_csv)
    return object_list

'''
Given a csv file, it will read a row from the csv and 
turn that into a list of a task's features. Each task 
will be appended to the tasks list and finally the 
tasks list will be returned.
'''
def read_in_task(csv_file):
    tasks = []
    with open(csv_file, 'rb') as f:
        reader = csv.reader(f)
        for row in reader:
            tasks.append(row)
    return tasks[1:] # tasks[0] is the list of names of the features.

    

'''
A function that returns a list of task objects.
It takes a list of tasks in list form, and converts
them to objects and adds them to the object_list.
'''
def make_objects(task_list):
    object_list = []
    for i in range(len(task_list)):
        newobject = Task()
        object_list.append(newobject)
        # task_list[i][j] is xcoord, ycoord, release time, duration, deadline
        for j in range(len(task_list[i])): 
            if (j == 0): #x coordinate value
                object_list[i].setX(task_list[i][0])
            
            if (j == 1): #y coordinate value
                object_list[i].setY(task_list[i][1])
                
            if (j == 2): #release time
                object_list[i].set_release_time(task_list[i][2])
                
            if (j == 3): #duration
                object_list[i].set_duration(task_list[i][3])
                
            if (j == 4): #deadline
                object_list[i].set_deadline(task_list[i][4])
            # With added features, we must add statements here.
    return object_list






            
    
