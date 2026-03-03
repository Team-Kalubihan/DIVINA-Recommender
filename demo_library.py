import json
from divina_recommender import RecommenderEngine, DiveSite, UserPreferences

def main():
    # 1. Sample data as if it came from an API (JSON)
    raw_sites_data = [
        {
            "id": "A1",
            "name": "Emerald Reef",
            "conditions": {
                "water_visibility": 18,
                "wave_height": 0.5,
                "current_speed": 0.2,
                "wind_speed": 5,
                "water_temperature": 26,
                "rain_probability": 0.05,
                "marine_biodiversity": 9
            },
            "difficulty": 2,
            "photography_score": 9,
            "max_depth": 15,
            "marine_life": ["Turtle", "Clownfish", "Parrotfish"],
            "distance_km": 10,
            "crowd_level": 0.2
        },
        {
            "id": "B2",
            "name": "Deep Wall",
            "conditions": {
                "water_visibility": 30,
                "wave_height": 1.2,
                "current_speed": 1.5,
                "wind_speed": 12,
                "water_temperature": 22,
                "rain_probability": 0.1,
                "marine_biodiversity": 7
            },
            "difficulty": 4,
            "photography_score": 6,
            "max_depth": 40,
            "marine_life": ["Shark", "Barracuda"],
            "distance_km": 45,
            "crowd_level": 0.1
        }
    ]

    raw_user_data = {
        "skill_level": 3,
        "preferred_marine_life": ["Turtle", "Shark"],
        "photography_priority": 8,
        "depth_preference": 20,
        "max_travel_distance": 50
    }

    # 2. Use the engine directly from data (dictionaries)
    engine = RecommenderEngine()
    recommendations = engine.recommend_from_data(raw_sites_data, raw_user_data)

    print("\n--- DIVINA API Recommendation Results ---")
    for i, rec in enumerate(recommendations, 1):
        print(f"{i}. {rec['site_name']} (ID: {rec['site_id']})")
        print(f"   Score: {rec['total_score']}")
        print(f"   Breakdown: {rec['breakdown']}")
        print("-" * 30)

    # 3. Custom Weights (Example of Flexibility)
    print("\n--- Using Custom Weights (Prioritizing Crowd Optimization) ---")
    custom_weights = RecommenderEngine.DEFAULT_WEIGHTS.copy()
    custom_weights["crowd_optimization"]["crowd_level"] = 0.50 # Increase to 50%
    custom_weights["environmental"]["water_visibility"] = 0.01 # Decrease visibility importance
    
    custom_engine = RecommenderEngine(custom_weights)
    custom_recs = custom_engine.recommend_from_data(raw_sites_data, raw_user_data)
    
    for i, rec in enumerate(custom_recs, 1):
        print(f"{i}. {rec['site_name']} Score: {rec['total_score']}")

if __name__ == "__main__":
    main()
