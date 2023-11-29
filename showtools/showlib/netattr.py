import re
import sys
import subprocess





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