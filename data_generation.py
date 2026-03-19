# Delivering a detailed end-to-end solution structured for easy presentation following evaluation guidelines:

import os
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import json
# Set seed for reproducibility
np.random.seed(42)
# ============================================
# PART 1: REALISTIC SYNTHETIC DATA GENERATION
# ============================================
print("=" * 60)
print("GENERATING REALISTIC ZOMATO-STYLE DATASET")
print("=" * 60)
# Define realistic food items with categories
items_db = {
    'Biryani': {'category': 'Main', 'price': 280, 'type': 'Non-Veg', 'cuisine': 'Indian'},
    'Paneer Tikka': {'category': 'Main', 'price': 220, 'type': 'Veg', 'cuisine': 'Indian'},
    'Butter Chicken': {'category': 'Main', 'price': 320, 'type': 'Non-Veg', 'cuisine': 'Indian'},
    'Dal Makhani': {'category': 'Main', 'price': 180, 'type': 'Veg', 'cuisine': 'Indian'},
    'Chicken Fried Rice': {'category': 'Main', 'price': 210, 'type': 'Non-Veg', 'cuisine': 'Chinese'},
    'Hakka Noodles': {'category': 'Main', 'price': 190, 'type': 'Veg', 'cuisine': 'Chinese'},
    
    'Raita': {'category': 'Side', 'price': 60, 'type': 'Veg', 'cuisine': 'Indian'},
    'Salan': {'category': 'Side', 'price': 70, 'type': 'Veg', 'cuisine': 'Indian'},
    'Naan': {'category': 'Bread', 'price': 40, 'type': 'Veg', 'cuisine': 'Indian'},
    'Roti': {'category': 'Bread', 'price': 30, 'type': 'Veg', 'cuisine': 'Indian'},
    'Papad': {'category': 'Side', 'price': 25, 'type': 'Veg', 'cuisine': 'Indian'},
    
    'Gulab Jamun': {'category': 'Dessert', 'price': 80, 'type': 'Veg', 'cuisine': 'Indian'},
    'Rasgulla': {'category': 'Dessert', 'price': 70, 'type': 'Veg', 'cuisine': 'Indian'},
    'Ice Cream': {'category': 'Dessert', 'price': 90, 'type': 'Veg', 'cuisine': 'Continental'},
    'Brownie': {'category': 'Dessert', 'price': 100, 'type': 'Veg', 'cuisine': 'Continental'},
    
    'Coke': {'category': 'Drink', 'price': 50, 'type': 'Veg', 'cuisine': 'Beverage'},
    'Lassi': {'category': 'Drink', 'price': 70, 'type': 'Veg', 'cuisine': 'Indian'},
    'Mineral Water': {'category': 'Drink', 'price': 20, 'type': 'Veg', 'cuisine': 'Beverage'},
    'Fresh Lime': {'category': 'Drink', 'price': 60, 'type': 'Veg', 'cuisine': 'Beverage'},
    
    'Samosa': {'category': 'Starter', 'price': 40, 'type': 'Veg', 'cuisine': 'Indian'},
    'Chicken Wings': {'category': 'Starter', 'price': 180, 'type': 'Non-Veg', 'cuisine': 'Continental'},
    'Spring Rolls': {'category': 'Starter', 'price': 120, 'type': 'Veg', 'cuisine': 'Chinese'},
    'Salad': {'category': 'Starter', 'price': 90, 'type': 'Veg', 'cuisine': 'Continental'},
}
items_list = list(items_db.keys())
# Meal completion rules (what naturally goes together)
meal_completion_rules = {
    'Biryani': ['Raita', 'Salan', 'Gulab Jamun'],
    'Butter Chicken': ['Naan', 'Roti', 'Raita'],
    'Dal Makhani': ['Roti', 'Naan', 'Papad'],
    'Paneer Tikka': ['Naan', 'Raita', 'Coke'],
    'Chicken Fried Rice': ['Spring Rolls', 'Coke', 'Ice Cream'],
    'Hakka Noodles': ['Spring Rolls', 'Coke'],
}
# Cities with behavior patterns
cities = ['Mumbai', 'Delhi', 'Bangalore', 'Kolkata', 'Hyderabad']
city_preferences = {
    'Mumbai': ['Butter Chicken', 'Paneer Tikka', 'Ice Cream'],
    'Delhi': ['Butter Chicken', 'Naan', 'Lassi'],
    'Bangalore': ['Biryani', 'Coke', 'Brownie'],
    'Kolkata': ['Biryani', 'Rasgulla', 'Lassi'],
    'Hyderabad': ['Biryani', 'Raita', 'Gulab Jamun'],
}
# Generate 15,000 realistic sessions
n_sessions = 15000
sessions_data = []
for session_id in range(n_sessions):
    # User profile
    user_id = np.random.randint(1, 6000)
    city = np.random.choice(cities)
    
    # Contextual factors
    hour = np.random.choice(range(8, 24), p=[0.02]*3 + [0.15]*3 + [0.05]*2 + [0.20]*3 + [0.05]*2 + [0.08]*3)  # Peak lunch/dinner
    day_of_week = np.random.randint(0, 7)
    
    if hour < 11:
        meal_time = 'breakfast'
    elif hour < 15:
        meal_time = 'lunch'
    elif hour < 20:
        meal_time = 'dinner'
    else:
        meal_time = 'late_night'
    
    # User segment (behavioral)
    user_segment = np.random.choice(['budget', 'premium', 'occasional'], p=[0.5, 0.3, 0.2])
    user_frequency = np.random.choice(['new', 'regular', 'power'], p=[0.3, 0.5, 0.2])
    
    # Restaurant
    restaurant_id = np.random.randint(1, 800)
    restaurant_type = np.random.choice(['chain', 'independent'], p=[0.4, 0.6])
    cuisine_type = np.random.choice(['Indian', 'Chinese', 'Continental', 'Mixed'], p=[0.5, 0.2, 0.15, 0.15])
    restaurant_rating = round(np.random.uniform(3.5, 4.8), 1)
    
    # Build cart (realistic evolution)
    cart_items = []
    cart_size = np.random.choice([1, 2, 3, 4], p=[0.3, 0.4, 0.2, 0.1])
    
    # Start with main dish (80% of time)
    if np.random.random() < 0.8:
        main_dishes = [k for k, v in items_db.items() if v['category'] == 'Main']
        # City preference influence
        if np.random.random() < 0.4:
            main_dishes = [d for d in main_dishes if d in city_preferences[city]] or main_dishes
        cart_items.append(np.random.choice(main_dishes))
    
    # Add more items
    for _ in range(cart_size - 1):
        available = [i for i in items_list if i not in cart_items]
        cart_items.append(np.random.choice(available))
    
    # Calculate cart value
    cart_value = sum([items_db[item]['price'] for item in cart_items])
    
    # Determine TRUE add-on (what user actually added - for training label)
    # Use meal completion logic + context
    candidate_addons = [i for i in items_list if i not in cart_items]
    
    # Apply meal completion rules (50% follow rules)
    true_addon = None
    if cart_items and np.random.random() < 0.5:
        for cart_item in cart_items:
            if cart_item in meal_completion_rules:
                possible = [a for a in meal_completion_rules[cart_item] if a not in cart_items]
                if possible:
                    true_addon = np.random.choice(possible)
                    break
    
    # Contextual patterns (30%)
    if not true_addon and np.random.random() < 0.3:
        if meal_time == 'late_night' and 'Dessert' in [items_db[i]['category'] for i in candidate_addons]:
            desserts = [i for i in candidate_addons if items_db[i]['category'] == 'Dessert']
            true_addon = np.random.choice(desserts)
        elif not any(items_db[i]['category'] == 'Drink' for i in cart_items):
            drinks = [i for i in candidate_addons if items_db[i]['category'] == 'Drink']
            if drinks:
                true_addon = np.random.choice(drinks)
    
    # Random (20% - noise)
    if not true_addon:
        true_addon = np.random.choice(candidate_addons)
    
    # User historical behavior (mock)
    user_order_count = np.random.poisson(5) if user_frequency == 'regular' else (np.random.poisson(15) if user_frequency == 'power' else np.random.poisson(1))
    user_avg_order_value = np.random.uniform(200, 600) if user_segment == 'budget' else np.random.uniform(500, 1200)
    
    # Session data
    sessions_data.append({
        'session_id': session_id,
        'user_id': user_id,
        'city': city,
        'hour': hour,
        'day_of_week': day_of_week,
        'meal_time': meal_time,
        'user_segment': user_segment,
        'user_frequency': user_frequency,
        'user_order_count': user_order_count,
        'user_avg_order_value': user_avg_order_value,
        'restaurant_id': restaurant_id,
        'restaurant_type': restaurant_type,
        'cuisine_type': cuisine_type,
        'restaurant_rating': restaurant_rating,
        'cart_items': ','.join(cart_items),
        'cart_size': len(cart_items),
        'cart_value': cart_value,
        'has_main': int(any(items_db[i]['category'] == 'Main' for i in cart_items)),
        'has_side': int(any(items_db[i]['category'] == 'Side' for i in cart_items)),
        'has_drink': int(any(items_db[i]['category'] == 'Drink' for i in cart_items)),
        'has_dessert': int(any(items_db[i]['category'] == 'Dessert' for i in cart_items)),
        'true_addon': true_addon,
        'addon_price': items_db[true_addon]['price'],
        'addon_category': items_db[true_addon]['category'],
    })
df_sessions = pd.DataFrame(sessions_data)
df_sessions.to_csv('zomato_cart_sessions.csv', index=False)
print(f"\nGenerated {len(df_sessions)} realistic sessions")
print(f"\nData Statistics:")
print(f"  - Unique Users: {df_sessions['user_id'].nunique()}")
print(f"  - Unique Restaurants: {df_sessions['restaurant_id'].nunique()}")
print(f"  - Cities: {df_sessions['city'].nunique()}")
print(f"  - Avg Cart Size: {df_sessions['cart_size'].mean():.2f}")
print(f"  - Avg Cart Value: ₹{df_sessions['cart_value'].mean():.2f}")
print(f"\nMeal Time Distribution:")
print(df_sessions['meal_time'].value_counts())
print(f"\nUser Segment Distribution:")
print(df_sessions['user_segment'].value_counts())
# Save items database
with open('items_database.json', 'w') as f:
    json.dump(items_db, f, indent=2)
