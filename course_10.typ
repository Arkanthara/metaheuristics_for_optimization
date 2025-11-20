= Evolutionary algorithms

== Genetic Algorithms

Too much population will prioritize too much exploration

=== Selection

This constitute the parents of next generation...

Apply concept of survival of the fittest: fitness proportionate principe: the higher the fitness is, more chances the individual has a chance to be selected...
Some stochasticity is preserved...

Risk of premature convergence in case of high selection pressure (selection pressure: how strongly the selection process favors better individuals) !!! 

Selection operator: how we pick the fittest individuals...

The choice is random, driven by the fitness !

So the selected population must have a higher fitness !

size of chosen population is a guided parameter

=== Crossover

n individuals children/offspring are created from the selected parents...

It's designed to mix information from 2 parents (genetic information -> position in the fitness landscape)

This is not deterministic, but driven with the crossover probability, a guided parameter

Different crossover operators...

Crossover is not problem dependent

=== Mutation

Additional way to further the exploration...

Mutation CAN be applied

Guiding parameter: probability to carry out a mutation 

=== Exploration vs exploitation

selection: exploitation (we can select multiple time same individual !)
mutation operator: exploration (Fixed at the begining: keep it small vs Temperature in SA !)
crossover operator: both exploration and exploitation... This parameter is very critical !

Crossover point is randomly chosen for each individual !!!

Note:
- In some genetic algorithms, we enforce elitism
- it consists in imposing that the top individual(s) (meaning with the highest fitness) are systematically included in the next generation.

We have more benefits coming from good individuals than fitness degradation..

On average, for a given population going through one generation
- the fitness gain (some individuals see their fitness go up) outweighs the fitness loses (some individuals experience fitness degradation)...

Diminishing returns: At first, we find big gold stones... Then, we have to find smaller gold stones, that takes more time !

=== Diversity of the population

2 distinct diversity measures:
- variance
- entropy

Crossover and mutation conterbalance effect of selection ! (Balance between exploration and exploitation)

=== What if my problem is a continuous optimization problem ?

We discretise the problem...

Deconding: I go from binary string to x value...

The entire population tend get closer to optimum value...

Highly effective in optimizing problems with challenging fitness...

Requirement: the only thing needed is the ability to compute the fitness function...
As no need to derivate fitness function, we can have:
- discontinuous fitness function
- time-varying fitness function (allow dynamic problem solving ! Like catch the target !)

==== Notes

Accuracy of the discretization which is related to the encoding...
Genetic algorithm is not stuck in local minima, and convergence is very fast.

However, due to stochasticity of the method and to the guided parameters, we need to make several runs... 

Encoding is not always suitable: to have high precision, we need very long binary string... So we need another encoding !

Take an encoding that is smart (for instance floating point encoding !)
