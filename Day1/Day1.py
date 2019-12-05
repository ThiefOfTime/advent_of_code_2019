import numpy as np


def calc_fuel(data: np.ndarray) -> int:
    return np.maximum(0, data // 3 - 2)


def part_1(data: np.ndarray) -> int:
    return np.sum(calc_fuel(data))


def part_2(data: np.ndarray) -> int:
    n_data = calc_fuel(data)
    return data if np.sum(data) <= 0 else n_data + part_2(n_data)


if __name__ == "__main__":
    with open("input.txt", "r") as file:
        inp = [int(x) for x in file]
    print(part_1(np.array(inp, dtype=np.int)))

    print(np.sum(part_2(np.array(inp, dtype=np.int))))
