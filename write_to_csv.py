# Comps 2014
# Larkin Flodin, Avery Johnson, Maraki Ketema, 
# Abby Lewis, Will Schifeling, and  Alex Trautman
import csv
from random import randint

task_features = ['x_coord', 'y_coord', 'release_time', 'duration', 'deadline']

'''
Generates a task as a list so that it may be written to a csv file.
Each parameter is the maximum possible value for that feature. The task
that is returned is: [x_coord, y_coord, release_time, duration, deadline].
It is required that deadline
is later or the same as the release time plus the duration of the task.
'''
def generate_task(x_constraint, y_constraint, max_release_time, max_duration, max_deadline):
    assert (max_deadline >= max_release_time + max_duration)
    task = []
    for feature in [x_constraint, y_constraint, max_release_time]:
        task.append(randint(0, feature))
    task.append(randint(0, max_duration)) # task duration
    task.append(randint(max_release_time + task[3], max_deadline)) # task deadline
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
    write_n_tasks(15, "test.csv")


if __name__ == '__main__':
    main()