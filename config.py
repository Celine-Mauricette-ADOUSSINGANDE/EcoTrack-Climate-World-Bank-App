import os
import logging
from dotenv import load_dotenv

load_dotenv()

# Logger configuration
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("ClimateApp")

# API Config
WB_API_URL = os.getenv("WB_API_BASE_URL", "https://api.worldbank.org/v2")
CACHE_EXPIRY = int(os.getenv("CACHE_EXPIRY_DAYS", 7))
API_KEY = os.getenv("CLIMATE_API_KEY") # Au cas où vous ajouteriez OpenWeather plus tard