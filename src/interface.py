import yaml
from subprocess import PIPE, run

# Specify path to configuration files.
devicesFilePath = "../conf/devices.yaml"
deviceTypeConfigFilePath = "../conf/device_type_config.yaml"

# Load configuration files as dictionaries.
with open(devicesFilePath) as f:
    devices = yaml.load(f)

with open(deviceTypeConfigFilePath) as f:
    deviceTypeConfigs = yaml.load(f)

# To avoid loading every request, initialize Zone and Diskgroup objects.
# Note that the need for these could be eliminated if someday a database was used.

diskGroups = []
zones = []


# Map drives by serial numbers to their current name (/dev/sd*). Add this key to the devices dictionary.
testOutput = subprocess.run("lsblk -o NAME,SERIAL", capture_output=True)
print(testOutput)

# first, grab the output of lsblk with serial and name listed.

# Go through this output in the for loop below and add the mountpoint to the dictionary.

for device in devices["disks"]:
    
    print(device["serial_number"])

# initialize DiskGroup objects

# print(devices["disks"][0]["serial_number"])