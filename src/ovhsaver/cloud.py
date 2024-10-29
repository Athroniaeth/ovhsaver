import logging
from datetime import datetime
from os import PathLike
from pathlib import Path
from typing import Union, Literal

from openstack import connection
from openstack.compute.v2.server import Server
from openstack.config import loader
from openstack.connection import Connection

from ovhsaver import logger


def time_to_open(date: datetime) -> bool:
    """
    Return if is online time or not

    Notes:
        it's 'online' time if it's 8h00 - 19h00 (Paris TZ)
        it's offline time if it's 19h00 - 8h00 (Paris TZ)

    """
    hour = date.hour
    is_weekend = date.weekday() in [5, 6]  # Saturday or Sunday

    conditions = (8 <= hour < 19, not is_weekend)

    result = all(conditions)
    logger.info(f"Time Open : {date:%H:%M:%S} - {result}\n")
    return result


def get_conn_openstack(cloud_name: str = "ovhcloud", config_path: Union[str, PathLike] = None) -> Connection:
    """
    Get connection to OpenStack cloud

    Args:
        cloud_name (str): Name of the cloud to connect to
        config_path (Union[str, PathLike]): Path to the clouds.yaml file

    Returns:
        Connection: Connection to OpenStack cloud

    """
    # Parse config path if given
    if config_path is not None:
        config_path = Path(config_path)

        if not config_path.exists():
            raise FileNotFoundError(f"File '{config_path}' not found")

        config_path = f"{config_path}"

    # Load OpenStack configuration from the specified clouds.yaml file
    config = loader.OpenStackConfig(config_files=[config_path])

    # Retrieve the cloud-specific configuration for 'ovhcloud'
    cloud_config = config.get_one_cloud(cloud=cloud_name)

    # Initialize the OpenStack connection using the specified cloud configuration
    conn = connection.Connection(config=cloud_config)

    return conn


def handle_server(
    server: Server,
    conn: Connection,
    today: datetime,
) -> Literal["STARTED", "SHELVED", "NOTHING"]:
    """
    Handle the server to start or suspend it

    Args:
        server (Server): Server to handle
        conn (Connection): Connection to OpenStack cloud
        today (datetime): Current date and time of the server

    """
    must_open = time_to_open(date=today)
    server_is_online = server.status == "ACTIVE"
    logger.info(f"Server '{server.name}' : {server.status}")

    if must_open and not server_is_online:
        logger.info(f"Server '{server.name}' : Starting server '{server.name}'...\n")
        conn.compute.unshelve_server(server.id)
        # conn.compute.wait_for_server(server, status="ACTIVE", failures=["ERROR"], interval=1, wait=360)
        return "STARTED"

    elif not must_open and server_is_online:
        logger.info(f"Server '{server.name}' : Suspending server '{server.name}'...\n")
        conn.compute.shelve_server(server)
        # conn.compute.wait_for_server(server, status="SHELVED", failures=["ERROR"], interval=1, wait=360)
        return "SHELVED"

    else:
        logger.info("Nothing to do\n")
        return "NOTHING"
