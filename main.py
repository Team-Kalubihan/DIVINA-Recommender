import pandas as pd
from src.divina_recommender.models import DiveSite, UserPreferences, EnvironmentalConditions
from src.divina_recommender.engine import RecommenderEngine

def load_sites_from_csv(file_path: str):
    df = pd.read_csv(file_path)
    return [DiveSite.from_dict(row.to_dict()) for _, row in df.iterrows()]

def main():
    # 1. Initialize Engine
    engine = RecommenderEngine()

    # 2. Load Dive Sites from CSV
    try:
        sites = load_sites_from_csv("data/sites.csv")
    except Exception as e:
        print(f"Error loading CSV: {e}")
        return

    # 3. Define User Preferences
    user = UserPreferences(
        skill_level=3,
        preferred_marine_life=["Manta Ray", "Turtle"],
        photography_priority=9.5,
        depth_preference=15.0,
        max_travel_distance=100.0
    )

    # 4. Get Recommendations
    recommendations = engine.recommend(sites, user)

    # 5. Print Results
    print("\n--- DIVINA Recommendation Results ---")
    print(f"User Preferences: Skill={user.skill_level}, Targets={user.preferred_marine_life}, Depth={user.depth_preference}m\n")
    
    for i, rec in enumerate(recommendations, 1):
        site = rec["site"]
        print(f"{i}. {site.name}")
        print(f"   Overall Score: {rec['score']:.2f}")
        print(f"   - Environmental Score (0.60 weight): {rec['breakdown']['environmental']:.2f}")
        print(f"   - User Preferences (0.25 weight): {rec['breakdown']['preferences']:.2f}")
        print(f"   - Crowd Optimization (0.15 weight): {rec['breakdown']['crowd']:.2f}")
        print(f"   Details: Vis={site.conditions.water_visibility}m, Diff={site.difficulty}, Crowd={site.crowd_level*100:.0f}%")
        print("-" * 50)

if __name__ == "__main__":
    main()
