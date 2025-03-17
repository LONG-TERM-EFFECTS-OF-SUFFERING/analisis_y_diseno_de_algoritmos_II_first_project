import math
from typing import List, NamedTuple

from classes.agent_group import AgentGroup, create_agent_group


class SocialNetwork(NamedTuple):
	n: int
	groups: List[AgentGroup]
	r_max: int

	def __str__(self) -> str:
		"""
		Returns a string representation of the SocialNetwork object.

		Returns
		-------
		str
			A string describing the social network, including the number of agent groups,
			the maximum resource value, and the internal conflict.
		"""
		result = f"""Social network with {self.n} agent groups and R_max = {self.r_max}
Internal conflict: {calculate_internal_conflict(self):.2f}
Agent groups:
"""
		for i, group in enumerate(self.groups):
			result += f"\tGroup {i}: {group}\n"

		return result

def calculate_internal_conflict(social_network: SocialNetwork):
	"""
	Calculates the Internal Conflict (IC) value of the social network.

	The internal conflict is a measure of opinion divergence across the network,
	calculated as the weighted average of the squared differences between the two
	opinions for each agent group.

	Formula:
	IC(SN) = (∑(n_i * (o_i,1 - o_i,2)²)) / (∑n_i)

	Parameters
	----------
	social_network: SocialNetwork

	Returns
	-------
	float
		The internal conflict value of the social network.
		Higher values indicate greater opinion divergence among agents.
	"""
	groups = social_network.groups

	numerator = 0
	denominator = 0

	for group in groups:
		n_i = group.n
		o_i1 = group.o_i1
		o_i2 = group.o_i2

		numerator += n_i * (o_i1 - o_i2)**2
		denominator += n_i

	return numerator / denominator

def apply_strategy(social_network: SocialNetwork, strategy: List[int]) -> SocialNetwork:
	"""
	Applies an opinion change strategy to the social network, creating a new modified network.

	This method implements the ModIC(SN,E) operation described in the problem statement,
	which removes agents whose opinions are adjusted according to the strategy.

	Parameters
	----------
	social_network: SocialNetwork

	strategy: List[int]
		A sequence of integers [e_0,e_1,...,e_(n - 1)] where e_i indicates the
		number of agents to be removed from group i.

	Returns
	-------
	List[AgentGroup]
		The list of agent groups with the applied modifications.

	Raises
	------
	ValueError
		If the length of the strategy does not match the number of agent groups.
		If any strategy value exceeds the number of agents in its corresponding group.

	Notes
	-----
	Groups where all agents are removed (e_i = n_i) will not be included in the resulting network.
	"""
	n = social_network.n
	groups = social_network.groups
	r_max = social_network.r_max

	if len(strategy) != n:
		raise ValueError("Error: the length of strategy must be equal to the number of agent groups")

	modified_groups = []

	for i, group in enumerate(groups):
		n_i = group.n
		e_i = strategy[i]

		if e_i < n_i:
			modified_group = create_agent_group(
					n_i - e_i,
					group.o_i1,
					group.o_i2,
					group.r
				)
			modified_groups.append(modified_group)
		elif e_i == n_i:
			n -= 1
		else: # e_i > n_i
			raise ValueError("Error: strategy value cannot be greater than the number of agents in the group")

	return SocialNetwork(n, modified_groups, r_max)

def calculate_effort(social_network: SocialNetwork, strategy: List[int]):
	"""
	Calculates the effort required to adjust opinions in the social network using the given strategy.

	The effort is calculated according to the formula:
	Effort(SN,E) = sum(ceil(|o_i,1 - o_i,2| * r_i * e_i))
	where e_i is the number of agents in group i whose opinions will be modified.

	Parameters
	----------
	social_network: SocialNetwork

	strategy : List[int]
		A list of integers where each value e_i indicates the number of agents in group i
		whose opinions will be modified. Must have the same length as the number of agent groups.

	Returns
	-------
	int
		The total effort required to implement the given strategy.

	Raises
	------
	ValueError
		If the length of the strategy list does not match the number of agent groups.

	Notes
	-----
	A strategy is applicable only if the calculated effort does not exceed R_max.
	"""
	n = social_network.n
	groups = social_network.groups

	if len(strategy) != n:
		raise ValueError("Error: the length of strategy must be equal to the number of agent groups")

	effort = 0

	for i, group in enumerate(groups):
		e_i = strategy[i]
		if e_i > 0:
			effort += math.ceil(
				abs(group.o_i1 - group.o_i2) * group.r * strategy[i]
			)

	return effort
