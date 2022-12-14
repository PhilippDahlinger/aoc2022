from utils.read_txt_data import txt_to_numpy, txt_to_str


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
        print(sand_counter)







def first():
    c = CaveSystem()
    c.simuale_all_sand()

def second():
    c = CaveSystem(floor=True)
    c.simuale_all_sand()

if __name__ == "__main__":
    first()
    second()