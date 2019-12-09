from typing import List


def intcode(phase_setting, inp, data: List[int], inp_count=0, i=0, pre_out=False) -> tuple:
    out = 0
    pos = 2
    base = 0
    memory = {}
    while not data[i] % 100 == 99:
        t_op = data[i]
        if t_op % 100 == 3:
            ind = data[i + 1] if t_op < 100 else (i + 1) if t_op < 200 else (data[i + 1] + base)
            if ind < len(data):
                data[ind] = inp if inp_count else phase_setting
            else:
                memory[ind] = inp if inp_count else phase_setting
            inp_count += 1
            i += 2
            continue
        elif t_op % 100 == 4:
            index = data[i + 1] if t_op < 100 else (i + 1) if t_op < 200 else (data[i + 1] + base)
            out = data[index] if index < len(data) else get_mem(memory, index)
            pos = 0
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
    return i, out, pos


def get_mem(memory, index):
    if index not in memory.keys():
        memory[index] = 0
    return memory[index]


with open("input.txt", "r") as file:
    inp = [int(x) for x in file.readline().split(",")]
    print("Part 1: ", intcode(phase_setting=1, inp=None, data=inp, pre_out=False)[1])
    print("Part 2: ", intcode(phase_setting=2, inp=None, data=inp, pre_out=False)[1])
