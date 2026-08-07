# app.py
import streamlit as st
import matplotlib.pyplot as plt
from database import INGREDIENT_DB  # Pulls database automatically

st.set_page_config(page_title="Raw Flavor Catalyst EQ", layout="centered")

st.title("🎛️ Raw Ingredient Matrix Mixer")
st.write("A clean workflow engine calling variables directly from your database script file.")

# Count entries to keep track of your 1000-item target goal
total_items = len(INGREDIENT_DB)
st.sidebar.metric(label="Total Database Library Count", value=f"{total_items} / 1000")
# 2. RUN WORKSPACE INTERFACE ROWS
st.subheader("📋 Fundamental Formulation Deck")
sorted_ingredients = sorted(list(INGREDIENT_DB.keys()))
recipe_rows = []

for i in range(1, 26):
    col1, col2 = st.columns()
    with col1:
        item = st.selectbox(f"CH {i:02d}", ["-- Open Matrix Field --"] + sorted_ingredients, key=f"item_{i}")
    with col2:
        amount = st.number_input("Grams Weight", min_value=0.0, value=0.0, step=0.5, key=f"amt_{i}")
    
    if item != "-- Open Matrix Field --" and amount > 0:
        recipe_rows.append({"name": item, "amount": amount})

# 3. EQUALIZER ALGORITHM ENGINE
totals = {"Salty": 0, "Sour": 0, "Sweet": 0, "Umami": 0, "Bitter": 0, "Spicy": 0}

for row in recipe_rows:
    ing = row["name"]
    factor = row["amount"] / 10.0 
    for taste in totals.keys():
        totals[taste] += INGREDIENT_DB[ing][taste.lower()] * factor

max_val = max(totals.values()) if max(totals.values()) > 0 else 1
for taste in totals:
    totals[taste] = int((totals[taste] / max_val) * 1000)

# 4. CHART OUTPUT
st.subheader("📊 Target Equalizer Frequencies")
tastes = list(totals.keys())
values = list(totals.values())
colors = ['#3498db', '#f1c40f', '#e74c3c', '#2ecc71', '#9b59b6', '#e67e22']

fig, ax = plt.subplots(figsize=(8, 4), facecolor='#1e1e1e')
ax.set_facecolor('#121212')
bars = plt.bar(tastes, values, color=colors, width=0.55, edgecolor='white', linewidth=0.5)

plt.ylim(0, 1150)
plt.ylabel("Normalized Frequency Load (0 - 1000)", color='white')
plt.grid(axis='y', linestyle='--', alpha=0.15, color='white')
ax.tick_params(colors='white', labelsize=10)
for spine in ax.spines.values():
    spine.set_color('#333333')

for bar in bars:
    yval = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2.0, yval + 25, f'{yval}', ha='center', va='bottom', color='white', fontweight='bold', fontsize=9)

st.pyplot(fig)
