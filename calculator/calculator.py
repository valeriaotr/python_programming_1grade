""" important modules """
import math
import typing as tp


def common_num(num_1, num_2):
    """function for transfer"""
    b_1 = ""
    sim = "0123456789ABCDEF"
    num_1, num_2 = int(num_1), int(num_2)
    if num_1 >= 0 and num_2 > 0:
        if 0 < num_2 <= 9:
            while num_1 > 0:
                b_1 = str(num_1 % num_2) + b_1
                num_1 = num_1 // num_2
            return b_1
        else:
            return "такая система счисления недоступна"
        print("")
    return "Числa должны быть положительными"


def match_case_calc_2(num_1: float, num_2: float, command: str) -> tp.Union[float, str]:  # type: ignore
    """function for math options"""
    match command:
        case "+":
            return num_1 + num_2
        case "-":
            return num_1 - num_2
        case "/":
            if num_2 != 0:
                return num_1 / num_2
            return f"Error"
        case "*":
            return num_1 * num_2
        case "**":
            return num_1**num_2
        case "перевод":
            return common_num(num_1, num_2)


def match_case_calc_1(num_1: float, command: str) -> tp.Union[float, str]:
    """function for math options"""
    match command:
        case "sin":
            return math.sin(num_1)
        case "cos":
            return math.cos(num_1)
        case "tan":
            return math.tan(num_1)
        case "^2":
            return num_1**2
        case "ln":
            if num_1 <= 0:
                return "невозможно по области определения"
            return math.log(num_1)
        case "lg":
            if num_1 <= 0:
                return "невозможно по области определения"
            return math.log10(num_1)
        case _:
            return "Недоступный оператор"


if __name__ == "__main__":
    while True:
        try:
            COMMAND = input("Введите операцию > ")
            if COMMAND in ("+", "-", "/", "*", "**", "перевод"):
                NUM_1 = float(input("Первое число > "))
                NUM_2 = float(input("Второе число > "))
                print(match_case_calc_2(NUM_1, NUM_2, COMMAND))
            elif COMMAND in ("^2", "cos", "sin", "tan", "ln", "lg"):
                NUM_1 = float(input("Введите число > "))
                print(match_case_calc_1(NUM_1, COMMAND))
            else:
                print("Такой операции не существует")
        except ValueError:
            print("Ошибка: вы ввели не число")