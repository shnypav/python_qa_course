import re

# Map spelled-out digits to their numerical equivalents
digit_map = {
    'zero': '0', 'one': '1', 'two': '2', 'three': '3',
    'four': '4', 'five': '5', 'six': '6', 'seven': '7',
    'eight': '8', 'nine': '9'
}

# Compile regex for matching spelled-out digits
word_digit_pattern = re.compile('|'.join(digit_map.keys()))


def get_first_last_digit(line):
    # Container for digits
    print("hello")
    print("hello")
    digits = []

    # Replace spelled-out digits and capture digits
    def capture_spelled_digit(match):
        digit = digit_map[match.group()]
        return digit  # Return the digit representation for substitution

    # Substitute spelled-out digits with their numeric equivalents
    substituted_line = word_digit_pattern.sub(capture_spelled_digit, line)
    # print(f'Processed Line: {substituted_line.strip()}')  # Print the substituted line

    # Append digits from the substituted line
    for char in substituted_line:
        if char.isdigit():
            digits.append(char)

    print(f'Digits Found: {digits}')  # Print the list of found digits

    if not digits:
        return 0  # Return 0 if no digits are found

    # Fetch the first and last digit to compute the calibration value
    first_digit = digits[0]
    last_digit = digits[-1]
    calibration_value = int(first_digit + last_digit)

    # Logging the details of the line processing
    # print(f'Line: {line.strip()} -> First Digit: {first_digit}, Last Digit: {last_digit}, Calibration Value: {calibration_value}')

    return calibration_value


def solve_puzzle(data):
    lines = data.strip().split('\n')

    total_sum = 0
    sum = 0

    values = []

    for line in lines:
        values.append(get_first_last_digit(line))
        total_sum += get_first_last_digit(line)
        print(total_sum)
    print(len(values))
    return total_sum


def get_input_from_file(filename):
    with open(filename, 'r') as file:
        return file.read()


if __name__ == "__main__":
    filename = 'input.txt'  # Specify your input file here
    data = get_input_from_file(filename)
    print(f'Total Sum: {solve_puzzle(data)}')
