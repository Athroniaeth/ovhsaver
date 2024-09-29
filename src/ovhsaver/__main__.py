from datetime import datetime, tzinfo

import pytz
from openstack import connection
from openstack.config import loader

from src.ovhsaver import CONFIG_PATH


def time_to_open(date: datetime) -> bool:
    """
    Return if is online time or not

    Notes:
        it's 'online' time if it's 8h00 - 19h00 (Paris TZ)
        it's offline time if it's 19h00 - 8h00 (Paris TZ)
    """
    hour = date.hour
    is_weekend = date.weekday() in [5, 6]  # Saturday or Sunday

    conditions = (
        8 <= hour < 19,
        not is_weekend
    )

    result = all(conditions)
    print(f"{hour=} ; {is_weekend=}")
    return result


if __name__ == "__main__":
    TIME_ZONE = pytz.timezone("Europe/Paris")
    TODAY = datetime.now(tz=TIME_ZONE)

    # Load OpenStack configuration from the specified clouds.yaml file
    config = loader.OpenStackConfig(config_files=[f'{CONFIG_PATH}'])

    # Retrieve the cloud-specific configuration for 'ovhcloud'
    cloud_config = config.get_one_cloud(cloud='ovhcloud')

    # Initialize the OpenStack connection using the specified cloud configuration
    conn = connection.Connection(config=cloud_config)

    time_is_online = time_to_open(date=TODAY)
    print(f"{time_is_online=}\n")

    # List the available compute instances
    for _server in conn.compute.servers():
        server = conn.compute.get_server(_server.id)
        server_is_online = (server.status == 'ACTIVE')

        print(f"Server '{server.name}' is {"'online'" if server_is_online else "'offline'"}")

        if time_is_online and not server_is_online:
            print(f'\tStarting server {server.name}...')
            # conn.compute.start_server(server.id)
            # conn.compute.wait_for_server(server, status='ACTIVE', failures=['ERROR'], interval=60, wait=360)

        elif not time_is_online and server_is_online:
            print(f'\tStopping server {server.name}...')
            # conn.compute.stop_server(server)
            # conn.compute.wait_for_server(server, status='SHUTOFF', failures=['ERROR'], interval=60, wait=360)

        else:
            print("Nothing to do")

        print()
