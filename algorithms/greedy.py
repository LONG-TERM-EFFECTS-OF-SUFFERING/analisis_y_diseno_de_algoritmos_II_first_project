import heapq
import math
from typing import List
from classes.agent_group import create_agent_group
from classes.social_network import SocialNetwork, calculate_internal_conflict, apply_strategy, calculate_max_effort


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



def greedy_moderation_by_discrepancy_rigidity_one_at_a_time(social_network: SocialNetwork) -> List[int]:
	"""
	Implements a greedy moderation strategy that selects the group with the highest discrepancy-to-rigidity ratio
	(|o_1 - o_2| / r) and moderates one agent at a time until the budget (r_max) is exhausted.

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
	n = len(social_network.groups)
	strategy = [0] * n  # Initialize strategy with zero moderation for all groups
	remaining_budget = social_network.r_max

	while remaining_budget > 0:
		# Select the group with the highest discrepancy-to-rigidity ratio
		best_index = -1
		best_ratio = -1

		for i, group in enumerate(social_network.groups):
			if group.n > strategy[i] and group.r > 0:  # Ensure there are agents left to moderate and r is nonzero
				ratio = abs(group.o_1 - group.o_2) / group.r
				if ratio > best_ratio:
					best_ratio = ratio
					best_index = i

		# If no valid group is found, break
		if best_index == -1:
			break

		# Calculate effort required to moderate one agent in the selected group
		selected_group = social_network.groups[best_index]
		effort = math.ceil(abs(selected_group.o_1 - selected_group.o_2) * selected_group.r)

		# If we can afford moderating one more agent, apply it
		if remaining_budget >= effort:
			strategy[best_index] += 1
			remaining_budget -= effort
		else:
			break  # Stop if we can't afford the next moderation step

	return strategy


def greedy_moderation_by_discrepancy(social_network: SocialNetwork) -> List[int]:
	"""
	Implements a greedy moderation strategy that selects the group with the highest discrepancy
	(|o_1 - o_2|) and moderates one agent at a time until the budget (r_max) is exhausted.

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
	n = len(social_network.groups)
	strategy = [0] * n  # Initialize strategy with zero moderation for all groups
	remaining_budget = social_network.r_max

	while remaining_budget > 0:
		# Select the group with the highest discrepancy
		best_index = -1
		best_discrepancy = 0

		for i, group in enumerate(social_network.groups):
			if group.n > strategy[i] and group.r > 0:  # Ensure there are agents left to moderate and r is nonzero
				discrepancy = abs(group.o_1 - group.o_2)
				if discrepancy > best_discrepancy:
					best_discrepancy = discrepancy
					best_index = i

		# If no valid group is found, break
		if best_index == -1:
			break

		# Calculate effort required to moderate one agent in the selected group
		selected_group = social_network.groups[best_index]
		effort = math.ceil(abs(selected_group.o_1 - selected_group.o_2) * selected_group.r)

		# If we can afford moderating one more agent, apply it
		if remaining_budget >= effort:
			strategy[best_index] += 1
			remaining_budget -= effort
		else:
			break  # Stop if we can't afford the next moderation step

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
				#print(effort_per_agent)
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


def greedy_absolute_reduction_heap(social_network: SocialNetwork) -> List[int]:
	"""
	Greedy strategy for moderation using absolute reduction optimized with a heap.

	Parameters:
	- social_network: Object containing groups of agents and maximum effort available.

	Returns:
	- List of integers indicating how many agents were moderated per group.
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

		max_agents_moderatable = group.n  # Can't moderate more than we have
		max_possible = remaining_budget // effort_per_agent  # Max we can afford
		agents_to_moderate = min(max_agents_moderatable, max_possible)

		if agents_to_moderate > 0:
			strategy[best_index] = agents_to_moderate
			remaining_budget -= math.ceil(agents_to_moderate * effort_per_agent)

	return strategy



def counting_sort_by_digit(arr, exp):
	n = len(arr)
	output = [0] * n
	count = [0] * 10  # Dígitos 0-9

	# Contar ocurrencias de cada dígito en la posición actual
	for group, value in arr:
		index = (value // exp) % 10
		count[index] += 1

	# Transformar count[i] en la posición acumulativa
	for i in range(1, 10):
		count[i] += count[i - 1]

	# Construir el arreglo ordenado
	for i in range(n - 1, -1, -1):
		group, value = arr[i]
		index = (value // exp) % 10
		output[count[index] - 1] = (group, value)
		count[index] -= 1

	return output

def radix_sort_groups(groups):
	# Convertimos la métrica en enteros multiplicando por 1000000 para precisión
	factor = 1000000000
	processed_groups = []

	for group in groups:
		if group.r > 0:  # Evitamos división por cero
			ratio = abs(group.o_1 - group.o_2) / group.r
			scaled_ratio = int(round(ratio * factor))  # Redondeamos para evitar errores de truncamiento
			processed_groups.append((group, scaled_ratio))

	if not processed_groups:
		return []

	# Encontrar el valor máximo para determinar la cantidad de dígitos
	max_value = max(value for _, value in processed_groups)

	# Aplicar Radix Sort por cada dígito
	exp = 1
	while max_value // exp > 0:
		processed_groups = counting_sort_by_digit(processed_groups, exp)
		exp *= 10

	# Extraer los grupos ordenados
	return [group for group, _ in processed_groups]

def greedy_moderation_with_radix_sort(social_network: SocialNetwork) -> List[int]:

	# Check if the effort required to moderate the entire social network is less than or equal to the max effort allowed.
	# If we have enough effort to moderate the entire social network, the optimal strategy is to moderate all agents in all groups.
	if calculate_max_effort(social_network) <= social_network.r_max:
		return [group.n for group in social_network.groups]

	n = len(social_network.groups)
	strategy = [0] * n  # Inicializamos la estrategia de moderación
	remaining_r = social_network.r_max  # Esfuerzo disponible

	# Ordenamos los grupos por la métrica de prioridad usando Radix Sort
	sorted_groups = radix_sort_groups(social_network.groups)
	sorted_groups.reverse()  # Invertimos el orden para que el mayor esté al principio

	for group in sorted_groups:
		if remaining_r <= 0:
			break

		index = social_network.groups.index(group)
		max_agents_moderatable = group.n

		effort_per_agent = abs(group.o_1 - group.o_2) * group.r
		if effort_per_agent == 0 or effort_per_agent > remaining_r:
			continue

		max_possible = remaining_r // effort_per_agent  # Máximo que podemos moderar

		agents_to_moderate = min(max_agents_moderatable, max_possible)

		if agents_to_moderate > 0:
			strategy[index] += agents_to_moderate
			remaining_r -= math.ceil(agents_to_moderate * effort_per_agent)

	return strategy
