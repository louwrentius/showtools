import sys
import subprocess
import re
#
# Get all network devices
#
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

def search_data_for_match(regex, data):
    data = data.decode('utf-8')
    match = re.search(regex,  data)
    if match:
        return match.group(1)
    return ''


def get_interface_data(interface):
    raw_data = subprocess.Popen(['ip','a','show', interface],
                                stdout=subprocess.PIPE).communicate()[0]
    return raw_data

def get_driver_data(interface, parameter):

    if parameter:
        command = ["ethtool",  parameter,  interface]
    else:
        command = ["ethtool",  interface]

    try:
        raw_data = subprocess.Popen(command,  stdout=subprocess.PIPE,
                                    stderr=subprocess.STDOUT).communicate()[0]
    except OSError:
        print("It seems that ethtool is not installed...")
        sys.exit(1)

    return raw_data


def get_interface_type(data):
    match = re.search('encap:(\S+)',  data)
    if match:
        return match.group(1)
    return ''

def get_network_device_data(dev, args):
    raw_ifconfig = get_interface_data(dev)
    raw_ethtool = get_driver_data(dev, "-i")
    raw_ethtool_extended = network.get_driver_data(dev, "")

    devicedata = []

    if args.link or args.all_opts:
        link = search_data_for_match('Link\ detected:\ (\S+)', raw_ethtool_extended)
        devicedata.append(link)

    if args.ipv4 or args.all_opts:
        ipv4 = search_data_for_match('inet (\S+)', raw_ifconfig)
        devicedata.append(ipv4)

    if args.ipv6 or args.all_opts:
        ipv6 = search_data_for_match('inet6 (\S+)', raw_ifconfig)
        devicedata.append(ipv6)

    if args.mac or args.all_opts:
        mac = search_data_for_match('ether (\S+)', raw_ifconfig)
        devicedata.append(mac)

    if args.show_type or args.all_opts:
        itype = search_data_for_match('link/(\S+)', raw_ifconfig)
        devicedata.append(itype)

    if args.driver or args.all_opts:
        driver = search_data_for_match('driver:\ (\S+)', raw_ethtool)
        devicedata.append(driver)

    if args.firmware_version or args.all_opts:
        firmware = search_data_for_match('firmware-version:\ (\S+)', raw_ethtool)
        devicedata.append(firmware)

