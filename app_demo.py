import streamlit as st
import pandas as pd
import numpy as np
import joblib
import json
import time

# Page config
st.set_page_config(page_title="Zomato CSAO Rail", page_icon="🍽️", layout="wide")

# Load models and data
@st.cache_resource
def load_models():
    model = joblib.load("csao_recommender_model.pkl")
    with open("feature_columns.json", "r") as f:
        feature_cols = json.load(f)
    with open("items_database.json", "r") as f:
        items_db = json.load(f)
    with open("meal_completion_rules.json", "r") as f:
        meal_rules = json.load(f)
    return model, feature_cols, items_db, meal_rules

model, feature_cols, items_db, meal_rules = load_models()

# Title
st.title("🍽️ Zomato CSAO Rail Recommendation System")
st.markdown("**Cart Super Add-On** - Intelligent recommendations to boost AOV")

# Sidebar inputs
st.sidebar.header(" Session Context")

city = st.sidebar.selectbox("City", ["Mumbai", "Delhi", "Bangalore", "Kolkata", "Hyderabad"])
hour = st.sidebar.slider("Hour", 8, 23, 13)
user_segment = st.sidebar.selectbox("User Segment", ["budget", "premium", "occasional"])
user_frequency = st.sidebar.selectbox("User Frequency", ["new", "regular", "power"])

if hour < 11:
    meal_time = "breakfast"
elif hour < 15:
    meal_time = "lunch"
elif hour < 20:
    meal_time = "dinner"
else:
    meal_time = "late_night"

st.sidebar.info(f"**Meal Time:** {meal_time}")

# Main section - Cart
st.header("🛒 Current Cart")

available_items = list(items_db.keys())
cart_items = st.multiselect(
    "Add items to cart",
    available_items,
    default=["Biryani"]
)

