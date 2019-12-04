d_input = range(235741, 706948 + 1)

count_numbers_1 = 0
count_numbers_2 = 0

for number in d_input:
    number_l = list(map(int, str(number)))
    if len(number_l) == 6 and number_l == sorted(number_l):
        count_numbers_1 += 1 if any(number_l.count(digit) > 1 for digit in set(number_l)) else 0
        count_numbers_2 += 1 if any(number_l.count(digit) == 2 for digit in set(number_l)) else 0

print("Part 1: ", count_numbers_1)
print("Part 2: ", count_numbers_2)