import numpy as np
import matplotlib.pyplot as plt
import argparse
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import time


class SA:
    def __init__(self, cities: np.ndarray) -> None:
        self.cities = cities
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

    def simulated_annealing(self) -> tuple:
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
        T_0 = 0

        # Initialize temperature
        for _ in range(100):
            new_path = self.permute(current)
            cost = self._cost(new_path)
            # index = np.argmin(cost)
            delta.append(cost - self._cost(current))
            current = new_path
        T = -np.mean(np.abs(delta)) / np.log(0.5)
        T_0 = T
        delta = 0
        current = path

        # Stopping condition
        while freezing < 3:
            # Equilibrum conditions
            if attempted >= self.num_cities * 100 or accepted >= self.num_cities * 12:
                if cost_improvment:
                    freezing = 0
                else:
                    freezing += 1
                cost_improvment = False
                attempted = 0
                accepted = 0
                T *= 0.9

            # Choose new path
            new_path = self.permute(current)
            delta = self._cost(new_path) - self._cost(current)
            if delta <= 0:
                current = new_path
                accepted += 1

            # Metropolis rule
            elif np.random.rand() < np.exp(-delta / T):
                current = new_path
                accepted += 1

            attempted += 1

            # Update best solution
            if self._cost(current) < best_cost:
                cost_improvment = True
                best_cost = self._cost(current)
                best_path = current

            iter += 1

        return best_path, iter, best_cost, T_0

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

    def parallel_tempering(
        self, max_iter: int = 10000, M: int = 4, type: str = "linear"
    ) -> tuple:
        paths = np.array([np.random.permutation(self.num_cities) for _ in range(M)])
        current = paths[np.random.randint(len(paths))]
        delta = []
        best_cost = self._cost(current)
        best_path = current
        iter = 0
        T_0 = 0

        # Initialize temperature
        for _ in range(100):
            new_path = self.permute(current)
            cost = self._cost(new_path)
            # index = np.argmin(cost)
            delta.append(cost - self._cost(current))
            current = new_path
        T = -np.mean(np.abs(delta)) / np.log(0.5) * self.generate_T_factors(M, type)
        T_0 = T[-1]
        delta = 0
        cost = np.array([self._cost(path) for path in paths])

        # Stopping condition
        for i in range(max_iter):
            for j in range(M):
                # Choose new path
                new_path = self.permute(paths[j])
                delta = self._cost(new_path) - self._cost(paths[j])
                if delta <= 0:
                    paths[j] = new_path
                    cost[j] = self._cost(new_path)

                # Metropolis rule
                elif np.random.rand() < np.exp(-delta / T[j]):
                    paths[j] = new_path
                    cost[j] = self._cost(new_path)

            # Change temperature according to cost
            index = np.argsort(cost, stable=True)
            cost = cost[index]
            paths = paths[index]

            # Update best solution
            if cost.min() < best_cost:
                best_cost = cost.min()
                best_path = paths[np.argmin(cost)]
                iter = i

        return best_path, iter, best_cost, T_0

    def graph(
        self,
        path: bool = False,
        title: list[str] = ["Greedy", "Simulated Annealing", "Parallel Tempering"],
        max_iter: int = 10000,
        M: int = 4,
        type: str = "exp",
    ):
        rounded = 4
        x = self.cities[:, 0]
        y = self.cities[:, 1]

        def plot_cities(fig, x, y, title: str):
            fig.add_trace(go.Scatter(x=x, y=y, mode="markers", name="cities"))
            fig.update_layout(
                title=title, xaxis=dict(scaleanchor="y"), yaxis=dict(scaleanchor="x")
            )
            fig.show()

        if path:
            if len(title) != 3:
                print("Don't forget to set titles !")
                title = ["Greedy", "Simulated Annealing", "Parallel Tempering"]
            start = time.time()
            greedy_result, greedy_cost = self.greedy()
            greedy_result = np.append(greedy_result, greedy_result[0])
            end = time.time()
            greedy_time = end - start
            start = time.time()
            sa_result, sa_iter, sa_cost, sa_T = self.simulated_annealing()
            sa_result = np.append(sa_result, sa_result[0])
            end = time.time()
            sa_time = end - start
            start = time.time()
            pt_result, pt_iter, pt_cost, pt_T = self.parallel_tempering(
                max_iter, M, type
            )
            pt_result = np.append(pt_result, pt_result[0])
            end = time.time()
            pt_time = end - start
            pt_type = type
            fig = make_subplots(
                rows=1,
                cols=2,
                column_widths=[0.3, 0.7],
                specs=[[{"type": "domain"}, {"type": "xy"}]],
            )
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
            plot_cities(fig, x, y, title=title[0])

            fig = make_subplots(
                rows=1,
                cols=2,
                column_widths=[0.3, 0.7],
                specs=[[{"type": "domain"}, {"type": "xy"}]],
            )
            fig.add_trace(
                go.Table(
                    header=dict(values=["Attribute", "Value"]),
                    cells=dict(
                        values=[
                            [
                                "Best fitness",
                                "Fitness ratio<br>(vs Greedy)",
                                "Fitness ratio<br>(vs PT)",
                                "Number iteration",
                                "Initial temperature",
                                "Execution time (s)",
                                "Execution time ratio<br>(vs Greedy)",
                                "Execution time ratio<br>(vs PT)",
                            ],
                            [
                                round(sa_cost, rounded),
                                round((greedy_cost) / sa_cost, rounded),
                                round((pt_cost) / sa_cost, rounded),
                                sa_iter,
                                round(sa_T, rounded),
                                round(sa_time, rounded),
                                round((greedy_time) / sa_time, rounded),
                                round((pt_time) / sa_time, rounded),
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
                    x=self.cities[sa_result, 0],
                    y=self.cities[sa_result, 1],
                    mode="lines",
                    line=dict(color="plum"),
                    name="path",
                )
            )
            plot_cities(fig, x, y, title=title[1])

            fig = make_subplots(
                rows=1,
                cols=2,
                column_widths=[0.3, 0.7],
                specs=[[{"type": "domain"}, {"type": "xy"}]],
            )
            fig.add_trace(
                go.Table(
                    header=dict(values=["Attribute", "Value"]),
                    cells=dict(
                        values=[
                            [
                                "Best fitness",
                                "Fitness ratio<br>(vs Greedy)",
                                "Fitness ratio<br>(vs SA)",
                                "Number iteration",
                                "Initial temperature",
                                "Method type",
                                "Execution time (s)",
                                "Execution time ratio<br>(vs Greedy)",
                                "Execution time ratio<br>(vs SA)",
                            ],
                            [
                                round(pt_cost, rounded),
                                round((greedy_cost) / pt_cost, rounded),
                                round((sa_cost) / pt_cost, rounded),
                                pt_iter,
                                round(pt_T, rounded),
                                pt_type,
                                round(pt_time, rounded),
                                round((greedy_time) / pt_time, rounded),
                                round((sa_time) / pt_time, rounded),
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
                    x=self.cities[pt_result, 0],
                    y=self.cities[pt_result, 1],
                    mode="lines",
                    line=dict(color="plum"),
                    name="path",
                )
            )
            plot_cities(fig, x, y, title=title[2])
        else:
            fig = go.Figure()
            plot_cities(fig, x, y, title=title[0])


def benchmark(num_city: int) -> np.ndarray:
    coordinates = 2 * np.pi * np.arange(num_city) / num_city
    return np.array([np.cos(coordinates), np.sin(coordinates)]).T


if __name__ == "__main__":
    # Create argument parser
    parser = argparse.ArgumentParser(description="TP3 - Traveling Salesman Problem")

    # Add arguments
    parser.add_argument(
        "-b",
        "--benchmark",
        help="Benchmark problem with human trivial solution (vertex polygon)",
    )
    parser.add_argument(
        "-r",
        "--random",
        help="Random problem of n cities",
    )

    # Parse arguments
    args = parser.parse_args()

    if args.benchmark:
        test = SA(benchmark(int(args.benchmark)))
        test.graph(
            path=True,
            title=[
                f"Benchmark: greedy for {args.benchmark} cities",
                f"Benchmark: simulated annealing for {args.benchmark} cities",
                f"Benchmark: parallel tempering for {args.benchmark} cities",
            ],
        )

    if args.random:
        test = SA(np.random.rand(args.random, 2))
        test.graph(
            path=True,
            title=[
                f"Random: greedy for {args.benchmark} cities",
                f"Random: simulated annealing for {args.benchmark} cities",
                f"Random: parallel tempering for {args.benchmark} cities",
            ],
        )
