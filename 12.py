import string
from collections import defaultdict
from queue import PriorityQueue


from utils.read_txt_data import txt_to_str



class Dijkstra:
    def __init__(self):
        self.map = txt_to_str("data/12.txt").split("\n")
        self.map = [list(s) for s in self.map]

        self.size = (len(self.map), len(self.map[0]))
        self.start_pos = None
        self.final_pos = None
        for i in range(self.size[0]):
            for j in range(self.size[1]):
                if self.map[i][j] == "S":
                    self.map[i][j] = "a"
                    self.start_pos = (i, j)
                if self.map[i][j] == "E":
                    self.final_pos = (i,j)
                    self.map[i][j] = "z"
        assert self.start_pos is not None
        assert self.final_pos is not None

        alphabet = list(string.ascii_lowercase)
        transl = {}
        for idx, letter in enumerate(alphabet):
            transl[letter] = idx

        self.map = [[transl[x] for x in line] for line in self.map]

        self.pred = {}
        self.explored = {}
        self.unexplored = defaultdict(lambda: 1000000)
        self.unexplored[self.final_pos] = 0

    def get_moves(self, pos):
        moves = []
        h = self.map[pos[0]][pos[1]]
        if pos[0] > 0 and h - self.map[pos[0] -1][pos[1]] <= 1:
            moves.append((pos[0] - 1, pos[1]))
        if pos[1] > 0 and h - self.map[pos[0]][pos[1] - 1]  <= 1:
            moves.append((pos[0], pos[1] - 1))
        if pos[0] < self.size[0] - 1 and h - self.map[pos[0] + 1][pos[1]] <= 1:
            moves.append((pos[0] + 1, pos[1]))
        if pos[1] < self.size[1] - 1 and h - self.map[pos[0]][pos[1] + 1] <= 1:
            moves.append((pos[0], pos[1] + 1))
        return moves

    def relax(self, u, v):
        if self.unexplored[u] + 1 < self.unexplored[v]:
            self.unexplored[v] = self.unexplored[u] + 1
            self.pred[v] = u

    def algo(self):
        while len(self.unexplored) > 0:
            # print(len(self.unexplored))
            u = min(self.unexplored, key=self.unexplored.get)
            for v in self.get_moves(u):
                if v not in self.explored:
                    self.relax(u, v)
            self.explored[u] = True
            del self.unexplored[u]

    def len_path(self, u):
        length = 0
        while u != self.final_pos:
            if u not in self.pred:
                return 1000000
            u = self.pred[u]
            length += 1
        return length




def first():
    dij = Dijkstra()
    dij.algo()
    print(dij.len_path(dij.start_pos))


def second():
    dij = Dijkstra()
    dij.algo()
    shortest_length = 100000
    for i in range(dij.size[0]):
        for j in range(dij.size[1]):
            if dij.map[i][j] == 0:
                shortest_length = min(dij.len_path((i,j)), shortest_length)
    print(shortest_length)

if __name__ == "__main__":
    first()
    second()