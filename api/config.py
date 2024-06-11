import os
from pathlib import Path

MODELS_ROOT_PATH = str(Path(__file__).parent.parent / "api" / "models")
ENCODERS_ROOT_PATH = str(Path(__file__).parent.parent / "api" / "encoders")

os.makedirs(MODELS_ROOT_PATH, exist_ok=True)
os.makedirs(ENCODERS_ROOT_PATH, exist_ok=True)
AVERAGE_SPEED_PER_HOURS = str(Path(__file__).parent / "valores_unicos_average_speed_per_hour.json")
TRIPS_PER_HOURS = str(Path(__file__).parent / "valores_unicos_trips_per_hour.json")