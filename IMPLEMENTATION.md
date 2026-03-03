# DIVINA Recommender Implementation Guide

This guide provides instructions on how to integrate the **DIVINA Recommender** engine into your own Python applications.

## 1. Installation

Ensure you have the library in your python path. If you are using `uv`:

```bash
uv add "divina-recommender @ git+https://github.com/Team-Kalubihan/DIVINA-Recommender.git
```

## 2. Core Concepts

The system operates on three primary data models:
- **DiveSite**: Represents a physical dive location with environmental conditions.
- **UserPreferences**: Represents the diver's skill level, interests, and gear requirements.
- **DiveShop**: Represents a business that facilitates trips to specific dive sites.

## 3. Basic Implementation

### Step 1: Initialize the Engine
The `RecommenderEngine` is the entry point for all calculations.

```python
from divina_recommender.engine import RecommenderEngine

engine = RecommenderEngine()
```

### Step 2: Define User Preferences
Create a `UserPreferences` object to represent your user's needs.

```python
from divina_recommender.models import UserPreferences

user = UserPreferences(
    skill_level=3,                 # 1-5 scale
    preferred_marine_life=["Turtle", "Ray"],
    photography_priority=8.0,      # 0-10 scale
    depth_preference=20.0,         # Meters
    max_travel_distance=50.0,      # Kilometers
    requires_rental=True,          # Shop specific
    preferred_price_level=2        # 1-4 scale
)
```

### Step 3: Prepare Dive Sites
You can instantiate `DiveSite` objects manually or via a dictionary (useful for JSON/CSV data).

```python
from divina_recommender.models import DiveSite

# Using dictionary helper
site_data = {
    "id": "site_01",
    "name": "Coral Garden",
    "water_visibility": 20.0,
    "wave_height": 0.5,
    "current_speed": 0.1,
    "wind_speed": 5.0,
    "water_temperature": 26.0,
    "rain_probability": 0.0,
    "marine_biodiversity": 9.0,
    "difficulty": 2,
    "photography_score": 9.0,
    "max_depth": 15.0,
    "marine_life": ["Turtle", "Anemone"],
    "distance_km": 12.0,
    "crowd_level": 0.2
}
site = DiveSite.from_dict(site_data)
sites = [site]
```

### Step 4: Get Recommendations

#### For Dive Sites:
```python
recommendations = engine.recommend(sites, user)

for rec in recommendations:
    print(f"Site: {rec['site_name']} | Score: {rec['total_score']}")
    # Breakdown includes 'environmental', 'user_preferences', and 'crowd_optimization'
```

#### For Dive Shops:
Shop recommendations consider both the shop's services and the quality of the sites they visit.

```python
from divina_recommender.models import DiveShop

shop = DiveShop.from_dict({
    "id": "shop_01",
    "name": "Blue Oceans",
    "rating": 4.5,
    "price_level": 2,
    "has_rental": True,
    "has_nitrox": True,
    "has_training": True,
    "is_tech_friendly": False,
    "dive_sites": ["site_01"], # List of site IDs
    "distance_km": 5.0
})

shop_recommendations = engine.recommend_shops([shop], user, sites)
```

## 4. Customizing Weights

If your application needs to prioritize specific factors (e.g., focusing entirely on environmental safety), you can pass custom weights to the engine:

```python
custom_weights = RecommenderEngine.DEFAULT_WEIGHTS.copy()
# Give environmental conditions 80% importance
custom_weights["environmental"]["water_visibility"] = 0.40 
# ... adjust other weights to sum correctly

engine = RecommenderEngine(custom_weights=custom_weights)
```

## 5. Data Format Reference

### Site Conditions (nested or flat)
The `DiveSite.from_dict` method is flexible. It can accept a flat dictionary (common for CSVs) or a nested dictionary for conditions:

```python
# Nested version (JSON style)
{
    "name": "Deep Blue",
    "conditions": {
        "water_visibility": 30,
        "wave_height": 1.0
    },
    ...
}
```

### Marine Life
`marine_life` can be provided as a Python `List[str]` or a comma-separated `string` (e.g., `"Shark, Turtle"`).
