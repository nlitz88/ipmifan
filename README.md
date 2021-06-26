# ipmifan

## Temporary explanation of the program's current structure:

#### Interface.py
Interface is essentially the gateway to all device data and device control. It provides access to current device readings for devices specified in the devices.yaml configuration file. It also provides controlling access to devices that can be manipulated through tools like ipmitool.

At a high level, interface.py both provides device data and allows devices to be controlled. Eventually this might be implemented as a REST API and split into its own project, as it could be used for a number of other applications.

#### Controller.py
This module is effectively the core of this project, as this module contains all of the logic to actually control the system's fans based on the data provided by interface. This is where all temperature calculations and fan speed decisions are made.

## Potential Future Plans/Ideas
- Make interface a REST API similar to how netdata provides system data.
- Build a basic bootstrap interface to make modifying configuration much easier.
- Add explanation/description of config files.