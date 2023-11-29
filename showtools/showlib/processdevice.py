
from rich import print as print
from . import (
    network,
    disk
)

def get_function_lookup_table():
    
    table = {
        "disk": disk.get_disk_device_data,
        "net": network.get_network_device_data
    }
    return table

def process_devices(args, devicetype, devices):
    devicedata = []
    lookuptable = get_function_lookup_table()
    for device in devices:
        devicedata.append(lookuptable[devicetype](device, args))
    return devicedata
   

