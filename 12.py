import string
from queue import PriorityQueue

import numpy as np

from utils.read_txt_data import txt_to_str

class AStar:

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

        self.map = np.array([[transl[x] for x in line] for line in self.map])
    def get_moves(self, pos):
        """
        Compute the reachable positions given the current position `pos` by moving
         one adjacent number into the hole.
        Parameters:
            `pos`: 16-tuple of the current position
        Returns:
            List of 16-tuples containing the reachable positions

        """
        moves = []
        h = self.map[pos]
        if pos[0] > 0 and self.map[pos[0] -1, pos[1]] - h <= 1:
            moves.append((pos[0] - 1, pos[1]))
        if pos[1] > 0 and self.map[pos[0], pos[1] - 1] - h <= 1:
            moves.append((pos[0], pos[1] - 1))
        if pos[0] < self.size[0] - 1 and self.map[pos[0] + 1, pos[1]] - h <= 1:
            moves.append((pos[0] + 1, pos[1]))
        if pos[1] < self.size[1] - 1 and self.map[pos[0], pos[1] + 1] - h <= 1:
            moves.append((pos[0], pos[1] + 1))
        return moves

    def is_goal(self, pos):
        """
        Test if the current position `pos` is the desired goal position
        Parameters:
            `pos`: 16-tuple of the current position
        Returns:
            Boolean: True if `pos`is goal position, False otherwise

        """
        return pos == self.final_pos

    def manhattan_heuristic(self, pos):
        """
        Computes the sum of the Manhattan distances of every tile
        to its desired position.
        Parameters:
            `pos`: 16-tuple of the current position
        Returns:
            Sum of the Manhattan distances.
        """

        return abs(pos[0] - self.final_pos[0]) + abs(pos[1] - self.final_pos[1])

    def a_star_algo(self, start_pos):
        """
        Execute the A* algorithm with the initial position `start_pos`.
        Uses the heuristic function `heuristic`.
        It raises an Assertion Error when the solution cannot be found.
        Parameters:
            `start_pos`: 16-tuple of the current position
            `heuristic`: Callable, which takes a position as a parameter and
            computes a heuristic value of that.
        Returns:
            The tuple (predecessors, num_steps) when the goal position is found.
        """
        expanded_nodes = {}
        predecessors = {}
        queue = PriorityQueue()
        queue.put((self.manhattan_heuristic(start_pos), 0, start_pos, None))
        num_steps = 0
        while queue.qsize() > 0:
            num_steps += 1
            ### BEGIN SOLUTION
            cost, bw_cost, pos, pred = queue.get()
            if expanded_nodes.get(pos, False):
                continue
            print("Current pos:", pos)
            predecessors[pos] = pred
            if self.is_goal(pos):
                return predecessors, num_steps
            expanded_nodes[pos] = True
            moves = self.get_moves(pos)
            for move in moves:
                if move not in expanded_nodes:
                    queue.put((self.manhattan_heuristic(move
                                         ) + bw_cost + 1, bw_cost + 1, move, pos))
            ### END SOLUTION
        raise ValueError("Fringe is empty!")

    def show_solution(self, start_pos, final_pos, predecessors):
        path = [final_pos]
        while final_pos != start_pos:
            final_pos = predecessors[final_pos]
            path.append(final_pos)
        for pos in reversed(path):
            print(pos)
        print(f"Länge der Lösung: {len(path)}")
        return len(path)


def first():
    astar = AStar()
    pred, num_steps  = astar.a_star_algo(astar.start_pos)
    astar.show_solution(astar.start_pos, astar.final_pos, pred)

if __name__ == "__main__":
    first()