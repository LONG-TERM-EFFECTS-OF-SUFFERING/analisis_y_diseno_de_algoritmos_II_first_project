import heapq
import math
from typing import List
from classes.agent_group import create_agent_group
from classes.social_network import SocialNetwork, calculate_max_effort


def greedy_absolute_reduction(social_network: SocialNetwork) -> List[int]:
	"""
	Implements the greedy strategy that selects the group with the highest absolute reduction
	in internal conflict per unit of effort and moderates agents from it.

	Parameters
	----------
	social_network : SocialNetwork
		The social network on which the greedy strategy is applied.

	Returns
	-------
	List[int]
		A list where each element represents the number of agents moderated in the corresponding group.

	Notes
	-----
	- The function ensures that it never moderates more agents than those available in a group.
	- The strategy iteratively selects the best group to moderate until resources are exhausted.
	"""
	# Check if the effort required to moderate the entire social network is less than or equal to the max effort allowed.
	# If we have enough effort to moderate the entire social network, the optimal strategy is to moderate all agents in all groups.
	if calculate_max_effort(social_network) <= social_network.r_max:
		return [group.n for group in social_network.groups]

	n = len(social_network.groups)
	strategy = [0] * n  # Initialize the moderation strategy (all zeros)
	remaining_r = social_network.r_max  # Remaining effort budget
	groups = social_network.groups[:]

	while remaining_r > 0:
		best_index = -1
		best_reduction = 0
		best_effort = float('inf')

		# Find the best group to moderate based on reduction per effort
		for i, group in enumerate(groups):
			if group.n > 0:  # Only consider groups with remaining agents
				reduction_per_agent = (group.o_1 - group.o_2) ** 2
				effort_per_agent = abs(group.o_1 - group.o_2) * group.r

				if effort_per_agent <= remaining_r:
					reduction_ratio = reduction_per_agent / effort_per_agent if effort_per_agent > 0 else 0
					if reduction_ratio > best_reduction:
						best_reduction = reduction_ratio
						best_index = i
						best_effort = effort_per_agent

		# If no valid group is found, stop
		if best_index == -1:
			break

		# Determine how many agents we can moderate
		group = groups[best_index]
		max_agents_moderatable = group.n  # We can't moderate more than we have
		max_possible = remaining_r // best_effort  # Max we can afford

		agents_to_moderate = min(max_agents_moderatable, max_possible)

		if agents_to_moderate > 0:
			strategy[best_index] += agents_to_moderate
			remaining_r -= math.ceil(agents_to_moderate * best_effort) # Deduct effort spent

			# Update group information
			groups[best_index] = create_agent_group(
				group.n - agents_to_moderate,
				group.o_1,
				group.o_2,
				group.r
			)

	return strategy


def greedy_moderation_by_discrepancy_rigidity(social_network: SocialNetwork) -> List[int]:
	"""
	Implements a greedy moderation strategy that selects the group with the highest discrepancy-to-rigidity ratio
	(|o_1 - o_2| / r) and moderates all the agents from that group that the remaining budget allows.

	Parameters
	----------
	social_network : SocialNetwork
		The social network containing agent groups and the available effort budget.

	Returns
	-------
	List[int]
		A list where each index represents an agent group, and the value at that index represents
		the number of agents moderated from that group.

	Notes
	-----
	- The function iteratively selects the group with the highest |o_1 - o_2| / r ratio.
	- It ensures that the effort spent does not exceed the maximum allowed (r_max).
	- If multiple groups have the same ratio, it prioritizes the first one found.
	"""
	# Check if the effort required to moderate the entire social network is less than or equal to the max effort allowed.
	# If we have enough effort to moderate the entire network, the optimal strategy is to moderate all agents in all groups.
	if calculate_max_effort(social_network) <= social_network.r_max:
		return [group.n for group in social_network.groups]

	groups = social_network.groups[:]
	n = len(groups)
	strategy = [0] * n  # Initialize strategy with zero moderation for all groups
	remaining_budget = social_network.r_max

	while remaining_budget > 0:
		# Select the group with the highest discrepancy-to-rigidity ratio
		best_index = -1
		best_ratio = -1
		best_effort = float('inf')

		for i, group in enumerate(groups):
			if group.n > 0:  # Ensure there are agents left to moderate and r is nonzero
				effort_per_agent = abs(group.o_1 - group.o_2) * group.r
				if effort_per_agent <= remaining_budget:
					ratio = abs(group.o_1 - group.o_2) / group.r if group.r > 0 else 1
					if ratio > best_ratio:
						best_ratio = ratio
						best_index = i
						best_effort = effort_per_agent

		# If no valid group is found, break
		if best_index == -1:
			break

		# No need to moderate the group
		if best_effort == 0:
			break

		# Determine how many agents we can moderate
		group = groups[best_index]
		max_agents_moderatable = group.n # We can't moderate more than we have
		max_possible = remaining_budget // best_effort  # Max number of agents we can afford to moderate

		agents_to_moderate = min(max_agents_moderatable, max_possible) # Calculate how many agents we can moderate

		if agents_to_moderate > 0:
			strategy[best_index] += agents_to_moderate
			remaining_budget -= math.ceil(agents_to_moderate * best_effort) # Deduct effort spent

			# Update group information
			groups[best_index] = create_agent_group(
				group.n - agents_to_moderate,
				group.o_1,
				group.o_2,
				group.r
			)

	return strategy


