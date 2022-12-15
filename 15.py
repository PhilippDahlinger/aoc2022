from utils.read_txt_data import txt_to_str


def first():
    data = txt_to_str("data/15.txt").split("\n")
    sensors = []
    beacons = []
    for line in data:
        s_x = int(line[line.find("=") + 1:line.find(",")])
        line = line[line.find(",") + 1:]
        s_y = int(line[line.find("=") + 1:line.find(":")])
        line = line[line.find(":") + 1:]
        b_x = int(line[line.find("=") + 1:line.find(",")])
        line = line[line.find(",") + 1:]
        b_y = int(line[line.find("=") + 1:])
        dist = abs(s_x - b_x) + abs(s_y - b_y)
        sensors.append((s_x, s_y, dist))
        beacons.append((b_x, b_y, dist))

    y = 2000000
    covered_areas = []
    for s_x, s_y, dist in sensors:
        r = dist - abs(s_y - y)
        if r < 0:
            continue
        else:
            covered_areas.append((s_x - r, s_x + r))
    covered_areas = sorted(covered_areas, key=lambda x: x[0])
    y_beacons = [b[0] for b in beacons if b[1] == y]
    covered_points = 0
    for p in range(min(covered_areas, key=lambda x: x[0])[0], max(covered_areas, key=lambda x: x[1])[1] + 1):
        if p in y_beacons:
            continue
        for c in covered_areas:
            if c[0] <= p <= c[1]:
                covered_points += 1
                break
    print(covered_points)


    print("stop")


def second():
    data = txt_to_str("data/15.txt").split("\n")
    sensors = []
    beacons = []
    for line in data:
        s_x = int(line[line.find("=") + 1:line.find(",")])
        line = line[line.find(",") + 1:]
        s_y = int(line[line.find("=") + 1:line.find(":")])
        line = line[line.find(":") + 1:]
        b_x = int(line[line.find("=") + 1:line.find(",")])
        line = line[line.find(",") + 1:]
        b_y = int(line[line.find("=") + 1:])
        dist = abs(s_x - b_x) + abs(s_y - b_y)
        sensors.append((s_x, s_y, dist))
        beacons.append((b_x, b_y, dist))
    x = 0
    y = 0
    upper_bound = 4000000
    while True:
        covered = False
        for s_x, s_y, dist in sensors:
            r = dist - abs(s_y - y) - abs(s_x - x)
            if r >= 0:
                x = s_x + dist - abs(s_y - y) + 1
                covered = True
                break
        if not covered:
            print(x, y)
            print(x * 4000000 + y)
            break
        if x > upper_bound:
            x = 0
            y += 1


if __name__ == "__main__":
    # first()
    second()