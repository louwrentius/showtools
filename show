#!/usr/bin/env python
#
# Author: Louwrentius
#
# Requirement: hdparm, ethtool, smartmontools
#

# Version: 1.03
#

import re
import subprocess
import sys
import os
import argparse


def set_arguments():

    #
    # Parse command line options
    #

    parser = argparse.ArgumentParser(description='Show detailed disk|net \
                                device information in ASCII table format')
    parser.add_argument('devicetype',  choices=['disk',  'net'],
                        help="Show disk information")

    sa = parser.add_argument_group(title="Generic settings", description="Options that apply for all device types.")
    sa.add_argument("-E",  "--transparent",
                    action="store_true",  help="Disable table formatting (no lines)")
    sa.add_argument("-g",  "--noheader",
                    action="store_true",  help="Disable table header (in transparent mode)")

    sg = parser.add_argument_group(title="Storage (generic)",
                                   description="Generic\
                                    options for storage devices")
    sg.add_argument("-a",  "--all-opts",
                    action="store_true",  help="show all information")
    sg.add_argument("-m",  "--model",
                    action="store_true",  help="device model")
    sg.add_argument("-S",  "--serial",
                    action="store_true",  help="device serial number")
    sg.add_argument("-D",  "--state",  action="store_true",
                    help="drive power status (active/standby)")
    sg.add_argument("-e",  "--apm",  action="store_true",
                    help="Advanced Power Mode")
    sg.add_argument("-s",  "--size",
                    action="store_true",  help="device size in Gigabytes")
    sg.add_argument("-f",  "--firmware",  action="store_true",
                    help="device firmware version")
    sg.add_argument("-c",  "--controller",  action="store_true",
                    help="controller to which device is connected")
    sg.add_argument("-p",  "--pcipath",  action="store_true",
                    help="/dev/disk/by-path/ ID of the device")
    sg.add_argument("-w",  "--wwn",  action="store_true",
                    help="device World Wide Name")
    sg.add_argument("-o",  "--scsi",  action="store_true",
                    help="/dev/by-id/scsi")

    ss = parser.add_argument_group(title="Storage (SMART)",  description=
                                   "Options based on SMART values of storage\
                                     devices")
    ss.add_argument("-t",  "--temp",  action="store_true",  help="temperature\
                    in Celcius")
    ss.add_argument("-H",  "--hours",  action="store_true",  help="power on\
                    hours")
    ss.add_argument("-P",  "--pending",  action="store_true",  help="pendinag\
                    sector count")
    ss.add_argument("-r",  "--reallocated",  action="store_true",  help=
                    "reallocated sector count")
    ss.add_argument("-R",  "--reallocatedevent",  action="store_true",  help=
                    "reallocated sector event count")
    ss.add_argument("-C",  "--crc",  action="store_true",  help="CRC error")
    ss.add_argument("-u",  "--startstop",  action="store_true",  help="spin up/down")
    ss.add_argument("-n",  "--park",  action="store_true",  help="head parking")


    nw = parser.add_argument_group(title="Network",
                                   description="Available options for\
                                   `network devices")

    nw.add_argument("-l",  "--link",  action="store_true",
                    help="network card link status")
    nw.add_argument("-4",  "--ipv4",  action="store_true",
                    help="IPv4 address")
    nw.add_argument("-6",  "--ipv6",  action="store_true",
                    help="IPv6 address")
    nw.add_argument("-M",  "--mac",  action="store_true",
                    help="hardware / MAC address")
    nw.add_argument("-T",  "--show-type",  action="store_true",
                    help="network card type")
    nw.add_argument("-d",  "--driver",  action="store_true",
                    help="driver module")
    nw.add_argument("-F",  "--firmware-version",  action="store_true",
                    help="firmware version")

    return parser


