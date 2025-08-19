import numpy as np
import pandas as pd
import ast
import yaml
from sklearn.pipeline import Pipeline
import pathlib
import warnings
import string
import pickle
from nltk.stem.porter import PorterStemmer
from nltk.corpus import stopwords
import nltk
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import (
    StandardScaler,
    MinMaxScaler,
    OneHotEncoder,
    OrdinalEncoder,
)

punc = string.punctuation
nltk.download("stopwords")
stpWrd = stopwords.words("english")

warnings.filterwarnings("ignore")

df = None


def load_data(data_path):
    return pd.read_csv(data_path)


def genre(txt):
    txt = ast.literal_eval(txt)
    ans = []
    for i in txt:
        ans.append(i["name"])
    return ans


def cast(txt):
    ans = []
    for i in txt:
        ans.append(i["name"])
    return ans


def keywords(txt):
    k = ast.literal_eval(txt)
    ans = []
    for i in k["keywords"]:
        ans.append(i["name"])
    return ans


def seprate(col_name, df, n=20, func=genre):
    df[col_name] = df[col_name].apply(func)
    dct = {}
    for i in df[col_name].values:
        for j in i:
            dct[j] = dct.get(j, 0) + 1
    sorted_comp = sorted(dct, key=lambda a: 1 / dct[a])[:n]
    for i in sorted_comp:
        df[i] = df[col_name].apply(lambda x: 1 if i in x else 0)
    df.drop(columns=[col_name], axis=1, inplace=True)
    return df


def preprocessText(txt):
    new_txt = ""
    for i in txt:
        i=i.lower()
        if i not in punc:
            new_txt += i

    ps = PorterStemmer()
    new_txt2 = []
    for word in new_txt.split():
        if word not in stpWrd and word.isalnum():
            new_txt2.append(ps.stem(word))

    return " ".join(new_txt2)


def create_story(df_, keyword_count, output_path):
    df = df_.copy()
    df["original_title"] = df["original_title"].apply(preprocessText)
    df["tagline"].fillna("", inplace=True)
    df["overview"].fillna("", inplace=True)
    df["tagline"] = df["tagline"].apply(preprocessText)
    df["overview"] = df["overview"].apply(preprocessText)
    df = seprate("genres", df)
    df = seprate("keywords", df, keyword_count, keywords)

    tf1 = TfidfVectorizer(max_features=100,ngram_range=(1, 2))
    tf2 = TfidfVectorizer(max_features=100,ngram_range=(1, 2))
    tf3 = TfidfVectorizer(max_features=300,ngram_range=(1, 2))
    X_title = tf1.fit_transform(df["original_title"])
    X_tagline = tf2.fit_transform(df["tagline"])
    X_overview = tf3.fit_transform(df["overview"])
    df = pd.concat(
        [
            df.reset_index(drop=True),
            pd.DataFrame(
                X_title.toarray(), columns=tf1.get_feature_names_out() + "_title"
            ),
        ],
        axis=1,
    )
    df = pd.concat(
        [
            df.reset_index(drop=True),
            pd.DataFrame(
                X_tagline.toarray(), columns=tf2.get_feature_names_out() + "_tagline"
            ),
        ],
        axis=1,
    )
    df = pd.concat(
        [
            df.reset_index(drop=True),
            pd.DataFrame(
                X_overview.toarray(), columns=tf3.get_feature_names_out() + "_over"
            ),
        ],
        axis=1,
    )
    df.drop(
        [
            "original_title",
            "overview",
            "release_date",
            "tagline",
            "poster_path",
            "budget",
            "adult",
            "id",
            "credits",
            "origin_country",
            "revenue",
            "cast",
            "crew",
            "production_companies",
            "popularity",
            "status",
            "title",
            "video",
            "vote_average",
            "vote_count",
            "hit/flop",
            "profit_per",
            "box-off",
            "runtime",
            "original_language",
            "production_countries",
            "spoken_languages",
        ],
        axis=1,
        inplace=True,
    )
    df.to_csv(output_path / "story.csv", index=False)


def create_cast(
    df_, output_path, prod_comp_count, prod_country_count, cast_count, crew_count
):
    df = df_.copy()
    df = seprate("production_companies", df, prod_comp_count)
    df = seprate("production_countries", df, prod_country_count)
    df = seprate("cast", df, cast_count, genre)
    df = seprate("crew", df, crew_count, genre)
    df.drop(
        [
            "budget",
            "adult",
            "id",
            "revenue",
            "title",
            "video",
            "credits",
            "genres",
            "origin_country",
            "keywords",
            "spoken_languages",
            "original_title",
            "overview",
            "popularity",
            "status",
            "vote_average",
            "vote_count",
            "hit/flop",
            "profit_per",
            "box-off",
            "tagline",
            "runtime",
            "poster_path",
            "release_date",
            "original_language",
        ],
        axis=1,
        inplace=True,
    )
    df.to_csv(output_path / "cast.csv", index=False)


def create_scale(df_, output_path):
    df=df_.copy()
    df["budget"] = df["budget"] / 1000000
    df["revenue"] = df["revenue"] / 1000000
    df["box-off"] = df["box-off"] / 1000000
    df.drop(
        [
            "id",
            "genres",
            "adult",
            "origin_country",
            "spoken_languages",
            "original_title",
            "overview",
            "status",
            "release_date",
            "production_companies",
            "production_countries",
            "tagline",
            "title",
            "video",
            "runtime",
            "original_language",
            "credits",
            "keywords",
            "poster_path",
            "cast",
            "crew",
        ],
        axis=1,
        inplace=True,
    )
    cf = ColumnTransformer(
        transformers=[
            ("ORencoding", OrdinalEncoder(), ["hit/flop"]),
            (
                "std",
                StandardScaler(),
                [
                    "budget",
                    "popularity",
                    "revenue",
                    "vote_average",
                    "vote_average",
                    "box-off",
                    "profit_per",
                ],
            ),
        ],
        remainder="passthrough",
    )

    ppl = Pipeline([("std", cf)])
    X = ppl.fit_transform(df)
    with open(output_path / "scale.pkl", "wb") as f:
        pickle.dump(X, f)

def Frontend(df_,output_path):
    df=df_.copy()
    df["release_date"] = pd.to_datetime(df["release_date"])
    df["release_year"] = df["release_date"].dt.year
    df["release_day"] = df["release_date"].dt.day_name()
    df["release_month"] = df["release_date"].dt.month_name()
    seprate("genres",df)
    seprate("keywords",df, 50, keywords)
    seprate("production_companies",df, 50)
    seprate("production_countries",df, 50)
    seprate("spoken_languages",df, 20)
    seprate("cast",df, 50, genre)
    seprate("crew",df, 50, genre)
    df.to_csv(output_path / 'Frontend.csv',index=False)

    
def main():
    curr_path = pathlib.Path(__file__)
    home_dir = curr_path.parent.parent.parent

    data_path = home_dir / "data" / "interim" / "new_movies_full.csv"
    output_path = home_dir / "data" / "processed"
    output_path.mkdir(parents=True, exist_ok=True)
    global df
    with open(home_dir / "params.yaml", "r") as f:
        params = yaml.safe_load(f)["dataset"]
    df = load_data(data_path)
    create_story(df, params["keyword_count"], output_path)
    create_cast(
        df,
        output_path,
        params["prod_comp_count"],
        params["prod_country_count"],
        params["cast_count"],
        params["crew_count"],
    )
    create_scale(df, output_path)
    Frontend(df,output_path)


if __name__=="__main__":
    main()