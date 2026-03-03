from dataclasses import dataclass
from typing import List, Dict, Any

@dataclass
class DiveShop:
    id: str
    name: str
    rating: float            # 0 to 5
    price_level: int         # 1 to 4 ($ to $$$$)
    has_rental: bool
    has_nitrox: bool
    has_training: bool
    is_tech_friendly: bool
    dive_sites: List[str]    # IDs of dive sites they visit
    distance_km: float

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'DiveShop':
        def safe_bool(val):
            if isinstance(val, bool): return val
            if isinstance(val, str): return val.lower() in ('true', '1', 'yes')
            return bool(val)

        return cls(
            id=str(data.get('id', '0')),
            name=data.get('name', 'Unknown Shop'),
            rating=float(data.get('rating', 4.0)),
            price_level=int(data.get('price_level', 2)),
            has_rental=safe_bool(data.get('has_rental', True)),
            has_nitrox=safe_bool(data.get('has_nitrox', False)),
            has_training=safe_bool(data.get('has_training', True)),
            is_tech_friendly=safe_bool(data.get('is_tech_friendly', False)),
            dive_sites=data.get('dive_sites', []),
            distance_km=float(data.get('distance_km', 50.0))
        )
