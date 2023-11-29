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

def process_lookup(lookup, args, dev):
    devicedata = { "device": { "value": dev, "justify": "left"}}
    for k, v in lookup.items():
        addoption = False
        if "all_opts" in args["generic_settings"].keys(): 
            addoption = True
        elif k in args["network"].keys():
            addoption = True
        if addoption:
            devicedata[k] = v
    return devicedata

def get_network_device_data(dev, args):
    lookup = netlookup.device_options_table(dev)
    devicedata = process_lookup(lookup, args, dev)
    return devicedata


