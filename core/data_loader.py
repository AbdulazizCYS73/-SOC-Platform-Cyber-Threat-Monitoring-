import pandas as pd

def load_logs():

    df = pd.read_csv("data/logs.csv")

    return df