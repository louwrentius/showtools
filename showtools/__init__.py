# Generates graphs from FIO output data for various IO queue depthts
#
# Output in PNG format.
#
# Requires matplotib and numpy.
#
import sys
from .showlib import (
    processdevice as process,
    displaytable as table,
    disk,
    network,
    argparsing,
)

def get_devices(devicetype):
    lookup = { "disk": disk.get_block_devices,
            "net": network.get_interfaces
        }
    
    devices = lookup[devicetype]()
    return devices

def process_arguments():
    parser = argparsing.set_arguments()
    try:
        args = parser.parse_args()
    except OSError:
        parser.print_help()
        sys.exit(1)

    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)

    return parser, args

def main():
    parser, args = process_arguments()
    processed_args = argparsing.process_argparse_data(parser, args)
    print(processed_args)
    devicetype = processed_args["positional arguments"]["devicetype"]
    devices = get_devices(devicetype)
    devicedata = process.process_devices(processed_args, devicetype, devices)
    #print(devicedata)
    
def throwaway():

    def get_table_header(args):

        header_options = (
            ('type','Type', 'disk','l'),
            ('model', 'Model', 'disk',"l"),
            ('serial', 'Serial Number', 'disk',"l"),
            ('state', 'State', 'disk',"r"),
            ('apm', 'APM', 'disk',"r"),
            ('size', 'GB', 'disk',"r"),
            ('speed', 'Gbps', 'disk',"l"),
            ('firmware', 'Firmware', 'disk',"l"),
            ('controller', 'Controller', 'disk',"l"),
            ('pcipath', '/dev/disk/by-path', 'disk',"l"),
            ('wwn', '/dev/disk/by-id/wwn*', 'disk',"l"),
            ('scsi', '/dev/disk/by-id/scsi*', 'disk',"l"),
            ('temp', 'Temp', 'disk',"r"),
            ('hours', 'Hours', 'disk',"r"),
            ('pending', 'PS', 'disk',"r"),
            ('reallocated', 'RS', 'disk',"r"),
            ('reallocatedevent', 'RSE', 'disk',"r"),
            ('crc', 'CRC', 'disk',"r"),
            ('startstop', 'Spin', 'disk',"r"),
            ('park', 'Park', 'disk',"r"),
            ('link', 'Link', 'net',"r"),
            ('ipv4', 'IPv4', 'net',"r"),
            ('ipv6', 'IPv6', 'net',"r"),
            ('mac', 'MAC', 'net',"r"),
            ('show_type', 'Type', 'net',"r"),
            ('driver', 'Driver', 'net',"r"),
            ('firmware', 'Firmware', 'net',"r"))

        header = ['Dev']

    for option in header_options:
            if option[2] == args.devicetype:
                if args.all_opts or getattr(args, option[0]):
                        if option[2] == args.devicetype:
                            header.append(option[1])

            #print "Header " + str(header)

            return header

    table_data = []
    table_header = get_table_header(args)

    for device in get_devices(devicetype):
        if not device.startswith("md") and not device.startswith("ram") and not device.startswith("loop"):
            devicedata = process.process_device(device, args)
            if devicedata:
                table_data.append(devicedata)

    table.display_table(table_header, table_data, args)
