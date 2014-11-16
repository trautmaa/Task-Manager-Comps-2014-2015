# Comps 2014
# Larkin Flodin, Avery Johnson, Maraki Ketema, 
# Abby Lewis, Will Schifeling, and  Alex Trautman
import csv
from random import randint

task_features = ['x_coord', 'y_coord', 'release_time', 'duration', 'deadline', 'name']

task_names = ['Grocery shopping', 'Get gas', 'Mow the lawn', 'Shovel the driveway', 'Go to laundromat', 'Go to curling practice', 'Meet with comps group', 'Apply to jobs', 'Make travel plans', 'Go to work', 'Take garbage out','Set the table', 'Clear the table', 'Clean room with direction' 'Put away groceries', 'Clean the bathroom with direction', 'Clean the kitchen', 'Dust', 'Vacuum', 'Mow lawn', 'Feed pets', 'Water plants', 'Put laundry in hamper', 'Help with laundry and eventually start doing own laundry', 'Help make dinner/make small meals on own', 'Help wash the car/wash car', 'Make bed', 'Help with yard work', 'Shovel snow', 'Wash dishes/load or empty dishwasher']

'''
Generates a task as a list so that it may be written to a csv file.
Each parameter is the maximum possible value for that feature. The task
that is returned is: [x_coord, y_coord, release_time, duration, deadline]
(where duration is deadline - release_time). It is required that deadline
is later or the same as the release time.
'''
def generate_task(x_constraint, y_constraint, release_time, max_duration, deadline):
    assert (deadline >= release_time)
    task = []
    for feature in [x_constraint, y_constraint, release_time]:
        task.append(randint(0, feature))
    task.append(randint(0, max_duration)) # task duration
    task.append(randint(release_time + task[3], deadline)) # task deadline
    random = randint(0, len(task_names) - 1)
    task.append(task_names[random]) # task name
    task_names.remove(task_names[random])

    return task

'''
A function that will write n tasks to a csv file.  It uses
generate_task to create the task to write. Right now the
constraints for generate_task are hard coded but that can 
be changed.  The name of the csv file is returned.
'''
def write_n_tasks(n, csv_file):
    with open(csv_file, 'wb') as f:
        writer = csv.writer(f)
        writer.writerow(task_features)
        for i in range(n):
            writer.writerow(generate_task(60, 60, 480, 120, 600))
    return csv_file

def main():
    write_n_tasks(10, "test.csv")


if __name__ == '__main__':
    main()