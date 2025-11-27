Fitness proportionnal -> fitness must be positive ! (Don't hesitate to add some constant value C to render fitness positive !)

== Rank selection

Rank population

Good approach to overcome the limitations of proportionate fitness selection.

Then probability to take individual depend on rank and not on fitness.

Parameter $beta$ controls the slope, so the selection pressure of the selection.

$beta = 1$ is uniform selection: no pressure !

$beta <= 2$ to have $p_n > 0$

== Tournament selection

Consist to pick $k$ individuals at random and take the highest fitness individu, and repeat the process n times.

One iteration of tournament works like that:
  
- ${x_1, ..., x_i, ..., x_j, ..., x_n}$
- $f(x_j) > f(x_i) =>$ keep $x_j$ and reject $x_i$

FPS: fitness proportionate selection

== Takeover time

It's a theoretical concept defined as the number of rounds of selection required (without crossover and mutation) to have the best individual taking over the entire selected population.

So time required with only selection to have a selected population composed only by best individual.

It's a measure of selection intensity

In general, $tau = n / 2$.

$m(t + 1) = $ number of copies of the best individual at generation $t + 1$.

$(d m) / (d t) = underbrace(alpha, "initial exp grouth") m (underbrace(1 - m / n, "late limitations of the carrying capacity of the system"))$

$1 - m / n$: this term gains more and more influence as m grows...

After computations, $tau = O(ln n)$. Important result in relation with the size of the population for GA....
This explain why taking $n$ around few hundreds is sufficient in general...

== Crossover approaches

- 2-point crossover
- uniform crossover: taking bit by bit and flip it according to probability.
  Sometimes, it can be excessive since each bit don't have same importance...

QAP: quadratic Assignment Problem

Be careful ! Sometimes, crossover give a non-admissible solution !

== Mutation operator

Basic swaps that have been considered in previous chapters...
- swapping 2 cities
- swapping 2 segments
- movement of single city

This is small minor changes to the "genetic material" (encoding of the solution)

Both crossover and selection are VITAL for GAs.

Case continuous... Depending on the function, the crossover can works or not make anything...

For such real continuous optimization problems, the particular encoding chosen is going to render the crossover ineffective.

We don't need the function, we only need the computation of the function...

== Schema theorem

Goal is to explain why it is working...

Central idea: bits motifs (each bit don't have same importance...)

For instance, there is some good schema in individus that contain part of optimal solution...
GA are good to extract good schema, amplify them...

A schema represents a subset of bit-strings in search space. Ex: $0*1**1*0$

A schema represents a hyperplane.
It's a subset of the search space.

Order of schema is number of $*$ that the schema contains.

Length: length between 2 extrema fixed points.
