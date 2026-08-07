# app.py
import streamlit as st
import matplotlib.pyplot as plt
import json
import os
from database import INGREDIENT_DB

st.set_page_config(page_title="Universal Taste Mixer Console", layout="centered")

STORAGE_FILE = "custom_storage.json"

# --- LOCAL FILE AUTO-SAVE ENGINE ---
def load_permanent_library():
    """Reads the local JSON file to pull permanently saved ingredients."""
    if os.path.exists(STORAGE_FILE):
        try:
            with open(STORAGE_FILE, "r") as f:
                return json.load(f)
        except Exception:
            return {}
    return {}

def save_permanent_library(data):
    """Writes custom ingredients permanently to the local directory file."""
    try:
        with open(STORAGE_FILE, "w") as f:
            json.dump(data, f, indent=4)
        return True
    except Exception:
        return False

# Initialize custom database from local long-term storage file
if "custom_db" not in st.session_state:
    st.session_state.custom_db = load_permanent_library()

if "temp_scan" not in st.session_state:
    st.session_state.temp_scan = None

# Merge base components with long-term custom additions
ACTIVE_DB = {**INGREDIENT_DB, **st.session_state.custom_db}

tab1, tab2 = st.tabs(["🎛️ Flavor Equalizer Deck", "🧬 AI Database Manager"])

# ==========================================
# TAB 1: THE EQUALIZER CONSOLE & COOKING ENGINE
# ==========================================
with tab1:
    st.title("🎛️ Culinary Matrix Mixing Deck")
    st.write("Formulate recipes and calculate chemical taste shifts across variables.")
    
    st.sidebar.metric(label="Library Active Capacity", value=f"{len(ACTIVE_DB)} Items")
    
    st.subheader("📋 Recipe Input Strips")
    sorted_options = sorted(list(ACTIVE_DB.keys()), key=str.lower)
    recipe_rows = []
    
    for i in range(1, 16):
        col1, col2, col3 = st.columns(3)
        with col1:
            item = st.selectbox(f"CH {i:02d}", ["-- Clear Matrix Link --"] + sorted_options, key=f"item_{i}")
        with col2:
            amount = st.number_input("Grams", min_value=0.0, value=0.0, step=1.0, key=f"amt_{i}")
        with col3:
            is_cooked = st.checkbox("Cooked", key=f"cook_{i}")
            
        if item != "-- Clear Matrix Link --" and amount > 0:
            recipe_rows.append({"name": item, "amount": amount, "cooked": is_cooked})

    totals = {"Salty": 0, "Sour": 0, "Sweet": 0, "Umami": 0, "Bitter": 0, "Spicy": 0}
    
    for row in recipe_rows:
        ing = row["name"]
        factor = row["amount"] / 10.0
        base_taste = ACTIVE_DB[ing].copy()
        
        if row["cooked"]:
            base_taste["sweet"] = base_taste["sweet"] * 1.35
            base_taste["umami"] = base_taste["umami"] * 1.20
            base_taste["bitter"] = base_taste["bitter"] + 5 if base_taste["umami"] > 40 else base_taste["bitter"]
            if base_taste["spicy"] > 10:
                base_taste["spicy"] = base_taste["spicy"] * 0.35
                base_taste["sweet"] = base_taste["sweet"] * 1.50
        
        for taste in totals.keys():
            totals[taste] += base_taste[taste.lower()] * factor

    max_val = max(totals.values()) if max(totals.values()) > 0 else 1
    for taste in totals:
        totals[taste] = int((totals[taste] / max_val) * 1000)

    st.subheader("📊 Calibrated Final Equalizer Display")
    tastes = list(totals.keys())
    values = list(totals.values())
    colors = ['#3498db', '#f1c40f', '#e74c3c', '#2ecc71', '#9b59b6', '#e67e22']
    
    fig, ax = plt.subplots(figsize=(8, 3.8), facecolor='#1e1e1e')
    ax.set_facecolor('#121212')
    bars = plt.bar(tastes, values, color=colors, width=0.55, edgecolor='white', linewidth=0.5)
    plt.ylim(0, 1150)
    plt.grid(axis='y', linestyle='--', alpha=0.15, color='white')
    ax.tick_params(colors='white', labelsize=10)
    for spine in ax.spines.values():
        spine.set_color('#333333')
    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2.0, yval + 25, f'{yval}', ha='center', va='bottom', color='white', fontweight='bold', fontsize=9)
    st.pyplot(fig)

