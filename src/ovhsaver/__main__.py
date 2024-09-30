from datetime import datetime

import pytz

from ovhsaver import CONFIG_PATH
from ovhsaver.cloud import get_conn_openstack, handle_server


if __name__ == "__main__":
    tz = pytz.timezone("Europe/Paris")
    today = datetime.now(tz=tz)

    conn = get_conn_openstack(config_path=CONFIG_PATH)

    # List the available compute instances
    for server in conn.compute.servers():
        handle_server(server, conn, today=today)
