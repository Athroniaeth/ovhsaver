import logging
from pathlib import Path

# Globals project paths
SRC_PATH = Path(__file__).parents[2]

# Custom project paths
CONFIG_PATH = SRC_PATH / "clouds.yaml"

# Logger configuration
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger("ovhsaver")
logger.setLevel(logging.INFO)
