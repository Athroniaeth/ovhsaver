import sys
from datetime import datetime
from pathlib import Path

import pytz

# Automatically add PYTHONPATH to the sys.path
SRC_FOLDER = Path(__file__).parents[1]
sys.path.append(f"{SRC_FOLDER}")

from ovhsaver import CONFIG_PATH  # noqa: E402
from ovhsaver.cloud import get_conn_openstack, handle_server  # noqa: E402


if __name__ == "__main__":
    tz = pytz.timezone("Europe/Paris")
    today = datetime.now(tz=tz)

    conn = get_conn_openstack(config_path=CONFIG_PATH)

    # List the available compute instances
    for server in conn.compute.servers():
        handle_server(server, conn, today=today)
