from itertools import product
from typing import List

from classes.social_network import (SocialNetwork, apply_strategy,
                                    calculate_effort,
                                    calculate_internal_conflict,
                                    calculate_max_effort)


def brute_force(social_network: SocialNetwork) -> List[int]:
	"""
	Finds the optimal strategy to minimize internal conflict in a social network
	using brute force approach by evaluating all possible combinations.

	This function exhaustively checks all possible agent moderation strategies and
	selects the one that minimizes internal conflict while staying within the
	maximum allowed effort (R_max).

	Parameters
	----------
	social_network : SocialNetwork
		The social network to optimize.

	Returns
	-------
	List[int]
		The best strategy as a list of integers where each value represents
			the number of agents to moderate in the corresponding group.

	Notes
	-----
	- Time complexity is exponential O(∏(n_i + 1)) where n_i is the number of
		agents in each group, as it evaluates all possible combinations.
	- If no valid strategy is found (all require more effort than R_max),
		the function will return None values.
	- This implementation is suitable only for small networks due to its
		exponential time complexity.
	"""
	# Check if the effort required to moderate the entire social network is less than or equal to the max effort allowed.
	# If we have enough effort to moderate the entire social network, the optimal strategy is to moderate all agents in all groups.
	if calculate_max_effort(social_network) <= social_network.r_max:
		return [group.n for group in social_network.groups]

	groups = social_network.groups
	max_effort = social_network.r_max
	ranges = [range(0, group.n + 1) for group in groups]
	cartesian_product = product(*ranges)

	best_strategy = None
	best_IC = float("inf")

	for strategy in cartesian_product:
		effort = calculate_effort(social_network, strategy)

		if effort <= max_effort:
			new_social_network = apply_strategy(social_network, strategy)
			conflict = calculate_internal_conflict(new_social_network)
			if conflict < best_IC:
				best_strategy = strategy
				best_IC = conflict

	return best_strategy
