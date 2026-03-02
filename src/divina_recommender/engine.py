from typing import List, Dict, Optional, Any
from .models import DiveSite, UserPreferences, EnvironmentalConditions

class RecommenderEngine:
    """
    Core Recommendation Engine for DIVINA.
    It is data-source agnostic and operates on DiveSite and UserPreferences objects.
    """
    
    # Default Weights from the specification
    DEFAULT_WEIGHTS = {
        "environmental": {
            "water_visibility": 0.18,
            "wave_height": 0.12,
            "current_speed": 0.10,
            "wind_speed": 0.07,
            "water_temperature": 0.05,
            "rain_probability": 0.04,
            "marine_biodiversity": 0.04
        },
        "user_preferences": {
            "preferred_marine_life": 0.07,
            "dive_difficulty_match": 0.06,
            "photography_friendly": 0.05,
            "depth_preference": 0.04,
            "travel_distance": 0.03
        },
        "crowd_optimization": {
            "crowd_level": 0.15
        }
    }

    def __init__(self, custom_weights: Optional[Dict[str, Any]] = None):
        """
        Initialize the engine with optional custom weights.
        """
        self.weights = custom_weights or self.DEFAULT_WEIGHTS
        
        # Normalization ranges (could also be made configurable)
        self.config = {
            "max_visibility": 30.0,
            "max_wave_height": 5.0,
            "max_current_speed": 5.0,
            "max_wind_speed": 40.0,
            "max_temp": 35.0,
            "min_temp": 10.0,
        }

    def _normalize(self, val: float, min_val: float, max_val: float, reverse: bool = False) -> float:
        norm = (val - min_val) / (max_val - min_val) if max_val != min_val else 0.5
        norm = max(0.0, min(1.0, norm))
        return 1.0 - norm if reverse else norm

    def calculate_environmental_score(self, site: DiveSite) -> float:
        cond = site.conditions
        w = self.weights["environmental"]
        c = self.config
        
        score = (
            self._normalize(cond.water_visibility, 0, c["max_visibility"]) * w["water_visibility"] +
            self._normalize(cond.wave_height, 0, c["max_wave_height"], reverse=True) * w["wave_height"] +
            self._normalize(cond.current_speed, 0, c["max_current_speed"], reverse=True) * w["current_speed"] +
            self._normalize(cond.wind_speed, 0, c["max_wind_speed"], reverse=True) * w["wind_speed"] +
            self._normalize(cond.water_temperature, c["min_temp"], c["max_temp"]) * w["water_temperature"] +
            self._normalize(cond.rain_probability, 0, 1.0, reverse=True) * w["rain_probability"] +
            self._normalize(cond.marine_biodiversity, 0, 10.0) * w["marine_biodiversity"]
        )
        return score / 0.60

    def calculate_preference_score(self, site: DiveSite, user: UserPreferences) -> float:
        w = self.weights["user_preferences"]
        
        # Marine Life Match
        ml_score = 0.0
        if user.preferred_marine_life:
            matches = set(site.marine_life).intersection(set(user.preferred_marine_life))
            ml_score = len(matches) / len(user.preferred_marine_life)
        
        # Difficulty Match
        diff_score = 1.0 - (abs(site.difficulty - user.skill_level) / 4.0)
        if user.skill_level < site.difficulty:
            diff_score *= 0.5 
            
        # Photography
        photo_score = self._normalize(site.photography_score, 0, 10.0)
        
        # Depth
        depth_score = 1.0 - (min(abs(site.max_depth - user.depth_preference), user.depth_preference) / user.depth_preference) if user.depth_preference > 0 else 1.0
        
        # Distance
        dist_score = self._normalize(site.distance_km, 0, user.max_travel_distance, reverse=True)

        score = (
            ml_score * w["preferred_marine_life"] +
            diff_score * w["dive_difficulty_match"] +
            photo_score * w["photography_friendly"] +
            depth_score * w["depth_preference"] +
            dist_score * w["travel_distance"]
        )
        return score / 0.25

    def calculate_crowd_score(self, site: DiveSite) -> float:
        w = self.weights["crowd_optimization"]
        return (1.0 - site.crowd_level) * w["crowd_level"] / 0.15

    def recommend(self, sites: List[DiveSite], user: UserPreferences) -> List[Dict[str, Any]]:
        """
        Ranks a list of DiveSite objects for a given User.
        """
        results = []
        for site in sites:
            env = self.calculate_environmental_score(site)
            pref = self.calculate_preference_score(site, user)
            crowd = self.calculate_crowd_score(site)
            
            total_score = (env * 0.60) + (pref * 0.25) + (crowd * 0.15)
            
            results.append({
                "site_id": site.id,
                "site_name": site.name,
                "total_score": round(total_score, 4),
                "breakdown": {
                    "environmental": round(env, 4),
                    "user_preferences": round(pref, 4),
                    "crowd_optimization": round(crowd, 4)
                }
            })
        
        return sorted(results, key=lambda x: x["total_score"], reverse=True)

    def recommend_from_data(self, sites_data: List[Dict], user_data: Dict) -> List[Dict]:
        """
        Helper method to process raw dictionaries (e.g. from a JSON API).
        """
        sites = [DiveSite.from_dict(s) for s in sites_data]
        user = UserPreferences.from_dict(user_data)
        return self.recommend(sites, user)
