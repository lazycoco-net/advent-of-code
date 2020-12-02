

if __name__ == '__main__':
    # Using hashing implementation. I'll put all numbers in a set. Then for each number I'll calculate the number it
    # needs for adding up to 2020 and check if the number is in that set. If found, then calculate the multiplication.
    # value in input_set takes O(1).
    with open('report_repair_input.txt', 'r') as f:
        input_set = set()
        for line in f:
            input_set.add(line.replace('\n', ''))

    for value in input_set:
        complement = 2020 - int(value)
        if str(complement) in input_set:
            print(f'Values found: {value} and {complement}')
            print(f'Multiplication: {int(value) * complement}')
            exit(0)

    print('No pair of values found that add to 2020')
