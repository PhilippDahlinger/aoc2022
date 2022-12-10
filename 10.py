import numpy as np

from utils.read_txt_data import txt_to_numpy, txt_to_str


class Device:
    def __init__(self, program, first_task=True):
        self.value = 1
        self.program = program
        self.current_line = None
        self.doing_adding = False
        self.pc = 0
        self.cycle_count = 1

        self.first_task = first_task

        self.screen = np.zeros((6, 40), dtype=int)



        self.total_signal_strength = 0

    def cycle(self, compute_signal_strength, use_crt):
        if compute_signal_strength and self.cycle_count % 40 == 20 and self.cycle_count < 230:
            signal_strength = self.value * self.cycle_count
            self.total_signal_strength += signal_strength
            print(self.cycle_count, self.value)

        if use_crt:
            x = (self.cycle_count - 1) % 40
            y = (self.cycle_count - 1) // 40
            if abs(x - self.value) <= 1:
                # draw
                self.screen[y, x] = 1

        if self.doing_adding:
            _, amount = self.current_line.split(" ")
            self.value += int(amount)
            self.doing_adding = False
        else:
            self.current_line = self.program[self.pc]
            self.pc += 1
            if self.current_line.startswith("noop"):
                pass
            else:
                self.doing_adding = True

        self.cycle_count += 1

    def execute(self):
        if self.first_task:
            compute_signal_strength = True
            use_crt = False
        else:
            compute_signal_strength = False
            use_crt = True
        while self.pc < len(self.program):
            self.cycle(compute_signal_strength, use_crt)
        if compute_signal_strength:
            print("Total Signal strength:", self.total_signal_strength)
        if use_crt:
            self.print_screen()

    def print_screen(self):
        for row in self.screen:
            row_str = ""
            for ch in row:
                row_str += "██" if ch > 0.5 else "  "
            print(row_str)



def first():
    program = txt_to_str("data/10.txt").split("\n")
    x = Device(program, first_task=True)
    x.execute()

def second():
    program = txt_to_str("data/10.txt").split("\n")
    x = Device(program, first_task=False)
    x.execute()




if __name__ == "__main__":
    first()
    second()