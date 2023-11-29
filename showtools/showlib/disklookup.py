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
        "device":{"value": dev,
                 "justify": "left"
                 },
        "model":{"value": diskattr.get_disk_model(smartdata),
                 "justify": "left"
                 },
        "type":{"value": diskattr.get_disk_type(dev),
                 "justify": "center"
                 },
        "serial":{"value": diskattr.get_disk_model(smartdata),
                 "justify": "left"
                 },
        "state":{"value": diskattr.get_disk_drivestate(hdparmdata),
                 "justify": "left"
                 },
        "apm":{"value": diskattr.get_disk_apmstate(hdparmdata),
                 "justify": "left"
                 },
        "size":{"value": smart.get_disk_size(smartdata),
                 "justify": "left"
                 },
        "speed":{"value": smart.get_disk_speed(smartdata),
                 "justify": "left"
                 },
        "firmware":{"value": smart.get_disk_firmware(smartdata),
                 "justify": "left"
                 },
        "controller":{"value": diskattr.get_pci_device_name(dev, pci_devices, disk_paths),
                 "justify": "left"
                 },
        "pcipath":{"value": diskattr.get_disk_path(dev, disk_paths),
                 "justify": "left"
                 },
        "wwn":{"value": diskattr.get_disk_wwn(dev, disk_ids),
                 "justify": "left"
                 },
        "scsi":{"value": diskattr.get_disk_scsi(dev, disk_ids),
                 "justify": "left"
                 },
        "temp":{"value": smart.get_generic_parameter_from_smart(smartdata, 'temperature'),
                 "justify": "left"
                 },
        "hours":{"value": smart.get_smart_attribute_from_json(smartdata, 'Power_On_Hours'),
                 "justify": "left"
                 },
        "pending":{"value": smart.get_pending_sectors(smartdata),
                 "justify": "left"
                 },
        "reallocated":{"value": smart.get_smart_attribute_from_json(smartdata, 'Reallocated_Sector_Ct'),
                 "justify": "left"
                 },
        "reallocatedevent":{"value": smart.get_smart_attribute_from_json(smartdata,"Reallocated_Event_Count"),
                 "justify": "left"
                 },

        "crc":{"value": smart.get_smart_attribute_from_json(smartdata, 'UDMA_CRC_Error_Count'),
                 "justify": "left"
                 },
        "startstop":{"value": smart.get_smart_attribute_from_json(smartdata, 'Start_Stop_Count'),
                 "justify": "left"
                 },
        "park":{"value": smart.get_smart_attribute_from_json(smartdata, 'Load_Cycle_Count'),
                 "justify": "left"
                 },
    }
    return lookup
