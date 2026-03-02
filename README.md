# DIVINA Recommender System

A flexible, data-agnostic Python library for ranking dive sites based on environmental conditions, user preferences, and crowd optimization.

## 🌊 Overview

The DIVINA Recommender uses a weighted multi-criteria decision analysis (MCDA) approach to provide personalized dive site recommendations. It is designed to be easily integrated into backend APIs (FastAPI, Flask, etc.) or used in data science notebooks.

### Weight Distribution (Default)
| Category | Factor | Weight |
| :--- | :--- | :--- |
| **Environmental (60%)** | Visibility, Waves, Current, Wind, Temp, Rain, Biodiversity | 0.60 |
| **User Prefs (25%)** | Marine Life, Difficulty, Photography, Depth, Distance | 0.25 |
| **Crowd Opt (15%)** | Google Maps Popular Times / Busyness | 0.15 |

---

## 🚀 Installation

### Using `uv` (Recommended)
Add the library to your project directly from the local path or repository:
```bash
uv add "/path/to/DIVINA-Recommender"
```

### Using `pip`
```bash
pip install "/path/to/DIVINA-Recommender"
```

---

## 🛠 Usage

### 1. Basic Integration (API-style)
The fastest way to use the library is with raw dictionary data (JSON-like).

```python
from divina_recommender import RecommenderEngine

engine = RecommenderEngine()

# Sample data (usually from your DB or API request)
sites = [
    {
        "id": "site_01",
        "name": "Coral Garden",
        "conditions": {
            "water_visibility": 20, "wave_height": 0.5, "current_speed": 0.1,
            "wind_speed": 5, "water_temperature": 26, "rain_probability": 0.1,
            "marine_biodiversity": 9
        },
        "difficulty": 2,
        "photography_score": 9.5,
        "max_depth": 15,
        "marine_life": ["Turtle", "Nudibranch"],
        "distance_km": 12,
        "crowd_level": 0.3
    }
]

user = {
    "skill_level": 3,
    "preferred_marine_life": ["Turtle"],
    "photography_priority": 9,
    "depth_preference": 18,
    "max_travel_distance": 50
}

# Get ranked recommendations
results = engine.recommend_from_data(sites, user)

print(results[0]["site_name"]) # Output: Coral Garden
print(results[0]["total_score"]) # Output: 0.84...
```

### 2. Custom Weight Configuration
You can adjust the importance of different factors at runtime.

```python
from divina_recommender import RecommenderEngine

# Create a custom weight profile
custom_weights = RecommenderEngine.DEFAULT_WEIGHTS.copy()

# Make crowd level 50% of the total score instead of 15%
custom_weights["crowd_optimization"]["crowd_level"] = 0.50

engine = RecommenderEngine(custom_weights=custom_weights)
```

### 3. Using Data Models (Strict Typing)
For better IDE support and type safety, use the provided dataclasses.

```python
from divina_recommender import RecommenderEngine, DiveSite, UserPreferences, EnvironmentalConditions

engine = RecommenderEngine()

user = UserPreferences(
    skill_level=3,
    preferred_marine_life=["Shark"],
    photography_priority=7.0,
    depth_preference=25.0,
    max_travel_distance=100.0
)

# recommend() accepts a List[DiveSite]
results = engine.recommend(list_of_dive_site_objects, user)
```

---

## 🛡 Robustness Features
- **Missing Data:** If a field is missing from your input data, the library uses sensible defaults (e.g., 10m visibility, 0.5 current speed).
- **Null Handling:** Automatically converts `NaN` or `None` values to defaults to prevent calculation errors.
- **Flexible Formats:** `marine_life` can be passed as a Python list `["Turtle", "Ray"]` or a comma-separated string `"Turtle, Ray"`.

## 🧪 Running Tests
The project includes a robustness test suite to verify data handling:
```bash
uv run test_robustness.py
```
