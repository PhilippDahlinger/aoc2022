from utils.read_txt_data import txt_to_str

def get_data():
    data = txt_to_str("./data/02.txt")
    pairs = data.split("\n")
    pairs = [pair.split(" ") for pair in pairs]
    return pairs

def first():
    data = get_data()

    transl = {
        "A": 1,
        "B": 2,
        "C": 3,
        "X": 1,
        "Y": 2,
        "Z": 3,
    }
    winning_points = {
        (1, 2): 6,
        (2, 3): 6,
        (3, 1): 6,
        (2, 1): 0,
        (3, 2): 0,
        (1, 3): 0,
        (1, 1): 3,
        (2, 2): 3,
        (3, 3): 3,
    }
    total_points = 0
    for pair in data:
        enc_pair = (transl[pair[0]], transl[pair[1]])
        total_points += winning_points[enc_pair]
        total_points += enc_pair[1]
    print(total_points)

def second():
    data = get_data()
    transl = {
        ("A", "X"): (1, 3),
        ("A", "Y"): (1, 1),
        ("A", "Z"): (1, 2),
        ("B", "X"): (2, 1),
        ("B", "Y"): (2, 2),
        ("B", "Z"): (2, 3),
        ("C", "X"): (3, 2),
        ("C", "Y"): (3, 3),
        ("C", "Z"): (3, 1)
    }
    winning_points = {
        (1, 2): 6,
        (2, 3): 6,
        (3, 1): 6,
        (2, 1): 0,
        (3, 2): 0,
        (1, 3): 0,
        (1, 1): 3,
        (2, 2): 3,
        (3, 3): 3,
    }
    total_points = 0
    for pair in data:
        enc_pair = transl[tuple(pair)]
        total_points += winning_points[enc_pair]
        total_points += enc_pair[1]
    print(total_points)


if __name__ == "__main__":
    second()