print(f"\n Saved items_database.json with {len(items_db)} items")
print("\n" + "=" * 60)
Generating refined realistic Zomato-style dataset with improved peak hour distributions and additional rules for presentation structure.
import os
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import json
# Set seed for reproducibility
np.random.seed(42)
# ============================================
# PART 1: REALISTIC SYNTHETIC DATA GENERATION
# ============================================
print("=" * 60)
print("GENERATING REALISTIC ZOMATO-STYLE DATASET")
print("=" * 60)
# Define realistic food items with categories
items_db = {
    'Biryani': {'category': 'Main', 'price': 280, 'type': 'Non-Veg', 'cuisine': 'Indian'},
    'Paneer Tikka': {'category': 'Main', 'price': 220, 'type': 'Veg', 'cuisine': 'Indian'},
    'Butter Chicken': {'category': 'Main', 'price': 320, 'type': 'Non-Veg', 'cuisine': 'Indian'},
    'Dal Makhani': {'category': 'Main', 'price': 180, 'type': 'Veg', 'cuisine': 'Indian'},
    'Chicken Fried Rice': {'category': 'Main', 'price': 210, 'type': 'Non-Veg', 'cuisine': 'Chinese'},
    'Hakka Noodles': {'category': 'Main', 'price': 190, 'type': 'Veg', 'cuisine': 'Chinese'},
    
    'Raita': {'category': 'Side', 'price': 60, 'type': 'Veg', 'cuisine': 'Indian'},
    'Salan': {'category': 'Side', 'price': 70, 'type': 'Veg', 'cuisine': 'Indian'},
    'Naan': {'category': 'Bread', 'price': 40, 'type': 'Veg', 'cuisine': 'Indian'},
    'Roti': {'category': 'Bread', 'price': 30, 'type': 'Veg', 'cuisine': 'Indian'},
    'Papad': {'category': 'Side', 'price': 25, 'type': 'Veg', 'cuisine': 'Indian'},
    
    'Gulab Jamun': {'category': 'Dessert', 'price': 80, 'type': 'Veg', 'cuisine': 'Indian'},
    'Rasgulla': {'category': 'Dessert', 'price': 70, 'type': 'Veg', 'cuisine': 'Indian'},
    'Ice Cream': {'category': 'Dessert', 'price': 90, 'type': 'Veg', 'cuisine': 'Continental'},
    'Brownie': {'category': 'Dessert', 'price': 100, 'type': 'Veg', 'cuisine': 'Continental'},
    
    'Coke': {'category': 'Drink', 'price': 50, 'type': 'Veg', 'cuisine': 'Beverage'},
    'Lassi': {'category': 'Drink', 'price': 70, 'type': 'Veg', 'cuisine': 'Indian'},
    'Mineral Water': {'category': 'Drink', 'price': 20, 'type': 'Veg', 'cuisine': 'Beverage'},
    'Fresh Lime': {'category': 'Drink', 'price': 60, 'type': 'Veg', 'cuisine': 'Beverage'},
    
    'Samosa': {'category': 'Starter', 'price': 40, 'type': 'Veg', 'cuisine': 'Indian'},
    'Chicken Wings': {'category': 'Starter', 'price': 180, 'type': 'Non-Veg', 'cuisine': 'Continental'},
    'Spring Rolls': {'category': 'Starter', 'price': 120, 'type': 'Veg', 'cuisine': 'Chinese'},
    'Salad': {'category': 'Starter', 'price': 90, 'type': 'Veg', 'cuisine': 'Continental'},
}
items_list = list(items_db.keys())
# Meal completion rules (what naturally goes together)
meal_completion_rules = {
    'Biryani': ['Raita', 'Salan', 'Gulab Jamun'],
    'Butter Chicken': ['Naan', 'Roti', 'Raita'],
    'Dal Makhani': ['Roti', 'Naan', 'Papad'],
    'Paneer Tikka': ['Naan', 'Raita', 'Coke'],
    'Chicken Fried Rice': ['Spring Rolls', 'Coke', 'Ice Cream'],
    'Hakka Noodles': ['Spring Rolls', 'Coke'],
}
# Cities with behavior patterns
cities = ['Mumbai', 'Delhi', 'Bangalore', 'Kolkata', 'Hyderabad']
city_preferences = {
    'Mumbai': ['Butter Chicken', 'Paneer Tikka', 'Ice Cream'],
    'Delhi': ['Butter Chicken', 'Naan', 'Lassi'],
    'Bangalore': ['Biryani', 'Coke', 'Brownie'],
    'Kolkata': ['Biryani', 'Rasgulla', 'Lassi'],
    'Hyderabad': ['Biryani', 'Raita', 'Gulab Jamun'],
}
# Generate 15,000 realistic sessions
n_sessions = 15000
sessions_data = []
for session_id in range(n_sessions):
    # User profile
    user_id = np.random.randint(1, 6000)
    city = np.random.choice(cities)
    
    # Contextual factors - peak hours at lunch and dinner
    hour = np.random.choice([8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23], 
                            p=[0.01, 0.02, 0.03, 0.08, 0.12, 0.15, 0.10, 0.04, 0.03, 0.10, 0.15, 0.10, 0.05, 0.02])
    day_of_week = np.random.randint(0, 7)
    
    if hour < 11:
        meal_time = 'breakfast'
    elif hour < 15:
        meal_time = 'lunch'
    elif hour < 20:
        meal_time = 'dinner'
    else:
        meal_time = 'late_night'
    
    # User segment (behavioral)
    user_segment = np.random.choice(['budget', 'premium', 'occasional'], p=[0.5, 0.3, 0.2])
    user_frequency = np.random.choice(['new', 'regular', 'power'], p=[0.3, 0.5, 0.2])
    
    # Restaurant
    restaurant_id = np.random.randint(1, 800)
    restaurant_type = np.random.choice(['chain', 'independent'], p=[0.4, 0.6])
    cuisine_type = np.random.choice(['Indian', 'Chinese', 'Continental', 'Mixed'], p=[0.5, 0.2, 0.15, 0.15])
    restaurant_rating = round(np.random.uniform(3.5, 4.8), 1)
    
    # Build cart (realistic evolution)
    cart_items = []
    cart_size = np.random.choice([1, 2, 3, 4], p=[0.3, 0.4, 0.2, 0.1])
    
    # Start with main dish (80% of time)
    if np.random.random() < 0.8:
        main_dishes = [k for k, v in items_db.items() if v['category'] == 'Main']
        # City preference influence
        if np.random.random() < 0.4:
            main_dishes = [d for d in main_dishes if d in city_preferences[city]] or main_dishes
        cart_items.append(np.random.choice(main_dishes))
    
    # Add more items
    for _ in range(cart_size - 1):
        available = [i for i in items_list if i not in cart_items]
        if available:
            cart_items.append(np.random.choice(available))
    
    # Calculate cart value
    cart_value = sum([items_db[item]['price'] for item in cart_items])
    
    # Determine TRUE add-on (what user actually added - for training label)
    candidate_addons = [i for i in items_list if i not in cart_items]
    
    # Apply meal completion rules (50% follow rules)
    true_addon = None
    if cart_items and np.random.random() < 0.5:
        for cart_item in cart_items:
            if cart_item in meal_completion_rules:
                possible = [a for a in meal_completion_rules[cart_item] if a not in cart_items]
                if possible:
                    true_addon = np.random.choice(possible)
                    break
    
    # Contextual patterns (30%)
    if not true_addon and np.random.random() < 0.3:
        if meal_time == 'late_night':
            desserts = [i for i in candidate_addons if items_db[i]['category'] == 'Dessert']
            if desserts:
                true_addon = np.random.choice(desserts)
        elif not any(items_db[i]['category'] == 'Drink' for i in cart_items):
            drinks = [i for i in candidate_addons if items_db[i]['category'] == 'Drink']
            if drinks:
                true_addon = np.random.choice(drinks)
    
    # Random (20% - noise)
    if not true_addon:
        true_addon = np.random.choice(candidate_addons)
    
    # User historical behavior (mock)
    user_order_count = np.random.poisson(5) if user_frequency == 'regular' else (np.random.poisson(15) if user_frequency == 'power' else np.random.poisson(1))
    user_avg_order_value = np.random.uniform(200, 600) if user_segment == 'budget' else np.random.uniform(500, 1200)
    
    # Session data
    sessions_data.append({
        'session_id': session_id,
        'user_id': user_id,
        'city': city,
        'hour': hour,
        'day_of_week': day_of_week,
        'meal_time': meal_time,
        'user_segment': user_segment,
        'user_frequency': user_frequency,
        'user_order_count': user_order_count,
        'user_avg_order_value': user_avg_order_value,
        'restaurant_id': restaurant_id,
        'restaurant_type': restaurant_type,
        'cuisine_type': cuisine_type,
        'restaurant_rating': restaurant_rating,
        'cart_items': ','.join(cart_items),
        'cart_size': len(cart_items),
        'cart_value': cart_value,
        'has_main': int(any(items_db[i]['category'] == 'Main' for i in cart_items)),
        'has_side': int(any(items_db[i]['category'] == 'Side' for i in cart_items)),
        'has_drink': int(any(items_db[i]['category'] == 'Drink' for i in cart_items)),
        'has_dessert': int(any(items_db[i]['category'] == 'Dessert' for i in cart_items)),
        'true_addon': true_addon,
        'addon_price': items_db[true_addon]['price'],
        'addon_category': items_db[true_addon]['category'],
    })
