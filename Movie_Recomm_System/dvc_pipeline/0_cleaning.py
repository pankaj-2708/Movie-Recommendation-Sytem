import ast
import pathlib
import warnings
import numpy as np
import pandas as pd
from sklearn.impute import SimpleImputer

warnings.filterwarnings("ignore")


def load_data(data_path):
    return pd.read_csv(data_path)


def save_data(df, output_path):
    df.to_csv(output_path, index=False)


def clean(df):
    df["poster_path"] = df["poster_path"].apply(
        lambda x: "https://image.tmdb.org/t/p/original" + str(x)
    )
    df["poster_path"][
        df["poster_path"] == "https://image.tmdb.org/t/p/originalnan"
    ] = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRoWcWg0E8pSjBNi0TtiZsqu8uD2PAr_K11DA&s"
    df.drop(
        columns=["backdrop_path", "homepage", "belongs_to_collection", "imdb_id"],
        inplace=True,
    )
    df.loc[df["budget"] == 0, "budget"] = np.nan
    df.drop_duplicates(inplace=True)
    df["tagline"].fillna("", inplace=True)
    df["overview"].fillna("", inplace=True)
    df.dropna(subset=["runtime", "release_date"], inplace=True)
    si = SimpleImputer(strategy="mean")
    si.fit(df["budget"].values.reshape(-1, 1))
    df["budget"] = si.transform(df["budget"].values.reshape(-1, 1)).ravel()
    df["cast"] = df["credits"].apply(lambda x: ast.literal_eval(x)["cast"])
    df["crew"] = df["credits"].apply(lambda x: ast.literal_eval(x)["crew"])
    df["box-off"] = df["revenue"] - df["budget"]
    df["hit/flop"] = df["box-off"].apply(lambda x: "hit" if x >= 0 else "flop")
    df["profit_per"] = df["box-off"] * 100 / df["budget"]
    return df


def main():
    curr_path = pathlib.Path(__file__)
    home_dir = curr_path.parent.parent.parent

    data_path = home_dir / "data" / "raw" / "new_movies_full.csv"
    output_path = home_dir / "data" / "interim"
    output_path.mkdir(parents=True, exist_ok=True)
    df = load_data(data_path)
    clean(df)
    save_data(df, output_path / "new_movies_full.csv")


if __name__ == "__main__":
    main()
