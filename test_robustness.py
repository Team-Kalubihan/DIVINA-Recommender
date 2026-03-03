import pandas as pd
from src.divina_recommender.models import DiveSite, UserPreferences
from src.divina_recommender.engine import RecommenderEngine
import io

def test_missing_column():
    # CSV with 'water_visibility' and 'difficulty' columns missing
    csv_data = """id,name,wave_height,current_speed,wind_speed,water_temperature,rain_probability,marine_biodiversity,photography_score,max_depth,marine_life,distance_km,crowd_level
1,Test Site,0.5,0.2,5.0,24.0,0.1,9.0,8.5,18.0,"Turtle",15.0,0.3
"""
    df = pd.read_csv(io.StringIO(csv_data))
    sites = [DiveSite.from_dict(row.to_dict()) for _, row in df.iterrows()]
    
    engine = RecommenderEngine()
    user = UserPreferences(3, ["Turtle"], 5.0, 20.0, 100.0)
    
    print(f"Testing missing 'water_visibility' and 'difficulty'...")
    recs = engine.recommend(sites, user)
    print(f"Success! Site: {recs[0]['site'].name}, Visibility: {recs[0]['site'].conditions.water_visibility}, Difficulty: {recs[0]['site'].difficulty}")

def test_null_values():
    # CSV with a NULL (NaN) value in current_speed
    csv_data = """id,name,water_visibility,wave_height,current_speed,wind_speed,water_temperature,rain_probability,marine_biodiversity,difficulty,photography_score,max_depth,marine_life,distance_km,crowd_level
1,Null Site,20,0.5,,5.0,24.0,0.1,9.0,2,8.5,18.0,"Turtle",15.0,0.3
"""
    df = pd.read_csv(io.StringIO(csv_data))
    print(f"\nTesting NULL value in 'current_speed'...")
    try:
        sites = [DiveSite.from_dict(row.to_dict()) for _, row in df.iterrows()]
        engine = RecommenderEngine()
        user = UserPreferences(3, ["Turtle"], 5.0, 20.0, 100.0)
        recs = engine.recommend(sites, user)
        print(f"Resulting current_speed: {recs[0]['site'].conditions.current_speed}")
        print(f"Overall Score: {recs[0]['score']}")
    except Exception as e:
        print(f"Failed as expected or unexpected: {type(e).__name__}: {e}")

if __name__ == "__main__":
    test_missing_column()
    test_null_values()
