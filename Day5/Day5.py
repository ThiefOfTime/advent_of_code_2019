from typing import List


def intcode(data: List[int]) -> int:
    i = 0
    while not data[i] % 100 == 99:
        t_op = data[i]
        if t_op % 100 == 3:
            t_inp = int(input("Please provide the unit ID: "))
            data[data[i + 1]] = t_inp
            i += 2
            continue
        elif t_op % 100 == 4:
            print(data[i + 1] if t_op > 99 else data[data[i + 1]])
            i += 2
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
    return data


with open("input.txt", "r") as file:
    inp = [int(x) for x in file.readline().split(",")]
    intcode(inp)
