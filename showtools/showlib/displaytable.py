#
# Get collumn size for proper table formatting
# Find the biggest string in a collumn
#
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