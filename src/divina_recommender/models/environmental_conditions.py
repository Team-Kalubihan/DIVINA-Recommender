from dataclasses import dataclass

@dataclass
class EnvironmentalConditions:
    water_visibility: float  # meters
    wave_height: float       # meters
    current_speed: float     # knots
    wind_speed: float        # knots
    water_temperature: float # Celsius
    rain_probability: float  # 0 to 1
    marine_biodiversity: float # 0 to 10 score
