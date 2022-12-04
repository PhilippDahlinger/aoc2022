from utils.read_txt_data import txt_to_str


def first():
    total = 0

    str_data = txt_to_str("data/04.txt")
    lines = str_data.split("\n")
    for line in lines:
        pairs = line.split(",")
        sets = []
        for pair in pairs:
            ranges = pair.split("-")
            sets.append(set(range(int(ranges[0]), int(ranges[1]) + 1)))
        if sets[0].issubset(sets[1]) or sets[1].issubset(sets[0]):
            total += 1
    print(total)

def second():
    total = 0

    str_data = txt_to_str("data/04.txt")
    lines = str_data.split("\n")
    for line in lines:
        pairs = line.split(",")
        sets = []
        for pair in pairs:
            ranges = pair.split("-")
            sets.append(set(range(int(ranges[0]), int(ranges[1]) + 1)))
        if len(sets[0].intersection(sets[1])) > 0:
            total += 1
    print(total)

if __name__ == "__main__":
    first()
    second()