def greedy_discrepancy_rigidity_heap(social_network: SocialNetwork) -> List[int]:
	"""
    Implements a greedy moderation strategy using a max-heap (priority queue) to efficiently select
    the group with the highest discrepancy-to-rigidity ratio (|o_1 - o_2| / r). The algorithm moderates
    all the agents from that group that the remaining budget allows.

    Parameters
    ----------
    social_network : SocialNetwork
        The social network containing agent groups and the available effort budget.

    Returns
    -------
    List[int]
        A list where each index represents an agent group, and the value at that index represents
        the number of agents moderated from that group.

    Notes
    -----
    - The function uses a max-heap (priority queue) for efficient selection of the best group.
    - The heap allows selecting the best group in O(1) time and updating in O(log n), reducing complexity.
    - It ensures that the effort spent does not exceed the maximum allowed (r_max).
    - If multiple groups have the same ratio, they are processed based on their initial heap order.
    """
	# Check if the effort required to moderate the entire social network is less than or equal to the max effort allowed.
	# If we have enough effort to moderate the entire social network, the optimal strategy is to moderate all agents in all groups.
	if calculate_max_effort(social_network) <= social_network.r_max:
		return [group.n for group in social_network.groups]

	groups = social_network.groups[:]
	n = len(groups)
	strategy = [0] * n  # Initialize strategy with zero moderation for all groups
	remaining_budget = social_network.r_max

	# Min-heap (negate value to simulate max-heap)
	heap = []
	for i, group in enumerate(groups):
		if group.r > 0:
			#reduction_per_agent = (group.o_1 - group.o_2) ** 2
			#effort_per_agent = abs(group.o_1 - group.o_2) * group.r
			reduction = abs(group.o_1 - group.o_2) / group.r  # Reduction per unit effort
			heapq.heappush(heap, (-reduction, i))

	while remaining_budget > 0 and heap:
		_, best_index = heapq.heappop(heap)
		group = groups[best_index]

		effort_per_agent = abs(group.o_1 - group.o_2) * group.r
		if effort_per_agent == 0 or effort_per_agent > remaining_budget:
			continue  # Avoid division by zero or exceeding budget

		max_agents_moderatable = group.n  # Can't moderate more agents than we have
		max_possible = remaining_budget // effort_per_agent  # Max we can afford
		agents_to_moderate = min(max_agents_moderatable, max_possible) # Calculate how many agents we can actually moderate

		if agents_to_moderate > 0:
			strategy[best_index] = agents_to_moderate
			remaining_budget -= math.ceil(agents_to_moderate * effort_per_agent)

	return strategy



