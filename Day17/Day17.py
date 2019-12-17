from typing import List
import numpy as np
from scipy.ndimage import convolve


def intcode(phase_setting, inp, data: List[int], inp_count=0, i=0, pre_out=False) -> tuple:
    out = []
    base = 0
    memory = {}
    out_line = []
    while not data[i] % 100 == 99:
        t_op = data[i]
        if t_op % 100 == 3:
            ind = data[i + 1] if t_op < 100 else (i + 1) if t_op < 200 else (data[i + 1] + base)
            if ind < len(data):
                data[ind] = inp[inp_count]
            else:
                memory[ind] = inp[inp_count]
            inp_count += 1
            i += 2
            continue
        elif t_op % 100 == 4:
            index = data[i + 1] if t_op < 100 else (i + 1) if t_op < 200 else (data[i + 1] + base)
            out_t = data[index] if index < len(data) else get_mem(memory, index)
            pos = 0
            i += 2
            if pre_out:
                if out_t == 10:
                    if len(out_line) > 0:
                        yield out_line
                    out_line = []
                else:
                    out_line.append(out_t % 2)
            else:
                out.append(out_t)
            continue
        elif t_op % 100 == 9:
            ind = data[i + 1] if t_op < 100 else (i + 1) if t_op < 200 else (data[i + 1] + base)
            base += data[ind] if ind < len(data) else get_mem(memory, ind)
            i += 2
            continue
        elif t_op % 100 in [5, 6]:
            dat = t_op // 100
            check = t_op % 100
            ind_1 = data[i + 1] if dat == 0 or dat % 10 == 0 else (i + 1) if dat % 10 == 1 else (data[i + 1] + base)
            ind_2 = data[i + 2] if dat == 0 or (dat // 10) % 10 == 0 else (i + 2) if (dat // 10) % 10 == 1 else (data[i + 2] + base)
            el2 = data[ind_2] if ind_2 < len(data) else get_mem(memory, ind_2)
            el1 = data[ind_1] if ind_1 < len(data) else get_mem(memory, ind_1)
            if el1 and check == 5:
                i = el2
            elif not el1 and check == 6:
                i = el2
            else:
                i += 3
            continue
        code, el1, el2, save_pos = data[i:i+4]
        if code > 99:
            opcode = code % 100
            if ((code // 100) % 10) % 2 == 0:
                ind_1 = el1 if (code // 100) % 10 == 0 else (el1 + base)
                el1 = data[el1] if ind_1 < len(data) else get_mem(memory, ind_1)

            if ((code // 1000) % 10) % 2 == 0:
                ind_2 = el2 if (code // 1000) % 10 == 0 else (el2 + base)
                el2 = data[el2] if ind_2 < len(data) else get_mem(memory, ind_2)

            if (code // 10000) % 2 == 0:
                save_pos = save_pos if code // 10000 == 0 else (save_pos + base)
        else:
            opcode = code
            el1 = data[el1] if el1 < len(data) else get_mem(memory, el1)
            el2 = data[el2] if el2 < len(data) else get_mem(memory, el2)
        if opcode in [1, 2]:
            if save_pos < len(data):
                data[save_pos] = (el1 + el2) if opcode == 1 else (el1 * el2)
            else:
                memory[save_pos] = (el1 + el2) if opcode == 1 else (el1 * el2)
        elif opcode in [7, 8]:
            if save_pos < len(data):
                data[save_pos] = int(el1 < el2) if opcode == 7 else int(el1 == el2)
            else:
                memory[save_pos] = int(el1 < el2) if opcode == 7 else int(el1 == el2)
        else:
            break
        i += 4
    if not pre_out:
        yield out


def get_mem(memory, index):
    if index not in memory.keys():
        memory[index] = 0
    return memory[index]


with open("input.txt", "r") as file:
    inp = [int(x) for x in file.readline().split(",")]
    inp_2 = inp.copy()

scaffold = []
for line in intcode(phase_setting=1, inp=None, data=inp, pre_out=True):
    scaffold.append(line)

intersections_coords = np.argwhere(convolve(np.array(scaffold), np.array([[0, 1, 0], [1, 1, 1], [0, 1, 0]]), mode='constant') == 5)

print(f"Part 1: {np.sum(intersections_coords[:,0] * intersections_coords[:,1])}")

inp_2[0] = 2

ascii_main_route = list(map(ord, list(','.join(["A", "C", "A", "B", "A", "A", "B", "C", "B", "C"])))) + [10]
ascii_a = list(map(ord, list("L,12,L,8,R,12"))) + [10]
ascii_b = list(map(ord, list("R,12,L,8,L,10"))) + [10]
ascii_c = list(map(ord, list("L,10,L,8,L,12,R,12"))) + [10]
live_feed = [ord("n"), 10]

arr = ascii_main_route
arr.extend(ascii_a)
arr.extend(ascii_b)
arr.extend(ascii_c)
arr.extend(live_feed)


print(f"Part 2: {list(i[-1] for i in intcode(phase_setting=2, inp=arr, data=inp_2, pre_out=False))[-1]}")

