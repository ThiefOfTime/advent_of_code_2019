import math
import numpy as np
from scipy.spatial import distance
np.seterr(divide='ignore', invalid='ignore')


def get_angle(a, b, c):
    ang = math.degrees(math.atan2(c[1] - b[1], c[0] - b[0]) - math.atan2(a[1] - b[1], a[0] - b[0]))
    return 360 - ang + 360 if ang < 0 else ang


with open("input.txt", "r") as data_file:
    data = data_file.readlines()

data = np.array([list(map(int, list(line.replace("\n", "").replace(".", "0").replace("#", "1")))) for line in data])
data_points = np.array(list(zip(*np.where(data == 1))))


ast_max, ast_pos = max((len(set(tuple(np.round((ast2 - ast1) / distance.euclidean(ast1, ast2), 8)) for ast2 in data_points if not np.array_equal(ast1, ast2))), tuple(ast1)) for ast1 in data_points)
print(f"Part1: {ast_max}")

data_points = list(tuple(a) for a in data_points)
explode = 0
while np.sum(data) > 1:
    remove = []
    ast_list = [(np.round(get_angle((0, ast_pos[1]), ast_pos, dp), 10),
                tuple(np.round((dp - np.array(ast_pos)) / distance.euclidean(np.array(ast_pos), dp), 8)),
                np.round(distance.euclidean(np.array(ast_pos), np.array(dp)), 8),
                dp) for dp in data_points]

    # sort by degree
    ast_list.sort()
    check_list = []
    for angle, val, dist, dp in ast_list:
        # skip used val values
        if val in check_list:
            continue
        else:
            check_list.append(val)
        # skip station point
        if dist == 0:
            continue

        sort_vals = [(v[2], v[3]) for v in ast_list if v[1] == val]
        # sort by distance
        sort_vals.sort()
        # astroid location to fire at
        d = sort_vals[0][1]
        data[d[0], d[1]] = 0
        # remove asteroid from known asteroid list
        data_points.remove(d)
        explode += 1
        if explode == 200:
            print(f"Part2: {(d[1], d[0])}  {d[1] * 100 + d[0]}")
            break

    if explode == 200:
        break

