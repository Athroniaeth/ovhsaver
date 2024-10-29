import sys
from pathlib import Path

# Automatically add PYTHONPATH to the sys.path
SRC_FOLDER = Path(__file__).parents[1]
sys.path.append(f"{SRC_FOLDER}")

from ovhsaver import logger  # noqa: E402
from ovhsaver.script import main  # noqa: E402

if __name__ == "__main__":
    return_code = 0

    try:
        main()
    except KeyboardInterrupt:
        logger.error("Script interrupted by user")
    except Exception as exception:
        return_code = 1
        logger.error(f"An error occurred: {exception}")
    finally:
        logger.info("Script ended")

    sys.exit(return_code)
