import copy

from utils.read_txt_data import txt_to_str


def first():
    data_str = txt_to_str("data/20.txt").split("\n")
    data = []
    for idx, x in enumerate(data_str):
        data.append((idx, int(x)))
    sorted_data = copy.deepcopy(data)
    for idx, x in sorted_data:
        # print([y[1] for y in data])
        pos = data.index((idx, x))
        del data[pos]
        new_pos = (pos + x) % len(data)
        data.insert(new_pos, (idx, x))
    # print( [y[1] for y in data])
    data = [x[1] for x in data]
    zero_pos = data.index(0)
    print(zero_pos)
    sol = 0
    for i in [1000, 2000, 3000]:
        pos = (zero_pos + i) % len(sorted_data)
        print(data[pos])
        sol += data[pos]
    # print(data[1000][1] + data[2000][1] + data[3000][1])
    print(sol)

def second():
    data_str = txt_to_str("data/20.txt").split("\n")
    data = []
    for idx, x in enumerate(data_str):
        data.append((idx, int(x) * 811589153))
    sorted_data = copy.deepcopy(data)
    for _ in range(10):
        for idx, x in sorted_data:
            # print([y[1] for y in data])
            pos = data.index((idx, x))
            del data[pos]
            new_pos = (pos + x) % len(data)
            data.insert(new_pos, (idx, x))
    data = [x[1] for x in data]
    zero_pos = data.index(0)
    print(zero_pos)
    sol = 0
    for i in [1000, 2000, 3000]:
        pos = (zero_pos + i) % len(sorted_data)
        print(data[pos])
        sol += data[pos]
    # print(data[1000][1] + data[2000][1] + data[3000][1])
    print(sol)

if __name__ == "__main__":
    # first()
    second()