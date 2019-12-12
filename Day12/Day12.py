import numpy as np
from math import gcd


with open("input.txt", "r") as planet_file:
    planet_file_lines = planet_file.readlines()
    planet_file_lines = [l.replace("\n", "").replace("<", "").replace(">", "").split(", ") for l in planet_file_lines]
planet_coords = np.array([[int(a.split("=")[1]) for a in line] for line in planet_file_lines])

planet_velos = np.zeros((4, 3), dtype=np.int)


planet_velos_d = planet_velos.copy()
planet_coords_d = planet_coords.copy()
for i in range(1000):
    for k in range(4):
        planet_velos_d[planet_coords_d < planet_coords_d[k]] += 1
        planet_velos_d[planet_coords_d > planet_coords_d[k]] -= 1

    planet_coords_d += planet_velos_d
print(f"Part1: {np.sum(np.sum(np.abs(planet_coords_d), axis=1) * np.sum(np.abs(planet_velos_d), axis=1))}")


pos = [0, 0, 0]
z = 0


def lcm(a, b):
    return (a*b)//gcd(a, b)


j = 0
planet_coords_c = planet_coords.copy()
planet_velos_c = planet_velos.copy()
hash_list_x = set()
hash_list_y = set()
hash_list_z = set()
while True:
    for k in range(4):
        planet_velos_c[planet_coords_c < planet_coords_c[k]] += 1
        planet_velos_c[planet_coords_c > planet_coords_c[k]] -= 1

    planet_coords_c += planet_velos_c

    pc = np.append(planet_coords_c, planet_velos_c, axis=0)
    pc_x, pc_y, pc_z = ''.join(map(str, pc[:, 0])), ''.join(map(str, pc[:, 1])), ''.join(map(str, pc[:, 2]))
    if pos[0] == 0:
        if pc_x in hash_list_x:
            pos[0] = j
        else:
            hash_list_x.add(pc_x)
    if pos[1] == 0:
        if pc_y in hash_list_y:
            pos[1] = j
        else:
            hash_list_y.add(pc_y)
    if pos[2] == 0:
        if pc_z in hash_list_z:
            pos[2] = j
        else:
            hash_list_z.add(pc_z)
    if pos[0] > 0 and pos[1] > 0 and pos[2] > 0:
        break
    j += 1


print(f"Part2: {lcm(lcm(pos[0], pos[1]), pos[2])}")
