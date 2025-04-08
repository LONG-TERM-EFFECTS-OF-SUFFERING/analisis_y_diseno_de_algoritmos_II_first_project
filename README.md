# Moderating internal conflict of opinion in a social network

## Statement

A social network $SN$ is a pair $\langle SA,R_{ \max } \rangle$, where $SA$ is a sequence of agent groups $SA = \langle a_0,\dots,a_{ n - 1 } \rangle$ and $R_{ \max } > 0 \land R_{ \max } \in \mathbb{ N }$ represents the maximum integer value available to moderate the opinions in the network $SN$.

An agent group $a_i$ is a tuple

$$
a_i = \langle n_i,o_{ i,1 },o_{ i,2 },r_i \rangle
$$

where:

- $n_i$: is the number of agents belonging to agent group $i$.

- $o_{ i,1 }$: represents the opinion of each agent in group $i$ about statement $1$.

	> $-100 \leq o_{ i,1 } \leq 100 \land o_{ i,1 } \in \mathbb{ Z }$.

- $o_{ i,2 }$: represents the opinion of each agent in group $i$ about statement $2$.

	> $-100 \leq o_{ i,2 } \leq 100 \land o_{ i,2 } \in \mathbb{ Z }$.

- $r_i$: represents the rigidity level of each agent in group $i$ ($0 \leq i < n$).

	> $0 \leq r_i \leq 1$.

The internal conflict value of a network $SN$ is defined as follows:

$$
\text{IC}(SN) = \frac{ \sum_{ i = 0 }^{ n - 1 }{ n_i * (o_{ i,1 } - o_{ i,2 })^2 } }{ n }
$$

> $n$ is the number of agent groups that there are in the social network $SN$.

A **strategy for opinion change** in a network $SN$ is a sequence:

$$
E = \langle e_0,e_1,\dots,e_{ n - 1 } \rangle
$$

where $e_i$ indicates the number of agents in group $i$ whose opinion will be modified, and the following constraints hold:

- $e_i \in \mathbb{ N }$.

- $0 \leq e_i \leq n_i$.

Applying an opinion change strategy $E$ to a network $SN$, denoted as $\text{ModIC}(SN,E)$, results in a new network ${SN}'$ where:

$$
{ n' }_i = n_i - e_i
$$

It is assumed that the agents whose opinions were adjusted by $E$ are no longer part of the resulting network ${SN}'$.

The **effort** required to adjust opinions in $SN$ using strategy $E$ is defined as:

$$
\text{Effort}(SN,E) = \sum_{ i = 0 }^{ n - 1 } \left \lceil |o_{ i,1 } - o_{ i,2 }| \cdot r_i \cdot e_i \right \rceil
$$

A strategy $E$ is **applicable** if:

$$
\text{Effort}(SN,E) \leq R_{ \max }
$$

### Input

A social network $SN = \langle SA,R_{ \max } \rangle$

### Output

An applicable opinion change strategy $E$ for the network $SN$, meaning:

$$
\text{Effort}(SN,E) \leq R_{ \max }
$$

such that:

$$
\text{IC}(\text{ModIC}(SN,E))
$$

is minimized.

## Analysis

- Each group of agents $a_i$ contributes

$$
n_i * (o_{ i,1 } - o_{ i,2 })^2
$$

to the internal conflict. If $k$ agents from that group are **moderated**, this contribution changes to

$$
(n_i - k) * (o_{ i,1 } - o_{ i,2 })^2
$$

## Instructions to execute it

- Create a Python virtual environment: `python -m venv .venv`.

	> This is optional, but recommended.

1. Install the libraries included in `requirements.txt`: `pip install -r requirements.txt`.

2. Run the main UI script: `python ./UI/main_UI.py`.
