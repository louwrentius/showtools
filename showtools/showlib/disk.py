import subprocess
import sys
import os
from rich import print as print
from . import (
    smart,
    diskattr,
    disklookup
)

def get_block_devices():
    devicepath = "/sys/block"
    diskdevices = os.listdir(devicepath)
    diskdevices.sort()
    return diskdevices


def get_hdparm_data(device):
    command = "hdparm -IC " + device
    try:
        p = subprocess.Popen([command],  stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,  shell=True)
        rawdata = p.communicate()
    except IOError:
        print("Is hdparm installed or are you root / using sudo?")
        sys.exit(1)

    returncode = p.returncode

    if returncode == 13:
        raise IOError
    if returncode == 127:
        raise OSError
    if returncode > 0:
        pass

    return rawdata


def process_lookup(lookup, args):
    devicedata = {}
    for k, v in lookup.items():
        addoption = False
        if args["generic_settings"]["all_opts"]: 
            addoption = True
        elif k in args["storage_generic"].keys() or k in args["storage_smart"].keys():
            addoption = True
        if addoption:
            devicedata[k] = v
    return devicedata

def get_disk_device_data(dev, args):
    fullpath = "/dev/" + dev
    hdparmdata = get_hdparm_data(fullpath)
    hdparmdata = diskattr.decode_data(hdparmdata[0])
    if smart.is_smart_used(args):
        smartdata = smart.get_smart_data(fullpath)
    lookup = disklookup.device_options_table(fullpath, hdparmdata, smartdata)
    devicedata = process_lookup(lookup, args)
    return devicedata
