wosrt case vs average case: average case is the average from execution with different initial conditions...

### worst case complexity

- Give us a sense of the difficultiy of the problem
- For many metaheuristics, it's often not representative of the "true" (in practice) cost of running it...
    - Ofentimes, they are much more efficient and effective.....

### Optimization

optimization -> discrete
             -> continuous (cost / objective function is continuous)

optimization -> deterministic
             -> stochastic (for most metaheuristic cases)

P   -> polynomial
NP  -> non-deterministic... We can verify the solution in polynomial time.
NP-Complete -> I can find a mapping between two NP-Complete problems
All NP-Complete problems are fondamentally equivalent -> there exist a polynomial time transformation from problem 1 to problem 2 so problem 1 and problem 2 are NP-Complete problems.
NP-Hard -> TSP (find a cycle in a graph)
NP-Complete -> hammilton cycle

graph-coloring -> NP-Complet
minimum graph-coloring -> NP-Hard

Problems that needs metaheuristics are NP-Hard

Do not consider metaheuristics for P or NP problems !!!!

metaheuristic: can I do it or not ? 

decision problem: -> yes, there is a solution in this problem.
optimization problem: -> what is the best solution ?

real life problems is secret of success for metaheuristics
Operation Research (OR)

Metaheuristic: explore search space in intelligent(adaptability / collective intelligence) way to find optimals.

Trade-off: if problem is P or NP, don't use metaheuristics !!! How good the solution is vs how much I pay
metaheuristic give not exact solution, but acceptable solution... => fight between "purists" and "practicalists"...

Heuristic: problem dependant -> lacking generality....

Metaheuristic: general approach stocastic because systematic approach is impossible....
Fluctuations are key to performing a number of tasks => fluctuations are good => generate fluctuations....

### Characterization of metaheuristics

#### good
metaheuristics  -> do not require a lot of assumptions
                -> fairly easy to implement/code
only requirement is that f can be computed.... It doesn't mean that an analytical expression of f exists.

#### bad
need guiding parameters (how much far must we go ???) found empirically
nowadays, ML is starting to be used to find the guiding parameters

need initial condition
require halting condition -> about trade-off: CPU vs quality

learning is an optimization !!!!

Easy to implement and can readily be parallized...

classically, they combine two key actions:
intensification and diversification, more commonly exploitation and exploration: eighte we search for more promising solutions in S, else we further analyse a found region of interest.....

trade-off :
- exploration vs exploitation
- diversification vs intensification

We need to find a suitable representation of the problem !!!

The coding/representation selected has a significant impact on how we move through the search space...

We need a function that give neighborhood and a search/exploration operator U initial condition -> U -> new state $\in$ neighborhood etc...

Output can be the exact solution or an approximate solution...
Is my approximate solution good enough ????

How to define neighborhood ??? It depends on the coding/representation of the configuration....

Most of the time, non-exhaustive search
But exhaustive search of neighborhood

local search -> at the neighbour level

random walk
neighborhood-dependent random walks: don't go away if the place is good

# A very basic metaheuristic (Iterated Local Search)

basin of attraction: a point in this basin will move to the local optimum

- reduce search space to search space of local optimum

nudge ~= push distance to nudge is our guided parameter
challenge choose the right strengh of our nudge....




