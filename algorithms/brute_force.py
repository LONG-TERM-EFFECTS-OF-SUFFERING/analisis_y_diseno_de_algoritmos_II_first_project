from itertools import product
from typing import List, Tuple

from classes.social_network import (SocialNetwork, apply_strategy,
                                    calculate_effort,
                                    calculate_internal_conflict)


def brute_force(social_network: SocialNetwork) -> Tuple[SocialNetwork, List[int]]: # Tuple[SocialNetwork, strategy]
	"""
	Finds the optimal strategy to minimize internal conflict in a social network
	using brute force approach by evaluating all possible combinations.

	This function exhaustively checks all possible agent removal strategies and
	selects the one that minimizes internal conflict while staying within the
	maximum allowed effort (R_max).

	Parameters
	----------
	social_network : SocialNetwork

	Returns
	-------
	Tuple[SocialNetwork, List[int], float]
		A tuple containing:
		- The resulting social network after applying the best strategy
		- The best strategy as a list of integers where each value represents
			the number of agents to remove from the corresponding group
		- The effort required to implement the best strategy

	Notes
	-----
	- Time complexity is exponential O(∏(n_i+1)) where n_i is the number of
		agents in each group, as it evaluates all possible combinations.
	- If no valid strategy is found (all require more effort than R_max),
		the function will return None values.
	- This implementation is suitable only for small networks due to its
		exponential time complexity.
	"""
	n = social_network.n
	agent_groups = social_network.groups
	max_effort = social_network.r_max
	ranges = [range(0, group.n + 1) for group in agent_groups]
	cartesian_product = product(*ranges)

	best_social_network = None
	best_strategy = None
	best_IC = float("inf")
	best_effort = float("inf")

	for strategy in cartesian_product:
		effort = calculate_effort(social_network, strategy)

		if effort <= max_effort:
			new_social_network = apply_strategy(social_network, strategy)
			conflict = calculate_internal_conflict(new_social_network)
			if conflict < best_IC:
				best_social_network = new_social_network
				best_strategy = strategy
				best_IC = conflict
				best_effort = effort

	return (best_social_network, best_strategy, best_effort)
