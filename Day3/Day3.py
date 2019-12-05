import numpy as np
from scipy.spatial.distance import cdist
from typing import List

CENTRAL_PORT = (3000, 8000)


def build_field(data: List[int]) -> np.ndarray:
    base = np.zeros((12000, 18000), dtype=np.int)
    curr_point_x = CENTRAL_PORT[0]
    curr_point_y = CENTRAL_PORT[1]
    for element in data:
        value = int(element[1:])
        if "L" in element:
            base[curr_point_y, curr_point_x - value:curr_point_x] += 1
            curr_point_x = curr_point_x - value
        elif "R" in element:
            base[curr_point_y, curr_point_x + 1:curr_point_x + value + 1] += 1
            curr_point_x = curr_point_x + value
        elif "D" in element:
            base[curr_point_y + 1: curr_point_y + value + 1, curr_point_x] += 1
            curr_point_y = curr_point_y + value
        else:
            base[curr_point_y - value: curr_point_y, curr_point_x] += 1
            curr_point_y = curr_point_y - value
    base[CENTRAL_PORT[0], CENTRAL_PORT[1]] = 0
    base[base > 1] = 1
    return base


def calculate_manhatten_distance(data_1: List[int], data_2: List[int]) -> int:
    field = build_field(data_1) + build_field(data_2)
    intersections = np.argwhere(field > 1)
    return min(cdist(np.array([[CENTRAL_PORT[1], CENTRAL_PORT[0]]]), intersections, metric='cityblock')[0])


def run_calculation(data_1: List[int], data_2: List[int]) -> int:
    field = build_field(data_1) + build_field(data_2)
    intersections = np.argwhere(field > 1)
    r_data_1 = calculate_steps_taken(data_1, field, intersections)
    r_data_2 = calculate_steps_taken(data_2, field, intersections)
    results = []
    for k in r_data_1.keys():
        results.append(r_data_1[k] + r_data_2[k])
    return min(results)


def calculate_steps_taken(data: List[int], field: np.ndarray, intersections: np.ndarray) -> int:
    steps = {tuple(i): 0 for i in intersections}
    curr_point_x = CENTRAL_PORT[0]
    curr_point_y = CENTRAL_PORT[1]
    c_steps = 0
    for element in data:
        value = int(element[1:])
        if "L" in element:
            items = field[curr_point_y, curr_point_x - value:curr_point_x]
            if 2 in items:
                pos = np.where(items == 2)[0]
                pos = (pos - len(items)) * (-1)
                for p in pos:
                    steps[(curr_point_y, curr_point_x - p)] += (c_steps + p) if steps[(curr_point_y, curr_point_x - p)] == 0 else 0
            curr_point_x -= value
        elif "R" in element:
            items = field[curr_point_y, curr_point_x + 1:curr_point_x + value + 1]
            if 2 in items:
                pos = np.where(items == 2)[0] + 1
                for p in pos:
                    steps[(curr_point_y, curr_point_x + p)] += (c_steps + p) if steps[(curr_point_y, curr_point_x + p)] == 0 else 0
            curr_point_x += value
        elif "D" in element:
            items = field[curr_point_y + 1: curr_point_y + value + 1, curr_point_x]
            if 2 in items:
                pos = np.where(items == 2)[0] + 1
                for p in pos:
                    steps[(curr_point_y + p, curr_point_x)] += (c_steps + p) if steps[(curr_point_y + p, curr_point_x)] == 0 else 0
            curr_point_y += value
        else:
            items = field[curr_point_y - value: curr_point_y, curr_point_x]
            if 2 in items:
                pos = np.where(items == 2)[0]
                pos = (pos - len(items)) * (-1)
                for p in pos:
                    steps[(curr_point_y - p, curr_point_x)] += (c_steps + p) if steps[(curr_point_y - p, curr_point_x)] == 0 else 0
            curr_point_y -= value
        c_steps += value
    return steps


if __name__ == "__main__":
    with open("input.txt", "r") as data:
        data_list = data.readlines()
        line_1_data = data_list[0].strip().split(",")
        line_2_data = data_list[1].strip().split(",")

    print("Part 1: ", int(calculate_manhatten_distance(line_1_data, line_2_data)))

    print("Part 2: ", run_calculation(line_1_data, line_2_data))