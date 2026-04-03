# Streamlit Deployment Guide

## Files added for deployment

- `app.py` - Main Streamlit app entry point
- `requirements.txt` - Python dependencies for Streamlit Cloud
- `items_database.json` - Item catalog used by the recommender
- `meal_completion_rules.json` - Meal-completion recommendation rules
- `city_preferences.json` - City-level preference priors
- `.streamlit/config.toml` - Theme configuration

## Run locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Deploy on Streamlit Community Cloud

1. Push this project to a GitHub repository.
2. Go to [https://share.streamlit.io](https://share.streamlit.io).
3. Click **New app**.
4. Choose your repository, branch, and set the main file path to `app.py`.
5. Click **Deploy**.

## Important note

The original repository references model files like `csao_recommender_model.pkl` and `feature_columns.json`, but those files are not present in the repo snapshot. This deployment package uses a self-contained recommendation engine based on the same project logic:

- meal completion rules
- cart composition
- city preferences
- user segment and frequency
- price-fit heuristics

If you later add the trained `.pkl` model files to the repo, the app can be upgraded to use true model inference.
