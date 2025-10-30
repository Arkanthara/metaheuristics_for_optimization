# Population methods

## Ant colonny

- Initial, random path
- after a short time: shorter path began to receive more traffic (pheromones)
- ants completing the shorter route returned to the nest faster, hence reinforced that path with pheromone sooner and more frequently

## Economy

Kirman 1993
Modelisation like ants colonny !! For instance, we have 2 apple... Ants will go first to one, then to the other...

## Interpretation ants colonny

initial: choose random path
leave pheromones

## 2 paths identical ???

The ants will finaly use an unique path !!!

## Mathematical model

key assumption: probability of choosing a given branch depends on the total amount of pheromone laid by all ants that traveled that branch since the start of the experiment.

let m denote the number of ants that have already traversed the system, and 


### Parameter $k$ ???

if k >> m, k >> U_m, Lm

$P_U(m + 1) = \frac{(U_m + k)^h}{(U_m + k)^h + (L_m + k)^h}$

$U_m + L_m = m$
$U_{m + 1} = U_m + \delta$
$L_{m + 1} = L_m + (1 - \delta)$

### Parameter h ??

$P_U(m + 1) = \frac{(U_m + k)^h}{(U_m + k)^h + (L_m + k)^h}$

What's happen with $U_m = \frac{m}{2}$ ???

$P_U(m + 1) = \frac{( m / 2 + k)^h}{(m / 2 + k)^h + (m / 2 + k)^h}$

With $U_m = 0$ -> P_U = 0

With $U_m = m$ -> P_U = 1


k bigger, we are closer to 0.5

m is bigger, probability will change quickly

In general, k = 20 and h = 2

Flexible, can be used on each kind of maximisation problems

### TSP

- visibility: $n_{ij} = \frac{1}{d_{ij}}$ when distance is close to $0$, visibility is close to infinity !!!


Ant quantity system
local
useful in dynamic environments
Deposition of pheromones on an edje is $\frac{Q}{d_{ij}}$ or $0$

Ant density:
local
We deposit a fix amount on each edge

Ant cycle system:

Global way to deposit pheromones (because we don't update at each path !!!)
On an edge, we deposit a quantity 

principes

- path is controlled by visibility and pheromone intensity
- pheromone intensity is globally affected
- ??

alpha: exploitation (consider the paths already visited)
beta: exploration

To update pheromones, we decrease current pheromones by evaporation factor and add new pheromones of ants

> [!WARNING]
> Lot of parameters to choose !!!!!!!!!!

Neighborhood ???
Neighborhood are constructed one by one
Not very relevant in this kind of problem

### Variant

probability q0... We are doing exploitation

No alpha parameter because exploitation is choose before in probability...

How we choose the city

How we deposit pheromones ???
We reinforce the best path found !!

### Performances

probability to go left or right depend on quantity of pheromones left on path


