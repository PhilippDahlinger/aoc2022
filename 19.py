import math

from utils.read_txt_data import txt_to_str

class Env:
    def __init__(self, cost):
        self.costs = cost

    def get_next_states(self, robots, res, t):
        def get_new_res(robots, res, time_producing):
            new_res = []
            for i in range(4):
                new_res.append(res[i] + robots[i] * time_producing)
            return new_res

        next_states = []

        # ore robot
        if robots[3] == 0 and robots[0] < 5 and t > 20:
            price = self.costs[0]
            missing_ore = price - res[0]
            wait_time = max(0, math.ceil(missing_ore / robots[0]))
            new_t = t - wait_time - 1
            if new_t > 0:
                new_res = get_new_res(robots, res, t - new_t)
                new_res[0] -= price
                new_robots = list(robots)
                new_robots[0] += 1
                next_states.append((tuple(new_robots), tuple(new_res), new_t))

        # clay robot
        if robots[3] == 0 and robots[1] < 12:
            price = self.costs[1]
            missing_ore = price - res[0]
            wait_time = max(0, math.ceil(missing_ore / robots[0]))
            new_t = t - wait_time - 1
            if new_t > 0:
                new_res = get_new_res(robots, res, t - new_t)
                new_res[0] -= price
                new_robots = list(robots)
                new_robots[1] += 1
                next_states.append((tuple(new_robots), tuple(new_res), new_t))

        # obsidian robot
        if robots[1] != 0:
            price_ore, price_clay = self.costs[2]
            missing_ore = price_ore - res[0]
            missing_clay = price_clay - res[1]
            wait_time = max(0, math.ceil(missing_ore / robots[0]), math.ceil(missing_clay / robots[1]))
            new_t = t - wait_time - 1
            if new_t > 0:
                new_res = get_new_res(robots, res, t - new_t)
                new_res[0] -= price_ore
                new_res[1] -= price_clay
                new_robots = list(robots)
                new_robots[2] += 1
                next_states.append((tuple(new_robots), tuple(new_res), new_t))

        # geode robot
        if robots[2] != 0:
            price_ore, price_obs = self.costs[3]
            missing_ore = price_ore - res[0]
            missing_obs = price_obs - res[2]
            wait_time = max(0, math.ceil(missing_ore / robots[0]), math.ceil(missing_obs / robots[2]))
            new_t = t - wait_time - 1
            if new_t > 0:
                new_res = get_new_res(robots, res, t - new_t)
                new_res[0] -= price_ore
                new_res[2] -= price_obs
                new_robots = list(robots)
                new_robots[3] += 1
                next_states.append((tuple(new_robots), tuple(new_res), new_t))
        return next_states


    def get_value(self, robots, res, t):
        next_state = self.get_next_states(robots, res, t)
        if len(next_state) == 0:
            return res[3] + t * robots[3]
        value = 0
        for new_s in next_state:
            value = max(value, self.get_value(new_s[0], new_s[1], new_s[2]))
        return value
def first():
    result = 0
    for line in  txt_to_str("data/19.txt").split("\n"):
        words = line.split(" ")
        idx = int(words[1][:-1])
        ore_cost = int(words[6])
        clay_cost = int(words[12])
        obs_cost = int(words[18]), int(words[21])
        geode_cost = int(words[27]), int(words[30])

        env = Env((ore_cost, clay_cost, obs_cost, geode_cost))
        value = env.get_value((1, 0, 0, 0), (0, 0, 0, 0), 24)
        print(idx, value)
        result += value * idx
    print(result)

def second():
    result = 1
    for line in  txt_to_str("data/19.txt").split("\n")[:3]:
        words = line.split(" ")
        idx = int(words[1][:-1])
        ore_cost = int(words[6])
        clay_cost = int(words[12])
        obs_cost = int(words[18]), int(words[21])
        geode_cost = int(words[27]), int(words[30])

        env = Env((ore_cost, clay_cost, obs_cost, geode_cost))
        # env = Env((2, 3, (3, 8), (3, 12)))
        value = env.get_value((1, 0, 0, 0), (0, 0, 0, 0), 32)
        print(idx, value)
        result *= value
    print(result)


if __name__ == "__main__":
    first()  # does not work with current heuristics from second
    second()