# Comps 2014
# Larkin Flodin, Avery Johnson, Maraki Keteman, 
# Abby Lewis, Will Schifeling, and  Alex Trauman
import csv
import random
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


def write_n_tasks(n, csv_file):
    with open(csv_file, 'wb') as f:
        writer = csv.writer(f)
        writer.writerow(task_features)
        for i in range(n):
            writer.writerow(generate_task(5, 5, 10, 2, 2))
    return csv_file

