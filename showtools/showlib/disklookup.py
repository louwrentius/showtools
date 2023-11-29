import subprocess
import os
from . import (
    diskattr,
    smart
)

def get_all_disk_paths():
    disk_by_path_data = subprocess.Popen(['ls',  '-alh',  '/dev/disk/by-path'],
                                         stdout=subprocess.PIPE,
                                         stderr=
                                         subprocess.PIPE).communicate()[0]
    return disk_by_path_data

def get_all_disk_ids():
    disk_by_id_data = subprocess.Popen(['ls',  '-alh',  '/dev/disk/by-id'],
                                       stdout=subprocess.PIPE,
                                       stderr=subprocess.PIPE).communicate()[0]
    return disk_by_id_data

def device_options_table(dev, hdparmdata, smartdata):
    dev = os.path.basename(dev)
    pci_devices = diskattr.get_pci_devices()
    disk_paths = get_all_disk_paths()
    disk_ids = get_all_disk_ids()
    lookup = {
        "model":{"func": diskattr.get_disk_model(smartdata),
                 "justify": "left"
                 },
        "type":{"func": diskattr.get_disk_type(dev),
                 "justify": "center"
                 },
        "serial":{"func": diskattr.get_disk_model(smartdata),
                 "justify": "left"
                 },
        "state":{"func": diskattr.get_disk_drivestate(hdparmdata),
                 "justify": "left"
                 },
        "apm":{"func": diskattr.get_disk_apmstate(hdparmdata),
                 "justify": "left"
                 },
        "size":{"func": smart.get_disk_size(smartdata),
                 "justify": "left"
                 },
        "speed":{"func": smart.get_disk_speed(smartdata),
                 "justify": "left"
                 },
        "firmware":{"func": smart.get_disk_firmware(smartdata),
                 "justify": "left"
                 },
        "controller":{"func": diskattr.get_pci_device_name(dev, pci_devices, disk_paths),
                 "justify": "left"
                 },
        "pcipath":{"func": diskattr.get_disk_path(dev, disk_paths),
                 "justify": "left"
                 },
        "wwn":{"func": diskattr.get_disk_wwn(dev, disk_ids),
                 "justify": "left"
                 },
        "scsi":{"func": diskattr.get_disk_scsi(dev, disk_ids),
                 "justify": "left"
                 },
        "temp":{"func": smart.get_generic_parameter_from_smart(smartdata, 'temperature'),
                 "justify": "left"
                 },
        "hours":{"func": smart.get_smart_attribute_from_json(smartdata, 'Power_On_Hours'),
                 "justify": "left"
                 },
        "pending":{"func": smart.get_pending_sectors(smartdata),
                 "justify": "left"
                 },
        "reallocated":{"func": smart.get_smart_attribute_from_json(smartdata, 'Reallocated_Sector_Ct'),
                 "justify": "left"
                 },
        "reallocatedevent":{"func": smart.get_smart_attribute_from_json(smartdata,"Reallocated_Event_Count"),
                 "justify": "left"
                 },

        "crc":{"func": smart.get_smart_attribute_from_json(smartdata, 'UDMA_CRC_Error_Count'),
                 "justify": "left"
                 },
        "startstop":{"func": smart.get_smart_attribute_from_json(smartdata, 'Start_Stop_Count'),
                 "justify": "left"
                 },
        "park":{"func": smart.get_smart_attribute_from_json(smartdata, 'Load_Cycle_Count'),
                 "justify": "left"
                 },
    }
    return lookup
