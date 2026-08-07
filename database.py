# database.py
# Normalized chemical flavor density values calculated per 10 grams of raw ingredient

INGREDIENT_DB = {
    # === MEATS & ANIMAL PROTEINS (Raw, Unseasoned Cuts) ===
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

    # === SEAFOOD COMPONENT DECK ===
    "Kombu (Dried Kelp)":              {"salty": 25, "sour": 1, "sweet": 8, "umami": 380, "bitter": 15, "spicy": 0},
    "Katsuobushi (Dried Bonito)":      {"salty": 18, "sour": 6, "sweet": 0, "umami": 310, "bitter": 18, "spicy": 0},
    "Niboshi (Dried Baby Sardines)":   {"salty": 45, "sour": 4, "sweet": 0, "umami": 260, "bitter": 65, "spicy": 0},
    "Dried Shiitake Mushrooms":        {"salty": 2,  "sour": 1, "sweet": 15, "umami": 290, "bitter": 25, "spicy": 0},
    "Dried Shrimp / Krill":            {"salty": 55, "sour": 2, "sweet": 12, "umami": 210, "bitter": 10, "spicy": 0},

    # === ALLIUMS & FRESH RAMEN VEGETABLES ===
    "Garlic (Raw Cloves)":             {"salty": 0, "sour": 2, "sweet": 8,   "umami": 12, "bitter": 4,  "spicy": 75},
    "Ginger (Raw Root)":               {"salty": 0, "sour": 4, "sweet": 10,  "umami": 5,  "bitter": 14, "spicy": 50},
    "Scallions / Green Onions (Raw)":  {"salty": 0, "sour": 0, "sweet": 12,  "umami": 8,  "bitter": 6,  "spicy": 12},
    "Yellow Onion (Raw)":              {"salty": 0, "sour": 1, "sweet": 25,  "umami": 10, "bitter": 2,  "spicy": 8},
    "Napa Cabbage (Raw)":              {"salty": 0, "sour": 0, "sweet": 14,  "umami": 15, "bitter": 3,  "spicy": 0},
    "Daikon Radish (Raw)":             {"salty": 0, "sour": 2, "sweet": 11,  "umami": 8,  "bitter": 12, "spicy": 15},
    "Bamboo Shoots (Raw/Plain)":       {"salty": 0, "sour": 0, "sweet": 4,   "umami": 10, "bitter": 18, "spicy": 0},
    "Bok Choy (Raw)":                  {"salty": 0, "sour": 0, "sweet": 8,   "umami": 14, "bitter": 6,  "spicy": 0},
    "Mashrooms - Wood Ear / Kikurage": {"salty": 0, "sour": 0, "sweet": 2,   "umami": 20, "bitter": 5,  "spicy": 0},
    "Mizuna Greens (Raw)":             {"salty": 0, "sour": 0, "sweet": 5,   "umami": 12, "bitter": 22, "spicy": 0},

    # === CITRUS & FRUITS (Raw Extraction Profiles) ===
    "Yuzu Juice (Fresh)":              {"salty": 0, "sour": 260, "sweet": 15,  "umami": 0, "bitter": 25, "spicy": 0},
    "Lemon Juice (Fresh)":             {"salty": 0, "sour": 250, "sweet": 12,  "umami": 0, "bitter": 8,  "spicy": 0},
    "Lime Juice (Fresh)":              {"salty": 0, "sour": 255, "sweet": 10,  "umami": 0, "bitter": 12, "spicy": 0},
    "Fuji Apple (Raw/Pureed)":         {"salty": 0, "sour": 35,  "sweet": 110, "umami": 2, "bitter": 1,  "spicy": 0},
    "Nashi Asian Pear (Raw)":          {"salty": 0, "sour": 20,  "sweet": 95,  "umami": 3, "bitter": 1,  "spicy": 0},

    # === SALTS, LIQUIDS & CHEMICAL ELEMENTS ===
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
