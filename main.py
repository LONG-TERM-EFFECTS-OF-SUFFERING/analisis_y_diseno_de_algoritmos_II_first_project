from algorithms.brute_force import brute_force
from classes.agent_group import AgentGroup, create_agent_group
from classes.social_network import SocialNetwork, apply_strategy


def load_social_network(path: str) -> SocialNetwork:
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
			n_i = int(line[0])
			o_i1 = int(line[1])
			o_i2 = int(line[2])
			r_i = float(line[3])

			agent_group = create_agent_group(n_i, o_i1, o_i2, r_i)
			agent_groups.append(agent_group)
		else:
			raise ValueError(f"Error: line {i} does not contain exactly 4 elements")

	return SocialNetwork(n, agent_groups, r_max)


if __name__ == "__main__":
	path = "input.txt"
	social_network = load_social_network(path)
	best_social_network, best_strategy, required_effort = brute_force(social_network)

	print("Original network:", social_network)
	print("Best social network:", best_social_network)
	print("Best strategy:", best_strategy)
	print("Required effort:", required_effort)
