from datetime import date

def first_py() -> bool:

    f_str = 'Веселая строка'
    print(f'{f_str = }')

    f_str = 2345
    print(f'{f_str = }')

    return True


def first_date() -> bool:

    date_1 = date.today()
    print(f'{date_1.isoformat() = }')

    date_2 = date(2025, 9, 25)
    print(f'{date_2.isoformat() = }')

    return True


def operator_for() -> bool:

    for i in [1, 2, 3, 4, 5]:
        print(f'{i = }')

    for j in range(1, 10, 2):
        print(f'{j = }')

    for letter in 'Millennium':
        print(f'{letter = }')

    return True


if __name__ == '__main__':
    # first_py()
    # first_date()
    operator_for()
