
class DeviceGroup:

    def __init__(self, name):
        self.name = name
        self.devices = []

    def addDevice(self, newDevice):
        self.devices.append(newDevice)

# Just thinking through how I want the program to work.    

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

    # Would it be practical to instead generalize this?
    # I.e., make a devices.json file where all devices are defined.
    # A disk group is defined with temperature thresholds, etc.

    # Here's another idea:
    #  While I think that recording temperature data should be easy enough, it would be nice to have these endpoints made available to me in
    # case I'd ever want to record them in something like prometheus. Soooo, while I could build out a little flask application that would serve up temperature data,
    # and build adapters for different data providers (that work via the command line), might just be easier to set that up with netdata.
    # THEN, just build out a fan controller script that uses that data to control the script.

    # The only reason that this is a little scary is because it depends on a large application like netdata running. Now granted, if I'm building up my own
    # shaky service, you could make that same argument, but the controller script could always just default to MAX fan values if it can't contact it's data provider.
    
    # Maybe that's what I can do: I can build out a data provider that collects data for all of the devices that you want to keep track of. So, here's how it's laid out:
    
    # Data Provider Microservice
    #   - Data provider flask application that serves up json sensor data for various devices.
    #   - Data provider will have no knowledge of the actual machine it's on, it'll just execute commands to get sensor data.
    #   - The Data provider will NOT have hard-coded cli commands to get sensor data, but will rather have various PROVIDER-ADAPTERS (json files)
    #     that will specificy a command to be run in order to get the type of data that they're meant for.
    #           - In a more advanced application, they coulld also provide meta-data about the data they're returning. These could be interpretted by the controller/receiver
    #             based on how they're being used.
    #     This way, when the controller script requests data, it will send the provider service a json request that will specify the type of provider to use.
    #     This endpoint will then grab the command from the corresponding provider-adapter specified in the GET request and will return the data provided by the specified command.
    #           - In a more (advanced) netdata-style implementation, it would also be cool to have an endpoint that enables the tracking of certain devices (that the consumer program (like ipmifan))
    #           data in something like a mongo database. This way, there would be more uniform access to both current and past readings.


    # ------------------------------------
    # OR, MOST SIMPLY: DataProviderSource object entries added to a "source.json" file. Basically, these entries would just maintain the commands needed to return the desired data.
    # Then, the controller just has to hit a generic endpoint on the provider where they specify the name of the Source entry, and they get the data from the commands of that entry back.
    # OR, the controller requests data (with the commands as the GET json), and then the provider returns the results. Again, not sure which is better.
    # ------------------------------------

    # THIS COULD ALSO BE IMPLEMENTED AS AN MQTT application where these values are published on topics. OR some data-providers could just constantly broadcast their responses over mqtt as well.

    # IPMI-FAN controller Microservice
    #   - This service will just implement the logic outlined in my notebook regarding how to set fan speeds, but ultimately at that point will just be
    #     a primitive consumer of the data from the Data Provider Microservice.
    #   - This could just be one of many services that get their data from the provider microservice. 
    #   - Long term, it would be nice to implement modules that define the same functions for retrieving the sensor data that they need, but just from different sources.
    #   - In other words, define a "DataSource" interface that is unique to this controller application that requires the classes to implement methods for retrieving
    #     (in the same format) hdd temps, cpu temps, ambient temps, etc., etc.
    #   - Based on some configurable value (maybe in a yaml file along with other options), this controller can just instantiate a data-provider according to where
    #     it's getting its data from.
    # 
    #   - Additionally, this program will have a devices.json file that specifies all of the different disk groups, cpus, sensors, etc. that the user wishes to monitor
    #     temperatures of--in this case to control fan speeds. 






# device_types.json will contain various types of devices and the general form of the commands needed to extract the data from them.
#   Will also include a device type "custom" that will accept custom commands in case it requires specialized commands due to some issue.]
#   I may also include 
# devices.json will contain actual device definitions that allow the user to specify the actual devices (and any relevant details needed).

# Upon initialization, the data provider will take the devices specified in devices.json and load them into a dictionary.
# Subsequently, it will match the serial numbers of the drives to their current /dev/ location and store that in a new dictionary field it creates.


# Some vocabulary for the system:
#       device_group: A device group defines the group of devices whose temperatures are all factored in to calculate the overall temperature / state of that group.
#            - This is useful, for instanace, for a group of hard drives, as you might not want to just look at the temperature of each drive all the time,
#               (assuming no extreme conditions for one device) but rather just the overall state of that group.
#
#       zone: A zone is what device_groups and devices are assigned to that fans control the temperature of. Fans, for instance, are assigned to a particular zone.
#             The fans that are assigned to a particular zone then are controlled according to the temperatures/states of the device_groups that have been
#             assigned to that zone.
#             Zones exist because, while you could assign fans to multiple device groups, you don't necessarily want the desired fan speed required for one
#             device group (say CPUs) to fight over the fan control.
#             While I could implement some logic to just take the highest fan speed calculated across the device_groups, I think it would be cleaner to loop through
#             zones and set the fans in that zone.
#             Still more efficient though to calculate all of the device_groups temps/state all in a row, as if you do it by zone, in theory a device_group could
#             be assigned to multiple zones, so you'd be calculating it unecessarily more than once.