def counting_sort_by_digit(arr, exp):
	"""
    Sorts an array of (group, value) pairs based on a specific digit using Counting Sort.
    This function is used as a subroutine in the Radix Sort algorithm.

    Parameters
    ----------
    arr : List[Tuple[AgentGroup, int]]
        A list of tuples where each tuple consists of an agent group and its scaled discrepancy-to-rigidity ratio.
    exp : int
        The current digit position to sort by (1, 10, 100, etc.).

    Returns
    -------
    List[Tuple[AgentGroup, int]]
        A new list where the groups are sorted based on the current digit position.

    Notes
    -----
    - This function sorts values based on the `exp`-th digit using Counting Sort.
    - The digit is extracted using integer division and modulo operations.
    - The sorting is stable, meaning it preserves the order of elements with the same digit value.
    """
	n = len(arr)
	output = [0] * n
	count = [0] * 10  # Digits 0-9

	# Count occurrences of each digit in the current position
	for group, value in arr:
		index = (value // exp) % 10
		count[index] += 1

	# Transform count[i] into the cumulative position
	for i in range(1, 10):
		count[i] += count[i - 1]

	# Build the sorted output array
	for i in range(n - 1, -1, -1): # Iterate in reverse to maintain stability
		group, value = arr[i]
		index = (value // exp) % 10
		output[count[index] - 1] = (group, value)
		count[index] -= 1

	return output


def radix_sort_groups(groups):
	"""
    Sorts agent groups based on the discrepancy-to-rigidity ratio (|o_1 - o_2| / r) using Radix Sort.
    This sorting technique ensures an efficient near-linear runtime complexity.

    Parameters
    ----------
    groups : List[AgentGroup]
        A list of agent groups to be sorted.

    Returns
    -------
    List[AgentGroup]
        A new list where the agent groups are sorted in descending order based on their discrepancy-to-rigidity ratio.

    Notes
    -----
    - The discrepancy-to-rigidity ratio is converted into an integer by multiplying by a large factor to preserve precision.
    - Radix Sort is used for sorting, making it more efficient than comparison-based sorting (O(n) instead of O(n log n)).
    - The function avoids division by zero by filtering out groups where `r == 0`.
    """
	factor = 1000000000 # Scaling factor to convert floating-point ratios into integers
	processed_groups = []

	# Compute and scale the discrepancy-to-rigidity ratio
	for group in groups:
		if group.r > 0:  # Avoid division by zero
			ratio = abs(group.o_1 - group.o_2) / group.r
			scaled_ratio = int(round(ratio * factor))  # Convert to an integer for sorting purposes
			processed_groups.append((group, scaled_ratio))

	if not processed_groups:
		return [] # Return an empty list if there are no valid groups

	# Find the maximum value to determine the number of digits
	max_value = max(value for _, value in processed_groups)

	# Apply radix sort on each digit
	exp = 1
	while max_value // exp > 0:
		processed_groups = counting_sort_by_digit(processed_groups, exp)
		exp *= 10

	# Extract and return the sorted agent groups in descending order
	return [group for group, _ in reversed(processed_groups)]


def greedy_moderation_with_radix_sort(social_network: SocialNetwork) -> List[int]:
	"""
    Implements a greedy moderation strategy by first sorting the groups using Radix Sort based on
    their discrepancy-to-rigidity ratio (|o_1 - o_2| / r) in descending order. The algorithm then moderates
    agents sequentially, ensuring the best reductions are applied first within the given budget.

    Parameters
    ----------
    social_network : SocialNetwork
        The social network containing agent groups and the available effort budget.

    Returns
    -------
    List[int]
        A list where each index represents an agent group, and the value at that index represents
        the number of agents moderated from that group.

    Notes
    -----
    - Radix Sort is used to achieve a near-linear sorting time, O(n).
    - Sorting the groups beforehand allows for efficient greedy selection in O(n).
    - It ensures that the effort spent does not exceed the maximum allowed (r_max).
    - After sorting, the algorithm processes the groups sequentially, moderating as many agents as possible.
    """
	# Check if the effort required to moderate the entire social network is less than or equal to the max effort allowed.
	# If we have enough effort to moderate the entire social network, the optimal strategy is to moderate all agents in all groups.
	if calculate_max_effort(social_network) <= social_network.r_max:
		return [group.n for group in social_network.groups]

	n = len(social_network.groups)
	strategy = [0] * n  # Initialize the moderation strategy (with all zeros)
	remaining_r = social_network.r_max  # Available effort budget

	# Sort the groups based on the discrepancy-to-rigidity ratio using Radix Sort
	sorted_groups = radix_sort_groups(social_network.groups)
	#sorted_groups.reverse()  # Invert the order to get the highest ratios first

	for group in sorted_groups:
		if remaining_r <= 0:
			break # No more budget available

		index = social_network.groups.index(group)
		max_agents_moderatable = group.n

		effort_per_agent = abs(group.o_1 - group.o_2) * group.r
		if effort_per_agent == 0 or effort_per_agent > remaining_r:
			continue

		max_possible = remaining_r // effort_per_agent  # Max number of agents we can afford to moderate

		agents_to_moderate = min(max_agents_moderatable, max_possible) # The number of agents we can actually moderate

		if agents_to_moderate > 0:
			strategy[index] += agents_to_moderate
			remaining_r -= math.ceil(agents_to_moderate * effort_per_agent)

	return strategy
