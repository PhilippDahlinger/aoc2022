import random

from asciimatics.event import KeyboardEvent

from utils.read_txt_data import txt_to_str

from time import sleep
from asciimatics.effects import Cycle, Stars
from asciimatics.renderers import FigletText
from asciimatics.scene import Scene
from asciimatics.screen import Screen


class CaveSystem:
    def __init__(self, floor=False):
        self.elts = {}
        data = txt_to_str("data/14.txt").split("\n")
        for line in data:
            pos_list = line.split(" -> ")
            for i in range(len(pos_list) - 1):
                pos_x_1, pos_y_1 = [int(c) for c in pos_list[i].split(",")]
                pos_x_2, pos_y_2 = [int(c) for c in pos_list[i + 1].split(",")]
                if pos_x_1 == pos_x_2:
                    assert pos_y_1 != pos_y_2, (pos_x_1, pos_x_2, pos_y_1, pos_y_2)
                    for y in range(min(pos_y_1, pos_y_2), max(pos_y_1, pos_y_2) + 1):
                        self.elts[pos_x_1, y] = "rock"
                else:
                    assert pos_x_1 != pos_x_2, (pos_x_1, pos_x_2, pos_y_1, pos_y_2)
                    for x in range(min(pos_x_1, pos_x_2), max(pos_x_1, pos_x_2) + 1):
                        self.elts[x, pos_y_1] = "rock"
        heights = [r[1] for r in self.elts]
        self.abyss_lvl = max(heights) + 2
        if floor:
            widths = [r[0] for r in self.elts]
            for x in range(min(widths) - 1000, max(widths) + 1000):
                self.elts[x, self.abyss_lvl] = "floor"
        self.widths = [r[0] for r in self.elts]
        self.offset_x = offset_x = min(self.widths) - 20
        self.offset_y = 0

        self.sand_elt = [500, 0]

    def step_sand_elt(self):
        if self.sand_elt[1] >= self.abyss_lvl:
            self.sand_elt = [500, 0]
            return False
        elif (self.sand_elt[0], self.sand_elt[1] + 1) not in self.elts:
            self.sand_elt[1] += 1
        elif (self.sand_elt[0] - 1, self.sand_elt[1] + 1) not in self.elts:
            self.sand_elt[0] -= 1
            self.sand_elt[1] += 1
        elif (self.sand_elt[0] + 1, self.sand_elt[1] + 1) not in self.elts:
            self.sand_elt[0] += 1
            self.sand_elt[1] += 1
        else:
            self.elts[tuple(self.sand_elt)] = "sand"
            self.sand_elt = [500, 0]
            return True

    def simulate_sand_elt(self):
        sand = [500, 0]
        if tuple(sand) in self.elts:
            return False
        while True:
            if sand[1] >= self.abyss_lvl:
                return False
            elif (sand[0], sand[1] + 1) not in self.elts:
                sand[1] += 1
            elif (sand[0] - 1, sand[1] + 1) not in self.elts:
                sand[0] -= 1
                sand[1] += 1
            elif (sand[0] + 1, sand[1] + 1) not in self.elts:
                sand[0] += 1
                sand[1] += 1
            else:
                self.elts[tuple(sand)] = "sand"
                return True

    def simuale_all_sand(self):
        sand_counter = 0
        while self.simulate_sand_elt():
            sand_counter += 1


def first(screen, set_position_only=True, frame_sleep=0.1):
    c = CaveSystem(floor=False)

    while True:
        screen.clear_buffer(fg=Screen.COLOUR_WHITE, bg=Screen.COLOUR_BLACK, attr=Screen.A_NORMAL)
        e = screen.get_event()
        if e is not None and type(e) == KeyboardEvent:
            if e.key_code == Screen.KEY_UP:
                c.offset_y -= 1
            if e.key_code == Screen.KEY_DOWN:
                c.offset_y += 1
            if e.key_code == Screen.KEY_LEFT:
                c.offset_x -= 1
            if e.key_code == Screen.KEY_RIGHT:
                c.offset_x += 1

        if set_position_only:
            c.simulate_sand_elt()
        else:
            c.step_sand_elt()
            screen.print_at("o", c.sand_elt[0] - c.offset_x, c.sand_elt[1] - c.offset_y, colour=Screen.COLOUR_RED)

        for elt in c.elts:
            if c.elts[elt] == "rock":
                symbol = "█"
                color = Screen.COLOUR_GREEN
            else:
                symbol = "o"
                color = Screen.COLOUR_CYAN
            screen.print_at(symbol, elt[0] - c.offset_x, elt[1] - c.offset_y, colour=color)
        screen.refresh()
        sleep(frame_sleep)


if __name__ == "__main__":
    set_inp = input("Animate falling sand? (y|n)")
    if set_inp == "y":
        set_position_only = False
    else:
        set_position_only = True
    if set_position_only:
        frame_sleep = 0.05
    else:
        frame_sleep = 0.02
    Screen.wrapper(lambda s: first(s, set_position_only=set_position_only, frame_sleep=frame_sleep))