def main():

    parser = set_arguments()

    try:
        args = parser.parse_args()
    except OSError:
        parser.print_help()
        sys.exit(1)

    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)

    devicetype = args.devicetype

    def get_table_header(args):

        header_options = (
            ('model', 'Model', 'disk'),
            ('serial', 'Serial Number', 'disk'),
            ('state', 'State', 'disk'),
            ('apm', 'APM', 'disk'),
            ('size', 'GB', 'disk'),
            ('firmware', 'Firmware', 'disk'),
            ('controller', 'Controller', 'disk'),
            ('pcipath', '/dev/disk/by-path', 'disk'),
            ('wwn', '/dev/disk/by-id/wwn*', 'disk'),
            ('scsi', '/dev/disk/by-id/scsi*', 'disk'),
            ('temp', 'Temp', 'disk'),
            ('hours', 'Hours', 'disk'),
            ('pending', 'PS', 'disk'),
            ('reallocated', 'RS', 'disk'),
            ('reallocatedevent', 'RSE', 'disk'),
            ('crc', 'CRC', 'disk'),
            ('startstop', 'Spin', 'disk'),
            ('park', 'Park', 'disk'),
            ('link', 'Link', 'net'),
            ('ipv4', 'IPv4', 'net'),
            ('ipv6', 'IPv6', 'net'),
            ('mac', 'MAC', 'net'),
            ('show_type', 'Type', 'net'),
            ('driver', 'Driver', 'net'),
            ('firmware', 'Firmware', 'net'))

        header = ['Dev']

        for option in header_options:
            if option[2] == args.devicetype:
                if args.all_opts or getattr(args, option[0]):
                        if option[2] == args.devicetype:
                            header.append(option[1])

        #print "Header " + str(header)

        return header

    table_data = []
    table_header = get_table_header(args)

    for device in get_devices(devicetype):
        if not device.startswith("md") and not device.startswith("ram"):
            devicedata = process_device(device, args)
            if devicedata:
                table_data.append(devicedata)

    display_table(table_header, table_data, args)


def get_devices(devicetype):

    if devicetype == "disk":
        devices = get_block_devices()

    elif devicetype == "net":
        devices = get_interfaces()

    for device in devices:
        yield device
    return

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


#
# Get all disk devices
#


def get_block_devices():
    devicepath = "/sys/block"
    diskdevices = os.listdir(devicepath)
    diskdevices.sort()
    return diskdevices


def get_pci_devices():
    try:
        pci_devices = subprocess.Popen(['lspci'],  stdout=subprocess.PIPE,
                                       stderr=
                                       subprocess.PIPE).communicate()[0]
        return pci_devices
    except:
        print "Error when executing lspci,  you might need 'pciutils'\
                 if you run a Red Hat flavour."
        sys.exit(1)


def get_all_disk_paths():
    disk_by_path_data = subprocess.Popen(['ls',  '-alh',  '/dev/disk/by-path'],
                                         stdout=subprocess.PIPE,
                                         stderr=
                                         subprocess.PIPE).communicate()[0]
    return disk_by_path_data


def get_all_disk_wwns():
    disk_by_id_data = subprocess.Popen(['ls',  '-alh',  '/dev/disk/by-id'],
                                       stdout=subprocess.PIPE,
                                       stderr=subprocess.PIPE).communicate()[0]
    return disk_by_id_data


def generic_match_finder(device, data, pattern, matchgroup, split, itemnumber):
    for item in data.splitlines():
        if device in item:
            regex = re.compile(pattern + '(.*)')
            match = regex.search(item)
            if match:
                model = match.group(matchgroup).split(split)[itemnumber]
                return model
    return ""


def get_disk_deviceid(diskdevice, diskbypathdata):
    deviceid = generic_match_finder(diskdevice, diskbypathdata, 'pci-0000:', 1,
                                    ".", 0)
    return deviceid


def get_disk_path(diskdevice, diskbypathdata):
    diskpath = generic_match_finder(diskdevice, diskbypathdata, 'pci-', 0, " ",
                                    0)
    return diskpath


def get_disk_wwn(diskdevice, diskbyiddata):
    diskwwn = generic_match_finder(diskdevice, diskbyiddata, 'wwn', 0, " ", 0)
    return diskwwn


def get_disk_scsi(diskdevice, diskbyiddata):
    diskscsi = generic_match_finder(diskdevice, diskbyiddata, 'scsi', 0, " ",
                                    0)
    return diskscsi


