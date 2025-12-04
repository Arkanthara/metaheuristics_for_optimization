Isolation of sub-populations can sometimes have surprising effects...

Concept of Advanced GA compared to the original Vanila-flavor GA: population with given structure...

Multi-populations GA (some island with population evolving inside... Then some mix-up between good individus)

Network GA. Hub selection...
topological interaction reflect the topology/structure of the network...
Each individu can interact with others...
Overall, we add more possibilities for the construction of GA.
This add some guided parameters to properly define...

A metaheuristic that is simple is a good thing

ring of connection: interact with neighborhood (with second neighborhood etc...)
simple way to account blablabla

Multi-populations

- rapid convergence
- Better diversity (local exploration at this island level + global exploitation by cross fertilization accross all islands...)

Note: system plateauing: diminishing return !

== Genetic Programing (GP)

Genetic algorithm applied to computer programs

Population based metaheuristic

Unsupervised fashion

symbolic regression: search for an expression that describe the function..
SR search over vast space of all possible symbolic  expressions...

interpretability/explainability (different from machine learning...)
We fully understand how the output program works
BUT we don't understand how EXACTLY the program was built.

automatic feature construction: related to schema theorem !

Behavior inference (like Reinforcement learning: example: we try to walk... At the begining we fall and finally we can walk, run etc...)

Program coding: how we form our genetic material

Tree based encoding
Stack based linear program (procedural programming)

This two approaches are equivalent !

Only requirement is that we can compute the fitness !!! (most central requirement for any metaheuristics !)

Unsupervised because no informations on what the function should be !

Cannot use any kind of programming languages !!! Use functional languages like Lisp
We want to manipulate expressions...
It is all based on representations...
Computer can represent same program in different ways...

Closure property: limit expressions to semantically correct expressions !

Root level: bias for functions: higher probability to choose a function
Leaf level: bias for terminals: higher probability to choose a terminal

Mutation: replace subroutine by another subroutine of approximatively the same size...
It is generated randomly from terminal and functions...

Example: search of optimal trading model (conversion d'argent entre differentes monaies...)

Stack based linear GP
non-procedural language: SQL ... procedural language (C, python, ...)

The operations must be adapted...
If an argument is missing, we do nothing
If the operation is invalid, we do nothing
