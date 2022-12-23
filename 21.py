from tqdm import tqdm

from utils.read_txt_data import txt_to_str


class MonkeyYelling:
    def __init__(self, second=False):
        data_str = txt_to_str("data/21.txt").split("\n")
        self.data = {}
        for line in data_str:
            words = line.split(" ")
            name = words[0][0:4]
            if len(words) == 2:
                number = int(words[1])
                self.data[name] = number
            else:
                m1 = words[1]
                op = words[2]
                m2 = words[3]
                self.data[name] = (m1, op, m2)

        self.second = second


    def reset_with_human(self, human_number):
        self.data["humn"] = human_number

    def decode(self, name, interior=False):
        if type(self.data[name]) == int:
            return self.data[name]
        m1, op, m2 = self.data[name]
        if self.second and interior and (m1 == "humn" or m2 == "humn"):
            return "human"
        v1 = self.decode(m1, interior=True)
        v2 = self.decode(m2, interior=True)
        if v1 == "human" or v2 == "human":
            return "human"
        if name == "root" and self.second:
            result = v1 == v2
        elif op == "+":
            result = v1 + v2
        elif op == "-":
            result = v1 - v2
        elif op == "*":
            result = v1 * v2
        else:
            result = v1 / v2
        return result

    def find_human(self):
        active_node = self.data["root"]
        m1, op, m2 = active_node
        if self.decode(m1) == "human":
            relevant = m1
            v = self.decode(m2)
            assert v != "human"
        else:
            relevant = m2
            v = self.decode(m2)
        print("stop")


def first():
    m = MonkeyYelling()
    print(m.decode("root"))


def second():
    m = MonkeyYelling(second=True)
    m.find_human()


if __name__ == "__main__":
    second()