def get_pci_device_name(diskdevice, pci_devices, diskbypathdata):
    deviceid = get_disk_deviceid(diskdevice, diskbypathdata)
    devicename = generic_match_finder(deviceid, pci_devices, deviceid, 1, ":",
                                      1)
    return devicename


def get_disk_model(hdparmdata):
    model = generic_match_finder("", hdparmdata, 'Model Number:', 1, ", ",
                                 0)
    return model.strip()


def get_disk_serial(hdparmdata):
    serial = generic_match_finder("", hdparmdata, 'Serial Number:', 1, ", ", 0)
    return serial.strip()

def get_disk_drivestate(hdparmdata):
    drivestate = generic_match_finder("", hdparmdata, 'drive state is:', 1, ", ", 0)
    return drivestate.strip()

def get_disk_apmstate(hdparmdata):
    apmstate = generic_match_finder("", hdparmdata, 'Advanced power management level:', 1, ", ", 0)
    return apmstate.strip()

def get_fdisk_size(device):
    command = "fdisk -l /dev/" + device
    p = subprocess.Popen([command],  stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE,  shell=True)
    rawdata = p.communicate()
    return rawdata[0]


def get_disk_size(dev):
    data = get_fdisk_size(dev)
    if data:
        raw = generic_match_finder("", data, ", ", 1, ", ", 0)
        bytes = raw.split(" ")[0]
        #Patch for " "octects of last entry
        bytes = bytes.split('\xc2')[0]
        gb = int(bytes) / 1000000000
        return str(gb)
    else:
        return ""


def get_disk_firmware(hdparmdata):
    match = generic_match_finder("", hdparmdata, 'Firmware Revision:', 1, ":",
                                 0)
    return match.strip()


def get_hdparm_data(device):
    command = "hdparm -IC " + device
    p = subprocess.Popen([command],  stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE,  shell=True)
    rawdata = p.communicate()
    returncode = p.returncode
    if returncode == 13:
        raise IOError
    if returncode == 127:
        raise OSError
    if returncode > 0:
    	pass
    return rawdata


def get_disk_data(device):

    try:
        data = get_hdparm_data(device)
        return data[0]
    except IOError:
        print "Error: Did you use sudo or are you root?"
        sys.exit(1)
    except OSError:
        print "Error: is hdparm installed?"
    sys.exit(1)

#
# Processing of SMART DATA
#


def get_parameter_from_smart(data, parameter, distance):
    regex = re.compile(parameter + '(.*)')
    match = regex.search(data)

    if match:
            tmp = match.group(1)
            length = len(tmp.split("   "))
            if length <= distance:
                distance = length-1

            #
            # SMART data is often a bit of a mess,  so this
            # hack is used to cope with this.
            #

            try:
                model = match.group(1).split("   ")[distance].split(" ")[1]
            except:
                model = match.group(1).split("   ")[distance+1].split(" ")[1]
            return str(model)
    return "?"


def get_smart_data(device):

    #
    # For debugging purposes
    #
    try:
        file = os.environ['smartdata']
        if os.path.isfile(file):
            f = open(file,  'r')
            data = f.read()
            return data
    except:
        pass

    try:
        child = subprocess.Popen(['smartctl',  '-a',  '-d',  'ata',  device],
                                 stdout=subprocess.PIPE,
                                 stderr=subprocess.PIPE)
    except OSError:
        print "Executing smartctl gave an error, is smartmontools installed?"
        sys.exit(1)

    rawdata = child.communicate()

    if child.returncode:
        child = subprocess.Popen(['smartctl',  '-a',  device],
                                 stdout=subprocess.PIPE,
                                 stderr=subprocess.PIPE)
        rawdata = child.communicate()
        if child.returncode == 1:
            return ""

    smartdata = rawdata[0]
    return smartdata

#
# Network functions
#


def search_data_for_match(regex, data):
    match = re.search(regex,  data)
    if match:
        return match.group(1)
    return ''


