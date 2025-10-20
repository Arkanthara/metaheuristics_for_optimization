import numpy as np
import matplotlib.pyplot as plt
import argparse
import random


class SA:
    def __init__(self, cities: np.ndarray) -> None:
        self.cities = cities
        self.num_cities = cities.shape[0]
        # self.swap_matrix = self._build_swap_matrix()

    def _cost(self, path: np.ndarray) -> float:
        assert len(path.shape) == 1, f"Path must be 1D ! Actual: {path.shape}"
        shift = np.roll(path, 1)
        return np.linalg.norm(self.cities[path] - self.cities[shift], axis=1).sum()

    # def _cost(self, paths: np.ndarray) -> np.ndarray:
    #     if len(paths.shape) != 2:
    #         paths = np.array([paths])
    #     assert len(paths.shape) == 2, (
    #         f"path must be list of paths, so 2D ! Actual path_shape: {paths.shape}"
    #     )
    #     shift = np.roll(paths, 1, axis=1)
    #     return np.linalg.norm(self.cities[paths] - self.cities[shift], axis=2).sum(
    #         axis=1
    #     )
    #
    # def _canonical(self, path: np.ndarray) -> tuple:
    #     """
    #     Function that put a path on canonical form.
    #     It means that all the variantions of the same path will be written in the same way.
    #     For that, working with tuple allows to use comparison between lists.
    #
    #     Parameters
    #     ----------
    #     path : np.ndarray
    #         Path to compute canonical form
    #
    #     Returns
    #     -------
    #     tuple
    #         Canonical form of the path
    #
    #     """
    #     same = [tuple(np.roll(path, i)) for i in range(len(path))]
    #     same += [tuple(np.roll(path[::-1], i)) for i in range(len(path))]
    #     return min(same)

    # def _build_swap_matrix(self) -> np.ndarray:
    #     n = self.num_cities
    #     init = np.arange(n).astype(int)
    #     matrix = []
    #     canonical_form = self._canonical(init)
    #     for i in range(n - 1):
    #         for j in range(i + 1, n):
    #             new_permutation = self._canonical(self._swap(init, i, j))
    #             if new_permutation not in matrix and new_permutation != canonical_form:
    #                 matrix.append(new_permutation)
    #     return np.array(matrix).astype(int)

    def _swap(self, path: np.ndarray, i: int, j: int) -> np.ndarray:
        swap_path = path.copy()
        swap_path[i], swap_path[j] = swap_path[j], swap_path[i]
        return swap_path

    def permute(self, path: np.ndarray) -> np.ndarray:
        i, j = np.random.choice(len(path), size=2)
        return self._swap(path, i, j)

    def greedy(self) -> np.ndarray:
        path = [np.random.choice(np.arange(self.num_cities).astype(int))]
        for i in range(self.num_cities - 1):
            distance = np.linalg.norm(self.cities - self.cities[path[i]], axis=1)
            distance[path] = np.inf
            path.append(np.argmin(distance))
        return np.array(path)

    def simulated_annealing(self) -> np.ndarray:
        path = np.random.permutation(self.num_cities)
        current = path
        delta = []
        accepted = 0
        attempted = 0
        freezing = 0
        cost_improvment = False
        best_cost = self._cost(current)
        best_path = path

        # Init temperature
        for i in range(100):
            new_path = self.permute(current)
            cost = self._cost(new_path)
            # index = np.argmin(cost)
            delta.append(cost - self._cost(current))
            current = new_path
        T = -np.mean(np.abs(delta)) / np.log(0.5)
        print(f"Initial temperature T_0: {T}")
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

            # Choose neighbor
            new_path = self.permute(current)
            delta = self._cost(new_path) - self._cost(current)
            if delta <= 0:
                current = new_path
                accepted += 1

            # Metropolis rule
            else:
                if np.random.rand() < np.exp(-delta / T):
                    current = new_path
                    accepted += 1
            attempted += 1

            # Update best solution
            if self._cost(current) < best_cost:
                # print(
                #     f"current best fitness: {best_cost} and new best fitness: {self._cost(current)[0]}"
                # )
                cost_improvment = True
                best_cost = self._cost(current)
                best_path = current

        return best_path

    def graph(
        self,
        path: np.ndarray = np.array([]),
        isPath: bool = False,
        title: str = "Graph",
    ):
        x = self.cities[:, 0]
        y = self.cities[:, 1]
        plt.figure()
        if isPath:
            if path.size == 0:
                print("You must provide a path if the option isPath is activated !")
                exit(0)
            path_x = self.cities[path, 0]
            path_y = self.cities[path, 1]
            plt.plot(path_x, path_y, color="green")
            plt.plot([path_x[-1], path_x[0]], [path_y[-1], path_y[0]], color="green")
        plt.plot(x, y, "ro")
        plt.title(title)
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

    # Parse arguments
    args = parser.parse_args()

    if args.benchmark:
        test = SA(benchmark(int(args.benchmark)))
        test.graph(test.greedy(), isPath=True)
        test.graph(test.simulated_annealing(), isPath=True)
