import pandas as pd
from src.divina_recommender.models import DiveSite, UserPreferences, EnvironmentalConditions, DiveShop
from src.divina_recommender.engine import RecommenderEngine

def load_sites_from_csv(file_path: str):
    df = pd.read_csv(file_path)
    return [DiveSite.from_dict(row.to_dict()) for _, row in df.iterrows()]

def load_shops_from_csv(file_path: str):
    df = pd.read_csv(file_path)
    shops = []
    for _, row in df.iterrows():
        data = row.to_dict()
        if isinstance(data.get('dive_sites'), str):
            data['dive_sites'] = [x.strip() for x in data['dive_sites'].split(',') if x.strip()]
        shops.append(DiveShop.from_dict(data))
    return shops

def main():
    # 1. Initialize Engine
    engine = RecommenderEngine()

    # 2. Load Data from CSV
    try:
        sites = load_sites_from_csv("data/sites.csv")
        shops = load_shops_from_csv("data/shops.csv")
    except Exception as e:
        print(f"Error loading data: {e}")
        return

    # 3. Define User Preferences
    user = UserPreferences(
        skill_level=3,
        preferred_marine_life=["Manta Ray", "Turtle"],
        photography_priority=9.5,
        depth_preference=15.0,
        max_travel_distance=100.0,
        requires_rental=True,
        preferred_price_level=2
    )

    # 4. Get Site Recommendations
    site_recs = engine.recommend(sites, user)

    # 5. Print Site Results
    print("\n--- DIVINA Dive Site Recommendations ---")
    print(f"User Preferences: Skill={user.skill_level}, Targets={user.preferred_marine_life}, Depth={user.depth_preference}m\n")
    
    for i, rec in enumerate(site_recs[:5], 1):
        print(f"{i}. {rec['site_name']} (ID: {rec['site_id']})")
        print(f"   Overall Score: {rec['total_score']:.2f}")
        print(f"   - Environmental Score: {rec['breakdown']['environmental']:.2f}")
        print(f"   - User Preferences: {rec['breakdown']['user_preferences']:.2f}")
        print(f"   - Crowd Optimization: {rec['breakdown']['crowd_optimization']:.2f}")
        print("-" * 40)

    # 6. Get Shop Recommendations
    shop_recs = engine.recommend_shops(shops, user, sites)

    # 7. Print Shop Results
    print("\n--- DIVINA Dive Shop Recommendations ---")
    for i, rec in enumerate(shop_recs, 1):
        print(f"{i}. {rec['shop_name']} (ID: {rec['shop_id']})")
        print(f"   Overall Score: {rec['total_score']:.2f}")
        print("-" * 40)

if __name__ == "__main__":
    main()
