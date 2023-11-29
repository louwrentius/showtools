import sys
from . import smart
import re
import subprocess



def decode_data(data):
    decoded = None
    if isinstance(data, bytes):
        decoded = data.decode('utf-8')
    elif isinstance(data, str):
        decoded = data
    else: 
        print(f"I can't deal with type {type(data)}")
        sys.exit(1)
    return decoded

def get_pci_devices():
    try:
        pci_devices = subprocess.Popen(['lspci'], stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()[0]
        return pci_devices
    except:
        print("Error when executing lspci,  you might need 'pciutils'\
                 if you run a Red Hat flavour.")
        sys.exit(1)


def generic_match_finder(device, data, pattern, matchgroup, split, itemnumber):
    
    for item in data.splitlines():
        item = decode_data(item)
        if device in item:
            regex = re.compile(pattern + '(.*)')
            match = regex.search(item)
            if match:
                model = match.group(matchgroup).split(split)[itemnumber]
                return model
    return ""

def get_pci_device_name(diskdevice, pci_devices, diskbypathdata):
    deviceid = get_disk_deviceid(diskdevice, diskbypathdata)
    devicename = generic_match_finder(deviceid, pci_devices, deviceid, 1, ":", 1)
    return devicename


def get_disk_serial(smartdata):
    serial = smart.get_generic_parameter_from_smart(smartdata, "serial")
    return serial.strip()


def get_disk_drivestate(hdparmdata):
    drivestate = generic_match_finder("", hdparmdata, 'drive state is:', 1, ", ", 0)
    return drivestate.strip()


def get_disk_apmstate(hdparmdata):
    apmstate = generic_match_finder("", hdparmdata, 'Advanced power management level:', 1, ", ", 0)
    return apmstate.strip()


def get_disk_deviceid(diskdevice, diskbypathdata):
    deviceid = generic_match_finder(diskdevice, diskbypathdata, 'pci-0000:', 1, ".", 0)
    return deviceid


def get_disk_path(diskdevice, diskbypathdata):
    diskpath = generic_match_finder(diskdevice, diskbypathdata, 'pci-', 0, " ", 0)
    return diskpath


def get_disk_wwn(diskdevice, diskbyiddata):
    diskwwn = generic_match_finder(diskdevice, diskbyiddata, 'wwn', 0, " ", 0)
    return diskwwn


def get_disk_scsi(diskdevice, diskbyiddata):
    diskscsi = generic_match_finder(diskdevice, diskbyiddata, 'scsi', 0, " ",0)
    return diskscsi

def get_disk_model(smartdata):
    model = smart.get_generic_parameter_from_smart(smartdata, "model")
    return model.strip()

def get_disk_type(dev):
    lookup = { "1":"HDD","0":"SDD"}
    device = f"/sys/block/{dev}/queue/rotational"
    with open(device,"r") as f:
        value = f.read()
    model = lookup[value.strip()]
    return model.strip()
