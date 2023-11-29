from . import (
    netlookup
)

def get_net_devices():
    netdevices = open('/proc/net/dev',  'r').readlines()
    return netdevices

def get_interfaces():
    interfaces = []
    devices = get_net_devices()
    for line in devices[2:]:
        data = line.split(':')
        interfaces.append(data[0].strip())
        interfaces.sort()
    return interfaces

def process_lookup(lookup, args):
    devicedata = {}
    for k, v in lookup.items():
        addoption = False
        if args["generic_settings"]["all_opts"]: 
            addoption = True
        elif k in args["network"].keys():
            addoption = True
        if addoption:
            devicedata[k] = v
    return devicedata

def get_network_device_data(dev, args):
    lookup = netlookup.device_options_table(dev)
    devicedata = process_lookup(lookup, args)
    return devicedata


