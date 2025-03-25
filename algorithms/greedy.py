import math
from typing import List
from classes.social_network import SocialNetwork, calculate_internal_conflict, apply_strategy

def greedy_absolute_reduction(social_network: SocialNetwork) -> List[int]:
    """
    Implements a greedy strategy to minimize internal conflict by removing agents,
    prioritizing those that provide the highest absolute conflict reduction per effort unit.

    Parameters
    ----------
    social_network: SocialNetwork
        The initial state of the social network.

    Returns
    -------
    List[int]
        A list representing the number of agents removed from each group.
    """
    groups = social_network.groups
    r_max = social_network.r_max
    num_groups = len(groups)
    strategy = [0] * num_groups  # Initialize strategy with zero removals

    # Generate possible removals sorted by absolute conflict reduction
    removal_options = []

    for i, group in enumerate(groups):
        for e_i in range(1, group.n + 1):  # Consider removing 1 to n agents (not all)
            new_n = group.n - e_i
            if new_n == 0:
                continue  # Avoid removing the entire group

            # Compute internal conflict reduction
            original_contribution = group.n * (group.o_1 - group.o_2) ** 2
            new_contribution = new_n * (group.o_1 - group.o_2) ** 2
            conflict_reduction = original_contribution - new_contribution

            # Compute effort required
            effort = math.ceil(abs(group.o_1 - group.o_2) * group.r * e_i)

            # Store the option (sorted by max conflict reduction first)
            removal_options.append((conflict_reduction, effort, e_i, i))

    # Sort by highest conflict reduction per effort spent (greedy criterion)
    removal_options.sort(reverse=True, key=lambda x: (x[0] / x[1] if x[1] > 0 else float('inf'), x[0]))

    # Apply removals while staying within budget
    for conflict_reduction, effort, e_i, i in removal_options:
        if effort <= r_max:
            strategy[i] += e_i  # Apply removal to group i
            r_max -= effort  # Deduct effort from budget

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