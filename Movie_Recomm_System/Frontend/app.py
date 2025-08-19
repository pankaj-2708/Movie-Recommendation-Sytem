import streamlit as st
import numpy as np
import pandas as pd
from eda_utility import *
from prediction_utility import *
from scipy.stats.mstats import winsorize
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go
import plotly.express as px
import json
import warnings

warnings.filterwarnings("ignore")


sd = st.sidebar
st.set_page_config(layout="wide", page_title="Movies Recommendation System")


if "show" not in st.session_state:
    st.session_state.show = False

if "btn2" not in st.session_state:
    st.session_state.btn2 = False

st.session_state.opt = sd.selectbox(
    label="Select one", options=["Recommendation system", "Data analysis"]
)
show = sd.button(label="Run")

if not st.session_state.show:
    if show:
        st.session_state.show = True
        st.rerun()

st.sidebar.markdown(
    """
---
#### 🔎 How it works
Select recommendation system for checking out movie recommender or select Data analysis to see graphs and insights about data.

---
#### 👨‍💻 Built With
- Python
- Streamlit
- TMDB Dataset
- Cosine Similarity
- Cookiecutter
- DVC
"""
)

if st.session_state.show:
    if st.session_state.opt == "Data analysis":
        st.header("Analysis on Movie's dataset")

        @st.cache_data
        def load_df():
            """
            Loads the processed movie dataset for frontend analysis.
            """
            return pd.read_csv("./data/processed/Frontend.csv")

        df = load_df()

        st.subheader("Profit Analysis")
        fig = px.histogram(
            df,
            winsorize(df["profit_per"], limits=[0.01, 0.01]),
            nbins=50,
            color="hit/flop",
            text_auto=True,
            title="Profit percentage vs No of movies",
            color_discrete_sequence=["green", "red"],
            labels={"x": "Percentage of Profit"},
        )
        fig.update_yaxes(title="Number of Movies")
        st.plotly_chart(fig)

        fig = px.pie(
            names=df["hit/flop"].value_counts().index,
            values=df["hit/flop"].value_counts().values,
            color_discrete_sequence=["green", "red"],
            title="Percentage of movies Hit and flop",
        ).update_traces(textposition="inside")
        st.plotly_chart(fig)

        st.divider()

        st.subheader("Budget Analysis")
        fig = px.histogram(
            df,
            x="budget",
            nbins=50,
            text_auto=True,
            color="hit/flop",
            color_discrete_sequence=["green", "red"],
            labels={"budget": "Budget in USD($)"},
            title="No of movies vs Budget",
            height=500,
        )
        fig.update_yaxes(title="Number of Movies")
        st.plotly_chart(fig)

        st.divider()

        st.subheader("Popularity Analysis")
        fig = px.histogram(
            df,
            x="popularity",
            text_auto=True,
            color="hit/flop",
            nbins=50,
            color_discrete_sequence=["green", "red"],
            labels={"popularity": "Popularity Score"},
            title="Popularity vs No of movies",
            height=500,
        )
        fig.update_yaxes(title="Number of Movies")
        st.plotly_chart(fig)

        fig = px.histogram(
            df,
            x="vote_average",
            text_auto=True,
            color="hit/flop",
            nbins=11,
            color_discrete_sequence=["green", "red"],
            labels={"vote_average": "Average Rating"},
            title="Average Rating vs No of movies",
            height=500,
        )
        fig.update_yaxes(title="Number of Movies")
        st.plotly_chart(fig)

        fig = px.histogram(
            df,
            x="vote_count",
            text_auto=True,
            color="hit/flop",
            nbins=50,
            color_discrete_sequence=["green", "red"],
            labels={"vote_count": "Average Votes"},
            title="Avernge No of votes vs No of movies",
            height=500,
        )
        fig.update_yaxes(title="Number of Movies")
        st.plotly_chart(fig)
        st.divider()

        st.subheader("Year wise Analysis")
        fig = px.histogram(
            df,
            x="release_year",
            text_auto=True,
            color="hit/flop",
            nbins=50,
            color_discrete_sequence=["green", "red"],
            labels={"release_year": "Years"},
            title="Year vs No of movies",
            height=500,
        )
        fig.update_yaxes(title="Number of Movies")
        st.plotly_chart(fig)
        st.divider()

        st.subheader("Month wise Analysis")
        fig = px.histogram(
            df,
            x="release_month",
            text_auto=True,
            color="hit/flop",
            nbins=50,
            color_discrete_sequence=["green", "red"],
            labels={"release_month": "Month"},
            title="Month vs No of movies",
            height=500,
        )
        fig.update_yaxes(title="Number of Movies")
        st.plotly_chart(fig)
        st.divider()

        st.subheader("Week wise Analysis")
        fig = px.histogram(
            df,
            x="release_day",
            text_auto=True,
            color="hit/flop",
            nbins=50,
            color_discrete_sequence=["green", "red"],
            labels={"release_day": "Day"},
            title="Week vs No of movies",
            height=500,
        )
        fig.update_yaxes(title="Number of Movies")
        st.plotly_chart(fig)
        st.divider()

        st.subheader("Runtime Analysis")
        px.histogram(x=df["runtime"], text_auto=True, color=df["hit/flop"], nbins=25)
        fig = px.histogram(
            df,
            x="runtime",
            text_auto=True,
            color="hit/flop",
            nbins=50,
            color_discrete_sequence=["green", "red"],
            labels={"runtime": "Runtime in minutes"},
            title="Runtime vs No of movies",
            height=500,
        )
        fig.update_yaxes(title="Number of Movies")
        st.plotly_chart(fig)
        st.divider()
        st.divider()

        st.header("Multivariate analysis")
        fig = px.scatter(
            df,
            x="budget",
            y="revenue",
            color="hit/flop",
            hover_name="original_title",
            title="Revenue vs Budget",
            color_discrete_sequence=["green", "red"],
            labels={"budget": "Budget", "revenue": "Revenue"},
        )
        st.plotly_chart(fig)

        st.divider()

        fig = px.scatter(
            df,
            x="popularity",
            y="revenue",
            color="hit/flop",
            hover_name="original_title",
            title="Popularity vs Revenue",
            color_discrete_sequence=["green", "red"],
            labels={"popularity": "Popularity", "revenue": "Revenue"},
        )
        st.plotly_chart(fig)

        st.divider()
        fig = px.scatter(
            df,
            x="vote_count",
            y="vote_average",
            color="hit/flop",
            hover_name="original_title",
            title="Vote_count vs Vote_average",
            color_discrete_sequence=["green", "red"],
            labels={"vote_average": "Average Rating", "vote_count": "No of Votes"},
        )
        st.plotly_chart(fig)

        st.divider()
        fig = px.scatter(
            df,
            x="release_year",
            y="vote_count",
            color="hit/flop",
            hover_name="original_title",
            title="Release Year vs Vote count",
            color_discrete_sequence=["green", "red"],
            labels={"release_year": "Year", "vote_count": "Vote count"},
        )
        st.plotly_chart(fig)

        st.divider()

        fig = px.scatter(
            df,
            x="release_year",
            y="vote_average",
            color="hit/flop",
            hover_name="original_title",
            title="Release Year vs Rating",
            color_discrete_sequence=["green", "red"],
            labels={"release_year": "Year", "vote_average": "Rating"},
        )
        st.plotly_chart(fig)

        st.divider()

        st.subheader("Correlation Heatmap")
        fig = px.imshow(
            df[
                [
                    "budget",
                    "popularity",
                    "revenue",
                    "runtime",
                    "vote_average",
                    "vote_count",
                    "box-off",
                ]
            ].corr(),
            text_auto=True,
            width=600,
            height=600,
        )
        st.plotly_chart(fig)
        st.divider()

        top_dict = None
        with open("./Movie_Recomm_System/Frontend/deps/top_dict.json", "r") as f:
            top_dict = json.load(fp=f)

        st.subheader("Genre wise Analysis")

        revenue_comp, no_of_movies, budget, revenueAndBudget = draw_graph(
            "Genres", top_dict["genres"]
        )
        st.plotly_chart(no_of_movies)
        st.plotly_chart(revenue_comp)
        st.plotly_chart(budget)
        st.plotly_chart(revenueAndBudget)

        st.divider()
        st.subheader("Production Companies Analysis (Top 50)")

        revenue_comp, no_of_movies, budget, revenueAndBudget = draw_graph(
            "Production Companies", top_dict["production_companies"]
        )
        st.plotly_chart(no_of_movies)
        st.plotly_chart(revenue_comp)
        st.plotly_chart(budget)
        st.plotly_chart(revenueAndBudget)

        st.divider()
        st.subheader("Production Countries Analysis (Top 50)")

        revenue_comp, no_of_movies, budget, revenueAndBudget = draw_graph(
            "Production Countries", top_dict["production_countries"]
        )
        st.plotly_chart(no_of_movies)
        st.plotly_chart(revenue_comp)
        st.plotly_chart(budget)
        st.plotly_chart(revenueAndBudget)

        st.divider()

        st.subheader("Cast (Top 50)")

        revenue_comp, no_of_movies, budget, revenueAndBudget = draw_graph(
            "Cast", top_dict["cast"]
        )
        st.plotly_chart(no_of_movies)
        st.plotly_chart(revenue_comp)
        st.plotly_chart(budget)
        st.plotly_chart(revenueAndBudget)

        st.divider()

        st.subheader("Crew (Top 50)")

        revenue_comp, no_of_movies, budget, revenueAndBudget = draw_graph(
            "Crew", top_dict["crew"]
        )
        st.plotly_chart(no_of_movies)
        st.plotly_chart(revenue_comp)
        st.plotly_chart(budget)
        st.plotly_chart(revenueAndBudget)

    else:
        allMoviesList = allmovies()

        st.header("Movie Recommender")
        movie = st.selectbox(options=allMoviesList, label="Select a movie")

        btn2 = st.button(label="Recommend")

        if not st.session_state.btn2:
            if btn2:
                st.session_state.btn2 = True

        if st.session_state.btn2:
            recomm = None
            poster_path = None

            st.subheader("On the basis of Story")
            recomm, poster_path, date = RecommendStory(movie)

            colA = st.columns(5)
            for i in range(len(colA)):
                with colA[i]:
                    st.image(poster_path[i], width=300)
                    st.write(f"{recomm[i]}({date[i]})")

            st.subheader("On the basis of Cast and crew")
            colA = st.columns(5)
            recomm, poster_path, date = Recommendcast(movie)

            for i in range(len(colA)):
                with colA[i]:
                    st.image(poster_path[i], width=300)
                    st.write(f"{recomm[i]}({date[i]})")

            st.subheader("On the basis of Scale")
            colA = st.columns(5)
            recomm, poster_path, date = Recommendscale(movie)

            for i in range(len(colA)):
                with colA[i]:
                    st.image(poster_path[i], width=300)
                    st.write(f"{recomm[i]}({date[i]})")
            st.session_state.btn2 = False

else:
    st.header("🎬 Movie Recommendation System")

    st.write(
        """
    This application recommends movies using **cosine similarity** based on three different aspects:
    """
    )

    st.subheader("📌 Recommendation Modes")
    st.write(
        """
    - **Story** – Based on movie overviews, taglines, and keywords  
    - **Cast & Crew** – Based on directors, writers, and actors  
    - **Scale & Popularity** – Based on budget, revenue, popularity, and user ratings
    """
    )

    st.subheader("📊 Dataset & Analysis")
    st.write(
        """
    The system uses the **TMDB 5000 Movies Dataset** and includes data visualizations 
    to explore trends in movie production, popularity, revenue, and more.
    """
    )

    st.subheader("🚀 How It Works")
    st.write(
        """
    Select a movie and choose the recommendation mode.  
    The system computes content-based similarity and shows you the top 5 similar movies with their posters.
    """
    )
