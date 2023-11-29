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

def unused(args, fullpath, devicedata, disk, diskdata):



    if smart.is_smart_used(args):
        disksmart = smart.get_smart_data(fullpath)

    if args.type or args.all_opts:
        disktype = disk.get_disk_type(dev)
        devicedata.append(disktype)

    if args.model or args.all_opts:
        diskmodel = disk.get_disk_model(disksmart)
        devicedata.append(diskmodel)

    if args.serial or args.all_opts:
        diskserial = disk.get_disk_serial(disksmart)
        devicedata.append(diskserial)

    if args.state or args.all_opts:
        drivestate = disk.get_disk_drivestate(diskdata)
        devicedata.append(drivestate)

    if args.apm or args.all_opts:
        apmstate = disk.get_disk_apmstate(diskdata)
        devicedata.append(apmstate)

    if args.size or args.all_opts:
        disksize = disk.get_disk_size(disksmart)
        devicedata.append(disksize)

    if args.speed or args.all_opts:
        linkspeed = disk.get_disk_speed(disksmart)
        devicedata.append(linkspeed)

    if args.firmware or args.all_opts:
        diskfw = disk.get_disk_firmware(disksmart)
        devicedata.append(diskfw)

    if args.controller or args.all_opts:
        pcidevice = get_pci_device_name(dev, pci_devices, disk_paths)
        devicedata.append(pcidevice)

    if args.pcipath or args.all_opts:
        devicepath = disk.get_disk_path(dev, disk_paths)
        devicedata.append(devicepath)

    if args.wwn or args.all_opts:
        devicewwn = disk.get_disk_wwn(dev, disk_wwns)
        devicedata.append(devicewwn)

    if args.scsi or args.all_opts:
        devicescsi = disk.get_disk_scsi(dev, disk_wwns)
        devicedata.append(devicescsi)

    #
    # SMART DATA
    #
    if args.temp or args.all_opts:
        disktemp = smart.get_generic_parameter_from_smart(disksmart,
                                            'temperature')
        devicedata.append(disktemp)

    if args.hours or args.all_opts:
        diskpoweronhours = smart.get_smart_attribute_from_json(smartdata, 'Power_On_Hours')
        devicedata.append(diskpoweronhours)

    

    if args.reallocated or args.all_opts:
        diskreallocatedsector = smart.get_smart_attribute_from_json(disksmart, 'Reallocated_Sector_Ct')
        devicedata.append(diskreallocatedsector)

    if args.reallocatedevent or args.all_opts:
        diskreallocatedevent = smart.get_smart_attribute_from_json(disksmart,"Reallocated_Event_Count")
        devicedata.append(diskreallocatedevent)

    if args.crc or args.all_opts:
        diskudmacrcerror = smart.get_smart_attribute_from_json(disksmart, 'UDMA_CRC_Error_Count')
        devicedata.append(diskudmacrcerror)

    if args.startstop or args.all_opts:
        diskstartstop = smart.get_smart_attribute_from_json(disksmart, 'Start_Stop_Count')
        devicedata.append(diskstartstop)

    if args.park or args.all_opts:
        diskloadcycle = smart.get_smart_attribute_from_json(disksmart, 'Load_Cycle_Count')
        devicedata.append(diskloadcycle)



