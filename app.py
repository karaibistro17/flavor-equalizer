# app.py
import streamlit as st
import matplotlib.pyplot as plt
import json
import os
from database import INGREDIENT_DB

st.set_page_config(page_title="Universal Taste Mixer Console", layout="centered")

STORAGE_FILE = "custom_storage.json"

# --- LOCAL FILE STORAGE ENGINE ---
def load_permanent_library():
    if os.path.exists(STORAGE_FILE):
        try:
            with open(STORAGE_FILE, "r") as f:
                return json.load(f)
        except Exception:
            return {}
    return {}

def save_permanent_library(data):
    try:
        with open(STORAGE_FILE, "w") as f:
            json.dump(data, f, indent=4)
        return True
    except Exception:
        return False

# Initialize custom database from local storage
if "custom_db" not in st.session_state:
    st.session_state.custom_db = load_permanent_library()

if "temp_scan" not in st.session_state:
    st.session_state.temp_scan = None

# Merge base files with custom profiles/overrides
ACTIVE_DB = {**INGREDIENT_DB, **st.session_state.custom_db}

tab1, tab2, tab3 = st.tabs(["🎛️ Flavor Equalizer Deck", "🧬 AI Database Manager", "⚙️ Library Override & Calibration"])

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
# TAB 2: AI DATABASE TERMINAL
# ==========================================
with tab2:
    st.title("🧬 AI Molecular Database Terminal")
    st.write("Scan new components and review chemical compositions.")
    
    st.subheader("🔬 Component Analysis Scanner")
    new_ing_name = st.text_input("Enter New Ingredient Name", placeholder="Type item here...")
    
    if st.button("💻 Execute Chemical Analysis"):
        if new_ing_name:
            with st.spinner("Processing molecular data structure..."):
                name_lower = new_ing_name.lower()
                computed_profile = {"salty": 0, "sour": 0, "sweet": 5, "umami": 10, "bitter": 2, "spicy": 0}
                
                if "fermented" in name_lower or "miso" in name_lower or "sauce" in name_lower or "tobanjan" in name_lower:
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
            st.session_state.custom_db[save_name] = st.session_state.temp_scan['profile']
            save_permanent_library(st.session_state.custom_db)
            st.success(f"Permanently locked '{save_name}' into database storage files!")
            st.session_state.temp_scan = None
            st.rerun()

# ==========================================
# TAB 3: THE CALIBRATION & OVERRIDE PANEL (WITH EDITABLE NAME)
# ==========================================
with tab3:
    st.title("⚙️ Database Calibration Panel")
    st.write("Tweak, rename, or overwrite flavor profile values for any item in your library.")
    
    all_sorted_options = sorted(list(ACTIVE_DB.keys()), key=str.lower)
    target_edit_item = st.selectbox("Select Ingredient to Re-calibrate:", all_sorted_options)
    
    if target_edit_item:
        st.markdown("---")
        current_profile = ACTIVE_DB[target_edit_item]
        
        # NEW FEATURE: EDITABLE NAME OVERRIDE TEXT STRIP
        st.subheader("✏️ Identity Calibration")
        new_name_input = st.text_input("Modify Ingredient Name Field:", value=target_edit_item)
        
        st.subheader("🎚️ Flavor Frequency Calibration")
        new_salty = st.slider("Salty Rating", 0, 450, int(current_profile.get("salty", 0)))
        new_sour = st.slider("Sour Rating", 0, 450, int(current_profile.get("sour", 0)))
        new_sweet = st.slider("Sweet Rating", 0, 450, int(current_profile.get("sweet", 0)))
        new_umami = st.slider("Umami Rating", 0, 450, int(current_profile.get("umami", 0)))
        new_bitter = st.slider("Bitter Rating", 0, 450, int(current_profile.get("bitter", 0)))
        new_spicy = st.slider("Spicy Rating", 0, 450, int(current_profile.get("spicy", 0)))
        
        col_save, col_del = st.columns(2)
        with col_save:
            if st.button("💾 Permanently Override & Calibrate"):
                updated_values = {
                    "salty": new_salty, "sour": new_sour, "sweet": new_sweet,
                    "umami": new_umami, "bitter": new_bitter, "spicy": new_spicy
                }
                
                # If name changed, copy numbers to new name slot, then delete the old one
                if new_name_input != target_edit_item:
                    st.session_state.custom_db[new_name_input] = updated_values
                    # If editing an old custom item, purge its old label
                    if target_edit_item in st.session_state.custom_db:
                        del st.session_state.custom_db[target_edit_item]
                    st.success(f"Renamed and re-calibrated item to '{new_name_input}'!")
                else:
                    # Regular value calibration override
                    st.session_state.custom_db[target_edit_item] = updated_values
                    st.success(f"Successfully re-calibrated profiles for '{target_edit_item}'!")
                
                save_permanent_library(st.session_state.custom_db)
                st.rerun()
                
        with col_del:
            if target_edit_item in st.session_state.custom_db:
                if st.button("🗑️ Completely Delete from Library"):
                    del st.session_state.custom_db[target_edit_item]
                    save_permanent_library(st.session_state.custom_db)
                    st.toast(f"Purged {target_edit_item} from custom storage channels.")
                    st.rerun()