df_sessions = pd.DataFrame(sessions_data)
df_sessions.to_csv('zomato_cart_sessions.csv', index=False)
print(f"\n Generated {len(df_sessions)} realistic sessions")
print(f"\nData Statistics:")
print(f"  - Unique Users: {df_sessions['user_id'].nunique()}")
print(f"  - Unique Restaurants: {df_sessions['restaurant_id'].nunique()}")
print(f"  - Cities: {df_sessions['city'].nunique()}")
print(f"  - Avg Cart Size: {df_sessions['cart_size'].mean():.2f}")
print(f"  - Avg Cart Value: ₹{df_sessions['cart_value'].mean():.2f}")
print(f"\nMeal Time Distribution:")
print(df_sessions['meal_time'].value_counts())
print(f"\nUser Segment Distribution:")
print(df_sessions['user_segment'].value_counts())
# Save items database
with open('items_database.json', 'w') as f:
    json.dump(items_db, f, indent=2)
with open('meal_completion_rules.json', 'w') as f:
    json.dump(meal_completion_rules, f, indent=2)
print(f"\nSaved items_database.json with {len(items_db)} items")
print(" Saved meal_completion_rules.json")
print("\n" + "=" * 60)


 Generating refined realistic Zomato-style dataset with improved statistics and supporting files for the hackathon solution.

 import os
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import json
# Set seed for reproducibility
np.random.seed(42)
print("=" * 60)
print("GENERATING REALISTIC ZOMATO-STYLE DATASET")
print("=" * 60)
# Define realistic food items with categories
items_db = {
    'Biryani': {'category': 'Main', 'price': 280, 'type': 'Non-Veg', 'cuisine': 'Indian'},
    'Paneer Tikka': {'category': 'Main', 'price': 220, 'type': 'Veg', 'cuisine': 'Indian'},
    'Butter Chicken': {'category': 'Main', 'price': 320, 'type': 'Non-Veg', 'cuisine': 'Indian'},
    'Dal Makhani': {'category': 'Main', 'price': 180, 'type': 'Veg', 'cuisine': 'Indian'},
    'Chicken Fried Rice': {'category': 'Main', 'price': 210, 'type': 'Non-Veg', 'cuisine': 'Chinese'},
    'Hakka Noodles': {'category': 'Main', 'price': 190, 'type': 'Veg', 'cuisine': 'Chinese'},
    
    'Raita': {'category': 'Side', 'price': 60, 'type': 'Veg', 'cuisine': 'Indian'},
    'Salan': {'category': 'Side', 'price': 70, 'type': 'Veg', 'cuisine': 'Indian'},
    'Naan': {'category': 'Bread', 'price': 40, 'type': 'Veg', 'cuisine': 'Indian'},
    'Roti': {'category': 'Bread', 'price': 30, 'type': 'Veg', 'cuisine': 'Indian'},
    'Papad': {'category': 'Side', 'price': 25, 'type': 'Veg', 'cuisine': 'Indian'},
    
    'Gulab Jamun': {'category': 'Dessert', 'price': 80, 'type': 'Veg', 'cuisine': 'Indian'},
    'Rasgulla': {'category': 'Dessert', 'price': 70, 'type': 'Veg', 'cuisine': 'Indian'},
    'Ice Cream': {'category': 'Dessert', 'price': 90, 'type': 'Veg', 'cuisine': 'Continental'},
    'Brownie': {'category': 'Dessert', 'price': 100, 'type': 'Veg', 'cuisine': 'Continental'},
    
    'Coke': {'category': 'Drink', 'price': 50, 'type': 'Veg', 'cuisine': 'Beverage'},
    'Lassi': {'category': 'Drink', 'price': 70, 'type': 'Veg', 'cuisine': 'Indian'},
    'Mineral Water': {'category': 'Drink', 'price': 20, 'type': 'Veg', 'cuisine': 'Beverage'},
    'Fresh Lime': {'category': 'Drink', 'price': 60, 'type': 'Veg', 'cuisine': 'Beverage'},
    
    'Samosa': {'category': 'Starter', 'price': 40, 'type': 'Veg', 'cuisine': 'Indian'},
    'Chicken Wings': {'category': 'Starter', 'price': 180, 'type': 'Non-Veg', 'cuisine': 'Continental'},
    'Spring Rolls': {'category': 'Starter', 'price': 120, 'type': 'Veg', 'cuisine': 'Chinese'},
    'Salad': {'category': 'Starter', 'price': 90, 'type': 'Veg', 'cuisine': 'Continental'},
}
items_list = list(items_db.keys())
# Meal completion rules
meal_completion_rules = {
    'Biryani': ['Raita', 'Salan', 'Gulab Jamun'],
    'Butter Chicken': ['Naan', 'Roti', 'Raita'],
    'Dal Makhani': ['Roti', 'Naan', 'Papad'],
    'Paneer Tikka': ['Naan', 'Raita', 'Coke'],
    'Chicken Fried Rice': ['Spring Rolls', 'Coke', 'Ice Cream'],
    'Hakka Noodles': ['Spring Rolls', 'Coke'],
}
cities = ['Mumbai', 'Delhi', 'Bangalore', 'Kolkata', 'Hyderabad']
city_preferences = {
    'Mumbai': ['Butter Chicken', 'Paneer Tikka', 'Ice Cream'],
    'Delhi': ['Butter Chicken', 'Naan', 'Lassi'],
    'Bangalore': ['Biryani', 'Coke', 'Brownie'],
    'Kolkata': ['Biryani', 'Rasgulla', 'Lassi'],
    'Hyderabad': ['Biryani', 'Raita', 'Gulab Jamun'],
}
# Generate 15,000 realistic sessions
n_sessions = 15000
sessions_data = []
for session_id in range(n_sessions):
    user_id = np.random.randint(1, 6000)
    city = np.random.choice(cities)
    
    # Peak hours - simple approach
    hour_probs = [0.01, 0.02, 0.03, 0.08, 0.12, 0.15, 0.10, 0.04, 0.03, 0.10, 0.15, 0.10, 0.05, 0.02, 0.01, 0.01]
    hour = np.random.choice(range(8, 24), p=hour_probs)
    day_of_week = np.random.randint(0, 7)
    
    if hour < 11:
        meal_time = 'breakfast'
    elif hour < 15:
        meal_time = 'lunch'
    elif hour < 20:
        meal_time = 'dinner'
    else:
        meal_time = 'late_night'
    
    user_segment = np.random.choice(['budget', 'premium', 'occasional'], p=[0.5, 0.3, 0.2])
    user_frequency = np.random.choice(['new', 'regular', 'power'], p=[0.3, 0.5, 0.2])
    
    restaurant_id = np.random.randint(1, 800)
    restaurant_type = np.random.choice(['chain', 'independent'], p=[0.4, 0.6])
    cuisine_type = np.random.choice(['Indian', 'Chinese', 'Continental', 'Mixed'], p=[0.5, 0.2, 0.15, 0.15])
    restaurant_rating = round(np.random.uniform(3.5, 4.8), 1)
    
    # Build cart
    cart_items = []
    cart_size = np.random.choice([1, 2, 3, 4], p=[0.3, 0.4, 0.2, 0.1])
    
    if np.random.random() < 0.8:
        main_dishes = [k for k, v in items_db.items() if v['category'] == 'Main']
        if np.random.random() < 0.4:
            main_dishes = [d for d in main_dishes if d in city_preferences[city]] or main_dishes
        cart_items.append(np.random.choice(main_dishes))
    
    for _ in range(cart_size - 1):
        available = [i for i in items_list if i not in cart_items]
        if available:
            cart_items.append(np.random.choice(available))
    
    cart_value = sum([items_db[item]['price'] for item in cart_items])
    
    # Determine TRUE add-on
    candidate_addons = [i for i in items_list if i not in cart_items]
    
    true_addon = None
    if cart_items and np.random.random() < 0.5:
        for cart_item in cart_items:
            if cart_item in meal_completion_rules:
                possible = [a for a in meal_completion_rules[cart_item] if a not in cart_items]
                if possible:
                    true_addon = np.random.choice(possible)
                    break
    
    if not true_addon and np.random.random() < 0.3:
        if meal_time == 'late_night':
            desserts = [i for i in candidate_addons if items_db[i]['category'] == 'Dessert']
            if desserts:
                true_addon = np.random.choice(desserts)
        elif not any(items_db[i]['category'] == 'Drink' for i in cart_items):
            drinks = [i for i in candidate_addons if items_db[i]['category'] == 'Drink']
            if drinks:
                true_addon = np.random.choice(drinks)
    
    if not true_addon:
        true_addon = np.random.choice(candidate_addons)
    
    user_order_count = np.random.poisson(5) if user_frequency == 'regular' else (np.random.poisson(15) if user_frequency == 'power' else np.random.poisson(1))
    user_avg_order_value = np.random.uniform(200, 600) if user_segment == 'budget' else np.random.uniform(500, 1200)
    
    sessions_data.append({
        'session_id': session_id,
        'user_id': user_id,
        'city': city,
        'hour': hour,
        'day_of_week': day_of_week,
        'meal_time': meal_time,
        'user_segment': user_segment,
        'user_frequency': user_frequency,
        'user_order_count': user_order_count,
        'user_avg_order_value': round(user_avg_order_value, 2),
        'restaurant_id': restaurant_id,
        'restaurant_type': restaurant_type,
        'cuisine_type': cuisine_type,
        'restaurant_rating': restaurant_rating,
        'cart_items': ','.join(cart_items),
        'cart_size': len(cart_items),
        'cart_value': cart_value,
        'has_main': int(any(items_db[i]['category'] == 'Main' for i in cart_items)),
        'has_side': int(any(items_db[i]['category'] == 'Side' for i in cart_items)),
        'has_drink': int(any(items_db[i]['category'] == 'Drink' for i in cart_items)),
        'has_dessert': int(any(items_db[i]['category'] == 'Dessert' for i in cart_items)),
        'true_addon': true_addon,
        'addon_price': items_db[true_addon]['price'],
        'addon_category': items_db[true_addon]['category'],
    })
