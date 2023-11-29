import subprocess
import os
import re
from . import (
    netattr
)

def search_data_for_match(regex, data):
    data = data.decode('utf-8')
    match = re.search(regex,  data)
    if match:
        return match.group(1)
    return ''

def device_options_table(dev):
    raw_ifconfig = netattr.get_interface_data(dev)
    raw_ethtool = netattr.get_driver_data(dev, "-i")
    raw_ethtool_extended = netattr.get_driver_data(dev, "")

    lookup = {
        "device": {"value": dev, "justify": "left"},
        "link":{"value": search_data_for_match('Link\ detected:\ (\S+)', raw_ethtool_extended) ,
                 "justify": "left"
                 },
        "ipv4":{"value": search_data_for_match('inet (\S+)', raw_ifconfig),
                 "justify": "left"
                 },
        "ipv6":{"value": search_data_for_match('inet6 (\S+)', raw_ifconfig),
                 "justify": "left"
                 },
        "mac":{"value": search_data_for_match('ether (\S+)', raw_ifconfig),
                 "justify": "left"
                 },
        "show_type":{"value": search_data_for_match('link/(\S+)', raw_ifconfig),
                 "justify": "left"
                 },
        "driver":{"value": search_data_for_match('driver:\ (\S+)', raw_ethtool),
                 "justify": "left"
                 },
        "firmware_version":{"value": search_data_for_match('firmware-version:\ (\S+)', raw_ethtool),
                 "justify": "left"
                 },
    }
    return lookup
