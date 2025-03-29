from typing import List
import os
from tabulate import tabulate  # Librería para mostrar tablas bonitas

from algorithms.brute_force import brute_force
from algorithms.dynamic import dynamic
from algorithms.greedy import greedy_absolute_reduction, greedy_absolute_reduction_heap, greedy_moderation_by_discrepancy_rigidity, greedy_moderation_with_radix_sort
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
		parts = lines[i].strip().split(',')
		if len(parts) != 4:
			raise ValueError(f"Invalid format on line {i + 1}: {lines[i]}")

		n, o_1, o_2, r = int(parts[0]), int(parts[1]), int(parts[2]), float(parts[3])
		agent_groups.append(create_agent_group(n, o_1, o_2, r))

	# Extract the maximum effort available
	r_max = int(lines[n_groups + 1].strip())

	return SocialNetwork(agent_groups, r_max)


def write_ouput(path: str, social_network: SocialNetwork, strategy: List[int]) -> None:
	effort = calculate_effort(social_network, strategy)
	modified_network = apply_strategy(social_network, strategy)
	IC = calculate_internal_conflict(modified_network)

	with open(path, "w") as file:
		file.write(f"{IC}\n")
		file.write(f"{effort}\n")
		file.write('\n'.join(map(str, strategy)))


def run_tests(directory: str, num_tests: int):
	"""
	Runs all test cases from a given directory and summarizes the results in a table.

	Parameters
	----------
	directory : str
		The folder where the test files are located.
	num_tests : int
		The number of test files (assumes they are named Prueba1.txt, Prueba2.txt, ...).
	"""
	results = []

	for i in range(1, num_tests + 1):
		filename = os.path.join(directory, f"Prueba{i}.txt")

		if not os.path.exists(filename):
			print(f"Warning: {filename} not found. Skipping...")
			continue

		# Cargar la red social desde el archivo
		social_network = load_social_network_from_txt(filename)
		#max_effort = social_network.r_max

		# Aplicar la estrategia voraz basada en reducción absoluta
		strategy_absolute = greedy_moderation_with_radix_sort(social_network)
		#required_effort_absolute = calculate_effort(social_network, strategy_absolute)
		modified_network_absolute = apply_strategy(social_network, strategy_absolute)
		conflict_absolute = calculate_internal_conflict(modified_network_absolute)

		# Aplicar la estrategia voraz basada en reducción absoluta * número de agentes
		strategy_discrepancy_rigidity = greedy_moderation_by_discrepancy_rigidity(social_network)
		#required_effort_discrepancy_rigidity = calculate_effort(social_network, strategy_discrepancy_rigidity)
		modified_network_discrepancy_rigidity = apply_strategy(social_network, strategy_discrepancy_rigidity)
		conflict_discrepancy_rigidity = calculate_internal_conflict(modified_network_discrepancy_rigidity)

		# Aplicar la estrategia dinámica para obtener el valor óptimo de la solución
		strategy_dynamic = dynamic(social_network)
		#required_effort_dynamic = calculate_effort(social_network, strategy_dynamic)
		modified_network_dynamic = apply_strategy(social_network, strategy_dynamic)
		conflict_dynamic = calculate_internal_conflict(modified_network_dynamic)

		# Guardar los resultados
		results.append([f"Prueba{i}", conflict_absolute, conflict_discrepancy_rigidity, conflict_dynamic])

	# Mostrar los resultados en una tabla
	#headers = ["Test Case", "Max effort", "Conflict (Absolute Reduction)", "Require effort", "Conflict (Optimal)", "Required effort"]
	headers = ["Test Case", "Conflict (Absolute Reduction)", "Conflict (Discrepancy/rigidity)", "Conflict (Optimal)"]
	print(tabulate(results, headers=headers, tablefmt="plain"))



if __name__ == "__main__":

	# # write_ouput("output.txt", social_network, brute_force_strategy)

	# Ejecutar la batería de pruebas
	run_tests("BateriaPruebas", 30)
