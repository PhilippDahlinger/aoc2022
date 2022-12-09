import math

from utils.read_txt_data import txt_to_numpy, txt_to_str

sign = lambda x: 0 if x == 0 else math.copysign(1, x)


class Rope:
    def __init__(self, length):
        self.length = length
        self.elts = []
        for e in range(length):
            self.elts.append([0, 0])
        self.visited = set()

    def move_dir(self, dir):
        if dir == "R":
            self.elts[0][1] += 1
        elif dir == "L":
            self.elts[0][1] -= 1
        elif dir == "U":
            self.elts[0][0] += 1
        elif dir == "D":
            self.elts[0][0] -= 1
        else:
            raise ValueError(dir)
        for i in range(1, self.length):
            head = self.elts[i - 1]
            tail = self.elts[i]
            for axis in [0, 1]:
                other_axis = 1 - axis
                if abs(head[axis] - tail[axis]) >= 2:
                    axis_dir = sign(head[axis] - tail[axis])
                    other_axis_dir = sign(head[other_axis] - tail[other_axis])
                    tail[axis] += axis_dir
                    tail[other_axis] += other_axis_dir
                    break
        self.visited.add(tuple(self.elts[-1]))

    def perform_move(self, move):
        dir, steps = move.split(" ")
        for i in range(int(steps)):
            self.move_dir(dir)


def first():
    moves = txt_to_str("data/09.txt").split("\n")
    rope = Rope(length=2)
    for move in moves:
        rope.perform_move(move)
    print(len(rope.visited))


def second():
    moves = txt_to_str("data/09.txt").split("\n")
    rope = Rope(length=10)
    for move in moves:
        rope.perform_move(move)
    print(len(rope.visited))


if __name__ == "__main__":
    first()
    second()
