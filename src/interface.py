import yaml
from subprocess import check_output
from devicegroup import DeviceGroup
from zone import Zone

# Specify path to configuration files.
# TODO: Make a general program configuration file and specify a /conf directory location where all can be located.
devicesFilePath = "/home/nlitz88/ipmifan/conf/devices.yaml"
deviceTypeConfigFilePath = "/home/nlitz88/ipmifan/conf/device_type_config.yaml"
deviceGroupsFilePath = "/home/nlitz88/ipmifan/conf/devicegroups.yaml"
zonesFilePath = "/home/nlitz88/ipmifan/conf/zones.yaml"

# Load configuration files as dictionaries.
with open(devicesFilePath) as f:
    devicesFile = yaml.safe_load(f)

with open(deviceTypeConfigFilePath) as f:
    deviceTypeConfigs = yaml.safe_load(f)

with open(deviceGroupsFilePath) as f:
    deviceGroupsFile = yaml.safe_load(f)

with open(zonesFilePath) as f:
    zonesFile = yaml.safe_load(f)

# Map drives by serial numbers to their current name (/dev/sd*). Add this key to the devices dictionary.
# NOTE: Might consider implementing this in a way that is more generic across different device types.
#       Could just be specificly for drives, but what if needed for PCIE devices, for instance?
#       Maybe custom python modules could be an option for this just to keep it out of the main file.
for device in devicesFile["disks"]:
    diskSerial = device["serial_number"]
    devLocation = check_output(["lsblk -o NAME,SERIAL | grep %s | cut -c 1-3" % diskSerial], shell=True, universal_newlines=True)
    device["devLocation"] = "/dev/" + str(devLocation).rstrip()

# To avoid loading every request, initialize Zone and DeviceGroup dictionaries.
# NOTE: that the need for these could be eliminated if someday a database was used.

deviceGroups = {}
zones = {}

# For each entry in devicegroups.yaml, create a new dict
for deviceGroup in deviceGroupsFile:
    # Create new key for devicegroup, whose value is an array of device dictionary objects.
    deviceGroups[deviceGroup] = []
for zone in zonesFile:
    # Create new key for zone, whose value is an array of devicegroup dictionary objects.
    zones[zone] = []

# For every device in devicesFile, add it to to the device list of the DeviceGroup that it has been assigned.
for grouping in devicesFile:
    for device in devicesFile[grouping]:
        if "device_group" not in device:
            device["device_group"] = "default"
        deviceGroups[device["device_group"]].append(device)
    
for deviceGroup in deviceGroupsFile:
    # TODO: Consider adding support for assigning a deviceGroup to multiple zones.
    if "zone" not in deviceGroup:
        deviceGroup["zone"] = "default"
    zones[deviceGroup["zone"]].append(deviceGroup)
