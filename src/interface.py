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

# To avoid loading every request, initialize Zone and DeviceGroup objects.
# NOTE: that the need for these could be eliminated if someday a database was used.

deviceGroups = []
zones = []

# Instantiate DeviceGroup and Zone objects for those specified in deviceGroupsFile and zonesFile.
# For every device group in the devicegroup config file list, create a new DeviceGroup instance and add it to the list.
for deviceGroup in deviceGroupsFile:
    deviceGroups.append(DeviceGroup(deviceGroup))
for zone in zonesFile:
    zones.append(Zone(zone))

# For every device in devicesFile, add it to to the device list of the DeviceGroup that it has been assigned.
for grouping in devicesFile:
    for device in devicesFile[grouping]:
        if "device_group" not in device:
            device["device_group"] = "default"
        
        if "zone" not in device:
            device["zone"] = "default"
