Metaheuristic: find solution by exploring in an intelligent way the search space.

Metaheuristic: based on local search !!!

Metaheuristic: there is non deterministic element (stochastic element) because we want to not be blocked in local optimum

How much must I smooth the landscape ?? (Parametrisation of metaheuristic...)

Coding strategy: how we represent the configuration/solution...

K = 1 => all "genes" are independent. K = 2 => we look at neighbors.

$x_1, ..., x_n$, fitness = $\sum_i x_i$

Using hypercube as representation instead of graph of fitness...We find global max !

=> Final result depend on the configuration proposed !
Strategy play a critical role in metaheuristic !!!

Idee: make as ants: multiple search of solutions at the same time !

# Chapter 2: Tabu Search

Basic idea: if I add memory, perhaps have I more luck to find a solution !!!

Markovian process: I go in the next step depending on my current step ! => memoryless

Tabu Search (TS)

- non Markovian
- build on local serach methods
- use memory structure to avoid local optima
- explore search space more intelligently and broadly => connected to experience replay in reinforcement learning...

Neighborhood depends on representation !!

Non-tabu solution: already visited 
Tabu-list: have particular structure (defines forbidden, points or attributes of points or moves...)
tabu-attribute is not a permanent one
  - no infinite memory considered !
  - constantly udpate the tabu list


- start
- choose initial configuration (empty tabu list)
- generate Neighborhood (local search)
- select best non-tabu neighbor
- update best solution
- end condition ? (Halting criterion)
- update tabu list
- update current solution
- iterate

Metaheuristics are not difficult !!! It's basic process !!! (But it's not simple, it's not trivial.... ??)

Random search: inefficient: explore only a small part of the space, and go multiple times on the same points....

Tabu search

  - short memory: follow the basin of attraction of local max... Stay here...
  - long memory: explore further (imposed by the tabu restrictions) and then follow the basin of attraction of global max.

Construction of tabu list is KEY !!!

When tabu memory is too large, we reach basin attraction of the max, but we continue to explore...Further exploration promoted by the exessively large size of the tabu list !

=> the choice of the structure of the tabu list will have a significant impact on the convergence of TS !!

Can we prove that it converges ???

### Convergence

- absolute convergence (looking for the global optimum in a given landscape)
- moderated convergence (looking for is good enough)

Depends on:

- memory length
- neighborhood / structure
- initial condition
- stopping criterion defines the concept of "good enough" solution
- fitness

1. Because of the non-Markovian (memory) nature of TS => most mathematical tools become ineffective to establish a convergence result.
2. There's one result, yet limited to some very drastic hypotheses.
3. Theses hypotheses ensure that an exhaustive search of the search space $S$ is achievable => garantees that the global optimum is found => converge

- if search space $S$ is finite (reasonable hypothesis)(still finite doesn't mean small !!)
- if neighborhood is symmetric ($s \in V(t) \Longrightarrow t \in V(s)$)
- if we can reach each point from each point (my network is connected)

THEN a TS that stores all visited points, and aslo is allowed to revisit oldest point will visit  the whole search...

We can't explain why it works most of the time...

When search is blocked (gets stuck), it can restart from oldest tabu point...

### Purposes

- avoid resampling previously visited
- improve efficiency of exploration process

How to build ?

  - previously visited configurations
  - attributes of previously visited configurations
  - other thing...??

Inverse tabu list => inverse move

Forbidden moves:
  
  - prevent cycles
  - encourages exploration
  - balance exploitation vs exploration
    Balance is coming from the structure of the tabu list (size M or banning time K)

Similar to the concept of "Fitness degradation"

Two types of memory:

- short-term memory
- long-term memory

### Short-term memory

- finite size tabu list (Size M: circular list) FIFO
- banning time (tenure time / tabu tenure) duration/number of steps to exclude elements ??????
  In general picked randomly within a given distribution.

Tabu list size M is different from banning time k.

-> 2 different parameters.

M and k are guiding parameters.

Best case scenario: the value of guiding parameter has little influence

#### Example 1 (not understand.....)

Based on hashing function

Array T of size M

attribute of solution h(x)

We want to ban this fitness value h(x) for k iterations at iteration k (construction and update T)

#### Example 2

at t = 0:
initialization:

| N | S | W | E |
| ------------- | -------------- | -------------- | ---- |
| 0 | 0 | 0 | 0 |

at t = 1:

move N => ban S to avoid returning to the previous configuration

we pick k = 2 => going S 

We are going to keep tracks of statistics of the moves we are making... (long-term memory)

Long-term memory: based on the statistics of all possibles moves
  -> at each step, when updating the tabu list, we also update the statistics.

### Long term memory

Construct tabu list to prevent moves, but in long-term, it doesn't work 

Long-term memory is essential here to avoid biases in movement selections....

(Random walker) after 5 moves NNNEE, N(3/5), E(2/5), S(0), W(0)

We want to penalize moves having a too high frequency (promote exploration)

Bonus-malus system can be further modulated (balance exploration exploitation)


### Memory usage

Several possibles implementations for combination of short-term/long-term

In metaheuristic, we need to keep a small number of guided parameters...

General rule of thomb for metaheuristic: minimise the number of guiding parameters

=> caution: some guiding parameters values may depend on one another

### Exploration vs Exploitation

number of forbidden moves, number small => exploration or intensification (high fitness solutions... ??) number bigger => exploration (exploitation instead ???) or diversification

balance exploration vs exploitation => There is no metric for this !!! It can be dynamic according to precedent results...

- notes about balancing exploration and exploitation

  1. there is no metrics for the balance => no indicator/no measure NO ABSOLUTE WAY of doing it (true for ALL metaheuristics => general issue)

  2. that balancing act is not static !!! It's dynamic !! It has to be updated as you move through the search space.. 
