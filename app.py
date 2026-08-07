import streamlit as st
import matplotlib.pyplot as plt

# Set mobile-responsive configuration
st.set_page_config(page_title="Flavor Mixer EQ", layout="centered")

# 1. EXPANDED KITCHEN DATABASE (Normalized per 1 standard unit)
DB = {
    "Soy Sauce (tbsp)":      {"salty": 250, "sour": 20,  "sweet": 10,  "umami": 200, "bitter": 5,   "spicy": 0},
    "Miso Paste (tbsp)":     {"salty": 180, "sour": 10,  "sweet": 30,  "umami": 250, "bitter": 15,  "spicy": 0},
    "Rice Vinegar (tbsp)":   {"salty": 0,   "sour": 300, "sweet": 15,  "umami": 0,   "bitter": 0,   "spicy": 0},
    "Mirin (tbsp)":          {"salty": 10,  "sour": 15,  "sweet": 220, "umami": 30,  "bitter": 0,   "spicy": 0},
    "Chili Oil (tsp)":       {"salty": 0,   "sour": 0,   "sweet": 5,   "umami": 10,  "bitter": 10,  "spicy": 280},
    "MSG (tsp)":             {"salty": 80,  "sour": 0,   "sweet": 0,   "umami": 450, "bitter": 0,   "spicy": 0},
    "Kosher Salt (tsp)":     {"salty": 400, "sour": 0,   "sweet": 0,   "umami": 0,   "bitter": 0,   "spicy": 0},
    "Brown Sugar (tbsp)":    {"salty": 0,   "sour": 0,   "sweet": 350, "umami": 0,   "bitter": 5,   "spicy": 0},
    "Roasted Garlic (g)":    {"salty": 0,   "sour": 2,   "sweet": 8,   "umami": 12,  "bitter": 1,   "spicy": 2},
    "Beef Broth (cup)":      {"salty": 60,  "sour": 5,   "sweet": 5,   "umami": 90,  "bitter": 2,   "spicy": 0},
    "Lemon Juice (tbsp)":    {"salty": 0,   "sour": 350, "sweet": 10,  "umami": 0,   "bitter": 5,   "spicy": 0},
    "Fish Sauce (tbsp)":     {"salty": 300, "sour": 5,   "sweet": 0,   "umami": 280, "bitter": 0,   "spicy": 0},
    "Tomato Paste (tbsp)":   {"salty": 10,  "sour": 40,  "sweet": 60,  "umami": 150, "bitter": 5,   "spicy": 0},
    "Parmesan Cheese (g)":   {"salty": 80,  "sour": 0,   "sweet": 0,   "umami": 180, "bitter": 10,  "spicy": 0},
    "Honey (tbsp)":          {"salty": 0,   "sour": 0,   "sweet": 380, "umami": 0,   "bitter": 0,   "spicy": 0},
    "Cayenne Pepper (tsp)":  {"salty": 0,   "sour": 0,   "sweet": 0,   "umami": 0,   "bitter": 5,   "spicy": 400},
}

st.title("🎛️ The Reverse Flavor Equalizer")
st.write("Input your recipe rows below to map out the final chemical taste profile.")

# 2. GENERATE THE INTERACTIVE RECIPE ROWS
st.subheader("📋 Recipe Input Grid")
recipe_rows = []

# Loop to dynamically create 10 ingredient rows (expandable up to 25)
for i in range(1, 11):
    col1, col2 = st.columns([2, 1])
    with col1:
        # User dropdown select
        item = st.selectbox(f"Row {i} - Ingredient", ["-- Empty Slot --"] + list(DB.keys()), key=f"item_{i}")
    with col2:
        # User number measurement input
        amount = st.number_input("Amount", min_value=0.0, value=0.0, step=0.25, key=f"amt_{i}")
    
    if item != "-- Empty Slot --" and amount > 0:
        recipe_rows.append({"name": item, "amount": amount})

# 3. RUN THE REAL-TIME MIXING LOGIC
totals = {"Salty": 0, "Sour": 0, "Sweet": 0, "Umami": 0, "Bitter": 0, "Spicy": 0}

for row in recipe_rows:
    ing = row["name"]
    amt = row["amount"]
    for taste in totals.keys():
        totals[taste] += DB[ing][taste.lower()] * amt

# Normalize calculations to your 0 - 1000 scale
max_val = max(totals.values()) if max(totals.values()) > 0 else 1
for taste in totals:
    totals[taste] = int((totals[taste] / max_val) * 1000)

# 4. RENDER THE DIGITAL EQUALIZER GRAPH
st.subheader("📊 Output Equalizer Monitor")

tastes = list(totals.keys())
values = list(totals.values())
colors = ['#3498db', '#f1c40f', '#e74c3c', '#2ecc71', '#9b59b6', '#e67e22'] # Custom high-contrast layout

fig, ax = plt.subplots(figsize=(8, 4), facecolor='#1e1e1e')
ax.set_facecolor('#121212')
bars = plt.bar(tastes, values, color=colors, width=0.55, edgecolor='white', linewidth=0.5)

plt.ylim(0, 1150)
plt.grid(axis='y', linestyle='--', alpha=0.15, color='white')
ax.tick_params(colors='white', labelsize=10)
for spine in ax.spines.values():
    spine.set_color('#333333')

# Draw digital value readouts above the slider paths
for bar in bars:
    yval = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2.0, yval + 25, f'{yval}', ha='center', va='bottom', color='white', fontweight='bold', fontsize=9)

st.pyplot(fig)
