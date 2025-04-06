import os
from typing import List

from tabulate import tabulate  # Library for displaying formatted tables

from algorithms.brute_force import brute_force
from algorithms.dynamic import dynamic_bottom_up, dynamic_top_down
from algorithms.greedy import (greedy_absolute_reduction,
                               greedy_moderation_by_discrepancy_rigidity,
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

def run_tests(directory: str, num_tests: int) -> None:
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
		# max_effort = social_network.r_max

		# Applying absolute reduction greedy strategy
		strategy_absolute = greedy_moderation_with_radix_sort(social_network)
		# required_effort_absolute = calculate_effort(social_network, strategy_absolute)
		modified_network_absolute = apply_strategy(social_network, strategy_absolute)
		conflict_absolute = calculate_internal_conflict(modified_network_absolute)

		# Apply the greedy strategy based on absolute reduction * number of agents
		strategy_discrepancy_rigidity = greedy_moderation_by_discrepancy_rigidity(social_network)
		# required_effort_discrepancy_rigidity = calculate_effort(social_network, strategy_discrepancy_rigidity)
		modified_network_discrepancy_rigidity = apply_strategy(social_network, strategy_discrepancy_rigidity)
		conflict_discrepancy_rigidity = calculate_internal_conflict(modified_network_discrepancy_rigidity)

		# Apply the dynamic strategy to obtain the optimal solution value
		strategy_dynamic = dynamic_bottom_up(social_network)
		# required_effort_dynamic = calculate_effort(social_network, strategy_dynamic)
		modified_network_dynamic = apply_strategy(social_network, strategy_dynamic)
		conflict_dynamic = calculate_internal_conflict(modified_network_dynamic)

		# Save the results
		results.append([test_case_name, conflict_absolute, conflict_discrepancy_rigidity, conflict_dynamic])

	# Display the results in a tabulate table
	headers = ["Test Case", "Conflict (Absolute Reduction)", "Conflict (Discrepancy/rigidity)", "Conflict (Optimal)"]
	print(tabulate(results, headers=headers, tablefmt="plain"))


if __name__ == "__main__":
	run_tests("tests", 2)
