# 🎬 Movie Recommendation System – Getting Started

Welcome! Follow these steps to set up and run the Movie Recommendation System locally.

See folder structure in readme.md 
---

## 📁 Project Overview

See `README.md` for folder structure and details.

---

## 🚀 Setup Steps

### 1. 📥 Download Dataset

- Get the dataset here(https://www.kaggle.com/datasets/pankajmaulekhi/tmdb-top-10000-movies-updated-till-2025)(#).
- Save it to `data/raw/`.

---

### 2. 🧪 Run Notebooks

Run these notebooks in order:

- `notebooks/0_cleaning.ipynb` – Exploratory Data Analysis and Cleaning
- `notebooks/1_creating_dataset.ipynb` – Dataset Creation
- `notebooks/2_model.ipynb` – Model Training

Outputs will be saved in `data/processed/`, `models/`, and related folders.

---

### 3. 🔐 Configure Environment

Create a `.env` file in the project root:

```env
API_URL=http://127.0.0.1:8000
```

---

### 4. 📦 Install Dependencies

Ensure Python 3.11+ is installed. Then run:

```bash
pip install -r requirements.txt
```

---

### 5. ⚙️ Start Backend (FastAPI)

```bash
uvicorn Movie_Recomm_System.Backend.main:app --reload
```
Access backend at [http://127.0.0.1:8000](http://127.0.0.1:8000) and docs at [/docs](http://127.0.0.1:8000/docs).

---

### 6. 🎨 Start Frontend (Streamlit)

```bash
streamlit run Movie_Recomm_System/Frontend/app.py
```
Frontend runs at [http://localhost:8501](http://localhost:8501).

---

**Tip:** Ensure `api_url` in `.env` matches your backend URL.
