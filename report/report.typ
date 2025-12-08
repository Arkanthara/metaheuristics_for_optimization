// Main report file
#import "template.typ": make-report, report-footnote
#import "metadata.typ": my-report
#import "@preview/theofig:0.1.0": definition
// #import "@preview/codly:1.3.0": *
// #import "@preview/codly-languages:0.1.1": *
// #show: codly-init.with()

// Main content
#show: make-report.with(my-report)

= Introduction
(0.25)
- Problem Introduction
- Search space
- Fitness
- Population Alg (selection, crossover, mutation) (idea behind)

#pagebreak()

= Methodology
(1.0)
- Initial Population
- selection
- crossover
- mutation
- validity $*$

#pagebreak()

= Implementation
(1.5)
- What are you doing to do with the parameters ?
- Pseudo-code

#pagebreak()

= Results
(1.0)
Explored variations of parameters

#pagebreak()

= Discussion
(2.0)
- Pm, Pc, Iterations
- Population Size, Tournament Size
- Program length, variable length (what must we change if program is not fixed size ??? theoretical... No need to implement it...)

#pagebreak()

= Conclusion
(0.25)