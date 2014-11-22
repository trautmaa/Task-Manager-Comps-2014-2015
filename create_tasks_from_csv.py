# Comps 2014
# Larkin Flodin, Avery Johnson, Maraki Ketema, 
# Abby Lewis, Will Schifeling, and  Alex Trautman

import csv
import re
import Objects

'''
Given a csv file, this function will call the read_in_task
function to retrieve the tasks and with those will call 
make_objects that returns a list of task objects, which
is then returned.
'''
def get_task_list(csv_file):
    tasks_from_csv = read_in_task(csv_file)
    task_list = make_objects(tasks_from_csv)
    return task_list

'''
Given a csv file, it will read a row from the csv and 
turn that into a list of a task's features. Each task 
will be appended to the tasks list and finally the 
tasks list will be returned.
'''
def read_in_task(csv_file):
    tasks = []
    with open(csv_file, 'rU') as f:
        reader = csv.reader(f, delimiter = ",")
        for row in reader:
            tasks.append(row)
    return tasks[1:] # tasks[0] is the list of names of the features.

    

'''
A function that returns a list of task objects.
It takes a list of tasks in list form, and converts
them to objects and adds them to the task_list.
'''
def make_objects(attribute_list):
    task_list = []
    for i in range(len(attribute_list)):
        newobject = Objects.Task(i)
        task_list.append(newobject)
        # task_list[i][j] is xcoord, ycoord, release time, duration, deadline, priority, required
        for j in range(len(attribute_list[i])): 
            if (j == 0): #x coordinate value
                task_list[i].setX(attribute_list[i][0])
            
            if (j == 1): #y coordinate value
                task_list[i].setY(attribute_list[i][1])
                
            if (j == 2): #release time
                task_list[i].set_release_time(attribute_list[i][2])
                
            if (j == 3): #duration
                task_list[i].set_duration(attribute_list[i][3])
                
            if (j == 4): #deadline
                task_list[i].set_deadline(attribute_list[i][4])
            
            if (j == 5): #priority
                task_list[i].set_priority(attribute_list[i][5])
                
            if (j == 6): #required
                task_list[i].set_required(attribute_list[i][6])
            
            if (j == 7): #time windows
                task_list[i].set_time_windows(getTimeWindows(attribute_list[i][7]))
                
            # With added features, we must add statements here.
    return task_list

def getTimeWindows(timeWindowString):
    timeWindows = []
    result = re.split("\],\[", timeWindowString)
    for i in result:
        daySplit = re.split(",", i)
        day = []
        t = 0
        while t < len(daySplit):
            a = re.search("([0-9]+)", daySplit[t])
            t+=1
            b = re.search("([0-9]+)", daySplit[t])
            t+=1
            day.append((int(a.group()),int(b.group())))
        timeWindows.append(day)
            
    
    return timeWindows







def main():
    get_task_list("test.csv")

if __name__ == "__main__":
    main()     
    



