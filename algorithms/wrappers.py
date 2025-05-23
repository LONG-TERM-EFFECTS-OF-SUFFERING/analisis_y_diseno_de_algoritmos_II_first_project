from typing import List, Tuple

from algorithms.brute_force import brute_force
from algorithms.dynamic import dynamic_bottom_up
from algorithms.greedy import greedy_moderation_with_radix_sort
from classes.social_network import (SocialNetwork, apply_strategy,
                                    calculate_effort,
                                    calculate_internal_conflict)


def calculate_effort_and_IC(social_network: SocialNetwork, strategy: List[int]) -> Tuple[float, float]:
	effort = calculate_effort(social_network, strategy)
	modified_network = apply_strategy(social_network, strategy)
	IC = calculate_internal_conflict(modified_network)
	return effort, IC

def modciFB(social_network: SocialNetwork) -> Tuple[List[int], float, float]:
	strategy = brute_force(social_network)
	return strategy, *calculate_effort_and_IC(social_network, strategy)

def modciPD(social_network: SocialNetwork) -> Tuple[List[int], float, float]:
	strategy = dynamic_bottom_up(social_network)
	return strategy, *calculate_effort_and_IC(social_network, strategy)

def modciV(social_network: SocialNetwork) -> Tuple[List[int], float, float]:

	strategy = greedy_moderation_with_radix_sort(social_network)

	return strategy, *calculate_effort_and_IC(social_network, strategy)
