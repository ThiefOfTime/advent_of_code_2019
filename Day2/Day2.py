def intcode(data):
    i = 0
    while i < len(data):
        if data[i] == 99 or i > len(data) - 4:
            return data
        opcode, el1, el2, save_pos = data[i:i+4]
        if opcode == 1:
            data[save_pos] = data[el1] + data[el2]
        elif opcode == 2:
            data[save_pos] = data[el1] * data[el2]
        else:
            return data
        i += 4
    return data


def part_1(data):
    data[1] = 12
    data[2] = 2
    return intcode(data)


def part_2(data):
    noun = 0
    # the verb only controls the last 2 digits
    # 
    for i in range(12, 100):
        n_data = data.copy()
        n_data[1] = i
        n_data[2] = 2
        res = intcode(n_data)[0]
        if res >= 19690720:
            noun = i - 1
            break
    for j in range(2, 99):
        n_data = data.copy()
        n_data[1] = noun
        n_data[2] = j
        res = intcode(n_data)[0]
        if res == 19690720:
            return 100 * noun + j



if __name__ == "__main__":
    with open("input.txt", "r") as data:
        data_list = data.readlines()[0]
        data_list = data_list.strip().split(",")
        data_list = [int(d) for d in data_list]
    print(part_1(data_list.copy())[0])

    print(part_2(data_list.copy()))
