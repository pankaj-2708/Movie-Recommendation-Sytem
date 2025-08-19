
import pandas as pd
import plotly.graph_objects as go
import warnings
import pickle
import numpy as np
warnings.filterwarnings("ignore")

def load_model_story():
    with open("./Movie_Recomm_System/Frontend/deps/story.pkl", "rb") as f:
        similarity1 = pickle.load(f)
    return similarity1


similarity1 = load_model_story()


def load_model_cast():
    with open("./Movie_Recomm_System/Frontend/deps/cast.pkl", "rb") as f:
        similarity2 = pickle.load(f)
    return similarity2


similarity2 = load_model_cast()


def load_model_scale():
    with open("./Movie_Recomm_System/Frontend/deps/scale.pkl", "rb") as f:
        similarity3 = pickle.load(f)
    return similarity3


similarity3 = load_model_scale()

def load_dataset1():
    return pd.read_csv("./Movie_Recomm_System/Frontend/deps/backend.csv")


df = load_dataset1()

def allmovies():
    release_years = df["release_year"].values
    titles = df["title"].values
    final = [f"{titles[i]} ({release_years[i]})" for i in range(len(titles))]
    return final


def RecommendStory(movie: str):
    index = df[df["title"] == movie.split("(")[0][:-1]].index[0]
    top5 = np.array(similarity1[index])
    similar_rows = df[df.index.isin(top5)]

    similar_movies = list(similar_rows["title"].values)
    posters = list(similar_rows["poster_path"].values)
    x = similar_rows["release_year"].values
    date1 = list(int(i) for i in x)

    return  similar_movies, posters,  date1



def Recommendcast(movie: str):
    index = df[df["title"] == movie.split("(")[0][:-1]].index[0]
    top5 = np.array(similarity2[index])
    similar_rows = df[df.index.isin(top5)]
    similar_movies = list(similar_rows["title"].values)
    posters = list(similar_rows["poster_path"].values)
    x = similar_rows["release_year"].values
    date = list(int(i) for i in x)
    return  similar_movies, posters,  date


def Recommendscale(movie: str):
    index = df[df["title"] == movie.split("(")[0][:-1]].index[0]
    top5 = np.array(similarity3[index])
    similar_rows = df[df.index.isin(top5)]
    similar_movies = list(similar_rows["title"].values)
    posters = list(similar_rows["poster_path"].values)
    x = similar_rows["release_year"].values
    date = list(int(i) for i in x)
    return  similar_movies, posters,  date