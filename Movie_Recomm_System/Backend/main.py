from fastapi import FastAPI
import pickle
import numpy as np
import pandas as pd
from functools import lru_cache
import psutil
import os

app = FastAPI()


@app.get("/memory")
def get_memory():
    process = psutil.Process(os.getpid())
    mem = process.memory_info().rss  # in bytes
    return {"memory_usage_mb": mem / (1024 * 1024)}


@lru_cache
def load_model_story():
    with open("./models/story.pkl", "rb") as f:
        similarity1 = pickle.load(f)
    return similarity1


similarity1 = load_model_story()


@lru_cache
def load_model_cast():
    with open("./models/cast.pkl", "rb") as f:
        similarity2 = pickle.load(f)
    return similarity2


similarity2 = load_model_cast()


@lru_cache
def load_model_scale():
    with open("./models/scale.pkl", "rb") as f:
        similarity3 = pickle.load(f)
    return similarity3


similarity3 = load_model_scale()


@lru_cache
def load_dataset1():
    return pd.read_csv("./data/processed/backend.csv")


df = load_dataset1()


@app.get("/allmovies")
def allmovies():
    release_years = df["release_year"].values
    titles = df["title"].values
    final = [f"{titles[i]} ({release_years[i]})" for i in range(len(titles))]
    return final


@app.get("/story")
def RecommendStory(movie: str):
    index = df[df["title"] == movie.split("(")[0][:-1]].index[0]
    top5 = np.array(similarity1[index])
    similar_rows = df[df.index.isin(top5)]

    similar_movies = list(similar_rows["title"].values)
    posters = list(similar_rows["poster_path"].values)
    x = similar_rows["release_year"].values
    date1 = list(int(i) for i in x)

    return {"similar_movies": similar_movies, "posters": posters, "date": date1}


@app.get("/cast")
def Recommendcast(movie: str):
    index = df[df["title"] == movie.split("(")[0][:-1]].index[0]
    top5 = np.array(similarity2[index])
    similar_rows = df[df.index.isin(top5)]
    similar_movies = list(similar_rows["title"].values)
    posters = list(similar_rows["poster_path"].values)
    x = similar_rows["release_year"].values
    date = list(int(i) for i in x)
    return {"similar_movies": similar_movies, "posters": posters, "date": date}


@app.get("/scale")
def Recommendscale(movie: str):
    index = df[df["title"] == movie.split("(")[0][:-1]].index[0]
    top5 = np.array(similarity3[index])
    similar_rows = df[df.index.isin(top5)]
    similar_movies = list(similar_rows["title"].values)
    posters = list(similar_rows["poster_path"].values)
    x = similar_rows["release_year"].values
    date = list(int(i) for i in x)
    return {"similar_movies": similar_movies, "posters": posters, "date": date}
