from dataclasses import dataclass
from typing import List, Dict, Any
import pandas as pd
from .environmental_conditions import EnvironmentalConditions

@dataclass
class DiveSite:
    id: str
    name: str
    conditions: EnvironmentalConditions
    difficulty: int          # 1 to 5
    photography_score: float # 0 to 10
    max_depth: float         # meters
    marine_life: List[str]
    distance_km: float
    crowd_level: float       # 0 to 1

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'DiveSite':
        """
        Creates a DiveSite from a dictionary. 
        Works for both flat CSV rows and nested JSON objects.
        """
        def safe_float(val, default):
            try:
                if val is None or (isinstance(val, float) and pd.isna(val)): return float(default)
                return float(val)
            except:
                return float(default)

        def safe_int(val, default):
            try:
                if val is None or (isinstance(val, float) and pd.isna(val)): return int(default)
                return int(val)
            except:
                return int(default)

        # Handle potential nested JSON structure for conditions
        cond_data = data.get('conditions', data) 
        
        cond = EnvironmentalConditions(
            water_visibility=safe_float(cond_data.get('water_visibility'), 10),
            wave_height=safe_float(cond_data.get('wave_height'), 1),
            current_speed=safe_float(cond_data.get('current_speed'), 0.5),
            wind_speed=safe_float(cond_data.get('wind_speed'), 10),
            water_temperature=safe_float(cond_data.get('water_temperature'), 20),
            rain_probability=safe_float(cond_data.get('rain_probability'), 0),
            marine_biodiversity=safe_float(cond_data.get('marine_biodiversity'), 5)
        )

        # Handle marine_life as list or comma-separated string
        ml = data.get('marine_life', [])
        if isinstance(ml, str):
            ml = [x.strip() for x in ml.split(',') if x.strip()]

        return cls(
            id=str(data.get('id', '0')),
            name=data.get('name', 'Unknown Site'),
            conditions=cond,
            difficulty=safe_int(data.get('difficulty'), 3),
            photography_score=safe_float(data.get('photography_score'), 5),
            max_depth=safe_float(data.get('max_depth'), 20),
            marine_life=ml,
            distance_km=safe_float(data.get('distance_km'), 50),
            crowd_level=safe_float(data.get('crowd_level'), 0.5)
        )
