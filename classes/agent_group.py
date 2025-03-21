from typing import NamedTuple


class AgentGroup(NamedTuple):
	n: int
	o_1: int
	o_2: int
	r: float


	def __str__(self) -> str:
		"""
		Returns a string representation of the AgentGroup object.

		Returns
		-------
		str
			A string describing the agent group, including the number of agents,
			their opinions on both statements, and their resistance level.
		"""
		return f"""Group of agents with {self.n} agents
	\to_i1 = {self.o_1}
	\to_i2 = {self.o_2}
	\tr = {self.r}"""

def create_agent_group(n: int, o_i1: int, o_i2: int, r: float):
	"""
	Initializes an AgentGroup with the specified number of agents, their opinions, and their resistance level.

	Parameters
	----------
	n (number of agents): int
		The number of agents in the group.

	o_i1 (first opinion): int
		The opinion of the agents on the first statement (must be between -100 and 100).

	o_i2 (second opinion): int
		The opinion of the agents on the second statement (must be between -100 and 100).

	r (resistance): float
		The resistance level of the agents (must be between 0 and 1).

	Raises
	------
	ValueError
		If first_opinion or second_opinion is not in the range [-100, 100].
		If resistance is not in the range [0, 1].
	"""
	if not -100 <= o_i1 <= 100:
		raise ValueError("Error: the first opinion must be between -100 and 100")

	if not -100 <= o_i2 <= 100:
		raise ValueError("Error: the second opinion must be between -100 and 100")

	if not 0 <= r <= 1:
		raise ValueError("Error: the resistance must be between 0 and 1")

	return AgentGroup(n, o_i1, o_i2, r)
