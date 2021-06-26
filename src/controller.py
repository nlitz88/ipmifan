import yaml

devicesFilePath = "devices.yaml"

with open("..\devices.yaml") as f:
    devices = yaml.load(f)

print(devices["disks"][0]["serial_number"])