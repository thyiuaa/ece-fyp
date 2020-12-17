from typing import List
import numpy as np


def correlation(X1: np.ndarray, X2: np.ndarray, start: List[int], length: List[int]) -> float:
    sum_of_multiple = np.sum(
        X1[start[0]:start[0] + length[0]][start[1] + length[1]]
        * X2[start[0]:start[0] + length[0]][start[1] + length[1]]
    )
    sqrt_of_multiple = np.sqrt(
        np.sum(np.square(X1[start[0]:start[0] + length[0]][start[1] + length[1]]))
        * np.sum(np.square(X2[start[0]:start[0] + length[0]][start[1] + length[1]]))
    )
    return sum_of_multiple / sqrt_of_multiple


def main():
    None


if __name__ == "__main__":
    main();
