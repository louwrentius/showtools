from rich.table import Table
from rich.console import Console
from rich.text import Text

def display(tabledata, args):
    headerdata = get_header()
    table = Table()
    columnorder = []

    for k, v in tabledata[0].items():
        column = headerdata[k]
        table.add_column(column, justify=v["justify"],no_wrap=True)
        columnorder.append(k)

    for row in tabledata:
        rowdata = []
        for column in columnorder:
            rowdata.append(f"{row[column]['value']}")
        table.add_row(*rowdata)
    
    console = Console()
    console.print(table)

def get_header():
    header_options = {
        'device': 'Device',
        'type': 'Type', 
        'model': 'Model', 
        'serial': 'Serial Number',
        'state': 'State',
        'apm': 'APM',
        'size': 'GB',
        'speed': 'Gbps',
        'firmware': 'Firmware',
        'controller': 'Controller',
        'pcipath': '/dev/disk/by-path',
        'wwn': '/dev/disk/by-id/wwn*',
        'scsi': '/dev/disk/by-id/scsi*',
        'temp': 'Temp',
        'hours': 'Hours',
        'pending': 'PS',
        'reallocated': 'RS',
        'reallocatedevent': 'RSE',
        'crc': 'CRC',
        'startstop': 'Spin',
        'park': 'Park',
        'link': 'Link',
        'ipv4': 'IPv4',
        'ipv6': 'IPv6',
        'mac': 'MAC',
        'show_type': 'Type',
        'driver': 'Driver',
        'firmware_version': 'Firmware',
    }
    return header_options