# Zomato CSAO Rail Recommendation System

### Requirements

Create a `requirements.txt` file with the following content:

```txt
streamlit==1.31.0
pandas==2.1.4
numpy==1.26.3
scikit-learn==1.4.0
joblib==1.3.2
plotly==5.18.0
```

## Problem Statement
Build an intelligent recommendation system for Zomato's Cart Super Add-On (CSAO) rail to suggest relevant items that increase AOV while maintaining high customer satisfaction.

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Run the demo app
streamlit run app.py
```

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

- `app.py` - Interactive Streamlit demo
- `csao_recommender_model.pkl` - Trained model
- `zomato_cart_sessions.csv` - Synthetic training data (15K sessions)
- `items_database.json` - 23 food items with metadata
- `meal_completion_rules.json` - Expert rules
- `model_results.json` - Evaluation metrics
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
  Streamlit-based interactive dashboard:
  - Upload / simulate user data  
  - Real-time fraud probability prediction  
  - Top-K risk ranking visualization  
  - Feature importance visualization  
  - City-wise risk analytics dashboard  

## Author
Mohit Kumar | IIT Kharagpur
'''
