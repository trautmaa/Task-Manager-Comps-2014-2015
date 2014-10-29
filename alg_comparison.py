# Comps 2014
# Larkin Flodin, Avery Johnson, Maraki Keteman, 
# Abby Lewis, Will Schifeling, and  Alex Trautman

from helper_functions import *
from greedy_by_order import run_greedy_by_order
from greedy_by_present_choice import run_greedy_by_present_choice
from brute_force import run_brute_force_alg
from write_to_csv import write_n_tasks

file_name = "test.csv"

'''
Prints the total number of tasks the algorithm with a particular name
has scheduled, as well as the percentage of tasks it has scheduled.
'''
def print_alg_results(alg_name, total_tasks, tasks_completed):
	print alg_name, "has scheduled", tasks_completed, "out of", \
		total_tasks, "or", \
		(100.0 * tasks_completed / total_tasks), \
		"percent of possible tasks."

'''
Loops forever, repeatedly generating new inputs for the problem,
solving them with all algorithms, and periodically printing
updates on the aggregate numbers solved by each algorithm.
'''
def comparison_loop():
	inputs_seen = 0
	total_tasks_seen = 0
	tasks_completed_brute = 0
	tasks_completed_order_deadline = 0
	tasks_completed_order_release = 0
	tasks_completed_choice_starting = 0
	tasks_completed_choice_completion = 0
	while True:
		inputs_seen += 1
		total_tasks_seen = inputs_seen * 10
		write_n_tasks(10, file_name)
		tasks_completed_brute += len(run_brute_force_alg(file_name))
		tasks_completed_order_release += len(run_greedy_by_order(file_name, order_by_release))
		tasks_completed_order_deadline += len(run_greedy_by_order(file_name, order_by_deadline))
		tasks_completed_choice_starting += len(run_greedy_by_present_choice(file_name, order_by_starting_time))
		tasks_completed_choice_completion += len(run_greedy_by_present_choice(file_name, order_by_ending_time))
		print inputs_seen, "inputs seen total."
		print_alg_results(
			"Brute force", total_tasks_seen, tasks_completed_brute)
		print_alg_results(
			"Greedy by release date", total_tasks_seen, tasks_completed_order_release)
		print_alg_results(
			"Greedy by deadline", total_tasks_seen, tasks_completed_order_deadline)
		print_alg_results(
			"Greedy by starting time", total_tasks_seen, tasks_completed_choice_starting)
		print_alg_results(
			"Greedy by finish time", total_tasks_seen, tasks_completed_choice_completion)

def main():
	comparison_loop()


if __name__ == '__main__':
	main()
