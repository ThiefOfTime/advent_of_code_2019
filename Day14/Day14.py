from collections import defaultdict
from math import ceil


def calc_ore(prod=1, cur_chemical="FUEL"):
    if cur_chemical == "ORE" or prod == 0:
        return prod
    else:
        prod_t = ceil(prod / data_dict[cur_chemical][0])
        overproduction_dict[cur_chemical] += prod_t * data_dict[cur_chemical][0] - prod
        cur_val = 0
        for amount, chemical in data_dict[cur_chemical][1]:
            total_amount_needed = amount * prod_t
            surplus = min(total_amount_needed, overproduction_dict[chemical])
            total_amount_needed -= surplus
            overproduction_dict[chemical] -= surplus
            cur_val += calc_ore(total_amount_needed, chemical)
        return cur_val


def binary_search(bottom, top):
    if top - bottom < 3:
        return bottom
    val = (bottom + (top - bottom) // 2) + 1
    return binary_search(bottom, val) if calc_ore(prod=val) > 1e12 else binary_search(val, top)


with open("input.txt", "r") as conv_file:
    conv_lines = conv_file.readlines()
    conv_lines = [line.strip().split(" => ") for line in conv_lines]
data_dict = {k.split(" ")[1]: (int(k.split(" ")[0]), [(int(j.split(" ")[0]), j.split(" ")[1]) for j in v.split(", ")]) for v, k in conv_lines}

overproduction_dict = defaultdict(int)


print(f"Part1: {calc_ore()}")
print(f"Part2: {binary_search(0, int(1e12))}")
