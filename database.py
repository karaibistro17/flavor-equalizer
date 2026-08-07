# database.py
# Base dictionary containing your core ingredients (per 10g raw)
INGREDIENT_DB = {
    # === MEATS & ANIMAL PROTEINS ===
    "Beef Brisket (Raw)":             {"salty": 5, "sour": 0, "sweet": 0, "umami": 65, "bitter": 2, "spicy": 0},
    "Beef Short Plate (Raw)":         {"salty": 5, "sour": 0, "sweet": 0, "umami": 62, "bitter": 1, "spicy": 0},
    "Beef 80/20 Ground Chuck":        {"salty": 5, "sour": 0, "sweet": 0, "umami": 58, "bitter": 2, "spicy": 0},
    "Beef Flank Steak (Raw)":         {"salty": 6, "sour": 0, "sweet": 0, "umami": 60, "bitter": 3, "spicy": 0},
    "Beef Tendon (Raw)":              {"salty": 4, "sour": 0, "sweet": 0, "umami": 40, "bitter": 1, "spicy": 0},
    "Pork Belly (Raw)":               {"salty": 4, "sour": 0, "sweet": 0, "umami": 55, "bitter": 1, "spicy": 0},
    "Pork Shoulder / Butt (Raw)":     {"salty": 4, "sour": 0, "sweet": 0, "umami": 58, "bitter": 2, "spicy": 0},
    "Pork Loin (Raw)":                {"salty": 5, "sour": 0, "sweet": 0, "umami": 50, "bitter": 2, "spicy": 0},
    "Ground Pork (Raw)":              {"salty": 4, "sour": 0, "sweet": 0, "umami": 54, "bitter": 2, "spicy": 0},
    "Chicken Tenders (Raw)":          {"salty": 4, "sour": 0, "sweet": 0, "umami": 45, "bitter": 1, "spicy": 0},
    "Chicken Thigh (Bone-In, Raw)":   {"salty": 4, "sour": 0, "sweet": 0, "umami": 52, "bitter": 1, "spicy": 0},
    "Duck Breast (Raw)":              {"salty": 5, "sour": 0, "sweet": 0, "umami": 68, "bitter": 3, "spicy": 0},
    "Lamb Shoulder (Raw)":            {"salty": 6, "sour": 0, "sweet": 0, "umami": 64, "bitter": 4, "spicy": 0},
    "Beef Marrow Bones (Raw)":        {"salty": 5, "sour": 0, "sweet": 5, "umami": 70, "bitter": 2, "spicy": 0},
    "Pork Trotters / Feet (Raw)":     {"salty": 4, "sour": 0, "sweet": 2, "umami": 65, "bitter": 3, "spicy": 0},

    # === RAMEN dashi DECK ===
    "Kombu (Dried Kelp)":              {"salty": 25, "sour": 1, "sweet": 8, "umami": 380, "bitter": 15, "spicy": 0},
    "Katsuobushi (Dried Bonito)":      {"salty": 18, "sour": 6, "sweet": 0, "umami": 310, "bitter": 18, "spicy": 0},
    "Niboshi (Dried Baby Sardines)":   {"salty": 45, "sour": 4, "sweet": 0, "umami": 260, "bitter": 65, "spicy": 0},
    "Dried Shiitake Mushrooms":        {"salty": 2,  "sour": 1, "sweet": 15, "umami": 290, "bitter": 25, "spicy": 0},
    "Dried Shrimp / Krill":            {"salty": 55, "sour": 2, "sweet": 12, "umami": 210, "bitter": 10, "spicy": 0},

    # === PURE CORE REAGENTS ===
    "Pure Sea Salt":                   {"salty": 400, "sour": 0, "sweet": 0,   "umami": 0,   "bitter": 0,  "spicy": 0},
    "MSG (Monosodium Glutamate)":      {"salty": 80,  "sour": 0, "sweet": 0,   "umami": 450, "bitter": 0,  "spicy": 0},
    "White Distilled Vinegar":         {"salty": 0,   "sour": 280, "sweet": 0,  "umami": 0,   "bitter": 0,  "spicy": 0},
    "Rice Vinegar (Pure)":             {"salty": 0,   "sour": 220, "sweet": 10, "umami": 0,   "bitter": 0,  "spicy": 0},
    "Koikuchi Shoyu (Raw Dark Soy)":   {"salty": 160, "sour": 15, "sweet": 8,   "umami": 130, "bitter": 4,  "spicy": 0},
    "Usukuchi Shoyu (Raw Light Soy)":  {"salty": 190, "sour": 12, "sweet": 5,   "umami": 110, "bitter": 3,  "spicy": 0},
    "White Miso Base (Unseasoned)":    {"salty": 110, "sour": 8,  "sweet": 50,  "umami": 160, "bitter": 8,  "spicy": 0},
    "Red Miso Base (Unseasoned)":      {"salty": 140, "sour": 12, "sweet": 25,  "umami": 210, "bitter": 14, "spicy": 0},
    "White Granulated Sugar":          {"salty": 0,   "sour": 0,  "sweet": 380, "umami": 0,   "bitter": 0,  "spicy": 0},
    "Mirin (True Hon-Mirin)":          {"salty": 2,   "sour": 5,  "sweet": 160, "umami": 15,  "bitter": 0,  "spicy": 0},
}

