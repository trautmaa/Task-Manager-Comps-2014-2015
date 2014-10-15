# Comps 2014
# Larkin Flodin, Avery Johnson, Maraki Keteman, 
# Abby Lewis, Will Schifeling, and  Alex Trauman
import csv


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



            
    
