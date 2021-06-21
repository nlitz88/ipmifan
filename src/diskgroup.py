import json

# This class defines a group of disks to be evaluated in determining necessary fan speeds.
class DiskGroup:

    # A diskgroup should be initialized once every time the service is started. This way it doesn't have to keep
    # reading from the json file.

    # If the user adds/modifies disks.json, the simple way to update the ipmifan instance would be to just restart
    # the systemd service.

    # Diskgroups will basically be defined in the disks.json file. A diskgroup json object will be created, and all
    # of its child disks will be defined under it.

    # Will need a constructor function that goes through the disks.json file to extract all disks from there groups and add them to an instance.
    # OR, could define a static factory method that reads through the file and returns an array of DiskGroup objects.

    # Maybe a factory method that grabs the json, and for each json diskgroup object defined, create a new diskgroup object,
    # this constructor would just accept the json, and these instances would just read the serial numbers from the json objects,
    # rather than using raw data structures to avoid complexity.