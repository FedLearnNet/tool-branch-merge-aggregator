"""Regenerate the left/right Iris example tables from data/iris.csv."""

import pandas as pd


def main():
    df = pd.read_csv("data/iris.csv")

    df = df.sample(frac=1, random_state=42).reset_index(drop=True)
    mid = len(df) // 2

    left = df.iloc[:mid].reset_index(drop=True)
    right = df.iloc[mid:].reset_index(drop=True)

    left.to_csv("data/left.csv", index=False)
    right.to_csv("data/right.csv", index=False)

    print("left shape:", left.shape)
    print("right shape:", right.shape)


if __name__ == "__main__":
    main()
