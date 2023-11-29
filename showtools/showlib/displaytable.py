from rich.table import Table
from rich.console import Console
from rich.text import Text

#def get_column_order(){
#    order = {
#        0: "model",
#        1: "type"
#    }
#    return order
#}

def display(tabledata, args):
    headerdata = get_header()
    table = Table()
    index = 0
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
        'firmware': 'Firmware',
    }
    return header_options

def get_collumn_size(table_header, table_data):

    col_count = len(table_data[0])
    col_widths = []

    for i in range(col_count):
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

    # print("All coll widths: " + str(col_widths))

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
    table_width = (sum(col_widths) + len(col_widths) * spacing * delimiter) - delimiter

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
            print('%s' % ' '*table_width)
            print(format % tuple(table_header))
            print('%s' % ' '*table_width)
    else:
        print('%s' % '-'*table_width)
        #print table_header
        print(format % tuple(table_header))
        print('%s' % '-'*table_width)

    #
    # Print actual table contents
    #
    for row in table_data:
        row.append("")
        print(format % tuple(row))

    if not args.transparent:
        print('%s' % '-'*table_width)