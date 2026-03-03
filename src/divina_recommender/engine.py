from typing import List, Dict, Optional, Any
from .models import DiveSite, UserPreferences, EnvironmentalConditions, DiveShop

class RecommenderEngine:
    """
    Core Recommendation Engine for DIVINA.
    It is data-source agnostic and operates on DiveSite, UserPreferences, and DiveShop objects.
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
        },
        "dive_shop": {
            "service_match": 0.30,
            "site_match": 0.30,
            "rating": 0.20,
            "price_match": 0.10,
            "distance": 0.10
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

    def calculate_shop_score(self, shop: DiveShop, user: UserPreferences, sites: List[DiveSite]) -> float:
        w = self.weights["dive_shop"]
        
        # Service Match
        service_score = 1.0
        if user.requires_rental and not shop.has_rental: service_score *= 0.2
        if user.requires_nitrox and not shop.has_nitrox: service_score *= 0.2
        if user.requires_training and not shop.has_training: service_score *= 0.5
        if user.is_tech_diver and not shop.is_tech_friendly: service_score *= 0.3
        
        # Site Match: Average site score for this shop
        shop_sites = [s for s in sites if s.id in shop.dive_sites]
        if not shop_sites:
            site_match_score = 0.5
        else:
            site_scores = []
            for site in shop_sites:
                env = self.calculate_environmental_score(site)
                pref = self.calculate_preference_score(site, user)
                crowd = self.calculate_crowd_score(site)
                site_scores.append((env * 0.60) + (pref * 0.25) + (crowd * 0.15))
            site_match_score = sum(site_scores) / len(site_scores)
            
        # Rating
        rating_score = self._normalize(shop.rating, 0, 5.0)
        
        # Price Match
        price_match_score = 1.0
        if user.preferred_price_level:
            price_match_score = 1.0 - (abs(shop.price_level - user.preferred_price_level) / 3.0)
            
        # Distance
        dist_score = self._normalize(shop.distance_km, 0, user.max_travel_distance, reverse=True)
        
        total_shop_score = (
            service_score * w["service_match"] +
            site_match_score * w["site_match"] +
            rating_score * w["rating"] +
            price_match_score * w["price_match"] +
            dist_score * w["distance"]
        )
        return total_shop_score

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

    def recommend_shops(self, shops: List[DiveShop], user: UserPreferences, sites: List[DiveSite]) -> List[Dict[str, Any]]:
        """
        Ranks a list of DiveShop objects for a given User.
        """
        results = []
        for shop in shops:
            score = self.calculate_shop_score(shop, user, sites)
            results.append({
                "shop_id": shop.id,
                "shop_name": shop.name,
                "total_score": round(score, 4)
            })
        return sorted(results, key=lambda x: x["total_score"], reverse=True)

    def recommend_from_data(self, sites_data: List[Dict], user_data: Dict) -> List[Dict]:
        """
        Helper method to process raw dictionaries (e.g. from a JSON API).
        """
        sites = [DiveSite.from_dict(s) for s in sites_data]
        user = UserPreferences.from_dict(user_data)
        return self.recommend(sites, user)
