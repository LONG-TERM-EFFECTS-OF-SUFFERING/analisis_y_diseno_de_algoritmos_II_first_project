import math
from typing import List

import numpy as np
from numpy.typing import NDArray

from classes.agent_group import AgentGroup
from classes.social_network import (SocialNetwork, apply_strategy,
                                    calculate_effort,
                                    calculate_internal_conflict,
                                    calculate_max_effort)


def get_solution_value(social_network: SocialNetwork) -> float:
	"""
	Calculates the minimum possible internal conflict in a social network using recursion.

	Parameters
	----------
	social_network : SocialNetwork
		The social network to optimize.

	Returns
	-------
	float
		The minimum internal conflict value achievable within the effort constraints.

	Notes
	-----
	- Time complexity: O(n * R_max * max(n_i)) where n is the number of groups, R_max is
	the maximum effort, and max(n_i) is the maximum number of agents in any group.
	"""
	groups = social_network.groups
	n = len(groups)
	r_max = social_network.r_max

	def IC(i: int, r: float):
		if i == 0:
			return 0
		else: # i > 0
			group = groups[i - 1]
			n = group.n
			o_1 = group.o_1
			o_2 = group.o_2
			r_i = group.r

			conflict_per_agent = (o_1 - o_2) ** 2
			effort_per_agent = abs(o_1 - o_2) * r_i

			min_conflict = float("inf")

			for k in range(n + 1):
				required_effort = math.ceil(effort_per_agent * k)

				if required_effort <= r:
					remaining_conflict = (n - k) * conflict_per_agent

					value = IC(i - 1, r - required_effort) + remaining_conflict

					if value < min_conflict:
						min_conflict = value

			return min_conflict

	min_conflict = IC(n, r_max)

	return min_conflict


def dynamic_bottom_up(social_network: SocialNetwork) -> List[int]:
	"""
	Finds the optimal strategy to minimize internal conflict in a social network
	using dynamic programming.

	This function efficiently finds the strategy that minimizes internal conflict
	while staying within the maximum allowed effort (R_max).

	Parameters
	----------
	social_network : SocialNetwork
		The social network to optimize.

	Returns
	-------
	List[int]
		The best strategy as a list of integers where each value represents
			the number of agents to remove from the corresponding group.

	Notes
	-----
	- Time complexity: O(n * R_max * max(n_i)) where n is the number of groups, R_max is
	   the maximum effort, and max(n_i) is the maximum number of agents in any group.
	- Space complexity: O(n * R_max).
	"""
	groups = social_network.groups
	n = len(groups)
	r_max = social_network.r_max

	# Check if the effort required to moderate the entire social network is less than or equal to the
	# max effort allowed. If we have enough effort to moderate the entire social network, the optimal
	# strategy is to moderate all agents in all groups
	if calculate_max_effort(social_network) <= r_max:
		return [group.n for group in groups]

	# Create DP matrices using NumPy for better performance
	# storage[i][r] = minimum conflict achievable for first i groups with r effort
	storage = np.full((n + 1, r_max + 1), np.inf)
	# decisions[i][r] = how many agents to moderate in group i to achieve storage[i][r]
	decisions = np.zeros((n + 1, r_max + 1), dtype=int)

	# Base case: no groups, no conflict
	storage[0, :] = 0

	# Bottom-up DP approach
	for i in range(1, n + 1):
		group = groups[i - 1]
		n_i = group.n
		o_1 = group.o_1
		o_2 = group.o_2
		r = group.r

		conflict_per_agent = (o_1 - o_2) ** 2
		effort_per_agent = abs(o_1 - o_2) * r

		for r in range(r_max + 1):
			# Try moderating k agents from current group
			for k in range(n_i + 1):
				required_effort = math.ceil(effort_per_agent * k)

				if required_effort <= r:
					# Calculate remaining conflict after moderating k agents
					remaining_conflict = (n_i - k) * conflict_per_agent

					# Total conflict = optimal conflict for previous groups + remaining conflict
					total_conflict = storage[i - 1, r - required_effort] + remaining_conflict

					if total_conflict < storage[i, r]:
						storage[i, r] = total_conflict
						decisions[i, r] = k

	# Reconstruct the optimal strategy
	optimal_strategy = [0] * n
	remaining_effort = r_max

	for i in range(n, 0, -1):
		group = groups[i - 1]
		k = decisions[i, remaining_effort]
		optimal_strategy[i - 1] = k

		effort_per_agent = abs(group.o_1 - group.o_2) * group.r
		required_effort = math.ceil(effort_per_agent * k)
		remaining_effort -= required_effort

	return optimal_strategy

UNKNOWN = -1

def dynamic_top_down_helper(groups: List[AgentGroup], i: int, j: int, storage: NDArray[np.float64],
							decisions: NDArray[np.int_]) -> float:
	if (storage[i, j] == UNKNOWN):
		group = groups[i - 1]
		n = group.n
		o_1 = group.o_1
		o_2 = group.o_2
		r = group.r

		conflict_per_agent = (o_1 - o_2) ** 2
		effort_per_agent = abs(o_1 - o_2) * r

		min_conflict = float("inf")

		for k in range(n + 1):
			required_effort = math.ceil(effort_per_agent * k)

			if required_effort <= j:
				remaining_conflict = (n - k) * conflict_per_agent

				value = dynamic_top_down_helper(groups, i - 1, j - required_effort, storage, decisions) \
							+ remaining_conflict

				if value < min_conflict:
					min_conflict = value
					decisions[i, j] = k

		storage[i, j] = min_conflict

		return storage[i, j]
	else:
		return storage[i, j]

def dynamic_top_down(social_network: SocialNetwork) -> List[int]:
	groups = social_network.groups
	n = len(groups)
	r_max = social_network.r_max

	# Check if the effort required to moderate the entire social network is less than or equal to the
	# max effort allowed. If we have enough effort to moderate the entire social network, the optimal
	# strategy is to moderate all agents in all groups
	# if calculate_max_effort(social_network) <= r_max:
	# 	return [group.n for group in groups]

	# Create DP matrices using NumPy for better performance
	# storage[i][r] = minimum conflict achievable for first i groups with r effort
	storage = np.full((n + 1, r_max + 1), UNKNOWN)
	decisions = np.zeros((n + 1, r_max + 1), dtype=int)

	# Base case: no groups, no conflict
	storage[0, :] = 0

	dynamic_top_down_helper(groups, n, r_max, storage, decisions)

	# Reconstruct the optimal strategy
	optimal_strategy = [0] * n
	remaining_effort = r_max

	for i in range(n, 0, -1):
		group = groups[i - 1]
		k = decisions[i, remaining_effort]
		optimal_strategy[i - 1] = k

		effort_per_agent = abs(group.o_1 - group.o_2) * group.r
		required_effort = math.ceil(effort_per_agent * k)
		remaining_effort -= required_effort

	return optimal_strategy
