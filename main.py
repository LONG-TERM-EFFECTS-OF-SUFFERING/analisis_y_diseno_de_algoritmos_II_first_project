from typing import List

from algorithms.brute_force import brute_force
from algorithms.dynamic import dynamic, get_solution_value
from algorithms.greedy import greedy_absolute_reduction, greedy_moderation_by_discrepancy_rigidity, greedy_moderation_efficiency
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


if __name__ == "__main__":
	path = "BateriaPruebas/Prueba2.txt"

	social_network = load_social_network_from_txt(path)
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
