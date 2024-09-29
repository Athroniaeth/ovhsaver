import logging
from datetime import datetime

import pytz

from ovhsaver import CONFIG_PATH
from ovhsaver.cloud import time_to_open, get_conn_openstack, handle_server

TIME_ZONE = pytz.timezone("Europe/Paris")
TODAY = datetime.now(tz=TIME_ZONE)

if __name__ == "__main__":
    conn = get_conn_openstack(config_path=CONFIG_PATH)
    time_is_online = time_to_open(date=TODAY)
    logging.info(f"{time_is_online=}\n")

    # List the available compute instances
    for server in conn.compute.servers():
        handle_server(server, conn)
