from typing import List


def print_by_row(X):
    for row in X:
        print(row)


def transformation(X: List[float], Mw: List[float]) -> List[float]:
    None # TODO: implement transformation


def translation(X: List[float], Tw: List[int]) -> List[float]:
    print("Translation: (", Tw[0], ",", Tw[1], ")")
    print("Before translation:")
    print_by_row(X)
    empty_row = [0] * len(X[0])
    new_X = []

    # vertical translation
    if Tw[1] == 0:
        new_X = X
    elif Tw[1] > 0:  # upwards
        new_X = X[Tw[1]:]
        for _ in range(Tw[1]): new_X.append(empty_row)
    else:  # downwards
        for _ in range(-Tw[1]): new_X.append(empty_row)
        new_X = new_X + X[:len(X) + Tw[1]]
    print("After vertical translation:")
    print_by_row(new_X)

    # horizontal translation
    print("After horizontal translation:")
    if Tw[0] == 0:
        None
    else:
        for i, row in enumerate(new_X):
            if Tw[0] < 0:  # move left
                new_X[i] = row[-Tw[0]:] + [0] * (-Tw[0])
            else:  # move right
                new_X[i] = [0] * (Tw[0]) + row[:len(row) - Tw[0]]

    print_by_row(new_X)
    return new_X


def affine_warping(X: List[float], Mw: List[float], Tw: List[int]) -> List[float]:
    return transformation(translation(X, Tw), Mw)
