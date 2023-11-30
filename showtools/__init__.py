import sys
from rich import print as print
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
    #print(processed_args)
    devicetype = processed_args["positional arguments"]["devicetype"]
    devices = get_devices(devicetype)
    devicedata = process.process_devices(processed_args, devicetype, devices)
    #print(devicedata)
    table.display(devicedata, processed_args)
    
