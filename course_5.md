# Simulated Annealing Part 2

Start with high temperature => lot of energy to explore

All is based on metropolis rule.

Two counters: number of iterations, number of accepted moves

number iterations: regular iteration count
number of accepted moves: blabla

TSP (Traveling Salesman Problem) is a benchmark problem.
It's a NP-Hard problem.
It's super-easy to implement.

Random initial configuration...
Actual solution is trivial for human, but not for a computer ($10^{30}$ solutions to explore...)

$f_{optimum} = 2\pi$

- $n = 30$ => small TSP benchmark
- Search space $S = 30!$ => huge !!!

> [!NOTE]
> There is no guarantee that you have found the GLOBAL minimum

Temperature higher => found solution at step 55000 instead of 5000 (T = 0.5 instead of T = 0.1)...
   => optimal solution found at T15 = 0.114 => a lot of explorations more !!!!

What is impact of Temperature and how to modify it in an efficient way ??

## guiding parameters

- Initial temperature T0 (high but not too...)
- Number of accepted moves
- How to decrease temperature
- Stopping criterion => has huge impact on whether or not the global optimum is found...

=> No way to properly define guided parameters !!!!

### Placment of electronic components

=> perhaps solution searched is not optimum solution, but solution that minimize heat impact or something else...

### Graph drawing

Node placement in a graph

Kind of moves chosen to search neighborhoods significantly influences the quality of the solutions obtained...

#### 2 opt-move

- Remove 2 edges and reconnect the path in a different way
- moves 2 non-adjacent edges
---
- Compute change in distance
- if $\Delta < 0$, new route is shorter and move is accepted
- Based on triangle inequality (Need to better understand... Is it because the method has chose best move ??)

TSP 500 is a relatively simple benchmark...

Fractal: shape that doesn't have ??

We can increase the difficulty of TSP by placing the cities on an irregular structure (fractal structure)

Include for instance mountains between cities etc...

> [!IMPORTANT]
> The core trade-off with metaheuristics
> Computing cost vs accuracy

There are decisions on NP-Hard problems that doesn't wait...
=> suboptimal solutions are much better than solutions depending on time to find it............

### Convergence (for SA)

Convergence has been proved (good) in a probabilitic sense (not great)

SA obtains a solution arbitrarily close to the global minimum with a probability arbitrary close to 1...

Not forget it's often with great CPU costs !!!

#### Conditions

- initial temperature must be high enough (to warrant sufficient room for exploration)
- temperature must not be decreased too quickly during search process ( reasonable temperature schedule )
- moves must be reversible
- Any feasible state of the system must be reachable from any other state in a finite number of moves (reasonable assumption !!!)


### Temperature / cooling schedule

- Temperature / cooling schedule: T must decrease, but not too fast...
- T should not decrease faster than C / log t for t >> 1 to ensure convergence of SA
- C is related to the fitness variations throughout S (problem dependent => it depends on the fitness landscape)

### Proof

fitness landscape (2D minimization problem)

continuous optimisation -> grid -> discrete one...

Search space : $card(S) = 10 \times 10$ => very small search space !!!

neighborhood: NSEW

Representation: single index between 1 and card(S)

We want to prove that we converge in a probabilistic sense.

$P(t, i) = ???$

Markov chain Monte Carlo MCMC

$P(t, i) = \sum_{j \in S}W_{ji}P(t - 1, j)$

$P(t + 1, j) = \sum_{i \in S} W_{ij}(t) P(t, i)$

$W_{ij}(t) )$ transition probability to move from configuration i to j at time t.

Depends on enery I have to climb hills...


W = [W_{ij}]_{100x100} = square matrix...

W_{ij} ??

Normalization condition (sum of probabilities = 1...)

The whole SA dynamics is embedded in the product of the W matrices...

Now we want to see if it depends on initial condition...

If T0 is hibh enough, all the rows have identical vaues...

High temperature:
After theses iterations, \prod_k = 0 ^ N W(k) has identical values on the rows.... => guarantees an exhaustive search of the search space !!!

Low temperature:
After theses iterations, this has an impact on metropolis rule => reduce number of moves => can not converge...  But it can also !!

=> choice of initial conditions can have big impact on final solution...
