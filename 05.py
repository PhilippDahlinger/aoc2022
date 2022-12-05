from utils.read_txt_data import txt_to_str


def get_start_pos():
    stacks = []
    stacks.append(["T", "P", "Z", "C", "S", "L", "Q", "N"])
    stacks.append(["L", "P", "T", "V", "H", "C", "G"])
    stacks.append(["D", "C", "Z", "F"])
    stacks.append(["G", "W", "T", "D", "L", "M", "V", "C"])
    stacks.append(["P", "W", "C"])
    stacks.append(["P", "F", "J", "D", "C", "T", "S", "Z"])
    stacks.append(["V", "W", "G", "B", "D"])
    stacks.append(["N", "J", "S", "Q", "H", "W"])
    stacks.append(["R", "C", "Q", "F", "S", "L", "V"])

    return stacks


def first():
    stacks = get_start_pos()
    data = txt_to_str("data/05.txt")
    for line in data.split("\n"):
        words = line.split(" ")
        start_idx = int(words[3]) - 1
        end_idx = int(words[5]) - 1
        amount = int(words[1])
        for i in range(amount):
            crate = stacks[start_idx].pop()
            stacks[end_idx].append(crate)

    result = ""
    for stack in stacks:
        result += stack[-1]
    print(result)

def second():
    stacks = get_start_pos()
    data = txt_to_str("data/05.txt")
    for line in data.split("\n"):
        words = line.split(" ")
        start_idx = int(words[3]) - 1
        end_idx = int(words[5]) - 1
        amount = int(words[1])
        stacks[end_idx] += stacks[start_idx][-amount:]
        for i in range(amount):
            del stacks[start_idx][-1]
    result = ""
    for stack in stacks:
        result += stack[-1]
    print(result)

if __name__ == "__main__":
    first()
    second()
