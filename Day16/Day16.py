from math import ceil
import numpy as np


def create_arrs(num_vals):
    mul_p = np.zeros((num_vals, num_vals), dtype=np.int)
    for i in range(num_vals):
        base_rep = np.roll(np.repeat(np.array([0, 1, 0, -1]), i + 1), -1)
        mul_p[i, :] = np.tile(base_rep, num_vals // len(base_rep) + 1)[:num_vals]
    return mul_p


with open("input.txt", "r") as inp_file:
    inp_numb = inp_file.read()
    offset = int(inp_numb[:7])

numbers_1 = np.array(list(map(int, list(inp_numb))))
numbers_2 = np.tile(numbers_1, 10000)

mul_arrs = create_arrs(len(numbers_1))

for i in range(1, 101):
    numbers_1 = np.abs(np.sum(numbers_1 * mul_arrs, axis=1)) % 10

print(f"Part1: {int(''.join(map(str, numbers_1[:8])))}")

basic_length = len(numbers_2)
for i in range(100):
    numbers_2 = np.flip(np.flip(numbers_2).cumsum()) % 10

offset = offset - len(numbers_2)
print(f"Part2: {int(''.join(map(str, numbers_2[offset: offset + 8])))}")


