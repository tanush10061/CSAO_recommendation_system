# Zomato CSAO Rail Recommendation System

This repository now includes a Netlify-ready static demo built from the original recommendation-system project logic. The deployable entry point is `index.html`.

## Deployable App

- `index.html` - main app entry point for Netlify
- `styles.css` - frontend styling
- `app.js` - recommendation engine and UI logic
- `netlify.toml` - Netlify configuration
- `items_database.json` - item catalog
- `meal_completion_rules.json` - meal-completion rules
- `city_preferences.json` - city-level recommendation priors

## Quick Start

```bash
python3 -m http.server 8000
```

Then open `http://localhost:8000`.

## Problem Statement
Build an intelligent recommendation system for Zomato's Cart Super Add-On (CSAO) rail to suggest relevant items that increase AOV while maintaining high customer satisfaction.

## Solution Overview

### Approach
- **Problem Framing**: Sequential ranking problem with meal completion logic
- **Model**: Random Forest Classifier with 48 engineered features
- **Hybrid System**: Rule-based + ML + contextual personalization

### Performance
- **AUC**: 0.756
- **Precision@8**: 0.65
- **NDCG@8**: 0.75
- **Latency**: <150ms (well under 300ms requirement)
- **Projected AOV Lift**: 18%

### Key Features
1. **Meal Completion Rules**: Biryani → Raita → Dessert → Drink
2. **Contextual Awareness**: Time, city, user segment
3. **Cold Start Handling**: Rule-based fallbacks for new users
4. **Dynamic Updates**: Recommendations change as items are added

## Files

- `index.html` - Interactive Netlify demo
- `app.js` - Frontend recommendation logic
- `styles.css` - Frontend styling
- `zomato_cart_sessions (1).csv` - Synthetic training data
- `items_database.json` - 23 food items with metadata
- `meal_completion_rules.json` - Expert rules
- `feature_importance.csv` - Top features

## Submission Checklist

- [x] **Data Generation**  
  Realistic, messy, city-wise dataset created with noise, missing values, and skewed distributions.

- [x] **Feature Engineering**  
  48 engineered features across 5 entities (User, Merchant, Transaction, Device, City).

- [x] **Model Training**  
  Random Forest model trained using proper temporal split (train on past → test on future).

- [x] **Evaluation**  
  AUC, Precision@K, and NDCG@K used to evaluate ranking + classification performance.

- [x] **System Design**  
  Inference latency optimized to <150ms (suitable for real-time production scoring).

- [x] **Business Impact**  
  Estimated +18% Average Order Value (AOV) lift via targeted ranking.

- [x] **Interactive Demo**  
  Browser-based dashboard with:
  - cart simulation
  - real-time recommendation ranking
  - feature importance visualization
  - context-aware add-on suggestions

## Author
Mohit Kumar | IIT Kharagpur
