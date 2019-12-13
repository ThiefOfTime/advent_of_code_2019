import numpy as np
from math import gcd


def lcm(a, b):
    return (a*b)//gcd(a, b)


with open("input.txt", "r") as planet_file:
    planet_file_lines = planet_file.readlines()
    planet_file_lines = [l.replace("\n", "").replace("<", "").replace(">", "").split(", ") for l in planet_file_lines]

planet_coords = np.array([[int(a.split("=")[1]) for a in line] for line in planet_file_lines])
planet_velos = np.zeros((4, 3), dtype=np.int)
pos = [0, 0, 0]
j = 0
hl_x, hl_y, hl_z = set(), set(), set()

while True:

    if j == 1000:
        print(f"Part1: {np.sum(np.sum(np.abs(planet_coords), axis=1) * np.sum(np.abs(planet_velos), axis=1))}")

    for k in range(4):
        planet_velos[planet_coords < planet_coords[k]] += 1
        planet_velos[planet_coords > planet_coords[k]] -= 1
    planet_coords += planet_velos

    pc = np.append(planet_coords, planet_velos, axis=0)
    pc_x, pc_y, pc_z = ''.join(map(str, pc[:, 0])), ''.join(map(str, pc[:, 1])), ''.join(map(str, pc[:, 2]))
    if pos[0] == 0:
        pos[0] = j if pc_x in hl_x else 0
        hl_x.add(pc_x)
    if pos[1] == 0:
        pos[1] = j if pc_y in hl_y else 0
        hl_y.add(pc_y)
    if pos[2] == 0:
        pos[2] = j if pc_z in hl_z else 0
        hl_z.add(pc_z)
    if all(pos):
        break
    j += 1

print(f"Part2: {lcm(lcm(pos[0], pos[1]), pos[2])}")