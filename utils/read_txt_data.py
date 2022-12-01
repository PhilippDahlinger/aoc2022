def txt_to_str(path):
    with open(path, "r") as file:
        data = file.read()
    return data