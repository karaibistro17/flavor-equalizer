# app.py
import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import json
import os
from database import INGREDIENT_DB
from google import genai
from google.genai import types

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

# --- ISOLATED BACKGROUND AI SCANNED ENGINE BLOCK ---
def run_molecular_ai_scan(ingredient_name, token_key):
    """Executes live chemical data mining completely decoupled from the UI loops to prevent syntax errors."""
    try:
        client = genai.Client(api_key=token_key)
        prompt = f"Analyze taste metrics for 10g raw '{ingredient_name}'. Range: 0-450. Max context anchors: Sea Salt salty:400, Sugar sweet:380, MSG umami:450, Vinegar sour:280. Return ONLY JSON object with keys: salty, sour, sweet, umami, bitter, spicy. No markdown formatting blocks."
        
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
            config=types.GenerateContentConfig(response_mime_type="application/json")
        )
        
        raw_text = response.text.strip().replace("```json", "").replace("```", "")
        computed_profile = json.loads(raw_text)
        
        # Clean whole integer compliance loop to lock out slider decimals
        validated_dict = {}
        for taste_key in ["salty", "sour", "sweet", "umami", "bitter", "spicy"]:
            raw_val = computed_profile.get(taste_key, 0)
            validated_dict[taste_key] = int(round(float(raw_val)))
            
        return validated_dict
    except Exception as network_error:
        st.error(f"Inference pipeline bottleneck: {network_error}")
        return None

# Initialize database session states cleanly
if "custom_db" not in st.session_state:
    st.session_state.custom_db = load_permanent_library()

if "temp_scan" not in st.session_state:
    st.session_state.temp_scan = None

if "target_profile" not in st.session_state:
    st.session_state.target_profile = None

if "target_name" not in st.session_state:
    st.session_state.target_name = ""

ACTIVE_DB = {**INGREDIENT_DB, **st.session_state.custom_db}

tab1, tab2, tab3 = st.tabs(["🎛️ Flavor Equalizer Deck", "🧬 AI Database Manager", "⚙️ Library Override & Calibration"])

