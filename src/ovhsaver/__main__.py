import os

from openstack import connection
from openstack.config import loader

from src.ovhsaver import CONFIG_PATH

# Load OpenStack configuration from the specified clouds.yaml file
config = loader.OpenStackConfig(config_files=[f'{CONFIG_PATH}'])

# Retrieve the cloud-specific configuration for 'ovhcloud'
cloud_config = config.get_one_cloud(cloud='ovhcloud')

# Initialize the OpenStack connection using the specified cloud configuration
conn = connection.Connection(config=cloud_config)

# List the available compute instances
for server in conn.compute.servers():
    print(server)
