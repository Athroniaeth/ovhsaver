import logging
from datetime import datetime
from typing import List

import pytz

from ovhsaver import CONFIG_PATH
from ovhsaver.cloud import get_conn_openstack, handle_server


def main(zone: str = "Europe/Paris", black_list: List[str] = None):
    """
    Main function to handle the OpenStack instances

    Args:
        zone (str): Timezone to use for the script
        black_list (List[str]): List of servers to ignore

    """
    if black_list is None:
        black_list = ["ovhcloud"]

    tz = pytz.timezone(zone)
    today = datetime.now(tz=tz)

    conn = get_conn_openstack(config_path=CONFIG_PATH)

    # Handle all servers in the cloud
    for server in conn.compute.servers():
        if server.name in black_list:
            logging.info(f"Skip server '{server.name}' (blacklisted)")
            continue
        handle_server(server, conn, today=today)
