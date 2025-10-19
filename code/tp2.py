import numpy as np
import matplotlib.pyplot as plt
import argparse


class SA:
    def __init__(self, cities: np.ndarray, T: float, iter: int = 500) -> None:
        self.T = T
        self.frozen = 0
        self.iter = iter
        self.cities = cities
        self.num_cities = cities.shape[0]

    def _cost(self, paths: np.ndarray) -> np.ndarray:
        if len(paths.shape) != 2:
            paths = np.array([paths])
        assert len(paths.shape) == 2, (
            f"path must be list of paths, so 2D ! Actual path_shape: {paths.shape}"
        )
        shift = np.roll(paths, 1, axis=1)
        return np.linalg.norm(self.cities[paths] - self.cities[shift], axis=2).sum(
            axis=1
        )

    def _canonical(self, path: np.ndarray) -> tuple:
        """
        Function that put a path on canonical form.
        It means that all the variantions of the same path will be written in the same way.
        For that, working with tuple allows to use comparison between lists.

        Parameters
        ----------
        path : np.ndarray
            Path to compute canonical form

        Returns
        -------
        tuple
            Canonical form of the path

        """
        same = [tuple(np.roll(path, i)) for i in range(len(path))]
        same += [tuple(np.roll(path[::-1], i)) for i in range(len(path))]
        return min(same)

    def _swap(self, path: np.ndarray, i: int, j: int) -> np.ndarray:
        swap_path = path.copy()
        swap_path[i], swap_path[j] = swap_path[j], swap_path[i]
        return swap_path

    def neighborhood(self, path: np.ndarray) -> np.ndarray:
        n = len(path)
        neighborhood = []
        canonical_form = self._canonical(path)
        for i in range(n - 1):
            for j in range(i + 1, n):
                new_path = self._canonical(self._swap(path, i, j))
                if new_path not in neighborhood and new_path != canonical_form:
                    neighborhood.append(new_path)
        return np.array(neighborhood).astype(int)

    def greedy(self) -> np.ndarray:
        current = np.random.permutation(self.num_cities)
        visited = []
        delta = 0
        while delta <= 0:
            visited.append(current)
            neighborhood = self.neighborhood(current)
            cost = self._cost(neighborhood)
            index = np.argmin(cost)
            delta = cost[index] - self._cost(current)[0]
            current = neighborhood[index]
        return visited[-1]

    def simulated_annealing(self) -> np.ndarray:
        path = np.random.permutation(self.num_cities)
        print(path)
        return np.array([])

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
        action="store_true",
        help="Benchmark problem with human trivial solution (30-vertex polygon)",
    )

    # Parse arguments
    args = parser.parse_args()

    if args.benchmark:
        test = SA(benchmark(30), 1)
        test.graph(test.greedy(), isPath=True)
