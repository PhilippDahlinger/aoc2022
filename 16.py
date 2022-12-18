import copy

import numpy as np

from utils.read_txt_data import txt_to_str

class Env:
    def __init__(self):
        self.nodes, self.ids, self.names = get_data()
        self.dists = floyd_warshall(self.nodes, self.ids)
        self.relevant_nodes = {n: self.nodes[n] for n in self.nodes if self.nodes[n]["relevant"]}

    def get_dist(self, a, b):
        id_a, id_b = self.ids[a], self.ids[b]
        return self.dists[id_a, id_b]

    def value_of_node(self, s, current_pos, current_time, enabled, look_aheads):
        d = self.get_dist(s, current_pos)
        if d + 1 >= current_time:
            return 0
        remaining_time_after_opening = current_time - d - 1
        reward = remaining_time_after_opening * self.nodes[s]["flow_rate"]
        new_enabled = copy.deepcopy(enabled)
        new_enabled.add(s)
        if look_aheads > 0:
            next_value = 0
            for new_s in self.relevant_nodes:
                if new_s in new_enabled:
                    continue
                new_s_value = self.value_of_node(new_s, s, remaining_time_after_opening, new_enabled, look_aheads - 1)
                next_value = max(next_value, new_s_value)
            reward += next_value
        return reward


    def multi_agent_value_of_pair_of_nodes(self, s1, s2, pos1, pos2, t1, t2, enabled, look_aheads):
        d1 = self.get_dist(s1, pos1)
        d2 = self.get_dist(s2, pos2)
        if d1 + 1 >= t1:
            return self.value_of_node(s2, pos2, t2, copy.deepcopy(enabled), look_aheads)
        elif d2 + 1 >= t2:
            return self.value_of_node(s1, pos1, t1, copy.deepcopy(enabled), look_aheads)
        new_t1 = t1 - d1 - 1
        new_t2 = t2 -d2 -1
        reward = new_t1 * self.nodes[s1]["flow_rate"] + new_t2 * self.nodes[s2]["flow_rate"]
        new_enabled = copy.deepcopy(enabled)
        new_enabled.add(s1)
        new_enabled.add(s2)
        if look_aheads > 0:
            next_value = 0
            for new_s1 in self.relevant_nodes:
                if new_s1 in new_enabled:
                    continue
                for new_s2 in self.relevant_nodes:
                    if  new_s1 == new_s2 or new_s2 in new_enabled:
                        continue
                    new_s1_s2_value = self.multi_agent_value_of_pair_of_nodes(new_s1, new_s2, s1, s2, new_t1, new_t2, new_enabled, look_aheads - 1)
                    next_value = max(next_value, new_s1_s2_value)
            reward += next_value
        return reward

def floyd_warshall(nodes, ids):
    shortest_dists = np.ones((len(nodes), len(nodes)), dtype=int) * 10000000
    for name, node in nodes.items():
        id_0 = ids[name]
        for nb in node["nbs"]:
            id_1 = ids[nb]
            shortest_dists[id_0, id_1] = 1
            shortest_dists[id_1, id_0] = 1
        shortest_dists[id_0, id_0] = 0

    for k in range(len(shortest_dists)):
        for i in range(len(shortest_dists)):
            for j in range(len(shortest_dists)):
                shortest_dists[i, j] = min(shortest_dists[i,j], shortest_dists[i, k] + shortest_dists[k, j])

    return shortest_dists
def get_data():
    data_str = txt_to_str("data/16.txt").split("\n")
    ids = {}
    names = {}
    nodes = {}

    for idx, line in enumerate(data_str):
        words = line.split(" ")
        name = words[1]
        ids[name] = idx
        names[idx] = name

        flow_rate = words[4]
        flow_rate = int(flow_rate.split("=")[1][:-1])
        nbs = words[9:]
        nbs = [nb[:-1] if nb[-1] == "," else nb for nb in nbs ]
        nodes[name] = {"id": idx, "flow_rate": flow_rate, "nbs": nbs, "relevant": flow_rate > 0 or name =="AA"}

    return nodes, ids, names


def first():
    env = Env()
    print(env.value_of_node("AA", "AA", 31, set(), 8))

def second():
    env = Env()
    # one_step_closer(0, env, "AA", "AA", 26, 26, {"AA"}, 3)
    one_step_closer(614, env, "ZD", "SJ", 23, 21, {"AA", "ZD", "SJ"}, 4)
    # one_step_closer(1306, env, "RL", "IG", 20, 17, {"AA", "ZD", "SJ", "RL", "IG"}, 2)
    print("---------------")
    # one_step_closer(1306, env, "RL", "IG", 20, 17, {"AA", "ZD", "SJ", "RL", "IG"}, 4)
    #
    # moves = []
    #
    # enabled = {"AA"}
    # total_reward = 0
    # for s1 in env.relevant_nodes:
    #     if s1 == "AA":
    #         continue
    #     for s2 in env.relevant_nodes:
    #         if s2 == "AA" or s2 <= s1:
    #             continue
    #         reward = env.multi_agent_value_of_pair_of_nodes(s1, s2, "AA", "AA", 26, 26, enabled, 2)
    #         moves.append((s1, s2, reward))
    # moves = list(reversed(sorted(moves, key=lambda x: x[2])))
    # p1, p2, _ = moves[0]
    # print("step:", p1, p2)
    # t1 = 26 - env.get_dist("AA", p1) - 1
    # t2 = 26 - env.get_dist("AA", p2) - 1
    # reward = t1 * env.nodes[p1]["flow_rate"] + t2 * env.nodes[p2]["flow_rate"]
    # total_reward += reward
    # enabled = {"AA", p1, p2}
    # moves = []
    # for s1 in env.relevant_nodes:
    #     if s1 in enabled:
    #         continue
    #     for s2 in env.relevant_nodes:
    #         if s1 == s2 or s2 in enabled:
    #             continue
    #         reward = env.multi_agent_value_of_pair_of_nodes(s1, s2, p1, p2, t1, t2, enabled, 2)
    #         moves.append((s1, s2, reward))
    # moves = list(reversed(sorted(moves, key=lambda x: x[2])))
    # p1, p2, reward = moves[0]
    # print(total_reward + reward)

def one_step_closer(prev_reward, env, p1, p2, t1, t2, enabled, look_aheads):
    moves = []
    for s1 in env.relevant_nodes:
        if s1 in enabled:
            continue
        for s2 in env.relevant_nodes:
            if s1 == s2 or s2 in enabled:
                continue
            reward = env.multi_agent_value_of_pair_of_nodes(s1, s2, p1, p2, t1, t2, enabled, look_aheads)
            moves.append((s1, s2, reward))
    moves = list(reversed(sorted(moves, key=lambda x: x[2])))
    new_p1, new_p2, reward = moves[0]

    new_t1 = t1 - env.get_dist(p1, new_p1) - 1
    new_t2 = t2 - env.get_dist(p2, new_p2) - 1
    this_step_reward = new_t1 * env.nodes[new_p1]["flow_rate"] + new_t2 * env.nodes[new_p2]["flow_rate"]

    print("New nodes", new_p1, new_p2)
    print("New times", new_t1, new_t2)
    print("Total expected reward", prev_reward + reward)
    print("Backward reward", prev_reward + this_step_reward)
    return new_p1, new_p2, prev_reward + this_step_reward, prev_reward + reward


if __name__ == "__main__":
    # first()
    second()