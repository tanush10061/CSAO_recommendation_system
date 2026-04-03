# Netlify Deployment Guide

## Files added for deployment

- `index.html` - Main Netlify entry point
- `styles.css` - UI styling
- `app.js` - Recommendation logic and UI behavior
- `netlify.toml` - Netlify publish and routing config
- `items_database.json` - Source item catalog from the project
- `meal_completion_rules.json` - Meal-completion rules from the project
- `city_preferences.json` - City-level preference priors

## Run locally as a static site

```bash
python3 -m http.server 8000
```

Then open `http://localhost:8000`.

## Deploy on Netlify

1. Push this project to your GitHub repository.
2. Go to [https://app.netlify.com](https://app.netlify.com).
3. Click **Add new site** and choose **Import an existing project**.
4. Select your GitHub repository.
5. Keep the default settings. Netlify will detect `netlify.toml`.
6. Click **Deploy site**.

## Important note

The original repository references model files like `csao_recommender_model.pkl` and `feature_columns.json`, but those files are not present in the repo snapshot. This deployment package uses a self-contained recommendation engine based on the same project logic:

- meal completion rules
- cart composition
- city preferences
- user segment and frequency
- price-fit heuristics

If you later add an external API or rewrite the model inference in JavaScript, this app can be extended further without changing the Netlify deployment flow.