# ==========================================
# TAB 1: THE EQUALIZER CONSOLE & TARGET ENGINE
# ==========================================
with tab1:
    st.title("🎛️ Culinary Matrix Mixing Deck")
    st.write("Formulate recipes and match your active codes against target style benchmarks.")
    
    st.sidebar.metric(label="Library Active Capacity", value=f"{len(ACTIVE_DB)} Items")
    
    st.markdown("### 🎯 Benchmark Alignment Target")
    target_input = st.text_input("Type a target dish to match (e.g., 'Tokyo Shoyu Ramen', 'Spicy Tonkotsu'):", 
                                 value=st.session_state.target_name, placeholder="Type profile target name...", key="target_input_field")
    
    if st.button("📈 Auto-Generate Target Benchmark Curve", key="btn_gen_target"):
        if target_input:
            t_lower = target_input.lower()
            profile = {"Salty": 500, "Sour": 100, "Sweet": 100, "Umami": 600, "Bitter": 50, "Spicy": 0}
            
            if "shoyu" in t_lower:
                profile = {"Salty": 750, "Sour": 150, "Sweet": 120, "Umami": 850, "Bitter": 80, "Spicy": 0}
            elif "miso" in t_lower:
                profile = {"Salty": 700, "Sour": 100, "Sweet": 180, "Umami": 900, "Bitter": 140, "Spicy": 100}
            elif "tonkotsu" in t_lower:
                profile = {"Salty": 650, "Sour": 50, "Sweet": 80, "Umami": 950, "Bitter": 60, "Spicy": 0}
            elif "shio" in t_lower:
                profile = {"Salty": 800, "Sour": 80, "Sweet": 50, "Umami": 750, "Bitter": 40, "Spicy": 0}
            elif "chili" in t_lower or "spicy" in t_lower:
                profile["Spicy"] = 750
                profile["Sweet"] += 250
            elif "sour" in t_lower or "thai" in t_lower or "mop" in t_lower:
                profile["Sour"] = 650
                profile["Sweet"] += 150
                
            st.session_state.target_profile = profile
            st.session_state.target_name = target_input
            st.rerun()
            
    if st.session_state.target_profile:
        st.caption(f"🎯 Currently matching recipe build against: **{st.session_state.target_name}**")
        if st.button("❌ Clear Target Curve", key="btn_clear_target"):
            st.session_state.target_profile = None
            st.session_state.target_name = ""
            st.rerun()

    st.markdown("---")
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
        totals[taste] = int(round((totals[taste] / max_val) * 1000))

    st.subheader("📊 Calibrated Final Equalizer Display")
    tastes = list(totals.keys())
    values = list(totals.values())
    colors = ['#3498db', '#f1c40f', '#e74c3c', '#2ecc71', '#9b59b6', '#e67e22']
    
    fig, ax = plt.subplots(figsize=(8, 4.2), facecolor='#1e1e1e')
    ax.set_facecolor('#121212')
    
    x_positions = np.arange(len(tastes))
    bars = plt.bar(x_positions, values, color=colors, width=0.55, edgecolor='white', linewidth=0.5, zorder=2)
    
    if st.session_state.target_profile:
        target_values = [st.session_state.target_profile[t] for t in tastes]
        plt.plot(x_positions, target_values, color='#ff4757', linestyle='--', marker='o', markersize=6, 
                 linewidth=2, label=f"Target: {st.session_state.target_name}", zorder=3)
        plt.legend(facecolor='#1e1e1e', labelcolor='white', framealpha=0.8, loc='upper right')

    plt.ylim(0, 1190)
    plt.xticks(x_positions, tastes)
    plt.grid(axis='y', linestyle='--', alpha=0.15, color='white')
    ax.tick_params(colors='white', labelsize=10)
    for spine in ax.spines.values():
        spine.set_color('#333333')
        
    for idx, bar in enumerate(bars):
        yval = bar.get_height()
        display_text = f'{yval}'
        if st.session_state.target_profile:
            t_val = st.session_state.target_profile[tastes[idx]]
            diff = yval - t_val
            display_text += f" ({'+' if diff >= 0 else ''}{diff})"
        plt.text(bar.get_x() + bar.get_width()/2.0, yval + 25, display_text, ha='center', va='bottom', color='white', fontweight='bold', fontsize=8)
        
    st.pyplot(fig)

# ==========================================
# TAB 2: LIVE AI DATABASE TERMINAL (SECURE CODEWAYS)
# ==========================================
with tab2:
    st.title("🧬 AI Molecular Database Terminal")
    st.write("Scan new components using live chemical food data analysis networks.")
    
    st.subheader("🔬 Component Analysis Scanner")
    new_ing_name = st.text_input("Enter New Ingredient Name", placeholder="Type item here...", key="ai_scan_input_field")
    
    if st.button("💻 Execute Chemical Analysis", key="btn_run_scan"):
        api_key = st.secrets.get("GEMINI_API_KEY") or os.environ.get("GEMINI_API_KEY")
        
        if not api_key:
            st.error("🔑 **API Key Connection Error:** Missing access token sequence inside your dashboard configuration environment.")
            st.markdown("""
            ### How to link your free API key:
            1. Go to your **Streamlit Cloud Dashboard**.
            2. Click on the **three dots (...)** next to your app name and select **Settings**.
            3. Go to the **Secrets** text console.
            4. Paste this exact configuration inside the block and click Save:
               ```text
               GEMINI_API_KEY = "your_actual_free_api_key_here"
               ```
            """)
        elif new_ing_name:
            with st.spinner("Streaming data profiles from live molecular food chemistry indexes..."):
                # Safe operational call channeled through the background function layer
                scan_result = run_molecular_ai_scan(new_ing_name, api_key)
                if scan_result:
