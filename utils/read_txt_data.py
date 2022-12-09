import numpy as np
import pandas as pd


def txt_to_str(path):
    with open(path, "r") as file:
        data = file.read()
    return data

def txt_to_numpy(path):
    return pd.read_csv(path, delimiter=" ").to_numpy()