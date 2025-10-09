We are looking after a good enough convergence

# Quadratic Assignment Problem (QAP)

Assignment Problem: assign an object to a location / a task to a person / ...

- n objects and n locations
- distances between locations
- weights or flows 

=> find optimal placment to minimise the overall cost function

$$f = \sum_{i, j}f_{ij}d_{r_i r_j}$$


### Why quadratic ???

- Not an obvious question
- underlying this QAP, we have decision variables $x_i = 0 \text{or} 1$ for object $i$ $\forall i = 1, ..., n$

The complete general formulation of QAP:

$$f = \sum_{i, j, k, p}f_{ij}d_{r_i r_j}x_k x_p$$

=> quadratic in the decision variables...

=> decision depend on other variables => we have $x_k$ and $x_p$ !!!!

Search space $S$ is therefore that of permutations of $n$ objects => $card(S) = n! \Longrightarrow$ NP-Hard problem !

QAP is a complex and challenging class of problems with actual real-life relevance. (facility layout / electronics / data analysis / hospital design / sheduling / ...)

## Example

PCB: Printed Circuit Board => minimise length of connections...

Manhattan distances: we can only move vertical or horizontal...

TSP: traveling salesman problem => falls under the umbrella of QAP...


=> Brute force is absolutely out of questions !!!! 

=> choose a particular representation for configurations in the search space !!!

search space: $p = (i_1, i_2, ..., i_n)$ with $p\left[0\right]$ the location 0 etc...

neighborhood: swapping two objects in the list.
Swapping 2 continuous object: swapping only objects that are neighbors in the list => $n - 1$ possibilities
swapping any 2 objects: $\dfrac{n(n - 1)}{2}$ possibilities
moving and inserting an object => we deplace an object and all other objects are shifted... => $n (n - 2) + 1$ possibilities

Tabu list: revert a move is banned for a banning time

The banning time / tenure time is picked randomly each time we add element to the tabu list...
$$k \in [0.9 \times n, 1.1 \times n + 4]$$ (in general...)

It's empirical !!!

Adding this stochasticity in the choice of the  improves the 

### NUG5 benchmark problem

It consists in a benchmark problem for the QAP class....

Benchmark is used to compare 2 techniques...

Benchmark:

  - only 1 path to the global optimum
  - solution known
  - capture quadratic structure typical of assignment-type problems

Start with random configuration...

# Chap 2 Simulated Annealing (SA)

Annealing: modify structure of the material to have a better structure

Quenching (trempe en français...): fast cooling...

In our case, we will heat up to give energy to the system to restructure the material, and then slow cooling to keep the obtained configuration...

Initial configuration is most likely suboptimal

## Intuitions about inner workings of SA

In physics, all system tend to achieve a stable state.

We want to minimise the energy minimisation (cost /fitness function)...

The process of heating up is the process of exploration...
slow cooling is exploitation

We want to minimise a given objective function

1. select arbitrary admissible initial solution
2. select initial "high temperature" (heating up process !!)
3. moves from the current configuration to reach its neighbors with probability $p$

$$p = min(1, e^{-\frac{\Delta E}{T}})$$ (Metropolis rule)

$$\Delta E = E_{new} - E_{old}$$

Boltzmann factor $e^{-\frac{\Delta E}{k_B T}}$

If $\Delta E < 0$ => my probability is 1 ($E_{new} < E_{old}$)
If $\Delta E > 0$ => my probability is smaller than 1 ($E_{new} > E_{old}$) 

More I move far away from 0, more my probability will be small...

Temperature $T$ is a *dynamic* guiding parameter (that controls the operations of the metaheuristic)

If $T$ is large, SA easily accepts a fitness degradation of the configuration (i.e. energy increase)

To go up the hill, we start heating system to climb hill and then we can slow cooling...

=> to go down with our energy, we begin to go up with the energy !!!

- start
- initial state (random) with initial temperature (high)
- counters: 1 for iterations, 1 for acceptance count
- generate new state, iter 
- heart of SA: pick random number and compare to exp(-blabla) if accepted, increase counter
- equilibrum state -> end condition -> cool down...
- etc...


Value of Temperature define the size of the neighborhood
