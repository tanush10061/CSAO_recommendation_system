import json
from pathlib import Path

import pandas as pd
import streamlit as st


BASE_DIR = Path(__file__).parent


st.set_page_config(
    page_title="Zomato CSAO Recommender",
    page_icon="🍽️",
    layout="wide",
)


@st.cache_data
def load_json(filename: str):
    with open(BASE_DIR / filename, "r", encoding="utf-8") as file:
        return json.load(file)


@st.cache_data
def load_feature_importance():
    path = BASE_DIR / "feature_importance.csv"
    if path.exists():
        return pd.read_csv(path)
    return pd.DataFrame(columns=["feature", "importance"])


@st.cache_data
def load_session_data():
    possible_files = [
        BASE_DIR / "zomato_cart_sessions.csv",
        BASE_DIR / "zomato_cart_sessions (1).csv",
    ]
    for path in possible_files:
        if path.exists():
            return pd.read_csv(path)
    return pd.DataFrame()


ITEMS_DB = load_json("items_database.json")
MEAL_RULES = load_json("meal_completion_rules.json")
CITY_PREFERENCES = load_json("city_preferences.json")


def infer_meal_time(hour: int) -> str:
    if hour < 11:
        return "breakfast"
    if hour < 15:
        return "lunch"
    if hour < 20:
        return "dinner"
    return "late_night"


def get_cart_profile(cart_items):
    cart_value = sum(ITEMS_DB[item]["price"] for item in cart_items)
    cart_size = len(cart_items)
    categories = [ITEMS_DB[item]["category"] for item in cart_items]
    cuisines = [ITEMS_DB[item]["cuisine"] for item in cart_items]

    return {
        "cart_value": cart_value,
        "cart_size": cart_size,
        "avg_price": cart_value / cart_size if cart_size else 0,
        "has_main": any(category == "Main" for category in categories),
        "has_side": any(category in {"Side", "Bread"} for category in categories),
        "has_drink": any(category == "Drink" for category in categories),
        "has_dessert": any(category == "Dessert" for category in categories),
        "cuisines": cuisines,
    }


def build_reason_tags(candidate, cart_items, city, meal_time, user_segment, profile):
    item = ITEMS_DB[candidate]
    tags = []

    if any(candidate in MEAL_RULES.get(cart_item, []) for cart_item in cart_items):
        tags.append("Completes the current meal")

    if item["cuisine"] in profile["cuisines"]:
        tags.append("Matches your current cart cuisine")

    if candidate in CITY_PREFERENCES.get(city, []):
        tags.append(f"Popular choice in {city}")

    if meal_time == "late_night" and item["category"] in {"Dessert", "Drink"}:
        tags.append("Fits late-night ordering behavior")

    if user_segment == "budget" and item["price"] <= 80:
        tags.append("Budget-friendly add-on")
    elif user_segment == "premium" and item["price"] >= 90:
        tags.append("Works well for premium baskets")

    if not tags:
        tags.append("Balanced complementary recommendation")

    return tags[:3]


def score_candidate(candidate, cart_items, city, meal_time, user_segment, user_frequency, profile):
    item = ITEMS_DB[candidate]
    score = 0.2

    meal_completion_score = sum(
        1 for cart_item in cart_items if candidate in MEAL_RULES.get(cart_item, [])
    )
    score += meal_completion_score * 0.28

    if item["cuisine"] in profile["cuisines"]:
        score += 0.12

    if candidate in CITY_PREFERENCES.get(city, []):
        score += 0.08

    if not profile["has_drink"] and item["category"] == "Drink":
        score += 0.14
    if not profile["has_dessert"] and item["category"] == "Dessert":
        score += 0.14
    if not profile["has_side"] and item["category"] in {"Side", "Bread"}:
        score += 0.15

    if meal_time == "lunch" and item["category"] in {"Drink", "Side"}:
        score += 0.06
    if meal_time == "dinner" and item["category"] in {"Dessert", "Bread", "Side"}:
        score += 0.06
    if meal_time == "late_night" and item["category"] in {"Dessert", "Drink"}:
        score += 0.09

    if user_segment == "budget":
        if item["price"] <= 80:
            score += 0.08
        elif item["price"] >= 200:
            score -= 0.04
    elif user_segment == "premium" and item["price"] >= 90:
        score += 0.06

    if user_frequency == "new" and meal_completion_score > 0:
        score += 0.05
    if user_frequency == "power" and item["category"] in {"Starter", "Dessert"}:
        score += 0.04

    projected_ratio = item["price"] / max(profile["cart_value"], 1)
    if 0.08 <= projected_ratio <= 0.35:
        score += 0.08
    elif projected_ratio > 0.7:
        score -= 0.06

    return max(0.0, min(score, 0.99))


