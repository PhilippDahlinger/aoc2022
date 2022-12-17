from collections import defaultdict

import numpy as np
from tqdm import tqdm

from utils.read_txt_data import txt_to_str

class Env:
    def __init__(self):
        jet_str = txt_to_str("data/17.txt")
        self.jet = list(jet_str)
        self.jet = [-1 if x == "<" else 1 for x in self.jet]
        self.step = 0
        self.real_step = 0
        self.rock_idx = 0
        self.settled = {}
        self.active_rock = None
        self.error = False

    def get_current_height(self):
        if len(self.settled) == 0:
            highest = -1
        else:
            highest = max(self.settled, key=lambda x: x[1])[1]
        return highest
    def simulate_rock(self):
        # create rock
        highest = self.get_current_height()
        self.active_rock = Rock(self.rock_idx, y_offset=highest + 4)
        while True:
            # sidewards mov
            current_jet = self.jet[self.step]
            self.step = (self.step + 1) % len(self.jet)
            self.real_step += 1
            rel_mov = [current_jet, 0]
            self.active_rock.move(rel_mov, self.settled)
            # downwards mov
            rel_mov = [0, -1]
            should_settle = not self.active_rock.move(rel_mov, self.settled)
            if should_settle:
                if self.step > 1000 and self.active_rock.tiles[0][1] < 10:
                    self.error = True
                for tiles in self.active_rock.tiles:
                    self.settled[tuple(tiles)] = 1
                # heuristic: remove lower parts
                self.settled = {t: 1 for t in self.settled if t[1] >= highest - 30}
                break
        self.rock_idx = (self.rock_idx + 1) % 5

    def visualize_settled(self):
        min_y = min(self.settled, key=lambda x: x[1])[1]
        max_y = self.get_current_height() + 5
        screen = np.zeros((max_y - min_y, 7))
        for t in self.settled:
            screen[-(t[1] - min_y) - 1, t[0]] = 1
        for row in screen:
            row_str = "|"
            for char in row:
                row_str += "." if char == 0 else "#"
            print(row_str + "|")
        print("-----------------------------------------------------------")

class Rock:
    def __init__(self, idx, y_offset):
        if idx == 0:
            self.tiles = [
                [2, y_offset], [3, y_offset], [4, y_offset], [5, y_offset]
            ]
        elif idx == 1:
            self.tiles = [
                [3, y_offset], [2, y_offset + 1], [3, y_offset + 1], [4, y_offset + 1], [3, y_offset + 2]
            ]
        elif idx == 2:
            self.tiles = [
                [2, y_offset], [3, y_offset], [4, y_offset], [4, y_offset + 1], [4, y_offset + 2]
            ]
        elif idx == 3:
            self.tiles = [
                [2, y_offset], [2, y_offset + 1], [2, y_offset + 2], [2, y_offset + 3]
            ]
        elif idx == 4:
            self.tiles = [
                [2, y_offset], [3, y_offset], [2, y_offset + 1], [3, y_offset + 1]
            ]
        else:
            raise ValueError()

    def move(self, rel_mov, settled):
        falling = rel_mov[0] == 0
        new_tiles = [[t[0] + rel_mov[0], t[1] + rel_mov[1]] for t in self.tiles]
        # check for collision
        for t in new_tiles:
            # boarders
            if falling:
                if t[1] < 0:
                    return False
            else:
                if t[0] < 0 or t[0] > 6:
                    return False

            if tuple(t) in settled:
                return False
        # all checks passed
        self.tiles = new_tiles
        return True



def first():
    env = Env()
    for i in range(2022):
        env.simulate_rock()
        env.visualize_settled()
    print(env.get_current_height() + 1)


def get_chosen_step():
    env = Env()
    step_at_0 = defaultdict(lambda: 0)
    for i in tqdm(range(1000000)):
        if i % 5 == 0:
            step_at_0[env.step] += 1
        env.simulate_rock()
    env.visualize_settled()
    print(step_at_0)
    chosen_step = max(step_at_0, key=lambda x: step_at_0[x])
    print(chosen_step, step_at_0[chosen_step])
    print(env.error)


def get_height(num_rocks):
    rock_offset = 3460
    height_offset = 5446
    rock_period = 1725
    height_inc = 2709
    rest_values = []
    env = Env()
    for i in range(3460):
        env.simulate_rock()

    for i in range(1725):
        rest_values.append(env.get_current_height() + 1 - height_offset)
        env.simulate_rock()


    if num_rocks < 3460:
        return None
    num_periods = (num_rocks - rock_offset) // rock_period
    height = height_offset + num_periods * height_inc
    remaining_rocks = (num_rocks - rock_offset) % rock_period
    height += rest_values[remaining_rocks]
    return height


def second():
    num_rocks = 1000000000000
    print(get_height(num_rocks))
    # env = Env()
    # for i in range(num_rocks):
    #     env.simulate_rock()
    # print(env.get_current_height() + 1)


    # # get_chosen_step()
    # cycles = []
    # chosen_step = 80
    # env = Env()
    # for i in tqdm(range(10000)):
    #
    #     if i % 5 == 0:
    #         if env.step == chosen_step:
    #             cycles.append((i, env.real_step, env.get_current_height() + 1))
    #     env.simulate_rock()
    # print(cycles[2], cycles[3],cycles[4])
    # print("stop")




if __name__ == "__main__":
    # first()
    second()