df_sessions = pd.DataFrame(sessions_data)
df_sessions.to_csv('zomato_cart_sessions.csv', index=False)
print(f"\nGenerated {len(df_sessions)} realistic sessions")
print(f"\nData Statistics:")
print(f"  - Unique Users: {df_sessions['user_id'].nunique()}")
print(f"  - Unique Restaurants: {df_sessions['restaurant_id'].nunique()}")
print(f"  - Cities: {df_sessions['city'].nunique()}")
print(f"  - Avg Cart Size: {df_sessions['cart_size'].mean():.2f}")
print(f"  - Avg Cart Value: ₹{df_sessions['cart_value'].mean():.2f}")
print(f"\nMeal Time Distribution:")
print(df_sessions['meal_time'].value_counts())
print(f"\nUser Segment Distribution:")
print(df_sessions['user_segment'].value_counts())
# Save supporting files
with open('items_database.json', 'w') as f:
    json.dump(items_db, f, indent=2)
with open('meal_completion_rules.json', 'w') as f:
    json.dump(meal_completion_rules, f, indent=2)
print(f"\n Saved items_database.json with {len(items_db)} items")
print(" Saved meal_completion_rules.json")
# Display sample
print(f"\nSample Data (first 3 rows):")
print(df_sessions.head(3).T)
print("\n" + "=" * 60)

 Generating refined synthetic dataset with comprehensive statistics for hackathon presentation structure.

 import os
import pandas as pd
import numpy as np
import json
np.random.seed(42)
print("=" * 60)
print("ZOMATHON CSAO SOLUTION - DATA GENERATION")
print("=" * 60)
# Food items database
items_db = {
    'Biryani': {'category': 'Main', 'price': 280, 'type': 'Non-Veg', 'cuisine': 'Indian'},
    'Paneer Tikka': {'category': 'Main', 'price': 220, 'type': 'Veg', 'cuisine': 'Indian'},
    'Butter Chicken': {'category': 'Main', 'price': 320, 'type': 'Non-Veg', 'cuisine': 'Indian'},
    'Dal Makhani': {'category': 'Main', 'price': 180, 'type': 'Veg', 'cuisine': 'Indian'},
    'Chicken Fried Rice': {'category': 'Main', 'price': 210, 'type': 'Non-Veg', 'cuisine': 'Chinese'},
    'Hakka Noodles': {'category': 'Main', 'price': 190, 'type': 'Veg', 'cuisine': 'Chinese'},
    'Raita': {'category': 'Side', 'price': 60, 'type': 'Veg', 'cuisine': 'Indian'},
    'Salan': {'category': 'Side', 'price': 70, 'type': 'Veg', 'cuisine': 'Indian'},
    'Naan': {'category': 'Bread', 'price': 40, 'type': 'Veg', 'cuisine': 'Indian'},
    'Roti': {'category': 'Bread', 'price': 30, 'type': 'Veg', 'cuisine': 'Indian'},
    'Papad': {'category': 'Side', 'price': 25, 'type': 'Veg', 'cuisine': 'Indian'},
    'Gulab Jamun': {'category': 'Dessert', 'price': 80, 'type': 'Veg', 'cuisine': 'Indian'},
    'Rasgulla': {'category': 'Dessert', 'price': 70, 'type': 'Veg', 'cuisine': 'Indian'},
    'Ice Cream': {'category': 'Dessert', 'price': 90, 'type': 'Veg', 'cuisine': 'Continental'},
    'Brownie': {'category': 'Dessert', 'price': 100, 'type': 'Veg', 'cuisine': 'Continental'},
    'Coke': {'category': 'Drink', 'price': 50, 'type': 'Veg', 'cuisine': 'Beverage'},
    'Lassi': {'category': 'Drink', 'price': 70, 'type': 'Veg', 'cuisine': 'Indian'},
    'Mineral Water': {'category': 'Drink', 'price': 20, 'type': 'Veg', 'cuisine': 'Beverage'},
    'Fresh Lime': {'category': 'Drink', 'price': 60, 'type': 'Veg', 'cuisine': 'Beverage'},
    'Samosa': {'category': 'Starter', 'price': 40, 'type': 'Veg', 'cuisine': 'Indian'},
    'Chicken Wings': {'category': 'Starter', 'price': 180, 'type': 'Non-Veg', 'cuisine': 'Continental'},
    'Spring Rolls': {'category': 'Starter', 'price': 120, 'type': 'Veg', 'cuisine': 'Chinese'},
    'Salad': {'category': 'Starter', 'price': 90, 'type': 'Veg', 'cuisine': 'Continental'},
}
items_list = list(items_db.keys())
meal_completion_rules = {
    'Biryani': ['Raita', 'Salan', 'Gulab Jamun'],
    'Butter Chicken': ['Naan', 'Roti', 'Raita'],
    'Dal Makhani': ['Roti', 'Naan', 'Papad'],
    'Paneer Tikka': ['Naan', 'Raita', 'Coke'],
    'Chicken Fried Rice': ['Spring Rolls', 'Coke', 'Ice Cream'],
    'Hakka Noodles': ['Spring Rolls', 'Coke'],
}
cities = ['Mumbai', 'Delhi', 'Bangalore', 'Kolkata', 'Hyderabad']
n_sessions = 15000
sessions_data = []
for session_id in range(n_sessions):
    user_id = np.random.randint(1, 6000)
    city = np.random.choice(cities)
    
    # Hour distribution
    hour = np.random.choice([8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23])
    day_of_week = np.random.randint(0, 7)
    
    if hour < 11:
        meal_time = 'breakfast'
    elif hour < 15:
        meal_time = 'lunch'
    elif hour < 20:
        meal_time = 'dinner'
    else:
        meal_time = 'late_night'
    
    user_segment = np.random.choice(['budget', 'premium', 'occasional'])
    user_frequency = np.random.choice(['new', 'regular', 'power'])
    
    restaurant_id = np.random.randint(1, 800)
    restaurant_type = np.random.choice(['chain', 'independent'])
    cuisine_type = np.random.choice(['Indian', 'Chinese', 'Continental', 'Mixed'])
    restaurant_rating = round(np.random.uniform(3.5, 4.8), 1)
    
    # Build cart
    cart_items = []
    cart_size = np.random.randint(1, 5)
    
    # Start with main dish 80% of time
    if np.random.random() < 0.8:
        main_dishes = [k for k, v in items_db.items() if v['category'] == 'Main']
        cart_items.append(np.random.choice(main_dishes))
    
    # Add more items
    for _ in range(cart_size - len(cart_items)):
        available = [i for i in items_list if i not in cart_items]
        if available:
            cart_items.append(np.random.choice(available))
    
    cart_value = sum([items_db[item]['price'] for item in cart_items])
    
    # TRUE add-on (label)
    candidate_addons = [i for i in items_list if i not in cart_items]
    
    true_addon = None
    # 50% follow meal completion rules
    if cart_items and np.random.random() < 0.5:
        for cart_item in cart_items:
            if cart_item in meal_completion_rules:
                possible = [a for a in meal_completion_rules[cart_item] if a not in cart_items]
                if possible:
                    true_addon = np.random.choice(possible)
                    break
    
    # 30% contextual
    if not true_addon and np.random.random() < 0.3:
        if meal_time == 'late_night':
            desserts = [i for i in candidate_addons if items_db[i]['category'] == 'Dessert']
            if desserts:
                true_addon = np.random.choice(desserts)
        elif not any(items_db[i]['category'] == 'Drink' for i in cart_items):
            drinks = [i for i in candidate_addons if items_db[i]['category'] == 'Drink']
            if drinks:
                true_addon = np.random.choice(drinks)
    
    # Random fallback
    if not true_addon:
        true_addon = np.random.choice(candidate_addons)
    
    user_order_count = np.random.randint(1, 30)
    user_avg_order_value = round(np.random.uniform(200, 1000), 2)
    
    sessions_data.append({
        'session_id': session_id,
        'user_id': user_id,
        'city': city,
        'hour': hour,
        'day_of_week': day_of_week,
        'meal_time': meal_time,
        'user_segment': user_segment,
        'user_frequency': user_frequency,
        'user_order_count': user_order_count,
        'user_avg_order_value': user_avg_order_value,
        'restaurant_id': restaurant_id,
        'restaurant_type': restaurant_type,
        'cuisine_type': cuisine_type,
        'restaurant_rating': restaurant_rating,
        'cart_items': ','.join(cart_items),
        'cart_size': len(cart_items),
        'cart_value': cart_value,
        'has_main': int(any(items_db[i]['category'] == 'Main' for i in cart_items)),
        'has_side': int(any(items_db[i]['category'] == 'Side' for i in cart_items)),
        'has_drink': int(any(items_db[i]['category'] == 'Drink' for i in cart_items)),
        'has_dessert': int(any(items_db[i]['category'] == 'Dessert' for i in cart_items)),
        'true_addon': true_addon,
        'addon_price': items_db[true_addon]['price'],
        'addon_category': items_db[true_addon]['category'],
    })
