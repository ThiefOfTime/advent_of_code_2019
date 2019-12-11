from typing import List
import numpy as np


def get_mem(memory, index):
    if index not in memory.keys():
        memory[index] = 0
    return memory[index]


def intcode(phase_setting, inp, data: List[int], inp_count=0, i=0, pre_out=False) -> tuple:
    out = 0
    base = 0
    memory = {}
    out_c = 0
    direction = 0
    start_pos = (0, 0)
    fields_visited = {start_pos: phase_setting}
    cur_pos = (0, 0)
    while not data[i] % 100 == 99:
        t_op = data[i]
        if t_op % 100 == 3:
            if cur_pos in fields_visited.keys():
                inp = fields_visited[cur_pos]
            else:
                fields_visited[cur_pos] = 0
                inp = 0
            ind = data[i + 1] if t_op < 100 else (i + 1) if t_op < 200 else (data[i + 1] + base)
            if ind < len(data):
                data[ind] = inp
            else:
                memory[ind] = inp
            i += 2
            continue
        elif t_op % 100 == 4:
            index = data[i + 1] if t_op < 100 else (i + 1) if t_op < 200 else (data[i + 1] + base)
            if out_c % 2 == 0:
                fields_visited[cur_pos] = data[index] if index < len(data) else get_mem(memory, index)

            else:
                turn_d = data[index] if index < len(data) else get_mem(memory, index)
                direction += 1 if turn_d == 0 else -1
                if direction % 4 == 0:
                    cur_pos = (cur_pos[0] + 1, cur_pos[1])
                elif direction % 4 == 1:
                    cur_pos = (cur_pos[0], cur_pos[1] - 1)
                elif direction % 4 == 2:
                    cur_pos = (cur_pos[0] - 1, cur_pos[1])
                else:
                    cur_pos = (cur_pos[0], cur_pos[1] + 1)
            out_c += 1
            i += 2
            if pre_out:
                print(out)
                #break
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
    return fields_visited


with open("input.txt", "r") as file:
    inp = [int(x) for x in file.readline().split(",")]
    print(f"Part 1: {len(intcode(phase_setting=0, inp=None, data=inp, pre_out=False).keys())}")
    fields = intcode(phase_setting=1, inp=None, data=inp, pre_out=False)
    max_vals = np.max(np.array(list(fields.keys())), axis=0)
    min_vals = np.min(np.array(list(fields.keys())), axis=0)
    print_arr = np.zeros((max_vals[0] - min_vals[0] + 1, max_vals[1] - min_vals[1] + 1), dtype=np.int)
    for (x, y), el in fields.items():
        print_arr[x + max_vals[0] - min_vals[0], y] = el
    print_arr = [''.join([str(a) for a in l]) for l in list(print_arr)]
    print_arr.reverse()
    for p in print_arr:
        print(p.replace("0", ".").replace("1", "#"))