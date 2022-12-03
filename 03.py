import string

from utils.read_txt_data import txt_to_str


def get_data():
    str_data = txt_to_str("data/03.txt")
    rucksacks = str_data.split("\n")
    return rucksacks

def first(rucksacks):
    total_priority = 0
    for r in rucksacks:
        first_half = set(r[:len(r)//2])
        second_half = set(r[len(r)//2:])
        intersection = first_half.intersection(second_half)
        elt = min(intersection)
        total_priority += get_priority(elt)
    print(total_priority)


alphabet = list(string.ascii_lowercase)
priorities = {}
for idx, letter in enumerate(alphabet):
    priorities[letter] = idx + 1

Alphabet = list(string.ascii_uppercase)
for idx, letter in enumerate(Alphabet):
    priorities[letter] = idx + 27

def get_priority(elt):
    return priorities[elt]

def second(rucksacks):
    total_priorites = 0
    for idx in range(0, len(rucksacks), 3):
        a, b, c = rucksacks[idx], rucksacks[idx + 1], rucksacks[idx + 2]
        badge = min(set(a).intersection(set(b), set(c)))
        total_priorites += get_priority(badge)
    print(total_priorites)


if __name__ == "__main__":
    rucksacks = get_data()
    first(rucksacks)
    second(rucksacks)