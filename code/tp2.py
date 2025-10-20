import numpy as np
import matplotlib.pyplot as plt
import argparse


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
        title: str = "Graph",
        greedy: bool = False,
        sa: bool = True,
        max_iter: int = 10000,
        M: int = 4,
        type: str = "exp",
    ):
        x = self.cities[:, 0]
        y = self.cities[:, 1]
        plt.figure()
        if path:
            if greedy:
                result, cost = self.greedy()
                plt.plot([], [], " ", label=f"Fitness: {cost}")
            elif sa:
                result, iter, cost, T = self.simulated_annealing()
                plt.plot(
                    [],
                    [],
                    " ",
                    label=f"Number of iterations: {iter}\nFitness: {cost}\n$T_0$: {T}",
                )
            else:
                result, iter, cost, T = self.parallel_tempering(max_iter, M, type)
                plt.plot(
                    [],
                    [],
                    " ",
                    label=f"Nb_iterations to find best fitness: {iter}\nFitness: {cost}\n$T_0$: {T}",
                )
            path_x = self.cities[result, 0]
            path_y = self.cities[result, 1]
            plt.plot(path_x, path_y, color="green", label="path")
            plt.plot([path_x[-1], path_x[0]], [path_y[-1], path_y[0]], color="green")
        plt.plot(x, y, "ro", label="cities")
        plt.title(title)
        plt.legend()
        plt.show()


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
            greedy=True,
            title=f"Benchmark: greedy for {args.benchmark} cities",
        )
        test.graph(
            path=True,
            title=f"Benchmark: simulated annealing for {args.benchmark} cities",
        )
        test.graph(
            path=True,
            sa=False,
            title=f"Benchmark: parallel tempering for {args.benchmark} cities",
        )

    if args.random:
        test = SA(np.random.rand(args.random, 2))
        test.graph(
            path=True,
            greedy=True,
            title=f"Benchmark: greedy for {args.benchmark} cities",
        )
        test.graph(
            path=True,
            title=f"Benchmark: simulated annealing for {args.benchmark} cities",
        )
        test.graph(
            path=True,
            sa=False,
            title=f"Benchmark: parallel tempering for {args.benchmark} cities",
        )
