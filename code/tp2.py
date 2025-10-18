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

    def _cost(self, path: np.ndarray) -> float:
        assert self.num_cities == len(path), (
            f"length of path must be of same length than number of cities (num_cities: {self.num_cities}    path_len: {len(path)}"
        )
        shift = np.roll(path, 1)

        return np.linalg.norm(self.cities[path] - self.cities[shift], axis=1).sum()

    def neighborhood(self, path: np.ndarray) -> np.ndarray:
        n = len(path)
        neighborhood = np.ones((int(n * (n - 1) / 2), 1)) @ path.reshape(1, -1)
        print(neighborhood)
        neighborhood.astype(int)
        for i in range(n - 1):
            for j in range(i + 1, n):
                neighborhood[i + j, i] = path[j]
                neighborhood[i + j, j] = path[i]
        print(neighborhood)
        return neighborhood

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
            plt.plot(path_x, path_y)
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
        test.graph()
        test.neighborhood(np.arange(4))
