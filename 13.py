from utils.read_txt_data import txt_to_numpy, txt_to_str
from  functools import cmp_to_key

def evaluate(p1, p2):
    idx = 0
    while True:
        if len(p1) <= idx and len(p2) <= idx:
            return 0
        if len(p1) <= idx:
            return 1
        if len(p2) <= idx:
            return -1
        left = p1[idx]
        right = p2[idx]
        t_l = type(left)
        t_r = type(right)
        if t_l == int and t_r == list:
            left = [left]
        elif t_l == list and t_r == int:
            right = [right]

        if t_l == int and t_r == int:
            if left < right:
                result = 1
            elif left == right:
                result = 0
            else:
                result =  -1
        else:
            # both lists
            result = evaluate(left, right)
        if result == 0:
            idx += 1
        else:
            return result


def first():
    data = txt_to_str("data/13.txt")
    pairs = data.split("\n\n")
    total = 0
    for idx, pair in enumerate(pairs):
        packages = pair.split("\n")
        packages = [eval(p) for p in packages]
        result = evaluate(packages[0], packages[1])
        if result > 0:
            total += idx + 1
    print(total)

def second():
    data = txt_to_str("data/13.txt")
    lines = [ l for l in data.split("\n") if l != ""]
    packages = [eval(l) for l in lines]
    packages += [[[2]], [[6]]]
    s = sorted(packages, key=cmp_to_key(lambda p1, p2: evaluate(p1, p2)), reverse=True)
    i1 = s.index([[2]]) + 1
    i2 = s.index([[6]]) + 1
    print(i1*i2)



if __name__ == "__main__":
    # first()
    second()