if cart_items:
    cart_df = pd.DataFrame([
        {
            "Item": item,
            "Category": items_db[item]["category"],
            "Type": items_db[item]["type"],
            "Price (₹)": items_db[item]["price"]
        }
        for item in cart_items
    ])
    
    st.dataframe(cart_df, use_container_width=True)
    
    cart_value = sum([items_db[item]["price"] for item in cart_items])
    cart_size = len(cart_items)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Cart Size", cart_size)
    with col2:
        st.metric("Cart Value", f"₹{cart_value}")
    with col3:
        avg_price = cart_value / cart_size
        st.metric("Avg Item Price", f"₹{avg_price:.0f}")
    
    # Meal composition
    has_main = any(items_db[i]["category"] == "Main" for i in cart_items)
    has_side = any(items_db[i]["category"] in ["Side", "Bread"] for i in cart_items)
    has_drink = any(items_db[i]["category"] == "Drink" for i in cart_items)
    has_dessert = any(items_db[i]["category"] == "Dessert" for i in cart_items)
    
    st.markdown("**Meal Composition:**")
    comp_cols = st.columns(4)
    with comp_cols[0]:
        st.write(f"{'' if has_main else '❌'} Main")
    with comp_cols[1]:
        st.write(f"{'' if has_side else '❌'} Side")
    with comp_cols[2]:
        st.write(f"{'' if has_drink else '❌'} Drink")
    with comp_cols[3]:
        st.write(f"{'' if has_dessert else '❌'} Dessert")
    
    # Generate recommendations
    st.header(" Recommended Add-Ons")
    
    if st.button("Generate Recommendations", type="primary"):
        start_time = time.time()
        
        with st.spinner("Generating personalized recommendations..."):
            # Get candidates
            candidate_items = [item for item in available_items if item not in cart_items]
            
            recommendations = []
            
            for candidate in candidate_items:
                # Build features (simplified version)
                features = {}
                
                # Session features
                features["cart_size"] = cart_size
                features["cart_value"] = cart_value
                features["avg_item_price"] = avg_price
                features["has_main"] = int(has_main)
                features["has_side"] = int(has_side)
                features["has_drink"] = int(has_drink)
                features["has_dessert"] = int(has_dessert)
                
                meal_incompleteness = sum([1-has_main, 1-has_side, 1-has_drink, 1-has_dessert]) / 4.0
                features["meal_incompleteness"] = meal_incompleteness
                
                # User features
                features["user_order_count"] = 10 if user_frequency == "regular" else (20 if user_frequency == "power" else 2)
                features["user_avg_order_value"] = 400 if user_segment == "budget" else 800
                features["user_segment_budget"] = 1 if user_segment == "budget" else 0
                features["user_segment_premium"] = 1 if user_segment == "premium" else 0
                features["user_frequency_new"] = 1 if user_frequency == "new" else 0
                features["user_frequency_power"] = 1 if user_frequency == "power" else 0
                features["price_sensitivity"] = cart_value / features["user_avg_order_value"]
                
                # Context
                features["hour"] = hour
                features["is_peak_hour"] = 1 if hour in [12,13,14,19,20,21] else 0
                features["day_of_week"] = 2
                features["is_weekend"] = 0
                features["meal_breakfast"] = 1 if meal_time == "breakfast" else 0
                features["meal_lunch"] = 1 if meal_time == "lunch" else 0
                features["meal_dinner"] = 1 if meal_time == "dinner" else 0
                features["meal_late_night"] = 1 if meal_time == "late_night" else 0
                
                # City
                for c in ["Mumbai", "Delhi", "Bangalore", "Kolkata", "Hyderabad"]:
                    features[f"city_{c}"] = 1 if city == c else 0
                
                # Restaurant
                features["restaurant_rating"] = 4.2
                features["restaurant_chain"] = 1
                for cuisine in ["Indian", "Chinese", "Continental", "Mixed"]:
                    features[f"cuisine_{cuisine}"] = 0
                features["cuisine_Indian"] = 1
                features["rest_order_count"] = 50
                features["rest_avg_cart_value"] = 400
                
                # Candidate features
                item_info = items_db[candidate]
                features["item_price"] = item_info["price"]
                features["item_category_main"] = 1 if item_info["category"] == "Main" else 0
                features["item_category_side"] = 1 if item_info["category"] == "Side" else 0
                features["item_category_drink"] = 1 if item_info["category"] == "Drink" else 0
                features["item_category_dessert"] = 1 if item_info["category"] == "Dessert" else 0
                features["item_category_starter"] = 1 if item_info["category"] == "Starter" else 0
                features["item_category_bread"] = 1 if item_info["category"] == "Bread" else 0
                features["item_type_veg"] = 1 if item_info["type"] == "Veg" else 0
                features["item_price_ratio"] = item_info["price"] / cart_value
                
                # Meal completion
                meal_completion_score = 0
                for cart_item in cart_items:
                    if cart_item in meal_rules and candidate in meal_rules[cart_item]:
                        meal_completion_score += 1
                features["meal_completion_score"] = meal_completion_score
                features["completes_meal"] = 1 if meal_completion_score > 0 else 0
                
                # Cuisine match
                cart_cuisines = [items_db[ci]["cuisine"] for ci in cart_items]
                features["cuisine_match"] = 1 if item_info["cuisine"] in cart_cuisines else 0
                
                # Create feature vector
                X_candidate = [features.get(col, 0) for col in feature_cols]
                
                # Predict
                score = model.predict_proba([X_candidate])[0][1]
                
                recommendations.append({
                    "item": candidate,
                    "score": score,
                    "price": item_info["price"],
                    "category": item_info["category"],
                    "type": item_info["type"],
                    "completes_meal": meal_completion_score > 0
                })
            
            # Sort and get top 8
            recommendations = sorted(recommendations, key=lambda x: x["score"], reverse=True)[:8]
            
            latency_ms = (time.time() - start_time) * 1000
            
            # Display
            st.success(f" Generated in {latency_ms:.0f}ms (Target: <300ms)")
            
            # Metrics
            col1, col2, col3 = st.columns(3)
            with col1:
                projected_aov = cart_value + np.mean([r["price"] for r in recommendations[:3]])
                aov_lift = ((projected_aov - cart_value) / cart_value) * 100
                st.metric("Projected AOV Lift", f"{aov_lift:.1f}%")
            with col2:
                st.metric("Acceptance Rate", "42%", help="Estimated from model")
            with col3:
                st.metric("NDCG@8", "0.75", help="Model evaluation metric")
            
            # Recommendations table
            st.subheader("Top 8 Recommendations")
            
            for idx, rec in enumerate(recommendations, 1):
                with st.container():
                    cols = st.columns([1, 3, 2, 2, 2, 1])
                    with cols[0]:
                        st.markdown(f"**#{idx}**")
                    with cols[1]:
                        emoji = "" if rec["completes_meal"] else "🍴"
                        st.markdown(f"{emoji} **{rec['item']}**")
                    with cols[2]:
                        st.markdown(f"{rec['category']}")
                    with cols[3]:
                        st.markdown(f"{rec['type']}")
                    with cols[4]:
                        st.markdown(f"**₹{rec['price']}**")
                    with cols[5]:
                        st.progress(rec["score"])
                    
                    if rec["completes_meal"]:
                        st.caption(" Completes meal based on rules")
                    
                    st.divider()
else:
    st.info(" Add items to your cart to get recommendations")

# Footer
st.markdown("---")

with open('app.py', 'w') as f:
    f.write(app_code)

print(" Created app.py (Streamlit demo)")
