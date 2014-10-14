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
    
    tasks = read_in_task('my.csv')

    
if __name__ == '__main__':
    main()
    
    
    
