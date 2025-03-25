from typing import List

from algorithms.brute_force import brute_force
from algorithms.dynamic import dynamic, get_solution_value
from algorithms.greedy import greedy_absolute_reduction, greedy_moderation_by_discrepancy_rigidity, greedy_moderation_efficiency
from classes.agent_group import create_agent_group
from classes.social_network import (SocialNetwork, apply_strategy,
                                    calculate_effort,
                                    calculate_internal_conflict)


def read_input(path: str) -> SocialNetwork:
	with open(path, "r") as file:
		content = file.readlines()

	first_line = content[0].strip().split()
	n = int(first_line[0])
	r_max = int(first_line[1])

	agent_groups = []

	if n > len(content) - 1:
		raise ValueError("Error: The number of agent groups exceeds the number of lines in the file")

	if n < len(content) - 1:
		raise ValueError("Error: The number of agent groups is less than the number of lines in the file")

	for i in range(1, n + 1):
		line = content[i].strip().split()

		if len(line) == 4:
			n = int(line[0])
			o_1 = int(line[1])
			o_2 = int(line[2])
			r_i = float(line[3])

			agent_group = create_agent_group(n, o_1, o_2, r_i)
			agent_groups.append(agent_group)
		else:
			raise ValueError(f"Error: line {i} does not contain exactly 4 elements")

	return SocialNetwork(agent_groups, r_max)

def write_ouput(path: str, social_network: SocialNetwork, strategy: List[int]) -> None:
	effort = calculate_effort(social_network, strategy)
	modified_network = apply_strategy(social_network, strategy)
	IC = calculate_internal_conflict(modified_network)

	with open(path, "w") as file:
		file.write(f"{IC}\n")
		file.write(f"{effort}\n")
		file.write('\n'.join(map(str, strategy)))


if __name__ == "__main__":
	path = "prueba4.txt"
	social_network = read_input(path)
	strategy_1 = brute_force(social_network)
	network_1 = apply_strategy(social_network, strategy_1)
	strategy_2  = get_solution_value(social_network)
	network_2 = apply_strategy(social_network, strategy_2)
	strategy_3 = greedy_absolute_reduction(social_network)
	network_3 = apply_strategy(social_network, strategy_3)
	strategy_4 = greedy_moderation_efficiency(social_network)
	network_4 = apply_strategy(social_network, strategy_4)
	strategy_5 = greedy_moderation_by_discrepancy_rigidity(social_network)
	network_5 = apply_strategy(social_network, strategy_5)

	print(social_network)

	print("Brute force strategy:")
	print("Strategy:", strategy_1)
	print(network_1)

	print("\nDynamic programming strategy:")
	print("Strategy:", strategy_2)
	print(network_2)

	print("\nGreedy absolute reduction strategy:")
	print("Strategy:", strategy_3)
	print(network_3)

	print("\nGreedy moderation efficiency strategy:")
	print("Strategy:", strategy_4)
	print(network_4)

	print("\nGreedy moderation by discrepancy and rigidity strategy:")
	print("Strategy:", strategy_5)
	print(network_5)

	# write_ouput("output.txt", social_network, brute_force_strategy)
