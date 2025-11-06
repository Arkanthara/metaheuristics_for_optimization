= Particle Swarm Optimization (PSO)

- Used for continuous optimization problems
- Birds mostly use vision. They look to 6 or 7 neighbors
- Fish use vision + lateral line sensing

AAA:
- Attraction (group cohesion)
- Avoidance (to ensure exploration... Safe zone around agents)
- Alignment (ex: cows follow the first... To many alignment)

== Principes

- Swarm intelligence: inspired by collective behavior of social animals where simple agents coordinate to achieve complex group behavior.
- Population based metaheuristic
- Balance between two competing behaviors:
  - track the top/best individual of the group
  - blabla

== Algorithm

Based on particles with a mechanistic viewpoint
However:
- point particles
- no dimension
- no collision
- no problem to dwel at the same location

The search space is the physical search space (2D, 3D, ND, ...)
Particles move with a given velocity. This is the core of PSO
Each element of the search space is a possible solution

=== Local best

Individual memory: at each iteration $t$, we update so-called particle-best or local-best
We go on a better place or we come back to our place

=== Global best

Attraction towards the global best:

- best overall fitness found up to iteration $t$ by the entire population of artifacts

- Social behavior ??? Yes, because of information sharing:
  - particles share information indirectly by broadcasting their best found solutions
  - allowing the swarm to converge toward promising regions (convergence is fast)

They are not decentralized: all-to-all connection

Discuss with all other particles ??? Not relevant because 

==== Components

- Personal experience
- Social experience
- Inertia (how much you want to go out of your way)

This give a rule of update of the particle !

==== Position

$v_i(t + 1) = \frac{x_i(t + 1) - x_i(t)}{\Delta t}$

$\Delta t = 1$ !!!

==== Velocity

$v_i(t + 1) = \underbrace{\omega}_{\text{inertia}}v_i(t) + \underbrace{\underbrace{c_1r_1(t + 1)}_{\text{weight}}[x_i^{\text{best}}(t) - x_i(t)]}_{\text{personal best}} +  \underbrace{c_2r_2(t + 1)[B(t) - x_i(t)]}_{\text{Global best}}$

$\omega, c_1, c_2$ are constant parameters to be specified
$r_1, r_2$ are random number. It allows stochasticity and promote exploration by modify the way the three components are combined

- No explicit concept of neighborhood
- But there's still exploration along the way through $r_1$ and $r_2$.

==== Guiding parameters

- $c_1$: cognitive coefficient (it's a kind of instinct)
- $c_2$: social coefficient
- Classically, $c_1 \approx c_2 \approx 2$, "Vanilla-flavor" PSO
- $\omega$: inertia (in general, less than $1$)

==== Notes

- impose bounds on absolute value of position and velocity
- prescribe maximum velocity (avoid too large velocities)
- prescribe position boundary
  - periodic boundary condition
    - particle direction is unchanged
    - keep same number of particles
    - impression of infinity
  - hard collisions (symmetric collisions)
    - introduce a little bit of randomness
    - change in direction of the velocity adds to the exploration behavior
    - keep in mind that theses collisions are purely border effects, so less prevalent than velocity update of the core

==== Remarks

- like Ants System, PSO is a population-based metaheuristic: create a set of solutions to a new generation of set of solutions.
  So it is straight forward to parallelize.
  Lot of variants
  In some variant, group of particles and they share informations when they meet themselves

- convergence: zero convergence proof ! But in general, PSO is characterized by rapid convergence speed
- implementation: super easy to implement
- balance between exploration and exploitation is based on the randomness and inertia in velocity update

There is a dynamic leadership

We have a cluster of particles around the maximum...