def get_interface_data(interface):
    raw_data = subprocess.Popen(['ifconfig',  interface],
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
        print "It seems that ethtool is not installed..."
        sys.exit(1)

    return raw_data


def get_interface_type(data):
    match = re.search('encap:(\S+)',  data)
    if match:
        return match.group(1)
    return ''


def is_smart_used(args):
    if args.temp or args.all_opts:
        return True
    if args.hours or args.all_opts:
        return True
    if args.pending or args.all_opts:
        return True
    if args.reallocated or args.all_opts:
        return True
    if args.reallocatedevent or args.all_opts:
        return True
    if args.crc or args.all_opts:
        return True
    if args.startstop or args.all_opts:
        return True
    if args.park or args.all_opts:
        return True
    return False


def process_device(dev, args):
    """
    This function gathers all data from a device and puts this data
    into a list. This list will become a single row in the output table.
    """

    devicedata = []

    devicedata.append(dev)

    if args.devicetype == "disk":

        fullpath = "/dev/" + dev

        diskdata = get_disk_data(fullpath)
        disksize = get_disk_size(dev)
        if not disksize:
            return None

        pci_devices = get_pci_devices()
        disk_paths = get_all_disk_paths()
        disk_wwns = get_all_disk_wwns()

        if is_smart_used(args):
            disksmart = get_smart_data(fullpath)

        if args.model or args.all_opts:
            diskmodel = get_disk_model(diskdata)
            devicedata.append(diskmodel)

        if args.serial or args.all_opts:
            diskserial = get_disk_serial(diskdata)
            devicedata.append(diskserial)

        if args.state or args.all_opts:
            drivestate = get_disk_drivestate(diskdata)
            devicedata.append(drivestate)

        if args.apm or args.all_opts:
            apmstate = get_disk_apmstate(diskdata)
            devicedata.append(apmstate)

        if args.size or args.all_opts:
            devicedata.append(disksize)

        if args.firmware or args.all_opts:
            diskfw = get_disk_firmware(diskdata)
            devicedata.append(diskfw)

        if args.controller or args.all_opts:
            pcidevice = get_pci_device_name(dev, pci_devices, disk_paths)
            devicedata.append(pcidevice)

        if args.pcipath or args.all_opts:
            devicepath = get_disk_path(dev, disk_paths)
            devicedata.append(devicepath)

        if args.wwn or args.all_opts:
            devicewwn = get_disk_wwn(dev, disk_wwns)
            devicedata.append(devicewwn)

        if args.scsi or args.all_opts:
            devicescsi = get_disk_scsi(dev, disk_wwns)
            devicedata.append(devicescsi)

        #
        # SMART DATA
        #

        if args.temp or args.all_opts:
            disktemp = get_parameter_from_smart(disksmart,
                                                'Temperature_Celsius', 10)
            devicedata.append(disktemp)

        if args.hours or args.all_opts:
            diskpoweronhours = get_parameter_from_smart(disksmart,
                                                        'Power_On_Hours', 12)
            devicedata.append(diskpoweronhours)

        if args.pending or args.all_opts:
            match1 = get_parameter_from_smart(disksmart,
                                              'Total_Pending_Sectors', 10)
            match2 = get_parameter_from_smart(disksmart,
                                              'Current_Pending_Sector', 10)

            if match1:
                diskcurrentpending = match1
            if match2:
                diskcurrentpending = match2
            if not match1 and not match2:
                diskcurrentpending = "?"

            devicedata.append(diskcurrentpending)

        if args.reallocated or args.all_opts:
            diskreallocatedsector = \
                get_parameter_from_smart(disksmart, 'Reallocated_Sector_Ct', 9)
            devicedata.append(diskreallocatedsector)

        if args.reallocatedevent or args.all_opts:
            diskreallocatedevent = \
                get_parameter_from_smart(disksmart,
                                         'Reallocated_Event_Count', 9)
            devicedata.append(diskreallocatedevent)

        if args.crc or args.all_opts:
            diskudmacrcerror =\
                get_parameter_from_smart(disksmart, 'UDMA_CRC_Error_Count',
                                         10)
            devicedata.append(diskudmacrcerror)

        if args.startstop or args.all_opts:
            diskstartstop =\
                get_parameter_from_smart(disksmart, 'Start_Stop_Count',
                                         10)
            devicedata.append(diskstartstop)

        if args.park or args.all_opts:
            diskloadcycle =\
                get_parameter_from_smart(disksmart, 'Load_Cycle_Count',
                                         10)
            devicedata.append(diskloadcycle)

    #
    # Network data
    #

    elif args.devicetype == "net":

        raw_ifconfig = get_interface_data(dev)
        raw_ethtool = get_driver_data(dev, "-i")
        raw_ethtool_extended = get_driver_data(dev, "")

        if args.link or args.all_opts:
            link = search_data_for_match('Link\ detected:\ (\S+)',
                                         raw_ethtool_extended)
            devicedata.append(link)

        if args.ipv4 or args.all_opts:
            ipv4 = search_data_for_match('inet addr:(\S+)', raw_ifconfig)
            devicedata.append(ipv4)

        if args.ipv6 or args.all_opts:
            ipv6 = search_data_for_match('inet6 addr: (\S+)', raw_ifconfig)
            devicedata.append(ipv6)

        if args.mac or args.all_opts:
            mac = search_data_for_match('HWaddr (\S+)', raw_ifconfig)
            devicedata.append(mac)

        if args.show_type or args.all_opts:
            itype = search_data_for_match('encap:(\S+)', raw_ifconfig)
            devicedata.append(itype)

        if args.driver or args.all_opts:
            driver = search_data_for_match('driver:\ (\S+)', raw_ethtool)
            devicedata.append(driver)

        if args.firmware_version or args.all_opts:
            firmware = search_data_for_match('firmware-version:\ (\S+)',
                                             raw_ethtool)
            devicedata.append(firmware)

    else:
        print "This is a bug, please inform the developer."
        sys.exit(1)

    #print "Devicedata " + str(devicedata)

    return devicedata

#
# Get collumn size for proper table formatting
# Find the biggest string in a collumn
#


def get_collumn_size(table_header, table_data):

    col_count = len(table_data[0])
    col_widths = []

    for i in xrange(col_count):
        collumn = []
        for row in table_data:

            header_length = len(table_header[i])
            data_length = len(row[i])

            #
            # The width of the header can be bigger than the data
            #

            if header_length > data_length:
                collumn.append(header_length)
            else:
                collumn.append(data_length)

        length = max(collumn)
        col_widths.append(length)

    #print "All coll widths: " + str(col_widths)

    return col_widths


def display_table(table_header, table_data, args):

    header_length = len(table_header)
    data_length = len(table_data[0])

    assert header_length == data_length, "Column count mismatch! %r/%r" % (header_length, data_length)

    col_widths = get_collumn_size(table_header, table_data)

    # Dirty hack to get a closing pipe character at the end of the row
    col_widths.append(1)

    # Some values to calculate the actual table with,  including spacing
    spacing = 1
    delimiter = 3
    table_width = (sum(col_widths) + len(col_widths) * spacing * delimiter) - \
        delimiter

    format = ""
    for col in col_widths:
	if args.transparent:
        	form = "  %-" + str(col) + "s "
	else:
        	form = "| %-" + str(col) + "s "
        format += form

    #
    # Print header
    #
    table_header.append("")
    if args.transparent:
        if not args.noheader:
            print '%s' % ' '*table_width
            print format % tuple(table_header)
            print '%s' % ' '*table_width
    else:
        print '%s' % '-'*table_width
        #print table_header
        print format % tuple(table_header)
        print '%s' % '-'*table_width

    #
    # Print actual table contents
    #
    for row in table_data:
        row.append("")
        print format % tuple(row)

    if not args.transparent:
        print '%s' % '-'*table_width

    #if hdparm_error:
    #    print "ERROR: hdparm not installed or not working!"

#
# Define table and add header as first row
# The header also defines the table / collumn width
#

#
# Main: get all devices and their data and display it in a table
#

if __name__ == "__main__":
    main()

