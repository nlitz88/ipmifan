import yaml
from subprocess import check_output

# Specify path to configuration files.
devicesFilePath = "/home/nlitz88/ipmifan/conf/devices.yaml"
deviceTypeConfigFilePath = "/home/nlitz88/ipmifan/conf/device_type_config.yaml"

# Load configuration files as dictionaries.
with open(devicesFilePath) as f:
    devices = yaml.safe_load(f)

with open(deviceTypeConfigFilePath) as f:
    deviceTypeConfigs = yaml.safe_load(f)

# To avoid loading every request, initialize Zone and Diskgroup objects.
# Note that the need for these could be eliminated if someday a database was used.

diskGroups = []
zones = []


# Map drives by serial numbers to their current name (/dev/sd*). Add this key to the devices dictionary.
for device in devices["disks"]:
    diskSerial = device["serial_number"]
    devLocation = check_output(["lsblk -o NAME,SERIAL | grep %s | cut -c 1-3" % diskSerial], shell=True, universal_newlines=True)
    device["devLocation"] = "/dev/" + str(devLocation).rstrip()



# initialize DiskGroup objects

# print(devices["disks"][0]["serial_number"])