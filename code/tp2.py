import numpy as np
import argparse
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import time
import os


class SA:
    def __init__(self, cities: np.ndarray) -> None:
        self.cities = cities[:, 1:].astype(float)
        self.cities_names = cities[:, 0]
        self.num_cities = cities.shape[0]

    def _cost(self, path: np.ndarray) -> float:
        assert len(path.shape) == 1, f"Path must be 1D ! Actual: {path.shape}"
        shift = np.roll(path, 1)
        return np.linalg.norm(self.cities[path] - self.cities[shift], axis=1).sum()

    def _swap(self, path: np.ndarray, i: int, j: int) -> np.ndarray:
        swap_path = path.copy()
        swap_path[i], swap_path[j] = swap_path[j], swap_path[i]
        return swap_path

    def permute(self, path: np.ndarray) -> np.ndarray:
        i, j = np.random.choice(len(path), size=2)
        return self._swap(path, i, j)

    def greedy(self) -> tuple:
        path = [np.random.choice(np.arange(self.num_cities).astype(int))]
        for i in range(self.num_cities - 1):
            distance = np.linalg.norm(self.cities - self.cities[path[i]], axis=1)
            distance[path] = np.inf
            path.append(np.argmin(distance))
        return np.array(path), self._cost(np.array(path))

    def init_temperature(self, path: np.ndarray, threshold: float = 0.5) -> float:
        cost = self._cost(path)
        delta = []
        for _ in range(100):
            delta.append(self._cost(np.random.permutation(self.num_cities)) - cost)
        return -np.mean(np.abs(delta)) / np.log(threshold)

    def simulated_annealing(
        self,
        threshold: float = 0.5,
        T_schedule: float = 0.9,
        enhanced_mode: bool = False,
    ) -> tuple:
        if enhanced_mode:
            path, _ = self.greedy()
        else:
            path = np.random.permutation(self.num_cities)
        current = path
        delta = []
        accepted = 0
        attempted = 0
        freezing = 0
        cost_improvment = False
        best_cost = self._cost(current)
        best_path = path
        iter = 0
        list_cost = [best_cost]

        # Initialize temperature
        T = self.init_temperature(path, threshold)
        T_0 = T
        delta = 0
        current = path

        # Stopping condition
        while freezing <= 3:
            # Equilibrum conditions
            if attempted >= self.num_cities * 100 or accepted >= self.num_cities * 12:
                if cost_improvment:
                    freezing = 0
                else:
                    freezing += 1
                cost_improvment = False
                attempted = 0
                accepted = 0
                T *= T_schedule

            # Choose new path
            new_path = self.permute(current)
            delta = self._cost(new_path) - self._cost(current)
            if delta <= 0:
                current = new_path
                accepted += 1
                list_cost.append(self._cost(current))

            # Metropolis rule
            elif np.random.rand() < np.exp(-delta / T):
                current = new_path
                accepted += 1
                list_cost.append(self._cost(current))

            attempted += 1

            # Update best solution
            if self._cost(current) < best_cost:
                cost_improvment = True
                best_cost = self._cost(current)
                best_path = current.copy()

            iter += 1

        return best_path, iter, best_cost, T_0, list_cost

    def generate_T_factors(self, M: int = 4, type: str = "linear") -> np.ndarray:
        x = np.arange(1, M + 1)

        if type == "linear":
            return x / x.max()
        elif type == "quad":
            quad = x**2
            return quad / quad.max()
        elif type == "exp":
            exp = np.exp(x)
            return exp / exp.max()
        elif type == "log":
            log = np.log(x)
            return log / log.max()
        else:
            print(f"{type} is not a valid type ! Default is 'linear'")
            return x / x.max()

    def swap_temperature(self, paths, T) -> np.ndarray:
        costs = [self._cost(path) for path in paths]
        for i in range(len(T) - 1):
            delta = (costs[i] - costs[i + 1]) * (1 / T[i] - 1 / T[i + 1])
            if delta < 0:
                paths[i], paths[i + 1] = paths[i + 1], paths[i]
                i += 1
            elif np.random.rand() < np.exp(-delta):
                paths[i], paths[i + 1] = paths[i + 1], paths[i]
                i += 1
        return paths

    def parallel_tempering(
        self,
        max_iter: int = 10000,
        M: int = -1,
        type: str = "exp",
        threshold: float = 0.5,
        swap_frequencie: int = 100,
        enhanced_mode: bool = False,
    ) -> tuple:
        if M == -1:
            M = int(np.sqrt(self.num_cities))
        if enhanced_mode:
            paths = np.array([self.greedy()[0] for _ in range(M)])
        else:
            paths = np.array([np.random.permutation(self.num_cities) for _ in range(M)])
        list_cost = [[self._cost(path)] for path in paths]
        best_cost = np.min(list_cost)
        best_path = paths[np.argmin(list_cost)].copy()
        iter = 0
        T_0 = 0

        # Initialize temperature
        T = self.init_temperature(paths[0], threshold) * self.generate_T_factors(
            M, type
        )
        T_0 = T[-1]
        delta = 0

        # Stopping condition
        for i in range(max_iter):
            for j in range(M):
                # Choose new path
                new_path = self.permute(paths[j])
                delta = self._cost(new_path) - self._cost(paths[j])
                if delta <= 0:
                    paths[j] = new_path
                    list_cost[j].append(self._cost(paths[j]))

                # Metropolis rule
                elif np.random.rand() < np.exp(-delta / T[j]):
                    paths[j] = new_path
                    list_cost[j].append(self._cost(paths[j]))

                cost = self._cost(paths[j])
                if cost < best_cost:
                    best_cost = cost
                    best_path = paths[j].copy()
                    iter = i

            # Change temperature according to cost
            if i % swap_frequencie == 0:
                paths = self.swap_temperature(paths, T)

        return best_path, iter, best_cost, T_0, list_cost

    def graph(
        self,
        path: bool = False,
        title: list[str] = ["Greedy", "Simulated Annealing", "Parallel Tempering"],
        pt_type: str = "exp",
        enhanced_mode: bool = False,
        threshold: float = 0.5,
        T_schedule: float = 0.9,
    ):
        rounded = 4
        x = self.cities[:, 0]
        y = self.cities[:, 1]

        def plot_cities(fig, x, y, title: str):
            fig.add_trace(
                go.Scatter(
                    x=x,
                    y=y,
                    name="cities",
                    mode="markers",
                    # Plot cities name
                    # mode="markers+text",
                    # text=self.cities_names,
                    # marker=dict(size=15, color="plum"),
                )
            )
            fig.update_layout(
                title=title, xaxis=dict(scaleanchor="y"), yaxis=dict(scaleanchor="x")
            )
            fig.show()

        def subplot(rows: int = 2, cols: int = 2):
            if rows == 2:
                specs = [
                    [{"type": "domain"}, {"type": "xy", "rowspan": 2}],
                    [{"type": "domain"}, None],
                ]
                return make_subplots(
                    rows=rows,
                    cols=cols,
                    column_widths=[0.5, 0.5],
                    row_heights=[0.72, 0.28],
                    specs=specs,
                )
            else:
                specs = [[{"type": "domain"}, {"type": "xy"}]]
                return make_subplots(
                    rows=rows,
                    cols=cols,
                    column_widths=[0.5, 0.5],
                    specs=specs,
                )

        if path:
            if len(title) != 3:
                print("Don't forget to set titles !")
                title = ["Greedy", "Simulated Annealing", "Parallel Tempering"]
            list_result = []
            list_cost = []
            list_time = []
            for _ in range(10):
                start = time.time()
                result, cost = self.greedy()
                end = time.time()
                result = np.append(result, result[0])
                list_result.append(result)
                list_cost.append(cost)
                list_time.append(end - start)
            greedy_result = list_result[np.argmin(list_cost)]
            greedy_cost = np.mean(list_cost)
            greedy_time = np.mean(list_time)

            list_result = []
            list_iter = []
            list_cost = []
            list_T = []
            list_time = []
            list_trace = []
            for _ in range(10):
                start = time.time()
                result, iter, cost, T, trace = self.simulated_annealing(
                    threshold=threshold,
                    T_schedule=T_schedule,
                    enhanced_mode=enhanced_mode,
                )
                end = time.time()
                result = np.append(result, result[0])
                list_result.append(result)
                list_cost.append(cost)
                list_iter.append(iter)
                list_T.append(T)
                list_trace.append(trace)
                list_time.append(end - start)
            sa_result = list_result[np.argmin(list_cost)]
            sa_cost = np.mean(list_cost)
            sa_iter = np.mean(list_iter)
            sa_T = np.mean(list_T)
            sa_time = np.mean(list_time)
            sa_trace = list_trace[np.argmin(list_cost)]

            list_result = []
            list_iter = []
            list_cost = []
            list_T = []
            list_time = []
            list_trace = []
            for _ in range(10):
                start = time.time()
                result, iter, cost, T, trace = self.parallel_tempering(
                    threshold=threshold,
                    type=pt_type,
                    enhanced_mode=enhanced_mode,
                    max_iter=20000,
                )
                end = time.time()
                result = np.append(result, result[0])
                list_result.append(result)
                list_cost.append(cost)
                list_iter.append(iter)
                list_T.append(T)
                list_time.append(end - start)
                list_trace.append(trace)
            pt_result = list_result[np.argmin(list_cost)]
            pt_cost = np.mean(list_cost)
            pt_iter = np.mean(list_iter)
            pt_T = np.mean(list_T)
            pt_time = np.mean(list_time)
            pt_trace = list_trace[np.argmin(list_cost)]

            fig = make_subplots(
                rows=1,
                cols=2,
                subplot_titles=("Simulated Annealing", "Parallel Tempering"),
                # column_widths=[0.5, 0.5],
                # specs=[[{"type": "domain"}, {"type": "xy"}]],
            )
            fig.add_trace(
                go.Scatter(
                    x=np.arange(len(sa_trace)),
                    y=sa_trace,
                    mode="lines",
                    showlegend=False,
                ),
                row=1,
                col=1,
            )
            fig.update_xaxes(title_text="Number of iterations", row=1, col=1)
            fig.update_yaxes(title_text="Fitness", row=1, col=1)
            for i in range(len(pt_trace)):
                fig.add_trace(
                    go.Scatter(
                        x=np.arange(len(pt_trace[i])),
                        y=pt_trace[i],
                        mode="lines",
                        name=f"T<sub>{i}",
                    ),
                    row=1,
                    col=2,
                )
            fig.update_xaxes(title_text="Number of iterations", row=2, col=1)
            fig.update_yaxes(title_text="Fitness", row=2, col=1)
            fig.show()

            fig = subplot(rows=1)
            fig.add_trace(
                go.Table(
                    header=dict(values=["Attribute", "Value"]),
                    cells=dict(
                        values=[
                            ["Best fitness", "Execution time (s)"],
                            [
                                round(greedy_cost, rounded),
                                round(greedy_time, rounded),
                            ],
                        ],
                        align=["left", "right"],
                        height=30,
                    ),
                ),
                row=1,
                col=1,
            )
            fig.add_trace(
                go.Scatter(
                    x=self.cities[greedy_result, 0],
                    y=self.cities[greedy_result, 1],
                    mode="lines",
                    line=dict(color="plum"),
                    name="path",
                )
            )

            fig.update_xaxes(
                title_text=f"Fitness: {np.round(self._cost(greedy_result[:-1]), 4)}",
                row=1,
                col=2,
            )
            plot_cities(fig, x, y, title=title[0])

            fig = subplot()
            fig.add_trace(
                go.Table(
                    header=dict(values=["Attribute", "Value"]),
                    cells=dict(
                        values=[
                            [
                                "Best fitness",
                                "Number iteration",
                                "Initial temperature",
                                "Enhanced mode",
                                "Initial acceptance rate",
                                "Temperature schedule",
                                "Execution time (s)",
                            ],
                            [
                                round(sa_cost, rounded),
                                sa_iter,
                                round(sa_T, rounded),
                                enhanced_mode,
                                f"{int(100 * threshold)}%",
                                f"T<sub>k+1</sub> = {T_schedule} T<sub>k</sub>",
                                round(sa_time, rounded),
                            ],
                        ],
                        align=["left", "right"],
                        height=30,
                    ),
                ),
                row=1,
                col=1,
            )
            fig.add_trace(
                go.Table(
                    header=dict(values=["Attribute", "Greedy", "PT"]),
                    cells=dict(
                        values=[
                            [
                                "Execution time ratio",
                                "Fitness ratio",
                            ],
                            [
                                round((greedy_time) / sa_time, rounded),
                                round((greedy_cost) / sa_cost, rounded),
                            ],
                            [
                                round((pt_time) / sa_time, rounded),
                                round((pt_cost) / sa_cost, rounded),
                            ],
                        ],
                        align=["left", "right"],
                        height=30,
                    ),
                ),
                row=2,
                col=1,
            )
            fig.add_trace(
                go.Scatter(
                    x=self.cities[sa_result, 0],
                    y=self.cities[sa_result, 1],
                    mode="lines",
                    line=dict(color="plum"),
                    name="path",
                )
            )
            fig.update_xaxes(
                title_text=f"Fitness: {np.round(self._cost(sa_result[:-1]), 4)}",
                row=1,
                col=2,
            )
            plot_cities(fig, x, y, title=title[1])

            fig = subplot()
            fig.add_trace(
                go.Table(
                    header=dict(values=["Attribute", "Value"]),
                    cells=dict(
                        values=[
                            [
                                "Best fitness",
                                "Number iteration",
                                "Initial temperature",
                                "Temperature schedule type",
                                "Enhanced mode",
                                "Initial acceptance rate",
                                "Execution time (s)",
                            ],
                            [
                                round(pt_cost, rounded),
                                pt_iter,
                                round(pt_T, rounded),
                                pt_type,
                                enhanced_mode,
                                f"{int(100 * threshold)}%",
                                round(pt_time, rounded),
                            ],
                        ],
                        align=["left", "right"],
                        height=30,
                    ),
                ),
                row=1,
                col=1,
            )
            fig.add_trace(
                go.Table(
                    header=dict(values=["Attribute", "Greedy", "SA"]),
                    cells=dict(
                        values=[
                            [
                                "Execution time ratio",
                                "Fitness ratio",
                            ],
                            [
                                round((greedy_time) / pt_time, rounded),
                                round((greedy_cost) / pt_cost, rounded),
                            ],
                            [
                                round((sa_time) / pt_time, rounded),
                                round((sa_cost) / pt_cost, rounded),
                            ],
                        ],
                        align=["left", "right"],
                        height=30,
                    ),
                ),
                row=2,
                col=1,
            )
            fig.add_trace(
                go.Scatter(
                    x=self.cities[pt_result, 0],
                    y=self.cities[pt_result, 1],
                    mode="lines",
                    line=dict(color="plum"),
                    name="path",
                )
            )
            fig.update_xaxes(
                title_text=f"Fitness: {np.round(self._cost(pt_result[:-1]), 4)}",
                row=1,
                col=2,
            )
            plot_cities(fig, x, y, title=title[2])
        else:
            fig = go.Figure()
            plot_cities(fig, x, y, title=title[0])


