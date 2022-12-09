import numpy as np

from utils.read_txt_data import txt_to_numpy, txt_to_str

def load_data():
    data = txt_to_str("data/08.txt")
    lines = data.split("\n")
    data  = [[int(x) for x in line] for line in lines]
    data = np.array(data)
    return data

def scan(data):
    m = np.maximum.accumulate(data, axis=0)
    d = np.diff(m, axis=0)
    inds = np.argwhere(d > 0.5)
    for i in inds:
        i[0] += 1
    return inds

def first():
    data = load_data()

    boarder = []
    for i in range(len(data)):
        boarder.append([0, i])
        boarder.append([i, 0])
        boarder.append([len(data) - 1, i])
        boarder.append([i, len(data) - 1])

    all_inds = set([tuple(x) for x in boarder])


    top_inds = scan(data)
    top_inds = set([tuple(x) for x in top_inds])
    all_inds = all_inds.union(top_inds)

    rot_data = np.rot90(data)
    rot_ids = scan(rot_data)
    rot_ids = set([(i[1], len(data) -1 - i[0]) for i in rot_ids])
    all_inds = all_inds.union(rot_ids)

    rot_data = np.rot90(rot_data)
    rot_ids = scan(rot_data)
    rot_ids = set([(len(data) - 1 -i[0], len(data) -1 - i[1]) for i in rot_ids])
    all_inds = all_inds.union(rot_ids)

    rot_data = np.rot90(rot_data)
    rot_ids = scan(rot_data)
    rot_ids = set([(len(data) -1 - i[1], i[0]) for i in rot_ids])
    all_inds = all_inds.union(rot_ids)
    print(all_inds)
    print(len(all_inds))



    print("stop")

def second():
    data = load_data()
    scores = np.zeros_like(data)
    for i in range(len(data)):
        for j in range(len(data)):
            # left view
            left_score = 0
            i_r = i - 1
            while i_r >= 0:
                left_score += 1
                if data[i_r, j] >= data[i, j]:
                    break
                i_r -= 1

            # right view
            right_score = 0
            i_r = i + 1
            while i_r <= len(data) - 1:
                right_score += 1
                if data[i_r, j] >= data[i, j]:
                    break
                i_r += 1

            # top view
            top_score = 0
            j_r = j - 1
            while j_r >= 0:
                top_score += 1
                if data[i, j_r] >= data[i, j]:
                    break
                j_r -= 1

            # bot view
            bot_score = 0
            j_r = j + 1
            while j_r <= len(data) - 1:
                bot_score += 1
                if data[i, j_r] >= data[i, j]:
                    break
                j_r += 1
            score = left_score * right_score * bot_score * top_score
            scores[i,j] = score

    print(scores)
    print(np.max(scores))

if __name__ == "__main__":
    second()