// Main report file
#import "template.typ": create-report-template

// Configure your report
#let my-report = create-report-template(
  // Required information
  logo: "./img/unige.pdf",
  logosize: 6cm,
  university: "University of Geneva",
  title: "Series 7: Genetic Programming",

  // Structured authors
  authors: (
    (
      name: "Michel Jean Joseph Donnet",
    ),
  ),

  // Optional information
  faculty: "Faculty of Science",
  // subtitle: "Report Subtitle",
  course-name: "Metaheuristics for Optimization",
  course-id: "14x013",
  illustrations: (
    (
      path: "./img/mutation.png",
      width: 11cm,
    ),
  ),
  //   (
  //     path: "./img/full_hist_R.png",
  //     width: 10cm,
  //   ),
  // ),
  project-name: "Metaheuristics for Optimization",
  date: none,

  // Document options
  toc: true,
  numbering: true,
  bibliography: none,
  appendix: false,
)
