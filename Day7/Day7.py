import numpy as np
from typing import List


def intcode(phase_setting, inp, data: List[int], inp_count=0, i=0, pre_out=False) -> tuple:
    out = 0
    pos = 2
    while not data[i] % 100 == 99:
        t_op = data[i]
        if t_op % 100 == 3:
            data[data[i + 1]] = inp if inp_count else phase_setting
            inp_count += 1
            i += 2
            continue
        elif t_op % 100 == 4:
            out = data[i + 1] if t_op > 99 else data[data[i + 1]]
            pos = 0
            i += 2
            if pre_out:
                break
            continue
        elif t_op % 100 in [5, 6]:
            dat = t_op // 100
            check = t_op % 100
            el2 = data[data[i + 2]] if dat == 0 or (dat // 10) % 10 == 0 else data[i + 2]
            el1 = data[data[i + 1]] if dat == 0 or dat % 10 == 0 else data[i + 1]
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
            el1 = data[el1] if (code // 100) % 10 == 0 else el1
            el2 = data[el2] if (code // 1000) % 10 == 0 else el2
            save_pos = data[save_pos] if code // 10000 == 1 else save_pos
        else:
            opcode, el1, el2 = code, data[el1], data[el2]
        if opcode in [1, 2]:
            data[save_pos] = el1 + el2 if opcode == 1 else el1 * el2
        elif opcode in [7, 8]:
            data[save_pos] = int(el1 < el2) if opcode == 7 else int(el1 == el2)
        else:
            break
        i += 4
    return i, out, pos


def feedback_loop(data, t_inp):
    stat = 0
    while not stat == 2:
        for name in data.keys():
            c_data = data[name]
            pos, n_inp, stat = intcode(c_data[0], t_inp, c_data[1], c_data[2], c_data[3], pre_out=True)
            t_inp = max(t_inp, n_inp)
            c_data[2] = 1
            c_data[3] = pos
    return t_inp


with open("input.txt", "r") as file:
    inp = [int(x) for x in file.readline().split(",")]

    print(max(intcode(amp[4], intcode(amp[3], intcode(amp[2], intcode(amp[1], intcode(amp[0], 0, inp.copy())[1],
                            inp.copy())[1], inp.copy())[1], inp.copy())[1], inp.copy())[1] for amp in
                    np.array(np.meshgrid(*(5*[list(range(0, 5))]))).T.reshape(-1, 5) if len(set(amp)) == 5))

    res = []
    settings = [amp for amp in np.array(np.meshgrid(*(5 * [list(range(5, 10))]))).T.reshape(-1, 5) if len(set(amp)) == 5]
    for setting in settings:
        work_dict = {}
        for i in range(1, 6):
            work_dict[f"amp{i}"] = [setting[i - 1], inp.copy(), 0, 0]
        res.append(feedback_loop(work_dict, 0))
    print(max(res))