def benchmark(num_city: int) -> np.ndarray:
    coordinates = 2 * np.pi * np.arange(num_city) / num_city
    return np.array(
        [np.arange(num_city).astype(int), np.cos(coordinates), np.sin(coordinates)]
    ).T


if __name__ == "__main__":
    # Create argument parser
    parser = argparse.ArgumentParser(description="TP3 - Traveling Salesman Problem")

    # Add arguments
    parser.add_argument(
        "-b",
        "--benchmark",
        help="Benchmark problem of N cities (trivial solution for humans !)",
    )
    parser.add_argument(
        "-r",
        "--random",
        help="Random problem of N cities",
    )
    parser.add_argument(
        "-d",
        "--datafile",
        help="Path to data file for problem with given data",
    )
    parser.add_argument(
        "-t",
        "--threshold",
        help="Acceptance rate of algorithms. Default is 50%%",
        default="0.5",
    )
    parser.add_argument(
        "-p",
        "--progression_type",
        help="Progression type of the sequence of factors for temperature in parallel tempering ('linear', 'quad', 'exp', 'log'). Default is 'quad'",
        default="quad",
    )

    # Parse arguments
    args = parser.parse_args()

    if args.benchmark:
        test = SA(benchmark(int(args.benchmark)))
        test.graph(
            path=True,
            threshold=float(args.threshold),
            T_schedule=0.9,
            pt_type=args.progression_type,
            title=[
                f"Benchmark: greedy for {args.benchmark} cities",
                f"Benchmark: simulated annealing for {args.benchmark} cities",
                f"Benchmark: parallel tempering for {args.benchmark} cities",
            ],
        )

    if args.random:
        test = SA(np.random.rand(int(args.random), 3))
        test.graph(
            path=True,
            threshold=float(args.threshold),
            T_schedule=0.95,
            pt_type=args.progression_type,
            title=[
                f"Random: greedy for {args.random} cities",
                f"Random: simulated annealing for {args.random} cities",
                f"Random: parallel tempering for {args.random} cities",
            ],
        )
    if args.datafile:
        data = np.genfromtxt(args.datafile, dtype=str)
        test = SA(data)
        test.graph(
            path=True,
            threshold=float(args.threshold),
            T_schedule=0.95,
            pt_type=args.progression_type,
            title=[
                f"{os.path.basename(args.datafile)}: greedy for {data.shape[0]} cities",
                f"{os.path.basename(args.datafile)}: simulated annealing for {data.shape[0]} cities",
                f"{os.path.basename(args.datafile)}: parallel tempering for {data.shape[0]} cities",
            ],
        )
