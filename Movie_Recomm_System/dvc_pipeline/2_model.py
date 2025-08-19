import numpy as np
import pandas as pd
import pickle
import pathlib
import yaml
from sklearn.metrics.pairwise import cosine_similarity


def load_data(data_path):
    return pd.read_csv(data_path)


def save_model(model, output_path):
    with open(output_path, "wb") as f:
        pickle.dump(model, f)


def create_model(X, output_path):
    similarity = cosine_similarity(X)
    new_simi = [[] for i in range(len(similarity))]
    for i in range(len(similarity)):
        new_simi[i] = np.argsort(similarity[i])[::-1][1:6]
    save_model(new_simi, output_path)


def Recommend(df, movie, new_simi):
    index = df[df["title"] == movie].index[0]
    top5 = np.array(new_simi[index])
    return df[df.index.isin(top5)]["title"]


def create_report(df, output_path):
    report_file = output_path / "report.txt"
    with open(report_file, "w") as report:
        for model_file in ["story.pkl", "cast.pkl", "scale.pkl"]:
            report.write(f"--- For model: {model_file} ---\n")
            with open(output_path / model_file, "rb") as mf:
                m = pickle.load(mf)

            for movie in [
                "The Dark Knight",
                "Inception",
                "The Godfather",
                "Toy Story",
                "The Shawshank Redemption",
            ]:
                report.write(f"\nMovie: {movie}\n")
                recommendations = Recommend(df, movie, m)
                report.write(f"Recommendations: {recommendations}\n")
            report.write("\n" + "=" * 50 + "\n\n")


def main():
    curr_path = pathlib.Path(__file__)
    home_dir = curr_path.parent.parent.parent

    output_path = home_dir / "models"
    data_path = home_dir / "data" / "processed"
    output_path.mkdir(parents=True, exist_ok=True)
    with open(home_dir / "params.yaml", "r") as f:
        params = yaml.safe_load(f)["model"]

    story = pd.read_csv(data_path / "story.csv").values
    create_model(story, output_path / "story.pkl")

    cast = pd.read_csv(data_path / "cast.csv").values
    create_model(cast, output_path / "cast.pkl")

    with open(data_path / "scale.pkl", "rb") as f:
        scale = pickle.load(f)
    create_model(scale, output_path / "scale.pkl")
    if params["gen_report"]:
        df = pd.read_csv(data_path / "Frontend.csv")
        create_report(df, output_path)

if __name__=="__main__":
    main()