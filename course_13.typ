Result depend on initial population and stochasticity

symbolic regression (try to find expression that represent the plot)

If too big dataset -> could not converge !!! => very challenging to make it working !!!

Flow control: need to supplement the data stack with a control stack

= Chapter 8: performance of metaheuristics

Goal: general way to analyze expectations in term of performance

metaheuristic algorithm working very well on big TSP is a strong algorithm ! But not means that it will work as good on other problems... 

We tune exploration and exploitation indirectly through parameters !!!

Must increase size of problem to see if metaheuristic works !!! Change in complexity regime for bigger problems !!!

Diminishing returns

Trying to have much probability of success require more fitness evaluation

=> Looking at good enough solution

=== Summary of key concepts for performance analysis 

- benchmark: true for all algorithms
  - evalutate
  - comparisons It's essential to test a metaheuristic in comparisons to other metaheuristics.
  ! There is no better algorithm than another !!!
- based on
  - real-life problems: real problem of interest
  - synthetic problems: TSP/NK-landscape

!!!! No universal metric to measure performance !!!

Use computation counts instead of wall-clock time !!!!

No-free-lunch: all metaheuristics will outperform another one for a given problem...
Not practical because don't tell us which one is better for given problem

-> never consider only 1 problem !

All points from specific solution to result is called trajectory

Taking all trajectory + average => A is equivalent to B...

In general, metaheuristics outperform our attempts

But for one particular problem, one can be better than another...