def get_recommendations(cart_items, city, hour, user_segment, user_frequency):
    profile = get_cart_profile(cart_items)
    meal_time = infer_meal_time(hour)
    candidates = [item for item in ITEMS_DB if item not in cart_items]

    recommendations = []
    for candidate in candidates:
        score = score_candidate(
            candidate,
            cart_items,
            city,
            meal_time,
            user_segment,
            user_frequency,
            profile,
        )
        recommendations.append(
            {
                "item": candidate,
                "category": ITEMS_DB[candidate]["category"],
                "type": ITEMS_DB[candidate]["type"],
                "price": ITEMS_DB[candidate]["price"],
                "score": round(score, 3),
                "reasons": build_reason_tags(
                    candidate, cart_items, city, meal_time, user_segment, profile
                ),
            }
        )

    recommendations.sort(key=lambda row: row["score"], reverse=True)
    return recommendations[:8], profile, meal_time


st.title("🍽️ Zomato CSAO Rail Recommendation System")
st.caption(
    "Deployable Streamlit demo for Cart Super Add-On recommendations using meal-completion and context-aware ranking."
)

with st.sidebar:
    st.header("Session Context")
    city = st.selectbox(
        "City", ["Mumbai", "Delhi", "Bangalore", "Kolkata", "Hyderabad"]
    )
    hour = st.slider("Hour of day", min_value=8, max_value=23, value=13)
    user_segment = st.selectbox("User Segment", ["budget", "premium", "occasional"])
    user_frequency = st.selectbox("User Frequency", ["new", "regular", "power"])

meal_time = infer_meal_time(hour)
st.sidebar.info(f"Meal Time: {meal_time.replace('_', ' ').title()}")

st.subheader("Current Cart")
cart_items = st.multiselect("Choose items already in the cart", list(ITEMS_DB.keys()), ["Biryani"])

if cart_items:
    recommendations, profile, meal_time = get_recommendations(
        cart_items, city, hour, user_segment, user_frequency
    )

    cart_df = pd.DataFrame(
        [
            {
                "Item": item,
                "Category": ITEMS_DB[item]["category"],
                "Type": ITEMS_DB[item]["type"],
                "Cuisine": ITEMS_DB[item]["cuisine"],
                "Price (INR)": ITEMS_DB[item]["price"],
            }
            for item in cart_items
        ]
    )
    st.dataframe(cart_df, use_container_width=True, hide_index=True)

    metric_cols = st.columns(4)
    metric_cols[0].metric("Cart Size", profile["cart_size"])
    metric_cols[1].metric("Cart Value", f"INR {profile['cart_value']}")
    metric_cols[2].metric("Average Item Price", f"INR {profile['avg_price']:.0f}")
    projected_addon_value = sum(row["price"] for row in recommendations[:3]) / 3
    lift = (projected_addon_value / max(profile["cart_value"], 1)) * 100
    metric_cols[3].metric("Projected AOV Lift", f"{lift:.1f}%")

    st.subheader("Top Recommendations")
    recommendations_df = pd.DataFrame(
        [
            {
                "Rank": idx,
                "Item": row["item"],
                "Category": row["category"],
                "Type": row["type"],
                "Price (INR)": row["price"],
                "Score": row["score"],
                "Why it fits": " | ".join(row["reasons"]),
            }
            for idx, row in enumerate(recommendations, start=1)
        ]
    )
    st.dataframe(recommendations_df, use_container_width=True, hide_index=True)

    st.subheader("Recommendation Cards")
    for row in recommendations[:4]:
        with st.container(border=True):
            title_col, score_col = st.columns([4, 1])
            title_col.markdown(f"### {row['item']}")
            score_col.metric("Score", f"{row['score']:.2f}")
            st.write(
                f"{row['category']} | {row['type']} | INR {row['price']}"
            )
            for reason in row["reasons"]:
                st.write(f"- {reason}")

    feature_importance = load_feature_importance()
    if not feature_importance.empty:
        st.subheader("Feature Importance Snapshot")
        top_features = feature_importance.head(10).set_index("feature")
        st.bar_chart(top_features["importance"])

    session_data = load_session_data()
    if not session_data.empty:
        st.subheader("Dataset Snapshot")
        analytics_cols = st.columns(3)
        analytics_cols[0].metric("Sample Sessions", len(session_data))
        analytics_cols[1].metric("Unique Users", session_data["user_id"].nunique())
        analytics_cols[2].metric("Unique Restaurants", session_data["restaurant_id"].nunique())

        city_counts = session_data["city"].value_counts().rename_axis("city").reset_index(name="sessions")
        st.bar_chart(city_counts.set_index("city"))
else:
    st.info("Add at least one cart item to generate recommendations.")

st.markdown("---")
st.markdown(
    "Built from your CSAO recommendation project as a Streamlit-ready demo that can be deployed without missing model artifacts."
)
