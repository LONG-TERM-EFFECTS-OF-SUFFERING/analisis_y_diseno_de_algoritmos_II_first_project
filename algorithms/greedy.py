import math
from typing import List
from classes.agent_group import create_agent_group
from classes.social_network import SocialNetwork, calculate_internal_conflict, apply_strategy


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
                #effort_per_agent = math.ceil(abs(group.o_1 - group.o_2) * group.r)
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



def greedy_moderation_efficiency(social_network: SocialNetwork) -> List[int]:
    """
    Determines a moderation strategy using a greedy approach that prioritizes groups based on
    their efficiency in reducing internal conflict per unit of effort spent.

    This strategy iteratively selects the group that provides the highest reduction in internal
    conflict per unit of effort until the available effort (R_max) is exhausted.

    Parameters
    ----------
    social_network : SocialNetwork
        The social network containing agent groups and the maximum available effort.

    Returns
    -------
    List[int]
        A list representing the number of agents to be moderated in each group.
        Example: [0, 2, 3, 0] means 0 agents moderated in the first group, 2 in the second, etc.

    Notes
    -----
    - The efficiency of moderating a group is calculated as:
      efficiency = (conflict reduction) / (effort required)
    - The algorithm stops when there is no more available effort or no further efficient modifications.
    """
    groups = social_network.groups
    r_max = social_network.r_max
    strategy = [0] * len(groups)

    while r_max > 0:
        options = []

        for i, group in enumerate(groups):
            if group.n > strategy[i]:  # Solo considerar si aún quedan agentes en el grupo
                e_i = strategy[i] + 1  # Probar moderar un agente más
                effort = math.ceil(abs(group.o_1 - group.o_2) * group.r * e_i)

                if effort <= r_max:
                    new_conflict = calculate_internal_conflict(
                        apply_strategy(social_network, [strategy[j] + (1 if j == i else 0) for j in range(len(groups))])
                    )
                    conflict_reduction = calculate_internal_conflict(social_network) - new_conflict
                    efficiency = conflict_reduction / effort if effort > 0 else float('inf')
                    options.append((efficiency, -conflict_reduction, i))  # Se ordenará por eficiencia y reducción absoluta

        if not options:
            break  # No hay más opciones viables

        options.sort(reverse=True)  # Ordenar de mayor a menor eficiencia

        best_efficiency, _, best_group = options[0]

        if best_efficiency == 0:
            break  # No se puede reducir más el conflicto

        strategy[best_group] += 1
        r_max -= math.ceil(abs(groups[best_group].o_1 - groups[best_group].o_2) * groups[best_group].r)

    return strategy


def greedy_moderation_by_discrepancy_rigidity(social_network: SocialNetwork) -> List[int]:
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