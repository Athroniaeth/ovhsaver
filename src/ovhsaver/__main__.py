import logging
import sys
from pathlib import Path

# Automatically add PYTHONPATH to the sys.path
SRC_FOLDER = Path(__file__).parents[1]
sys.path.append(f"{SRC_FOLDER}")

from ovhsaver.script import main  # noqa: E402


if __name__ == "__main__":
    return_code = 0
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

    try:
        main()
    except KeyboardInterrupt:
        logging.error("Script interrupted by user")
    except Exception as exception:
        return_code = 1
        logging.error(f"An error occurred: {exception}")
    finally:
        logging.info("Script ended")

    sys.exit(return_code)
