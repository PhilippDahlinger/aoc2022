from utils.read_txt_data import txt_to_str


def find_idx(len_msg):
    msg = txt_to_str("data/06.txt")
    str_idx = len_msg
    while True:
        sub_msg = msg[str_idx-len_msg:str_idx]
        if len(set(sub_msg)) == len_msg:
            break
        str_idx += 1
    print (str_idx)

if __name__ == "__main__":
    find_idx(4)
    find_idx(14)

