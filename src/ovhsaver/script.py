from datetime import datetime
from typing import List

import pytz

from ovhsaver import CONFIG_PATH, logger
from ovhsaver.cloud import get_conn_openstack, handle_server


def main(zone: str = "Europe/Paris", black_list: List[str] = None):
    """
    Main function to handle the OpenStack instances

    Args:
        zone (str): Timezone to use for the script
        black_list (List[str]): List of servers to ignore

    """
    if black_list is None:
        black_list = ["ovhsaver", "pipeforms"]

    tz = pytz.timezone(zone)
    today = datetime.now(tz=tz)
    conn = get_conn_openstack(config_path=CONFIG_PATH)

    # Handle all servers in the cloud
    for server in conn.compute.servers():
        # L4 is GPU server, we don't want to touch it
        # Also, we don't want to touch the servers in the black list
        condition = (
            server.name.startswith("l4"),
            server.name in black_list
        )

        if any(condition):
            logger.info(f"Skip server '{server.name}' (blacklisted)\n")
            continue

        handle_server(server, conn, today=today)
