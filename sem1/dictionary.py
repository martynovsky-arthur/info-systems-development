# Подсчитать сколько раз каждая гласная встертилась в слове
def count_vowels(word: str) -> dict[str, int]:

    vowels: set[str] = set('aioeu')

    found: dict[str, int] = {}

    for letter in word:
        if letter in vowels:
            if not found.get(letter):
                found[letter] = 0
            found[letter] += 1

    return found


if __name__ == '__main__':
    found: dict[str, int] = count_vowels('Millennium')
    for k, v in found.items():
        print(f'{k = }, {v = }')
