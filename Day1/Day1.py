import numpy as np


def get_input():
    with open("input.txt", "r") as file:
        return file.readlines()


def calc_fuel(data):
    return np.maximum(0, data // 3 - 2)


def part_1(data):
    return np.sum(calc_fuel(data))


def part_2(data):
    if np.sum(data) > 0:
        res = np.zeros(len(data), dtype=np.int)
        while np.sum(data) > 0:
            data = calc_fuel(data)
            res += data
        return np.sum(res)
    else:
        return 0


if __name__ == "__main__":
    inp = get_input()
    inp = [int(x.strip()) for x in inp if len(x.strip()) > 0]
    print(part_1(np.array(inp, dtype=np.int)))

    print(part_2(np.array(inp, dtype=np.int)))
