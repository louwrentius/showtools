# showtools

Assorted Linux targeted python or shell scripts that show system information, such as:

- All network interfaces and some of their propertis
- All storage devices (hdd/sdd) and some of their properties (SMART)

# Showifs

This script shows all interfaces and their status. A screenshot shows you what is shown:

![showifs][1]

As you can see, it shows you the:

* Type of interface
* Link status 
* Associeated IP-address (ipv4 only)
* Hardware address
* Kernel module used
* Firmware version 

[1]: http://louwrentius.com/static/images/showinterfaces01.png

# Showdisks

This script shows information about all storage devices in your system.

The script shows you the:

* Model
* Serial number
* Size (in MB)
* Firmware version
* Storage controller to which the device is connected
* Device path (which may help you identify to which port the storage device is connected)

![showdisks][2]

[2]: http://louwrentius.com/static/images/showdisks01.png

# Showsmart

This script shows all storage devices and some key SMART values that may tell something about the health of the device.

The script shows you:

* The temperature of the device
* How many poweron hours the drive has seen
* How many reallocated sectors it has
* How many pending sectors there are (bad sectors)
* How many CRC errors the device has seen (cable issues)

There may be more indicators included which might be relevant.

[3]: http://louwrentius.com/static/images/showsmart.png