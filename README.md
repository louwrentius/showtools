# showtools

This tool displays information about disks or network cards in a nice
ASCII table format on the command line. 

- All network interfaces and some of their properties
- All storage devices (hdd/sdd) and some of their properties (SMART)

Examples:

Show information about network interfaces:

![network][0]

[0]: http://louwrentius.com/static/images/shownet.png

Show SMART information about disks:

PS = Pending Sector
RS = Reallocated Sector
RSE = Reallocated Sector Event

![showdisk01][1]

[1]: http://louwrentius.com/static/images/showdisk01.png

Show /dev/disk/by-\* information:

![showdisk02][2]

[2]: http://louwrentius.com/static/images/showdisk02.png

Usage:

    root@nano:~/gold/showtools# ./show
    usage: show [-h] [-a] [-m] [-S] [-s] [-f] [-c] [-p] [-w] [-o] [-t] [-H] [-P]
                [-r] [-R] [-C] [-l] [-4] [-6] [-M] [-T] [-d] [-F]
                {disk,net}
    show: error: too few arguments
    usage: show [-h] [-a] [-m] [-S] [-s] [-f] [-c] [-p] [-w] [-o] [-t] [-H] [-P]
                [-r] [-R] [-C] [-l] [-4] [-6] [-M] [-T] [-d] [-F]
                {disk,net}

    Show detailed disk|net device information in ASCII table format

    positional arguments:
      {disk,net}            Show disk information

    optional arguments:
      -h, --help            show this help message and exit

    Storage (generic):
      Generic options for storage devices

      -a, --all-opts        show all information
      -m, --model           device model
      -S, --serial          device serial number
      -s, --size            device size in Gigabytes
      -f, --firmware        device firmware version
      -c, --controller      controller to which device is connected
      -p, --pcipath         /dev/disk/by-path/ ID of the device
      -w, --wwn             device World Wide Name
      -o, --scsi            /dev/by-id/scsi

    Storage (SMART):
      Options based on SMART values of storage devices

      -t, --temp            temperature in Celcius
      -H, --hours           power on hours
      -P, --pending         pending sector count
      -r, --reallocated     reallocated sector count
      -R, --reallocatedevent
                            reallocated sector event count
      -C, --crc             CRC error

    Network:
      Available options for network devices

      -l, --link            network card link status
      -4, --ipv4            IPv4 address
      -6, --ipv6            IPv6 address
      -M, --mac             hardware / MAC address
      -T, --show-type       network card type
      -d, --driver          driver module
      -F, --firmware-version
                            firmware version

