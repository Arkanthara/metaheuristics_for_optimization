= PSO

- Naturally, PSO is used to solve CONTINUOUS optimization problems
- However, extension to discrete optimization problems can be obtained
- A number of variants for combinatorial optimization problems have been developped

- First quality of PSO is very easy to implement
- Second quality is convergence which is fast: low cost

= Firefly algorithm

- developped in 2009
- largly inspired by PSO
- success with hard optimization problems, but still limited in terms of working with general problems
- biological inspiration
  - flashing behavior of fireflies with light intensity that attract others
  - emit light to attract mates or preys and degree of attraction is proportional to the intensity of the light source
- We consider a formulation for continuous optimization but discrete version exists

== Principes

- Population of $N$ fireflies
- Each firefly $i$ represent a candidate solution in the search space $S$
- Fitness function:
  - Each firefly $i$ emits light with intensity $I_i$ that depends on the value $f(x_i)$ (that is proportional to the intensity $I_i$)
  - For a maximization problem, we consider $f(x_i(t)) = I_i$
- Attractiveness proportional to the brightness (reminiscent of the global best with PSO... It's the social information):
  - fireflies are attracted to others that are brighter
  - attractiveness decreases with distance and light absorption
- At each iteration $t$, we inspect all firefly pairs $(i, j)$ with $1 <= i <= n$ and $i < j <= n$, given a population of $n$ fireflies.
  - If $I_i < I_j$ (from the perspective of firefly $i$: it seeks fireflies that are brighter)

== Attractiveness

$beta = beta_0 e^(- gamma r_(ij)^2)$

- $beta_0$: initial attractiveness
- $r_(ij)$: distance between $x_i$ and $x_j$
- $gamma$: tune balance between exploration and exploitation
  - $gamma r_(ij)^2$ is with no dimensions, so $gamma$ dimension is $1 / r_(ij) = m^(-2)$
    - small $gamma << 1$: exploration (far away informations coming to the firefly !). Broad seach across the entire search space !
    - large $gamma >> 1$: exploitation. Light is quickly absorbed !
#note[Choice of gamma is important to ensure a balance behavior !]

If I take a function that decrease linearly, I will explore all the time because of all informations coming all the time !
- rapid decrease of $beta$ with distance !
- avoid attracting fireflies that are too far away !

== Movement Rule

$x_i^("new") = underbrace(x_i, "Current position") + underbrace(beta_0 e^(-gamma r_(ij)^2), "Attractiveness") times underbrace((x_j - x_i), "Distance between the two fireflies") + underbrace(alpha epsilon, "stochastic term")$

$alpha epsilon$: stochastic component
- $alpha$: constant randomization parameter
- $epsilon$: stochastic distribution
  - Uniform distribution
  - Normal distribution $N(0, 1)$
  - Levy distribution: $"Levy"(lambda)$
So it's like a random walk with drift towards good solution

== Random walks

- Brownian motion (jumps or steps given by a Gaussian distribution)
- Levy random walk: if there is no food, we can make big jumps to change region ! (follow power law) Better balance between exploitation and exploration

=== Levy flights

- occasional large amplitude jumps
  - balance between
    - large amplitude jumps: good for high exploratory
    - small amplitude jumps: local exploration enabling intensification/exploitation
- high risk = high returns !! (like in financial systems !)

= Cuckoo search

- developped in 2010
- population-based metaheuristic
- Geared toward continuous optimization
- based on cuckoo biologic

== Principles

- Number of available nests: $n$
- Each cuckoo "lays" a fictitious egg (i.e., a solution $x$) and randomly places it in a given nest (position $i$ in the table)
  - at each iteration, a nest is randomly selected and its solution is modified according to a Levy flight (1st stochastic component): exploratory mechanism
  - This new modified solution is then compared with that of another nest
  - blabla

The quality of a nest is $f(x_i)$: fitness value

- There is a probability $p_a$ which is a stochastic component that the host discovers the egg $=>$ forcing the cuckoo out of the present nest !
  - we then replace a fraction $p_a$ of nests among those that contain the worst solutions by new nests chosen at random according to Levy flight

Just like PSO and Firefly, Cuckoo Search (CS) give a rapid convergence
$p_a$: guiding parameter that control how many worst solutions will be replaced
There is an analogy between $p_a$ for CS and T for SA.

= Evolutionary Algorithms

It's a family of metaheuristics

== Introduction

- Stochastic population-based metaheuristic introduced in the 70s
- Based on concept of Darwinian evolution: natural selection of survival of the fitness (fitness and not cost function !)
- best individuals mate (selection) and evolve
- Overall components
  - selection: select best guys in a population for reproduction (exploitation)
  - mutation: if no mutation, always same genetic material and no improvements (exploration) 
  - crossover of fittest individuals: amplify mutations that give advantages

- Goal: search for high-quality solutions
- Family of techniques: evolutionary algorithms:
  - Genetic Algorithms (GA - John Holland (amazing computer science scientist))
  - Evolution Strategy (ES)
  - Genetic Programming (GP)

==== Key features of GA

- population-based
- probabilistic operators
- global search capability
- black-box optimization: we only need to be able to compute the fitness function

== Principles

- $N$ individuals candidate solution in the search space
- choice of the representation is important ! We use particular encoding based on principle of genetic. Encoding is genetic material.
  - binary encoding (MaxOne)
  - real value encoding (PSO, FF, CS)
  - permutation encoding (TSP). Highly useful for combinatorial problems
- Maximisation of the fitness !

- random initialization (just like other metaheuristics) This is AFTER choosing a specific encoding of the solution
- loop/iterative process
  - population in each iteration is called a generation (cycle of life ! Parents->child->parents....)
- blabla
- Halting condition is implicitly referring to the choice of a particular halting criterion

==== Balance between exploration and exploitation

- insert best solution in last generation (process of elitism)
- elitism: replace the worst by the better
- population size is kept constant throughout the evolution ($N$ parents generate $N$ children)
