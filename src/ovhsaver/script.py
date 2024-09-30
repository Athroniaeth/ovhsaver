from datetime import datetime

import pytz

from ovhsaver import CONFIG_PATH
from ovhsaver.cloud import get_conn_openstack, handle_server


def main(zone: str = "Europe/Paris"):
    """
    Main function to handle the OpenStack instances

    Args:
        zone (str): Timezone to use for the script

    """
    tz = pytz.timezone(zone)
    today = datetime.now(tz=tz)

    conn = get_conn_openstack(config_path=CONFIG_PATH)

    # List the available compute instances
    for server in conn.compute.servers():
        handle_server(server, conn, today=today)
