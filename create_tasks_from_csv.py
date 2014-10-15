# Comps 2014
# Larkin Flodin, Avery Johnson, Maraki Keteman, 
# Abby Lewis, Will Schifeling, and  Alex Trauman
import csv


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


def get_object_list(csv_file):
    tasks_from_csv = read_in_task(csv_file)
    object_list = make_objects(tasks_from_csv)
    return object_list

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






            
    
