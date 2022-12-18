from collections import deque

from utils.read_txt_data import txt_to_str

def get_data():
    data_str = txt_to_str("data/18.txt").split("\n")
    data = set()
    for line in data_str:
        data.add(tuple(int(x) for x in line.split(",")))
    return data
def first():
    data = get_data()

    surface = 6 * len(data)
    for x, y, z in data:
        for i in [-1, 1]:
            if (x + i, y , z) in data:
                surface -= 1
            if (x, y + i , z) in data:
                surface -= 1
            if (x, y , z + i) in data:
                surface -= 1
    print(surface)


def get_interior(neg_data):

    def _get_component(p, comps, idx):
        q = deque()
        q.append(p)
        while len(q) > 0:
            x, y, z = q.popleft()
            if comps[(x,y, z)] != -1:
                continue
            comps[(x,y,z)] = idx
            nbs = []
            for i in [-1, 1]:
                nbs.append((x + i, y, z))
                nbs.append((x, y + i, z))
                nbs.append((x, y, z + i))
            for nb in nbs:
                if nb not in comps:
                    continue
                q.append(nb)

    comp_idx = 0
    comps = {}
    for p in neg_data:
        comps[p] = -1
    for p in comps:
        if comps[p] == -1:
            _get_component(p, comps, comp_idx)
            comp_idx += 1

    outside_idx = 0
    interior = {p for p in comps if comps[p] > outside_idx}
    return interior




def second():
    data = get_data()
    # for i in range(3):
    #     print(min(data, key=lambda x: x[i])[i])
    #     print(max(data, key=lambda x: x[i])[i])

    neg_data = set()
    for i in range(-1, 23):
        for j in range(-1, 23):
            for k in range(-1, 23):
                if (i,j,k) not in data:
                    neg_data.add((i,j,k))
    interior = get_interior(neg_data)

    surface = 6 * len(data)
    for x, y, z in data:
        nbs = []
        for i in [-1, 1]:
            nbs.append((x + i, y, z))
            nbs.append((x, y + i, z))
            nbs.append((x, y, z + i))

        for nb in nbs:
            if nb in data or nb in interior:
                surface -= 1
    print(surface)




if __name__ == "__main__":
    # first()
    second()