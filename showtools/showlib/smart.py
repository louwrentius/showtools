import sys
import subprocess
import json

def get_smart_data(device):
    try:
        child = subprocess.Popen(['smartctl', '-j',  '-a',  '-d',  'ata',  device],
                                 stdout=subprocess.PIPE,
                                 stderr=subprocess.PIPE)
    except OSError:
        print("Executing smartctl gave an error, is smartmontools installed?")
        sys.exit(1)

    rawdata = child.communicate()

    if child.returncode:
        child = subprocess.Popen(['smartctl', '-j',  '-a',  device],
                                 stdout=subprocess.PIPE,
                                 stderr=subprocess.PIPE)
        rawdata = child.communicate()
        if child.returncode == 1:
            return ""

    smartdata = rawdata[0]
    try:
        smartdata = json.loads(smartdata)
    except json.JSONDecodeError as e:
        print("Invalid JSON syntax:", e)    
    return smartdata

def get_smart_attribute_from_json(json, attribute):
    returndata = "?"
    for item in json["ata_smart_attributes"]["table"]:
        if item["name"] == attribute:
            returndata = str(item["raw"]["value"])
    return returndata

def get_smart_conversion_dict():
    conversion_dict = {
        "temperature"               : ["temperature", "current"],
        "model"                     : ["model_name"],
        "firmware"                   : ["firmware_version"],
        "size"                      : ["user_capacity", "bytes"],
        "speed"                     : ["interface_speed","current","string"],
        "serial"                    : ["serial_number"]
    }
    return conversion_dict

def get_generic_parameter_from_smart(data, parameter):
    table = get_smart_conversion_dict()
    path = table[parameter]
    returndata = data
    for x in path:
        try:
            returndata = returndata[x]
        except KeyError:
            returndata = "?"
            break
    return str(returndata)

def get_disk_speed(smartdata):
    returndata = get_generic_parameter_from_smart(smartdata, "speed")
    return str(returndata) 


def get_disk_size(smartdata):
    rawdata = get_generic_parameter_from_smart(smartdata, "size")
    returndata = round(float(rawdata) / 1000000000)
    return str(returndata)


def get_disk_firmware(smartdata):
    match = get_generic_parameter_from_smart(smartdata, "firmware")
    return match.strip()

def get_pending_sectors(smartdata):
    match1 = get_smart_attribute_from_json(smartdata,
                                        'Total_Pending_Sectors')
    match2 = get_smart_attribute_from_json(smartdata,
                                        'Current_Pending_Sector')

    if match1:
        diskcurrentpending = match1
    if match2:
        diskcurrentpending = match2
    if not match1 and not match2:
        diskcurrentpending = "?"

    return diskcurrentpending
