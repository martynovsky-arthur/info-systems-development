def person():
    person = ['Иванов', 1990, 'mail']


def count_vowels(new_word: str) -> list[str]:
    '''
    Parameters
        new_word: str - Слово для подсчета гласных

    Return
        found: list - Список из найденых гласных
    '''

    vowels: list[str] = list('aiueo')
    found: list[str] = []
    for letter in new_word:
        if letter in vowels and letter not in found:
            found.append(letter)

    return found


def count_set(new_word: str) -> set[str]:
    return set('aiueo').intersection(set(new_word))


if __name__ == '__main__':
    print(count_vowels('Martynovsky'))
    print(count_set('Martynovsky'))
