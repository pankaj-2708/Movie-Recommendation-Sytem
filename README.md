# Movie_Recomm_System
# 🎥 Movie Recommendation System using Content-Based Filtering

A powerful and interactive **content-based movie recommender system** that suggests movies based on three distinct perspectives: **story**, **cast & crew**, and **scale**. Built with Python and Streamlit using the **TMDb 5000 Movie Dataset**, the system also includes an interactive data analysis dashboard.

[Live demo](https://movie-recommendation-sytem-lmtmej7gbqccfnhxf2rtqm.streamlit.app/)

---

## 🚀 Features

* 🔍 **Three distinct recommendation strategies**:

  1. **Story-based**: Uses the movie's `title`, `overview`, and `tagline` to recommend movies with similar themes and narratives.
  2. **Cast & Crew-based**: Leverages information about `cast`, `crew`, `production companies`, and `production countries` to suggest movies with similar creators or production styles.
  3. **Scale-based**: Considers numerical attributes like `budget`, `revenue`, `profit`, and `popularity` to suggest movies of similar commercial scale or success.

* 📊 **Exploratory Data Analysis (EDA)** section to interactively explore the TMDb dataset (5,000 movies).

* 🧠 Uses **cosine similarity** from scikit-learn to calculate similarity between movies.

* 🎨 Clean and responsive **Streamlit** UI.

* 🎞️ Shows posters and movie titles in an easy-to-browse layout.

* 🧰 Sidebar customization and filtering options.

* API is dockerized and hosted on aws and code is attached here. API docker image -> docker pull pankajmaulekhi/movie-recomm-api:latest
---

## 📁 Dataset

* **Source**: [Dataset](https://www.kaggle.com/datasets/pankajmaulekhi/tmdb-top-10000-movies-updated-till-2025)
* Fields used: `title`, `overview`, `tagline`, `cast`, `crew`, `production_companies`, `production_countries`, `budget`, `revenue`, `popularity`, etc.

---

## 🛠️ Technologies Used

* Python
* Pandas & NumPy
* scikit-learn (`cosine_similarity`)
* Streamlit
* Plotly (for interactive visualizations)
* TMDb Dataset
* Fast-api
* Cokkie-cutter

---

## 📦 Installation

1. **Clone this repository:**

   ```bash
   git clone https://github.com/pankaj-2708/RecommendationSystem
   cd movie-recommendation-system
   ```

**[Read docs for detailed setup here](https://github.com/pankaj-2708/Movie-Recommendation-Sytem/blob/main/docs/docs/getting-started.md)**
---



## Acknowledgements

* [TMDb](https://www.themoviedb.org/) for providing the dataset
* [Kaggle](https://www.kaggle.com/datasets/pankajmaulekhi/tmdb-top-10000-movies-updated-till-2025)
* [Streamlit](https://streamlit.io/) for making UI effortless
* scikit-learn for ML utilities


## Folder Structure
<a target="_blank" href="https://cookiecutter-data-science.drivendata.org/">
    <img src="https://img.shields.io/badge/CCDS-Project%20template-328F97?logo=cookiecutter" />
</a>

## Project Organization

```
├── .dvc
    └── .gitignore
├── .env
├── .gitattributes
├── .gitignore
├── Dockerfile
├── Makefile
├── Movie_Recomm_System
    ├── Frontend
    │   ├── __pycache__
    │   ├── app.py
    │   ├── deps
    │   │   ├── Frontend.csv
    │   │   ├── backend.csv
    │   │   ├── cast.pkl
    │   │   ├── scale.pkl
    │   │   ├── story.pkl
    │   │   └── top_dict.json
    │   ├── eda_utility.py
    │   └── prediction_utility.py
    └── dvc_pipeline
    │   ├── 0_cleaning.py
    │   ├── 1_creating_dataset.py
    │   └── 2_model.py
├── README.md
├── docs
    ├── .gitkeep
    └── docs
    │   ├── getting-started.md
    │   └── index.md
├── dvc.lock
├── dvc.yaml
├── notebooks
    ├── .gitkeep
    ├── 0_cleaning.ipynb
    ├── 1_creating_datasets.ipynb
    └── 2_model.ipynb
├── params.yaml
├── pyproject.toml
├── references
    └── .gitkeep
└── requirements.txt
```

--------