# ==========================================
# TAB 2: AI DATABASE TERMINAL (SCAN, PERMANENT SAVE, DELETE)
# ==========================================
with tab2:
    st.title("🧬 AI Molecular Database Terminal")
    st.write("Scan new components, review chemical compositions, and manage your permanent custom library.")
    
    st.subheader("🔬 Component Analysis Scanner")
    new_ing_name = st.text_input("Enter New Ingredient Name", placeholder="Type item here...")
    
    if st.button("💻 Execute Chemical Analysis"):
        if new_ing_name:
            with st.spinner("Processing molecular data structure..."):
                name_lower = new_ing_name.lower()
                computed_profile = {"salty": 0, "sour": 0, "sweet": 5, "umami": 10, "bitter": 2, "spicy": 0}
                
                if "fermented" in name_lower or "miso" in name_lower or "sauce" in name_lower:
                    computed_profile["umami"] += 180
                    computed_profile["salty"] += 140
                if "shoot" in name_lower or "bamboo" in name_lower or "mushroom" in name_lower:
                    computed_profile["umami"] += 80
                    computed_profile["bitter"] += 15
                if "vinegar" in name_lower or "pickle" in name_lower or "sour" in name_lower:
                    computed_profile["sour"] += 220
                if "chili" in name_lower or "spicy" in name_lower or "paste" in name_lower:
                    computed_profile["spicy"] += 200
                    computed_profile["bitter"] += 10
                if "sweet" in name_lower or "honey" in name_lower or "syrup" in name_lower:
                    computed_profile["sweet"] += 300
                
                st.session_state.temp_scan = {"name": new_ing_name, "profile": computed_profile}
        else:
            st.warning("Please input an item name before executing a scan.")

    if st.session_state.temp_scan:
        st.info(f"🧬 **Analysis Complete for:** {st.session_state.temp_scan['name']}")
        st.write(st.session_state.temp_scan['profile'])
        
        if st.button("💾 Save Permanently to Library"):
            save_name = f"{st.session_state.temp_scan['name']} (AI Scanned)"
            
            # 1. Update session memory
            st.session_state.custom_db[save_name] = st.session_state.temp_scan['profile']
            
            # 2. Write to long-term storage file
            if save_permanent_library(st.session_state.custom_db):
                st.success(f"Permanently locked '{save_name}' into database storage files!")
            else:
                st.error("File storage locked. Saved temporarily to session cache instead.")
                
            st.session_state.temp_scan = None
            st.rerun()

    st.markdown("---")

    st.subheader("🗑️ Library Management Console")
    
    if st.session_state.custom_db:
        st.write("Review or delete permanently stored custom ingredients:")
        
        for custom_item in list(st.session_state.custom_db.keys()):
            col_name, col_del = st.columns([4, 1])
            with col_name:
                st.text(f"🔸 {custom_item}")
            with col_del:
                if st.button("Delete", key=f"del_{custom_item}"):
                    # 1. Delete from running dictionary
                    del st.session_state.custom_db[custom_item]
                    # 2. Re-write the file to save the deletion
                    save_permanent_library(st.session_state.custom_db)
                    st.toast(f"Purged {custom_item} from permanent database storage.")
                    st.rerun()
    else:
        st.caption("Your permanent storage profiles are empty. Base records inside 'database.py' remain factory-locked.")
