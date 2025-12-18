SAT: try to define assignation that minimize problem (ex: backpack problem)

Get a sense of how the solutions are distributed in the search space

Minimize the energy like in physics !

A XOR B <=> A + B modulo 2 !

Problem not satisfiable => energy is 1 !

We need to choose between one constraint or another constraint ...

How to go from unsatisfiable problem to satisfiable problem ?

XORSAT is not a difficult problem: we can convert it to matrix and then there exists algorithms that are in polynomial time...

However, polynomial time can switch to exponential time depending on hardness of the problem (phase transition)

cal(N) has to be large enough to be statisticaly significant...

Sample large enough to have good statistics !

With a tree, problem is satisfiable

With a forest, problem is always satisfiable

With cycles, problem can becomes unsatisfiable...

=> check how many edges are 1 (because it flip values => even number of 1 give satisfiable problem)

So adding more edge to a graph create more cycles and the problem becomes unsatisfiable...

If degree of graph is less than 1, we have only forest and trees !

If we have giant components, we can have cycles

Rank of matrix: how many rows are independent from each others ??
