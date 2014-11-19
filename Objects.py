# Comps 2014
# Larkin Flodin, Avery Johnson, Maraki Ketema, 
# Abby Lewis, Will Schifeling, and  Alex Trautman


'''
A class to represent how many different locations there are for each task
'''
class Category:
    def __init__(self):
        self.category_list = []
        
    def __init__(self, task_list):
        self.category_list = task_list
            
    def add_to_list(self, task):
        self.category_list.append(task)

'''
Task is a class that contains seven variables:
task.x is the task's x coordinate.
task.y is the task's y coordinate.
task.release_time is the task's release time.
task.duration is the task's duration.
task.deadline is the task's deadline.
task.priority is the task's priority
task.required represents whether the task is required
'''    
class Task:
    def __init__(self, id):
        self.id = id
        pass
    
    def setX(self, x):
        self.x = int(x)

    def setY(self, y):
        self.y = int(y)
        
    def set_release_time(self, r):
        self.release_time = int(r)

    def set_duration(self, dur):
        self.duration = int(dur)

    def set_deadline(self, dead):
        self.deadline = int(dead)
        
    def set_priority(self, priority):
        self.priority = int(priority)
        
    def set_required(self, required):
        self.required = required
        
    #This is a list of days. Each day has a list of time windows
    def set_time_windows(self, time_windows):
        self.time_windows = time_windows
        
    def getProfit (self):
        return self.priority

    def __str__(self):
        string_representation = "(ID: " + str(self.id) + ", Location: (" + str(self.x) + " " \
        + str(self.y) + "), Release Time: " + str(self.release_time) \
        + ", Duration: " + str(self.duration) + ", Deadline: " \
        + str(self.deadline) + ", Priority: " + str(self.priority) + ", Required: " + str(self.required) + ")"
        return string_representation
    
    def __eq__(self, other):
        return self.id == other.id
    
    def __ne__(self, other):
        return self.id != other.id
    
'''
 A class to hold the schedule for an individual day
'''   
class Route:
    def __init__(self):
        self.task_list = []
        self.ending_times = []
        
    def set_task_list(self, task_list, ending_times):
        self.task_list = task_list
        self.ending_times = ending_times
    
    def append(self, task, ending_time):
        self.task_list.append(task)
        self.ending_times.append(ending_time)
    
    def add_to_task_list(self, task, ending_time, index):
        self.task_list[index] = task
        self.ending_times[index] = ending_time
    
    def get_task(self, index):
        return self.task_list[index]
    
    def get_ending_time(self, index):
        return self.ending_times[index]
    
    def remove_segment(self, startIndex, endIndex):
        self.task_list = self.task_list[:startIndex] + self.task_list[endIndex:]
        self.ending_times = self.ending_times[:startIndex] + self.ending_times[endIndex:]
    
    def __len__(self):
        return len(self.task_list)
    
    def __str__(self):
        result = "["
        for task in range(len(self.task_list)):
            result = str(result) + "(task: " + str(self.task_list[task]) + ", ending at: " + str(self.ending_times[task]) + ")\n"
        return result + "]"

'''
 A class to hold the routes for an individual day, representing the entire schedule
'''  
class Schedule:
    def __init__(self):
        self.route_list = []
        
    def append(self, route):
        self.route_list.append(route)
    
    def get_route(self, index):
        return self.route_list[index]
    
    def __len__(self):
        return len(self.route_list)
        
    
    
