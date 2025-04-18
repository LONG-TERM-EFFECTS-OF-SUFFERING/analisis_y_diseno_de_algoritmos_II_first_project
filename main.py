import os
from typing import List
import time

from tabulate import tabulate  # Library for displaying formatted tables

from algorithms.brute_force import brute_force
from algorithms.dynamic import dynamic_bottom_up, dynamic_top_down
from algorithms.greedy import (greedy_discrepancy_rigidity_heap,
                               greedy_moderation_with_radix_sort)
from classes.agent_group import create_agent_group
from classes.social_network import (SocialNetwork, apply_strategy,
                                    calculate_effort,
                                    calculate_internal_conflict)


def load_social_network_from_txt(file_path: str) -> SocialNetwork:
	"""
	Loads a social network from a TXT file following the specified format.

	Parameters
	----------
	file_path : str
		The path to the TXT file containing the social network data.

	Returns
	-------
	SocialNetwork
		A SocialNetwork object containing the agent groups and the maximum effort available.

	Raises
	------
	ValueError
		If the file format is incorrect or contains invalid values.
	"""
	with open(file_path, "r") as file:
		lines = file.readlines()

	# Extract the number of agent groups
	n_groups = int(lines[0].strip())

	agent_groups = []

	# Extract each agent group's data
	for i in range(1, n_groups + 1):
		parts = lines[i].strip().split(",")
		if len(parts) != 4:
			raise ValueError(f"Error: invalid format on line {i + 1}: {lines[i]}")

		n, o_1, o_2, r = int(parts[0]), int(parts[1]), int(parts[2]), float(parts[3])
		agent_groups.append(create_agent_group(n, o_1, o_2, r))

	# Extract the maximum effort available
	r_max = int(lines[n_groups + 1].strip())

	return SocialNetwork(agent_groups, r_max)


def write_output(path: str, social_network: SocialNetwork, strategy: List[int]) -> None:
	"""
	Writes the results of applying a moderation strategy to a social network to a file.

	This function calculates the effort required to implement the strategy,
	applies the strategy to create a modified network, calculates the resulting
	internal conflict, and writes these results to a text file.

	Parameters
	----------
	path : str
		The file path where the output should be written.

	social_network : SocialNetwork
		The original social network to which the strategy is applied.

	strategy : List[int]
		The strategy to apply, where each value represents the number of agents
		to moderate from the corresponding group.

	Returns
	-------
	None
		The function writes the results to a file but does not return a value.

	Notes
	-----
	The output file format is:
	- Line 1: the internal conflict value after applying the strategy.
	- Line 2: the effort required to implement the strategy.
	- Line 3 and beyond: each value of the strategy on a separate line.
	"""
	effort = calculate_effort(social_network, strategy)
	modified_network = apply_strategy(social_network, strategy)
	IC = calculate_internal_conflict(modified_network)

	with open(path, "w") as file:
		file.write(f"{IC}\n")
		file.write(f"{effort}\n")
		file.write('\n'.join(map(str, strategy)))


def run_tests(directory: str, num_tests: int, strategies) -> None:
	"""
	Executes a series of tests on social network moderation strategies and compares their performance.

	Parameters
	----------
	directory : str
		The folder where the test files are located.
	num_tests : int
		The number of test files (assumes they are named test_01.txt, test_02.txt, ...).
	"""
	results = []

	for i in range(1, num_tests + 1):
		test_case_name = f"test_{i:02}"  # Format test case name with leading zero if i < 10
		filename = os.path.join(directory, f"{test_case_name}.txt")

		if not os.path.exists(filename):
			print(f"Warning: {filename} not found. Skipping...")
			continue

		# Load the social network from the file
		social_network = load_social_network_from_txt(filename)
		max_effort = social_network.r_max

		partial_results = [test_case_name]
		for strategy_name, strategy_func in strategies.items():
			start_time = time.perf_counter()
			solution = strategy_func(social_network)
			end_time = time.perf_counter()
			execution_time = end_time - start_time
			modified_network = apply_strategy(social_network, solution)
			final_conflict = calculate_internal_conflict(modified_network)

			# Save the results
			#partial_results.append(strategy_name)
			partial_results.append(final_conflict)
			#partial_results.append(execution_time)

		# Save the results
		#if final_conflict > 0:
		results.append(partial_results)

	# Display the results in a tabulate table
	headers = ["Test Case", "Dynamic", "With heap", "With radix sort"]
	#headers = ["Test Case", "Discrepancy/rigidity time", "With heap time", "With radix sort time"]
	#headers = ["Test Case", "With heap time", "With radix sort time"]
	print(tabulate(results, headers=headers, tablefmt="plain"))


if __name__ == "__main__":
	strategies = {
	"Dynamic": dynamic_bottom_up,
    "Heap-Based Greedy": greedy_discrepancy_rigidity_heap,
    "Radix Sort Greedy": greedy_moderation_with_radix_sort,
	}
	run_tests("tests", 30, strategies)
