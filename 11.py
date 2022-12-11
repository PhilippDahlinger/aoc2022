from collections import deque

from tqdm import tqdm

from utils.read_txt_data import txt_to_numpy, txt_to_str
import time

class Monkey:
    def __init__(self, desc, div_by_3):
        lines = desc.split("\n")
        self.id = int(lines[0][-2])

        items_str = lines[1][lines[1].find(":") + 2:]
        self.items = deque([int(x) for x in items_str.split(", ")])

        operation_str = lines[2][lines[2].find("=") + 2:].split(" ")
        if operation_str[1] == "+":
            self.operation = lambda x: x + int(operation_str[-1])
        else:
            if operation_str[-1] == "old":
                self.operation = lambda x: x * x
            else:
                self.operation = lambda x: x * int(operation_str[-1])

        self.div_by_3 = div_by_3

        self.test_number = int(lines[3].split(" ")[-1])
        self.true_monkey = int(lines[4].split(" ")[-1])
        self.false_monkey = int(lines[5].split(" ")[-1])

        self.inspection_counter = 0


    def receive_item(self, new_item):
        self.items.append(new_item)

    def make_turn(self, all_monkeys, total_modulo):
        while len(self.items) > 0:
            self.inspection_counter += 1
            item = self.items.popleft()

            if total_modulo is not None:
                item = item % total_modulo
            after_inspect = self.operation(item)
            if self.div_by_3:
                after_boredom = after_inspect // 3
            else:
                after_boredom = after_inspect


            if after_boredom % self.test_number == 0:
                new_monkey = self.true_monkey
            else:
                new_monkey = self.false_monkey
            all_monkeys[new_monkey].receive_item(after_boredom)


class MonkeyCircle:
    def __init__(self, complete_desc, div_by_3):
        self.all_monkeys = []
        for desc in complete_desc.split("\n\n"):
            self.all_monkeys.append(Monkey(desc, div_by_3))

        for i in range(len(self.all_monkeys)):
            assert i == self.all_monkeys[i].id

        if div_by_3:
            self.total_modulo = None
        else:
            self.total_modulo = 1
            for m in self.all_monkeys:
                self.total_modulo *= m.test_number


    def round(self):
        for monkey in self.all_monkeys:
            monkey.make_turn(all_monkeys=self.all_monkeys, total_modulo=self.total_modulo)

    def get_monkey_business(self):
        ics = []
        for monkey in self.all_monkeys:
            ics.append(monkey.inspection_counter)
        ics = sorted(ics)
        print(ics[-1] * ics[-2])
def first():
    complete_desc = txt_to_str("data/11.txt")
    mc = MonkeyCircle(complete_desc, div_by_3=True)
    for i in range(20):
        mc.round()
    mc.get_monkey_business()

def second():
    t1 = time.time()
    complete_desc = txt_to_str("data/11.txt")
    mc = MonkeyCircle(complete_desc, div_by_3=False)
    for i in tqdm(range(10000)):
        mc.round()
    mc.get_monkey_business()
    print("Time of part 2:", time.time() - t1)


if __name__ == "__main__":
    first()
    second()