import argparse

def set_arguments():
    parser = argparse.ArgumentParser(description='Show detailed disk|net device information in ASCII table format')
    parser.add_argument('devicetype',  choices=['disk', 'net'], help="Show disk information")

    sa = parser.add_argument_group(title="generic_settings", description="Options that apply for all device types.")
    sa.add_argument("-E",  "--transparent", action="store_true", help="Disable table formatting (no lines)")
    sa.add_argument("-g",  "--noheader", action="store_true",  help="Disable table header (in transparent mode)")
    sa.add_argument("-a",  "--all-opts", action="store_true",  help="show all information")

    sg = parser.add_argument_group(title="storage", description="Generic options for storage devices")

    sg.add_argument("-m",  "--model",action="store_true", help="device model")
    sg.add_argument("-k",  "--type",action="store_true", help="device type (HDD/SDD)")
    sg.add_argument("-S",  "--serial",action="store_true", help="device serial number")
    sg.add_argument("-D",  "--state", action="store_true", help="drive power status (active/standby)")
    sg.add_argument("-e",  "--apm", action="store_true", help="Advanced Power Mode")
    sg.add_argument("-s",  "--size", action="store_true", help="device size in Gigabytes")
    sg.add_argument("-z",  "--speed", action="store_true", help="SATA Link in Gbps")
    sg.add_argument("-f",  "--firmware", action="store_true", help="device firmware version")
    sg.add_argument("-c",  "--controller",  action="store_true", help="controller to which device is connected")
    sg.add_argument("-p",  "--pcipath",  action="store_true", help="/dev/disk/by-path/ ID of the device")
    sg.add_argument("-w",  "--wwn",  action="store_true", help="device World Wide Name")
    sg.add_argument("-o",  "--scsi",  action="store_true", help="/dev/by-id/scsi")
    sg.add_argument("-t",  "--temp",  action="store_true",  help="temperature in Celcius")
    sg.add_argument("-H",  "--hours",  action="store_true",  help="power on hours")
    sg.add_argument("-P",  "--pending",  action="store_true",  help="pending sector count")
    sg.add_argument("-r",  "--reallocated",  action="store_true",  help="reallocated sector count")
    sg.add_argument("-R",  "--reallocatedevent",  action="store_true",  help="reallocated sector event count")
    sg.add_argument("-C",  "--crc",  action="store_true",  help="CRC error")
    sg.add_argument("-u",  "--startstop",  action="store_true",  help="spin up/down")
    sg.add_argument("-n",  "--park",  action="store_true",  help="head parking")

    nw = parser.add_argument_group(title="network", description="Available options for network devices")
    nw.add_argument("-l",  "--link",  action="store_true", help="network card link status")
    nw.add_argument("-4",  "--ipv4",  action="store_true", help="IPv4 address")
    nw.add_argument("-6",  "--ipv6",  action="store_true", help="IPv6 address")
    nw.add_argument("-M",  "--mac",  action="store_true", help="hardware / MAC address")
    nw.add_argument("-T",  "--show-type",  action="store_true", help="network card type")
    nw.add_argument("-d",  "--driver",  action="store_true", help="driver module")
    nw.add_argument("-F",  "--firmware-version",  action="store_true", help="firmware version")
    return parser

def clean_option_groups(processed, groups):
    result = {}
    for group in groups:
        opts = {k: v for k, v in processed[group].items() if v}
        result[group] = opts
    return result

def process_argparse_data(parser, args):
    processed = {}
    arg_groups = {}
    groups = []
    for group in parser._action_groups:
        group_dict={a.dest:getattr(args,a.dest,None) for a in group._group_actions}
        arg_groups[group.title]=argparse.Namespace(**group_dict)
        processed[group.title] = vars(arg_groups[group.title])
        groups.append(str(group.title))
    processed = clean_option_groups(processed, groups)
    return processed
