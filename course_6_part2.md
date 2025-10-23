# Population metaheuristic

Based on ant colony optimization first introduced by marco dorigo in 1991

ant colony metaheuristics is inspired from entomology (science of insects) and ethology (science of animal behavior)

We are looking for a group of agents that acts efficiently together !!!

Ants are very good at minimizing

Find food is costly => find strategy to avoid to die !!!

We are not useful to ants, but ants are useful to us... If we die, ants are good, and if ants die, we are bad...

Ants are very numerous => importance of number

swarm intelligence (intelligence d'essaim)

importance: not individual capabilities but how they act together !!! (from simplicity to complexity)
 => swarm intelligence: not stored in brain of an individual element, but in the entire group

swarm intelligence => distributed intelligence

distributed information processing system

Collaboration can solve problems that single elements can't

Hallmark of complex systems: "the whole is more than the sum of its parts"

- lack of central controller => decentralized operations
- repeated local actions => global outcome => solution to a problem !!!
- collective behaviors are emergent properties
- This so-called self-organization is paradigmatic or complex systems

Through repeated local interactions, there's emergence of a global scale (macroscopic) ordering of the system.

## Benefits of a group

- robustness: if 1 ant die, the others, will not be stopped => no central element, no leader !
- scalability: we can add more birds or more fish to a group and it will continue to work ! (no human system like this !!!)
- adaptivity: (it's a word for intelligence) system can adjust and continue to operate in presence of new constraints or dynamic changes

swarm intelligence is part of AI !!!
AI is more than just deep learning !!!

## Ant colony optimization

- excellent to solve a range of combinatorial optimization problems (QAP, routing, sorting, etc...)
- key ingredient: fictitious pheromones that promote deeper exploration of some promising regions of the search space !!

Ants: 
- they take random path at the begining
- finally, they find best path thanks to pheromones that are more stark on shortest path because less evaporated.

To have coordination, we need interaction between agents...Without interaction, no coordination !!!
In ant case, they make it indirectly !! => this is called stigmergy: indirect coordination among agents...(ex: wikipedia)

chemotaxis: ants perceive the strength of the smell (concentration in pheromone) and move toward the higher concentration area
A central element is evaporation time => limit duration of action of those pheromone trails (in Tabu Search: tenure time !!)
This balance exploration and exploitation !!!

Initial: pure exploration 
After short time: begin to exploit
Eventually: high exploitation

