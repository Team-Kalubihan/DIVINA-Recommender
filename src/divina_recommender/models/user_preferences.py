from dataclasses import dataclass
from typing import List, Optional, Dict, Any

@dataclass
class UserPreferences:
    skill_level: int
    preferred_marine_life: List[str]
    photography_priority: float
    depth_preference: float
    max_travel_distance: float
    # New shop-related preferences
    preferred_price_level: Optional[int] = None
    requires_rental: bool = False
    requires_nitrox: bool = False
    requires_training: bool = False
    is_tech_diver: bool = False

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'UserPreferences':
        return cls(
            skill_level=int(data.get('skill_level', 3)),
            preferred_marine_life=data.get('preferred_marine_life', []),
            photography_priority=float(data.get('photography_priority', 5.0)),
            depth_preference=float(data.get('depth_preference', 20.0)),
            max_travel_distance=float(data.get('max_travel_distance', 100.0)),
            preferred_price_level=data.get('preferred_price_level'),
            requires_rental=bool(data.get('requires_rental', False)),
            requires_nitrox=bool(data.get('requires_nitrox', False)),
            requires_training=bool(data.get('requires_training', False)),
            is_tech_diver=bool(data.get('is_tech_diver', False))
        )
