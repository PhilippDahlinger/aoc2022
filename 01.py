from utils.read_txt_data import txt_to_str

def process_data():
    data_str = txt_to_str("./data/01.txt")
    split_1 = data_str.split("\n\n")
    split_2 = [s.split("\n") for s in split_1]
    data = []
    for elve in split_2:

        data.append([int(it) for it in elve if it != ""])
    return data

def first(data):
    totals = []
    for elve in data:
        totals.append(sum(elve))
    return max(totals)

def second(data):
    totals = []
    for elve in data:
        totals.append(sum(elve))
    totals = sorted(totals)
    return sum(totals[-3:])

if __name__ == "__main__":
    data = process_data()
    print(first(data))
    print(second(data))
