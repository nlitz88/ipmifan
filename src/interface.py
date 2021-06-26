import yaml

# Specify path to configuration files.
devicesFilePath = "../devices.yaml"
deviceTypeConfigFilePath = "../device_type_config.yaml"

# Load configuration files as dictionaries.
with open(devicesFilePath) as f:
    devices = yaml.load(f)

with open(deviceTypeConfigFilePath) as f:
    deviceTypeConfigs = yaml.load(f)


print(devices["disks"][0]["serial_number"])