df_sessions = pd.DataFrame(sessions_data)
df_sessions.to_csv('zomato_cart_sessions.csv', index=False)
print(f”\n Generated {len(df_sessions)} realistic sessions")
print(f"\nData Statistics:")
print(f"  - Unique Users: {df_sessions['user_id'].nunique()}")
print(f"  - Unique Restaurants: {df_sessions['restaurant_id'].nunique()}")
print(f"  - Cities: {df_sessions['city'].nunique()}")
print(f"  - Unique Items: {len(items_db)}")
print(f"  - Avg Cart Size: {df_sessions['cart_size'].mean():.2f}")
print(f"  - Avg Cart Value: ₹{df_sessions['cart_value'].mean():.2f}")
print(f"\nMeal Time Distribution:")
print(df_sessions['meal_time'].value_counts())
print(f"\nUser Segment Distribution:")
print(df_sessions['user_segment'].value_counts())
# Save supporting files
with open('items_database.json', 'w') as f:
    json.dump(items_db, f, indent=2)
with open('meal_completion_rules.json', 'w') as f:
    json.dump(meal_completion_rules, f, indent=2)
print(f"\n Files saved successfully")
print("\n" + "=" * 60)


Delivering a detailed end-to-end solution structured for easy presentation following evaluation guidelines:
import os
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import json
# Set seed for reproducibility
np.random.seed(42)
# ============================================
# PART 1: REALISTIC SYNTHETIC DATA GENERATION
# ============================================
print("=" * 60)
print("GENERATING REALISTIC ZOMATO-STYLE DATASET")
print("=" * 60)
# Define realistic food items with categories
items_db = {
    'Biryani': {'category': 'Main', 'price': 280, 'type': 'Non-Veg', 'cuisine': 'Indian'},
    'Paneer Tikka': {'category': 'Main', 'price': 220, 'type': 'Veg', 'cuisine': 'Indian'},
    'Butter Chicken': {'category': 'Main', 'price': 320, 'type': 'Non-Veg', 'cuisine': 'Indian'},
    'Dal Makhani': {'category': 'Main', 'price': 180, 'type': 'Veg', 'cuisine': 'Indian'},
    'Chicken Fried Rice': {'category': 'Main', 'price': 210, 'type': 'Non-Veg', 'cuisine': 'Chinese'},
    'Hakka Noodles': {'category': 'Main', 'price': 190, 'type': 'Veg', 'cuisine': 'Chinese'},
    
    'Raita': {'category': 'Side', 'price': 60, 'type': 'Veg', 'cuisine': 'Indian'},
    'Salan': {'category': 'Side', 'price': 70, 'type': 'Veg', 'cuisine': 'Indian'},
    'Naan': {'category': 'Bread', 'price': 40, 'type': 'Veg', 'cuisine': 'Indian'},
    'Roti': {'category': 'Bread', 'price': 30, 'type': 'Veg', 'cuisine': 'Indian'},
    'Papad': {'category': 'Side', 'price': 25, 'type': 'Veg', 'cuisine': 'Indian'},
    
    'Gulab Jamun': {'category': 'Dessert', 'price': 80, 'type': 'Veg', 'cuisine': 'Indian'},
    'Rasgulla': {'category': 'Dessert', 'price': 70, 'type': 'Veg', 'cuisine': 'Indian'},
    'Ice Cream': {'category': 'Dessert', 'price': 90, 'type': 'Veg', 'cuisine': 'Continental'},
    'Brownie': {'category': 'Dessert', 'price': 100, 'type': 'Veg', 'cuisine': 'Continental'},
    
    'Coke': {'category': 'Drink', 'price': 50, 'type': 'Veg', 'cuisine': 'Beverage'},
    'Lassi': {'category': 'Drink', 'price': 70, 'type': 'Veg', 'cuisine': 'Indian'},
    'Mineral Water': {'category': 'Drink', 'price': 20, 'type': 'Veg', 'cuisine': 'Beverage'},
    'Fresh Lime': {'category': 'Drink', 'price': 60, 'type': 'Veg', 'cuisine': 'Beverage'},
    
    'Samosa': {'category': 'Starter', 'price': 40, 'type': 'Veg', 'cuisine': 'Indian'},
    'Chicken Wings': {'category': 'Starter', 'price': 180, 'type': 'Non-Veg', 'cuisine': 'Continental'},
    'Spring Rolls': {'category': 'Starter', 'price': 120, 'type': 'Veg', 'cuisine': 'Chinese'},
    'Salad': {'category': 'Starter', 'price': 90, 'type': 'Veg', 'cuisine': 'Continental'},
}
items_list = list(items_db.keys())
# Meal completion rules (what naturally goes together)
meal_completion_rules = {
    'Biryani': ['Raita', 'Salan', 'Gulab Jamun'],
    'Butter Chicken': ['Naan', 'Roti', 'Raita'],
    'Dal Makhani': ['Roti', 'Naan', 'Papad'],
    'Paneer Tikka': ['Naan', 'Raita', 'Coke'],
    'Chicken Fried Rice': ['Spring Rolls', 'Coke', 'Ice Cream'],
    'Hakka Noodles': ['Spring Rolls', 'Coke'],
}
# Cities with behavior patterns
cities = ['Mumbai', 'Delhi', 'Bangalore', 'Kolkata', 'Hyderabad']
city_preferences = {
    'Mumbai': ['Butter Chicken', 'Paneer Tikka', 'Ice Cream'],
    'Delhi': ['Butter Chicken', 'Naan', 'Lassi'],
    'Bangalore': ['Biryani', 'Coke', 'Brownie'],
    'Kolkata': ['Biryani', 'Rasgulla', 'Lassi'],
    'Hyderabad': ['Biryani', 'Raita', 'Gulab Jamun'],
}
# Generate 15,000 realistic sessions
n_sessions = 15000
sessions_data = []
for session_id in range(n_sessions):
    # User profile
    user_id = np.random.randint(1, 6000)
    city = np.random.choice(cities)
    
    # Contextual factors
    hour = np.random.choice(range(8, 24), p=[0.02]*3 + [0.15]*3 + [0.05]*2 + [0.20]*3 + [0.05]*2 + [0.08]*3)  # Peak lunch/dinner
    day_of_week = np.random.randint(0, 7)
    
    if hour < 11:
        meal_time = 'breakfast'
    elif hour < 15:
        meal_time = 'lunch'
    elif hour < 20:
        meal_time = 'dinner'
    else:
        meal_time = 'late_night'
    
    # User segment (behavioral)
    user_segment = np.random.choice(['budget', 'premium', 'occasional'], p=[0.5, 0.3, 0.2])
    user_frequency = np.random.choice(['new', 'regular', 'power'], p=[0.3, 0.5, 0.2])
    
    # Restaurant
    restaurant_id = np.random.randint(1, 800)
    restaurant_type = np.random.choice(['chain', 'independent'], p=[0.4, 0.6])
    cuisine_type = np.random.choice(['Indian', 'Chinese', 'Continental', 'Mixed'], p=[0.5, 0.2, 0.15, 0.15])
    restaurant_rating = round(np.random.uniform(3.5, 4.8), 1)
    
    # Build cart (realistic evolution)
    cart_items = []
    cart_size = np.random.choice([1, 2, 3, 4], p=[0.3, 0.4, 0.2, 0.1])
    
    # Start with main dish (80% of time)
    if np.random.random() < 0.8:
        main_dishes = [k for k, v in items_db.items() if v['category'] == 'Main']
        # City preference influence
        if np.random.random() < 0.4:
            main_dishes = [d for d in main_dishes if d in city_preferences[city]] or main_dishes
        cart_items.append(np.random.choice(main_dishes))
    
    # Add more items
    for _ in range(cart_size - 1):
        available = [i for i in items_list if i not in cart_items]
        cart_items.append(np.random.choice(available))
    
    # Calculate cart value
    cart_value = sum([items_db[item]['price'] for item in cart_items])
    
    # Determine TRUE add-on (what user actually added - for training label)
    # Use meal completion logic + context
    candidate_addons = [i for i in items_list if i not in cart_items]
    
    # Apply meal completion rules (50% follow rules)
    true_addon = None
    if cart_items and np.random.random() < 0.5:
        for cart_item in cart_items:
            if cart_item in meal_completion_rules:
                possible = [a for a in meal_completion_rules[cart_item] if a not in cart_items]
                if possible:
                    true_addon = np.random.choice(possible)
                    break
    
    # Contextual patterns (30%)
    if not true_addon and np.random.random() < 0.3:
        if meal_time == 'late_night' and 'Dessert' in [items_db[i]['category'] for i in candidate_addons]:
            desserts = [i for i in candidate_addons if items_db[i]['category'] == 'Dessert']
            true_addon = np.random.choice(desserts)
        elif not any(items_db[i]['category'] == 'Drink' for i in cart_items):
            drinks = [i for i in candidate_addons if items_db[i]['category'] == 'Drink']
            if drinks:
                true_addon = np.random.choice(drinks)
    
    # Random (20% - noise)
    if not true_addon:
        true_addon = np.random.choice(candidate_addons)
    
    # User historical behavior (mock)
    user_order_count = np.random.poisson(5) if user_frequency == 'regular' else (np.random.poisson(15) if user_frequency == 'power' else np.random.poisson(1))
    user_avg_order_value = np.random.uniform(200, 600) if user_segment == 'budget' else np.random.uniform(500, 1200)
    
    # Session data
    sessions_data.append({
        'session_id': session_id,
        'user_id': user_id,
        'city': city,
        'hour': hour,
        'day_of_week': day_of_week,
        'meal_time': meal_time,
        'user_segment': user_segment,
        'user_frequency': user_frequency,
        'user_order_count': user_order_count,
        'user_avg_order_value': user_avg_order_value,
        'restaurant_id': restaurant_id,
        'restaurant_type': restaurant_type,
        'cuisine_type': cuisine_type,
        'restaurant_rating': restaurant_rating,
        'cart_items': ','.join(cart_items),
        'cart_size': len(cart_items),
        'cart_value': cart_value,
        'has_main': int(any(items_db[i]['category'] == 'Main' for i in cart_items)),
        'has_side': int(any(items_db[i]['category'] == 'Side' for i in cart_items)),
        'has_drink': int(any(items_db[i]['category'] == 'Drink' for i in cart_items)),
        'has_dessert': int(any(items_db[i]['category'] == 'Dessert' for i in cart_items)),
        'true_addon': true_addon,
        'addon_price': items_db[true_addon]['price'],
        'addon_category': items_db[true_addon]['category'],
    })
df_sessions = pd.DataFrame(sessions_data)
df_sessions.to_csv('zomato_cart_sessions.csv', index=False)
print(f"\nGenerated {len(df_sessions)} realistic sessions")
print(f"\nData Statistics:")
print(f"  - Unique Users: {df_sessions['user_id'].nunique()}")
print(f"  - Unique Restaurants: {df_sessions['restaurant_id'].nunique()}")
print(f"  - Cities: {df_sessions['city'].nunique()}")
print(f"  - Avg Cart Size: {df_sessions['cart_size'].mean():.2f}")
print(f"  - Avg Cart Value: ₹{df_sessions['cart_value'].mean():.2f}")
print(f"\nMeal Time Distribution:")
print(df_sessions['meal_time'].value_counts())
print(f"\nUser Segment Distribution:")
print(df_sessions['user_segment'].value_counts())
# Save items database
with open('items_database.json', 'w') as f:
    json.dump(items_db, f, indent=2)
print(f"\n Saved items_database.json with {len(items_db)} items")
print("\n" + "=" * 60)
Generating refined realistic Zomato-style dataset with improved peak hour distributions and additional rules for presentation structure.
import os
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import json
# Set seed for reproducibility
np.random.seed(42)
# ============================================
# PART 1: REALISTIC SYNTHETIC DATA GENERATION
# ============================================
print("=" * 60)
print("GENERATING REALISTIC ZOMATO-STYLE DATASET")
print("=" * 60)
# Define realistic food items with categories
items_db = {
    'Biryani': {'category': 'Main', 'price': 280, 'type': 'Non-Veg', 'cuisine': 'Indian'},
    'Paneer Tikka': {'category': 'Main', 'price': 220, 'type': 'Veg', 'cuisine': 'Indian'},
    'Butter Chicken': {'category': 'Main', 'price': 320, 'type': 'Non-Veg', 'cuisine': 'Indian'},
    'Dal Makhani': {'category': 'Main', 'price': 180, 'type': 'Veg', 'cuisine': 'Indian'},
    'Chicken Fried Rice': {'category': 'Main', 'price': 210, 'type': 'Non-Veg', 'cuisine': 'Chinese'},
    'Hakka Noodles': {'category': 'Main', 'price': 190, 'type': 'Veg', 'cuisine': 'Chinese'},
    
    'Raita': {'category': 'Side', 'price': 60, 'type': 'Veg', 'cuisine': 'Indian'},
    'Salan': {'category': 'Side', 'price': 70, 'type': 'Veg', 'cuisine': 'Indian'},
    'Naan': {'category': 'Bread', 'price': 40, 'type': 'Veg', 'cuisine': 'Indian'},
    'Roti': {'category': 'Bread', 'price': 30, 'type': 'Veg', 'cuisine': 'Indian'},
    'Papad': {'category': 'Side', 'price': 25, 'type': 'Veg', 'cuisine': 'Indian'},
    
    'Gulab Jamun': {'category': 'Dessert', 'price': 80, 'type': 'Veg', 'cuisine': 'Indian'},
    'Rasgulla': {'category': 'Dessert', 'price': 70, 'type': 'Veg', 'cuisine': 'Indian'},
    'Ice Cream': {'category': 'Dessert', 'price': 90, 'type': 'Veg', 'cuisine': 'Continental'},
    'Brownie': {'category': 'Dessert', 'price': 100, 'type': 'Veg', 'cuisine': 'Continental'},
    
    'Coke': {'category': 'Drink', 'price': 50, 'type': 'Veg', 'cuisine': 'Beverage'},
    'Lassi': {'category': 'Drink', 'price': 70, 'type': 'Veg', 'cuisine': 'Indian'},
    'Mineral Water': {'category': 'Drink', 'price': 20, 'type': 'Veg', 'cuisine': 'Beverage'},
    'Fresh Lime': {'category': 'Drink', 'price': 60, 'type': 'Veg', 'cuisine': 'Beverage'},
    
    'Samosa': {'category': 'Starter', 'price': 40, 'type': 'Veg', 'cuisine': 'Indian'},
    'Chicken Wings': {'category': 'Starter', 'price': 180, 'type': 'Non-Veg', 'cuisine': 'Continental'},
    'Spring Rolls': {'category': 'Starter', 'price': 120, 'type': 'Veg', 'cuisine': 'Chinese'},
    'Salad': {'category': 'Starter', 'price': 90, 'type': 'Veg', 'cuisine': 'Continental'},
}
items_list = list(items_db.keys())
# Meal completion rules (what naturally goes together)
meal_completion_rules = {
    'Biryani': ['Raita', 'Salan', 'Gulab Jamun'],
    'Butter Chicken': ['Naan', 'Roti', 'Raita'],
    'Dal Makhani': ['Roti', 'Naan', 'Papad'],
    'Paneer Tikka': ['Naan', 'Raita', 'Coke'],
    'Chicken Fried Rice': ['Spring Rolls', 'Coke', 'Ice Cream'],
    'Hakka Noodles': ['Spring Rolls', 'Coke'],
}
# Cities with behavior patterns
cities = ['Mumbai', 'Delhi', 'Bangalore', 'Kolkata', 'Hyderabad']
city_preferences = {
    'Mumbai': ['Butter Chicken', 'Paneer Tikka', 'Ice Cream'],
    'Delhi': ['Butter Chicken', 'Naan', 'Lassi'],
    'Bangalore': ['Biryani', 'Coke', 'Brownie'],
    'Kolkata': ['Biryani', 'Rasgulla', 'Lassi'],
    'Hyderabad': ['Biryani', 'Raita', 'Gulab Jamun'],
}
# Generate 15,000 realistic sessions
n_sessions = 15000
sessions_data = []
for session_id in range(n_sessions):
    # User profile
    user_id = np.random.randint(1, 6000)
    city = np.random.choice(cities)
    
    # Contextual factors - peak hours at lunch and dinner
    hour = np.random.choice([8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23], 
                            p=[0.01, 0.02, 0.03, 0.08, 0.12, 0.15, 0.10, 0.04, 0.03, 0.10, 0.15, 0.10, 0.05, 0.02])
    day_of_week = np.random.randint(0, 7)
    
    if hour < 11:
        meal_time = 'breakfast'
    elif hour < 15:
        meal_time = 'lunch'
    elif hour < 20:
        meal_time = 'dinner'
    else:
        meal_time = 'late_night'
    
    # User segment (behavioral)
    user_segment = np.random.choice(['budget', 'premium', 'occasional'], p=[0.5, 0.3, 0.2])
    user_frequency = np.random.choice(['new', 'regular', 'power'], p=[0.3, 0.5, 0.2])
    
    # Restaurant
    restaurant_id = np.random.randint(1, 800)
    restaurant_type = np.random.choice(['chain', 'independent'], p=[0.4, 0.6])
    cuisine_type = np.random.choice(['Indian', 'Chinese', 'Continental', 'Mixed'], p=[0.5, 0.2, 0.15, 0.15])
    restaurant_rating = round(np.random.uniform(3.5, 4.8), 1)
    
    # Build cart (realistic evolution)
    cart_items = []
    cart_size = np.random.choice([1, 2, 3, 4], p=[0.3, 0.4, 0.2, 0.1])
    
    # Start with main dish (80% of time)
    if np.random.random() < 0.8:
        main_dishes = [k for k, v in items_db.items() if v['category'] == 'Main']
        # City preference influence
        if np.random.random() < 0.4:
            main_dishes = [d for d in main_dishes if d in city_preferences[city]] or main_dishes
        cart_items.append(np.random.choice(main_dishes))
    
    # Add more items
    for _ in range(cart_size - 1):
        available = [i for i in items_list if i not in cart_items]
        if available:
            cart_items.append(np.random.choice(available))
    
    # Calculate cart value
    cart_value = sum([items_db[item]['price'] for item in cart_items])
    
    # Determine TRUE add-on (what user actually added - for training label)
    candidate_addons = [i for i in items_list if i not in cart_items]
    
    # Apply meal completion rules (50% follow rules)
    true_addon = None
    if cart_items and np.random.random() < 0.5:
        for cart_item in cart_items:
            if cart_item in meal_completion_rules:
                possible = [a for a in meal_completion_rules[cart_item] if a not in cart_items]
                if possible:
                    true_addon = np.random.choice(possible)
                    break
    
    # Contextual patterns (30%)
    if not true_addon and np.random.random() < 0.3:
        if meal_time == 'late_night':
            desserts = [i for i in candidate_addons if items_db[i]['category'] == 'Dessert']
            if desserts:
                true_addon = np.random.choice(desserts)
        elif not any(items_db[i]['category'] == 'Drink' for i in cart_items):
            drinks = [i for i in candidate_addons if items_db[i]['category'] == 'Drink']
            if drinks:
                true_addon = np.random.choice(drinks)
    
    # Random (20% - noise)
    if not true_addon:
        true_addon = np.random.choice(candidate_addons)
    
    # User historical behavior (mock)
    user_order_count = np.random.poisson(5) if user_frequency == 'regular' else (np.random.poisson(15) if user_frequency == 'power' else np.random.poisson(1))
    user_avg_order_value = np.random.uniform(200, 600) if user_segment == 'budget' else np.random.uniform(500, 1200)
    
    # Session data
    sessions_data.append({
        'session_id': session_id,
        'user_id': user_id,
        'city': city,
        'hour': hour,
        'day_of_week': day_of_week,
        'meal_time': meal_time,
        'user_segment': user_segment,
        'user_frequency': user_frequency,
        'user_order_count': user_order_count,
        'user_avg_order_value': user_avg_order_value,
        'restaurant_id': restaurant_id,
        'restaurant_type': restaurant_type,
        'cuisine_type': cuisine_type,
        'restaurant_rating': restaurant_rating,
        'cart_items': ','.join(cart_items),
        'cart_size': len(cart_items),
        'cart_value': cart_value,
        'has_main': int(any(items_db[i]['category'] == 'Main' for i in cart_items)),
        'has_side': int(any(items_db[i]['category'] == 'Side' for i in cart_items)),
        'has_drink': int(any(items_db[i]['category'] == 'Drink' for i in cart_items)),
        'has_dessert': int(any(items_db[i]['category'] == 'Dessert' for i in cart_items)),
        'true_addon': true_addon,
        'addon_price': items_db[true_addon]['price'],
        'addon_category': items_db[true_addon]['category'],
    })
df_sessions = pd.DataFrame(sessions_data)
df_sessions.to_csv('zomato_cart_sessions.csv', index=False)
print(f"\n Generated {len(df_sessions)} realistic sessions")
print(f"\nData Statistics:")
print(f"  - Unique Users: {df_sessions['user_id'].nunique()}")
print(f"  - Unique Restaurants: {df_sessions['restaurant_id'].nunique()}")
print(f"  - Cities: {df_sessions['city'].nunique()}")
print(f"  - Avg Cart Size: {df_sessions['cart_size'].mean():.2f}")
print(f"  - Avg Cart Value: ₹{df_sessions['cart_value'].mean():.2f}")
print(f"\nMeal Time Distribution:")
print(df_sessions['meal_time'].value_counts())
print(f"\nUser Segment Distribution:")
print(df_sessions['user_segment'].value_counts())
# Save items database
with open('items_database.json', 'w') as f:
    json.dump(items_db, f, indent=2)
with open('meal_completion_rules.json', 'w') as f:
    json.dump(meal_completion_rules, f, indent=2)
print(f"\nSaved items_database.json with {len(items_db)} items")
print(" Saved meal_completion_rules.json")
print("\n" + "=" * 60)


 Generating refined realistic Zomato-style dataset with improved statistics and supporting files for the hackathon solution.

 import os
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import json
# Set seed for reproducibility
np.random.seed(42)
print("=" * 60)
print("GENERATING REALISTIC ZOMATO-STYLE DATASET")
print("=" * 60)
# Define realistic food items with categories
items_db = {
    'Biryani': {'category': 'Main', 'price': 280, 'type': 'Non-Veg', 'cuisine': 'Indian'},
    'Paneer Tikka': {'category': 'Main', 'price': 220, 'type': 'Veg', 'cuisine': 'Indian'},
    'Butter Chicken': {'category': 'Main', 'price': 320, 'type': 'Non-Veg', 'cuisine': 'Indian'},
    'Dal Makhani': {'category': 'Main', 'price': 180, 'type': 'Veg', 'cuisine': 'Indian'},
    'Chicken Fried Rice': {'category': 'Main', 'price': 210, 'type': 'Non-Veg', 'cuisine': 'Chinese'},
    'Hakka Noodles': {'category': 'Main', 'price': 190, 'type': 'Veg', 'cuisine': 'Chinese'},
    
    'Raita': {'category': 'Side', 'price': 60, 'type': 'Veg', 'cuisine': 'Indian'},
    'Salan': {'category': 'Side', 'price': 70, 'type': 'Veg', 'cuisine': 'Indian'},
    'Naan': {'category': 'Bread', 'price': 40, 'type': 'Veg', 'cuisine': 'Indian'},
    'Roti': {'category': 'Bread', 'price': 30, 'type': 'Veg', 'cuisine': 'Indian'},
    'Papad': {'category': 'Side', 'price': 25, 'type': 'Veg', 'cuisine': 'Indian'},
    
    'Gulab Jamun': {'category': 'Dessert', 'price': 80, 'type': 'Veg', 'cuisine': 'Indian'},
    'Rasgulla': {'category': 'Dessert', 'price': 70, 'type': 'Veg', 'cuisine': 'Indian'},
    'Ice Cream': {'category': 'Dessert', 'price': 90, 'type': 'Veg', 'cuisine': 'Continental'},
    'Brownie': {'category': 'Dessert', 'price': 100, 'type': 'Veg', 'cuisine': 'Continental'},
    
    'Coke': {'category': 'Drink', 'price': 50, 'type': 'Veg', 'cuisine': 'Beverage'},
    'Lassi': {'category': 'Drink', 'price': 70, 'type': 'Veg', 'cuisine': 'Indian'},
    'Mineral Water': {'category': 'Drink', 'price': 20, 'type': 'Veg', 'cuisine': 'Beverage'},
    'Fresh Lime': {'category': 'Drink', 'price': 60, 'type': 'Veg', 'cuisine': 'Beverage'},
    
    'Samosa': {'category': 'Starter', 'price': 40, 'type': 'Veg', 'cuisine': 'Indian'},
    'Chicken Wings': {'category': 'Starter', 'price': 180, 'type': 'Non-Veg', 'cuisine': 'Continental'},
    'Spring Rolls': {'category': 'Starter', 'price': 120, 'type': 'Veg', 'cuisine': 'Chinese'},
    'Salad': {'category': 'Starter', 'price': 90, 'type': 'Veg', 'cuisine': 'Continental'},
}
items_list = list(items_db.keys())
# Meal completion rules
meal_completion_rules = {
    'Biryani': ['Raita', 'Salan', 'Gulab Jamun'],
    'Butter Chicken': ['Naan', 'Roti', 'Raita'],
    'Dal Makhani': ['Roti', 'Naan', 'Papad'],
    'Paneer Tikka': ['Naan', 'Raita', 'Coke'],
    'Chicken Fried Rice': ['Spring Rolls', 'Coke', 'Ice Cream'],
    'Hakka Noodles': ['Spring Rolls', 'Coke'],
}
cities = ['Mumbai', 'Delhi', 'Bangalore', 'Kolkata', 'Hyderabad']
city_preferences = {
    'Mumbai': ['Butter Chicken', 'Paneer Tikka', 'Ice Cream'],
    'Delhi': ['Butter Chicken', 'Naan', 'Lassi'],
    'Bangalore': ['Biryani', 'Coke', 'Brownie'],
    'Kolkata': ['Biryani', 'Rasgulla', 'Lassi'],
    'Hyderabad': ['Biryani', 'Raita', 'Gulab Jamun'],
}
# Generate 15,000 realistic sessions
n_sessions = 15000
sessions_data = []
for session_id in range(n_sessions):
    user_id = np.random.randint(1, 6000)
    city = np.random.choice(cities)
    
    # Peak hours - simple approach
    hour_probs = [0.01, 0.02, 0.03, 0.08, 0.12, 0.15, 0.10, 0.04, 0.03, 0.10, 0.15, 0.10, 0.05, 0.02, 0.01, 0.01]
    hour = np.random.choice(range(8, 24), p=hour_probs)
    day_of_week = np.random.randint(0, 7)
    
    if hour < 11:
        meal_time = 'breakfast'
    elif hour < 15:
        meal_time = 'lunch'
    elif hour < 20:
        meal_time = 'dinner'
    else:
        meal_time = 'late_night'
    
    user_segment = np.random.choice(['budget', 'premium', 'occasional'], p=[0.5, 0.3, 0.2])
    user_frequency = np.random.choice(['new', 'regular', 'power'], p=[0.3, 0.5, 0.2])
    
    restaurant_id = np.random.randint(1, 800)
    restaurant_type = np.random.choice(['chain', 'independent'], p=[0.4, 0.6])
    cuisine_type = np.random.choice(['Indian', 'Chinese', 'Continental', 'Mixed'], p=[0.5, 0.2, 0.15, 0.15])
    restaurant_rating = round(np.random.uniform(3.5, 4.8), 1)
    
    # Build cart
    cart_items = []
    cart_size = np.random.choice([1, 2, 3, 4], p=[0.3, 0.4, 0.2, 0.1])
    
    if np.random.random() < 0.8:
        main_dishes = [k for k, v in items_db.items() if v['category'] == 'Main']
        if np.random.random() < 0.4:
            main_dishes = [d for d in main_dishes if d in city_preferences[city]] or main_dishes
        cart_items.append(np.random.choice(main_dishes))
    
    for _ in range(cart_size - 1):
        available = [i for i in items_list if i not in cart_items]
        if available:
            cart_items.append(np.random.choice(available))
    
    cart_value = sum([items_db[item]['price'] for item in cart_items])
    
    # Determine TRUE add-on
    candidate_addons = [i for i in items_list if i not in cart_items]
    
    true_addon = None
    if cart_items and np.random.random() < 0.5:
        for cart_item in cart_items:
            if cart_item in meal_completion_rules:
                possible = [a for a in meal_completion_rules[cart_item] if a not in cart_items]
                if possible:
                    true_addon = np.random.choice(possible)
                    break
    
    if not true_addon and np.random.random() < 0.3:
        if meal_time == 'late_night':
            desserts = [i for i in candidate_addons if items_db[i]['category'] == 'Dessert']
            if desserts:
                true_addon = np.random.choice(desserts)
        elif not any(items_db[i]['category'] == 'Drink' for i in cart_items):
            drinks = [i for i in candidate_addons if items_db[i]['category'] == 'Drink']
            if drinks:
                true_addon = np.random.choice(drinks)
    
    if not true_addon:
        true_addon = np.random.choice(candidate_addons)
    
    user_order_count = np.random.poisson(5) if user_frequency == 'regular' else (np.random.poisson(15) if user_frequency == 'power' else np.random.poisson(1))
    user_avg_order_value = np.random.uniform(200, 600) if user_segment == 'budget' else np.random.uniform(500, 1200)
    
    sessions_data.append({
        'session_id': session_id,
        'user_id': user_id,
        'city': city,
        'hour': hour,
        'day_of_week': day_of_week,
        'meal_time': meal_time,
        'user_segment': user_segment,
        'user_frequency': user_frequency,
        'user_order_count': user_order_count,
        'user_avg_order_value': round(user_avg_order_value, 2),
        'restaurant_id': restaurant_id,
        'restaurant_type': restaurant_type,
        'cuisine_type': cuisine_type,
        'restaurant_rating': restaurant_rating,
        'cart_items': ','.join(cart_items),
        'cart_size': len(cart_items),
        'cart_value': cart_value,
        'has_main': int(any(items_db[i]['category'] == 'Main' for i in cart_items)),
        'has_side': int(any(items_db[i]['category'] == 'Side' for i in cart_items)),
        'has_drink': int(any(items_db[i]['category'] == 'Drink' for i in cart_items)),
        'has_dessert': int(any(items_db[i]['category'] == 'Dessert' for i in cart_items)),
        'true_addon': true_addon,
        'addon_price': items_db[true_addon]['price'],
        'addon_category': items_db[true_addon]['category'],
    })
df_sessions = pd.DataFrame(sessions_data)
df_sessions.to_csv('zomato_cart_sessions.csv', index=False)
print(f"\nGenerated {len(df_sessions)} realistic sessions")
print(f"\nData Statistics:")
print(f"  - Unique Users: {df_sessions['user_id'].nunique()}")
print(f"  - Unique Restaurants: {df_sessions['restaurant_id'].nunique()}")
print(f"  - Cities: {df_sessions['city'].nunique()}")
print(f"  - Avg Cart Size: {df_sessions['cart_size'].mean():.2f}")
print(f"  - Avg Cart Value: ₹{df_sessions['cart_value'].mean():.2f}")
print(f"\nMeal Time Distribution:")
print(df_sessions['meal_time'].value_counts())
print(f"\nUser Segment Distribution:")
print(df_sessions['user_segment'].value_counts())
# Save supporting files
with open('items_database.json', 'w') as f:
    json.dump(items_db, f, indent=2)
with open('meal_completion_rules.json', 'w') as f:
    json.dump(meal_completion_rules, f, indent=2)
print(f"\n Saved items_database.json with {len(items_db)} items")
print(" Saved meal_completion_rules.json")
# Display sample
print(f"\nSample Data (first 3 rows):")
print(df_sessions.head(3).T)
print("\n" + "=" * 60)

 Generating refined synthetic dataset with comprehensive statistics for hackathon presentation structure.

 import os
import pandas as pd
import numpy as np
import json
np.random.seed(42)
print("=" * 60)
print("ZOMATHON CSAO SOLUTION - DATA GENERATION")
print("=" * 60)
# Food items database
items_db = {
    'Biryani': {'category': 'Main', 'price': 280, 'type': 'Non-Veg', 'cuisine': 'Indian'},
    'Paneer Tikka': {'category': 'Main', 'price': 220, 'type': 'Veg', 'cuisine': 'Indian'},
    'Butter Chicken': {'category': 'Main', 'price': 320, 'type': 'Non-Veg', 'cuisine': 'Indian'},
    'Dal Makhani': {'category': 'Main', 'price': 180, 'type': 'Veg', 'cuisine': 'Indian'},
    'Chicken Fried Rice': {'category': 'Main', 'price': 210, 'type': 'Non-Veg', 'cuisine': 'Chinese'},
    'Hakka Noodles': {'category': 'Main', 'price': 190, 'type': 'Veg', 'cuisine': 'Chinese'},
    'Raita': {'category': 'Side', 'price': 60, 'type': 'Veg', 'cuisine': 'Indian'},
    'Salan': {'category': 'Side', 'price': 70, 'type': 'Veg', 'cuisine': 'Indian'},
    'Naan': {'category': 'Bread', 'price': 40, 'type': 'Veg', 'cuisine': 'Indian'},
    'Roti': {'category': 'Bread', 'price': 30, 'type': 'Veg', 'cuisine': 'Indian'},
    'Papad': {'category': 'Side', 'price': 25, 'type': 'Veg', 'cuisine': 'Indian'},
    'Gulab Jamun': {'category': 'Dessert', 'price': 80, 'type': 'Veg', 'cuisine': 'Indian'},
    'Rasgulla': {'category': 'Dessert', 'price': 70, 'type': 'Veg', 'cuisine': 'Indian'},
    'Ice Cream': {'category': 'Dessert', 'price': 90, 'type': 'Veg', 'cuisine': 'Continental'},
    'Brownie': {'category': 'Dessert', 'price': 100, 'type': 'Veg', 'cuisine': 'Continental'},
    'Coke': {'category': 'Drink', 'price': 50, 'type': 'Veg', 'cuisine': 'Beverage'},
    'Lassi': {'category': 'Drink', 'price': 70, 'type': 'Veg', 'cuisine': 'Indian'},
    'Mineral Water': {'category': 'Drink', 'price': 20, 'type': 'Veg', 'cuisine': 'Beverage'},
    'Fresh Lime': {'category': 'Drink', 'price': 60, 'type': 'Veg', 'cuisine': 'Beverage'},
    'Samosa': {'category': 'Starter', 'price': 40, 'type': 'Veg', 'cuisine': 'Indian'},
    'Chicken Wings': {'category': 'Starter', 'price': 180, 'type': 'Non-Veg', 'cuisine': 'Continental'},
    'Spring Rolls': {'category': 'Starter', 'price': 120, 'type': 'Veg', 'cuisine': 'Chinese'},
    'Salad': {'category': 'Starter', 'price': 90, 'type': 'Veg', 'cuisine': 'Continental'},
}
items_list = list(items_db.keys())
meal_completion_rules = {
    'Biryani': ['Raita', 'Salan', 'Gulab Jamun'],
    'Butter Chicken': ['Naan', 'Roti', 'Raita'],
    'Dal Makhani': ['Roti', 'Naan', 'Papad'],
    'Paneer Tikka': ['Naan', 'Raita', 'Coke'],
    'Chicken Fried Rice': ['Spring Rolls', 'Coke', 'Ice Cream'],
    'Hakka Noodles': ['Spring Rolls', 'Coke'],
}
cities = ['Mumbai', 'Delhi', 'Bangalore', 'Kolkata', 'Hyderabad']
n_sessions = 15000
sessions_data = []
for session_id in range(n_sessions):
    user_id = np.random.randint(1, 6000)
    city = np.random.choice(cities)
    
    # Hour distribution
    hour = np.random.choice([8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23])
    day_of_week = np.random.randint(0, 7)
    
    if hour < 11:
        meal_time = 'breakfast'
    elif hour < 15:
        meal_time = 'lunch'
    elif hour < 20:
        meal_time = 'dinner'
    else:
        meal_time = 'late_night'
    
    user_segment = np.random.choice(['budget', 'premium', 'occasional'])
    user_frequency = np.random.choice(['new', 'regular', 'power'])
    
    restaurant_id = np.random.randint(1, 800)
    restaurant_type = np.random.choice(['chain', 'independent'])
    cuisine_type = np.random.choice(['Indian', 'Chinese', 'Continental', 'Mixed'])
    restaurant_rating = round(np.random.uniform(3.5, 4.8), 1)
    
    # Build cart
    cart_items = []
    cart_size = np.random.randint(1, 5)
    
    # Start with main dish 80% of time
    if np.random.random() < 0.8:
        main_dishes = [k for k, v in items_db.items() if v['category'] == 'Main']
        cart_items.append(np.random.choice(main_dishes))
    
    # Add more items
    for _ in range(cart_size - len(cart_items)):
        available = [i for i in items_list if i not in cart_items]
        if available:
            cart_items.append(np.random.choice(available))
    
    cart_value = sum([items_db[item]['price'] for item in cart_items])
    
    # TRUE add-on (label)
    candidate_addons = [i for i in items_list if i not in cart_items]
    
    true_addon = None
    # 50% follow meal completion rules
    if cart_items and np.random.random() < 0.5:
        for cart_item in cart_items:
            if cart_item in meal_completion_rules:
                possible = [a for a in meal_completion_rules[cart_item] if a not in cart_items]
                if possible:
                    true_addon = np.random.choice(possible)
                    break
    
    # 30% contextual
    if not true_addon and np.random.random() < 0.3:
        if meal_time == 'late_night':
            desserts = [i for i in candidate_addons if items_db[i]['category'] == 'Dessert']
            if desserts:
                true_addon = np.random.choice(desserts)
        elif not any(items_db[i]['category'] == 'Drink' for i in cart_items):
            drinks = [i for i in candidate_addons if items_db[i]['category'] == 'Drink']
            if drinks:
                true_addon = np.random.choice(drinks)
    
    # Random fallback
    if not true_addon:
        true_addon = np.random.choice(candidate_addons)
    
    user_order_count = np.random.randint(1, 30)
    user_avg_order_value = round(np.random.uniform(200, 1000), 2)
    
    sessions_data.append({
        'session_id': session_id,
        'user_id': user_id,
        'city': city,
        'hour': hour,
        'day_of_week': day_of_week,
        'meal_time': meal_time,
        'user_segment': user_segment,
        'user_frequency': user_frequency,
        'user_order_count': user_order_count,
        'user_avg_order_value': user_avg_order_value,
        'restaurant_id': restaurant_id,
        'restaurant_type': restaurant_type,
        'cuisine_type': cuisine_type,
        'restaurant_rating': restaurant_rating,
        'cart_items': ','.join(cart_items),
        'cart_size': len(cart_items),
        'cart_value': cart_value,
        'has_main': int(any(items_db[i]['category'] == 'Main' for i in cart_items)),
        'has_side': int(any(items_db[i]['category'] == 'Side' for i in cart_items)),
        'has_drink': int(any(items_db[i]['category'] == 'Drink' for i in cart_items)),
        'has_dessert': int(any(items_db[i]['category'] == 'Dessert' for i in cart_items)),
        'true_addon': true_addon,
        'addon_price': items_db[true_addon]['price'],
        'addon_category': items_db[true_addon]['category'],
    })
df_sessions = pd.DataFrame(sessions_data)
df_sessions.to_csv('zomato_cart_sessions.csv', index=False)
print(f”\n Generated {len(df_sessions)} realistic sessions")
print(f"\nData Statistics:")
print(f"  - Unique Users: {df_sessions['user_id'].nunique()}")
print(f"  - Unique Restaurants: {df_sessions['restaurant_id'].nunique()}")
print(f"  - Cities: {df_sessions['city'].nunique()}")
print(f"  - Unique Items: {len(items_db)}")
print(f"  - Avg Cart Size: {df_sessions['cart_size'].mean():.2f}")
print(f"  - Avg Cart Value: ₹{df_sessions['cart_value'].mean():.2f}")
print(f"\nMeal Time Distribution:")
print(df_sessions['meal_time'].value_counts())
print(f"\nUser Segment Distribution:")
print(df_sessions['user_segment'].value_counts())
# Save supporting files
with open('items_database.json', 'w') as f:
    json.dump(items_db, f, indent=2)
with open('meal_completion_rules.json', 'w') as f:
    json.dump(meal_completion_rules, f, indent=2)
print(f"\n Files saved successfully")
print("\n" + "=" * 60)