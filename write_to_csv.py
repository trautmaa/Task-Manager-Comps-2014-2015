# Comps 2014
# Larkin Flodin, Avery Johnson, Maraki Keteman, 
# Abby Lewis, Will Schifeling, and  Alex Trautman

import csv
import random

task_features = ['x_coord', 'y_coord', 'release_time', 'duration', 'deadline']

'''
Generates a task as a list so that it may be written to a csv file.
Each parameter is the range for that feature... Ie the task's x coordinate
will randomly be between 0 and x_constraint. The task that is returned is:
[x_coord, y_coord, release_time, duration, deadline] (where deadline is
release time + duration + some random extra_time)
'''
def generate_task(x_constraint, y_constraint, release_time, duration, extra_time):
    features = [x_constraint, y_constraint, release_time, duration, extra_time]
    task = []
    for feature in features:
        task.append(random.randint(0, feature))
    task[4] = task[2] + task[3] + task[4] # deadline = release_time + duration + extra time
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
            writer.writerow(generate_task(1000, 1000, 1000, 0, 1000))
    return csv_file

def main():
    write_n_tasks(10, "test.csv")


if __name__ == '__main__':
    main()