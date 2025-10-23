Not too high => may not converge !!!
Too high => too many computations !!!

MonteCarlo Markov Chain probability to go from a point to another
(Simulated Annealing is hidden behind probability)
Jumps are independent 
So how dependent is it to initial position

Temperature depends on the problem !!!

Markov chains are memoryless

Temperature schedule: has impact on convergence !!!
T(t + 1) t + 1: new stage (because already enough node visited or enough try made)

not enough iterations to have probability to go on local minimum around 0...

Bringing the temperature too fast will increase the probability to go on local minimum !!!

Recipe:

general problems
- problem coding
- choice of elementary moves

specific to SA
- $\Delta E$ following a move must be easily computed
- possible constraints must either be easily translated into restrictions on the moves, or implemented by adding a suitable positive penalization term of the fitness
- choice of initial configuration

temperature choice in practice: get 100 iterations and take average $\Delta E$ with random points choosen. Then compute temperature according to threshold $\tau_0$

Standard deviation must be reasonable => if 100 iterations are not sufficient, take more !!!

$e^{-\frac{\Delta E}{T_0}} = \tau_0 = \frac{1}{2}$ => I choose to accept 50% of the moves !!!

How to define the cooling schedule ?? => in general, geometric law...

How to define equilibrium state ??

How to define stopping criteria ??

Consistencies in value obtained -> redo experiment for X different initial configurations !!!!
=> there is a cost to validation and statistical consistency !!!

Ne pas faire confiance aux random-number-generators !!! Ils sont en général pseudo-aléatoires !!

Couple metaheuristic to classical optimization technique !!!

## Parallel Tempering

Heat up and cool down multiple times !!!!

MonteCarlo -> stochastic !!!

Idea: avoiding to getting stuck in a local minimum !!!
=> allows fitness degradation !!!
=> same use of metropolis rule !!
PT vs SA: PT: we keep same temperature !!! SA: Temperature decrease !!

Parallel exploration with different fixed temperatures.... We swap between 2 replicas 

For swapping: $P = min(1, e^{\Delta_{ij}}) = min(1, e^{(E_i - E_j)(\frac{1}{T_i} - \frac{1}{T_j})})$

Statistically, good solutions will gradually travel from one replica to another.

=> balance exploration vs exploitation !!!! achieved by configuration swapping.

guiding parameters SA: T and T schedule !!!

guiding parameters PT: number of replicas M (in general $\sqrt{N}$), configuration swapping frequency, sequence of temperatures