# --- AUTOMATED DATA INJECTION SCRIPT BLOCKS ---

# 1. Injection Block: Leafy & Bitter Cruciferous Greens (15 items)
cruciferous = ["Bok Choy", "Gai Lan (Chinese Broccoli)", "Tatsoi", "Komatsuna", "Napa Cabbage", 
               "Kale", "Cabbage (Green)", "Cabbage (Red)", "Savoy Cabbage", "Brussels Sprouts", 
               "Watercress", "Arugula", "Mustard Greens", "Swiss Chard", "Broccoli Rabe"]
for veg in cruciferous:
    INGREDIENT_DB[f"{veg} (Raw)"] = {"salty": 0, "sour": 0, "sweet": 8, "umami": 14, "bitter": 24, "spicy": 0}

# 2. Injection Block: Sweet & Earthy Root Vegetables (15 items)
roots = ["Carrot", "Daikon Radish", "Parsnip", "Turnip", "Red Beet", "Golden Beet", "Rutabaga", 
         "Radish (Red)", "Lotus Root", "Burdock Root (Gobo)", "Taro", "Yam", "Sweet Potato", 
         "Jicama", "Ginger Root"]
for veg in roots:
    # Ginger gets special overrides in the interface, but shares this base physical array structure
    spicy_val = 50 if "Ginger" in veg else 0
    INGREDIENT_DB[f"{veg} (Raw)"] = {"salty": 0, "sour": 2, "sweet": 38, "umami": 10, "bitter": 8, "spicy": spicy_val}

# 3. Injection Block: High-Acid Fruiting Nightshades & Pods (15 items)
fruiting = ["Tomato (Red)", "Tomato (Green)", "Cherry Tomato", "Tomatillo", "Eggplant (Japanese)", 
            "Eggplant (Globe)", "Bell Pepper (Green)", "Bell Pepper (Red)", "Bell Pepper (Yellow)", 
            "Cucumber", "Okra", "Zucchini", "Yellow Squash", "Snap Peas", "Snow Peas"]
for veg in fruiting:
    sour_val = 45 if "Tomato" in veg or "Tomatillo" in veg else 10
    umami_val = 40 if "Tomato" in veg else 12
    INGREDIENT_DB[f"{veg} (Raw)"] = {"salty": 0, "sour": sour_val, "sweet": 22, "umami": umami_val, "bitter": 4, "spicy": 0}

# 4. Injection Block: Allium Sharp Aromatics (10 items)
alliums = ["Garlic Cloves", "Yellow Onion", "Red Onion", "White Onion", "Shallots", 
           "Leeks", "Scallions (Green Part)", "Scallions (White Base)", "Chives", "Ramps"]
for veg in alliums:
    spicy_val = 75 if "Garlic" in veg else 15
    INGREDIENT_DB[f"{veg} (Raw)"] = {"salty": 0, "sour": 2, "sweet": 18, "umami": 12, "bitter": 6, "spicy": spicy_val}

# 5. Injection Block: Citrus & Fruit Acid Drivers (15 items)
fruits = ["Yuzu Juice", "Lemon Juice", "Lime Juice", "Sudachi Juice", "Kabosu Juice", 
          "Fuji Apple", "Nashi Asian Pear", "White Peach", "Green Apple", "Pineapple", 
          "Orange Juice", "Grapefruit Juice", "Meyer Lemon", "Kumquat", "Persimmon"]
for fr in fruits:
    sour_val = 250 if "Juice" in fr or "Lemon" in fr or "Lime" in fr else 30
    sweet_val = 15 if sour_val > 200 else 110
    INGREDIENT_DB[f"{fr} (Raw)"] = {"salty": 0, "sour": sour_val, "sweet": sweet_val, "umami": 2, "bitter": 12, "spicy": 0}
