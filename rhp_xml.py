#!/usr/bin/env python
"""rhp_xml.py; Read Rhapsody archive file and write as .xml file

"""

__author__ = "Eric Dortmans"
__copyright__ = "Copyright 2015, Eric Dortmans"

import sys, os, argparse, rhp, xml

def data2xml(data, default_flow_style, indent):
    root_tag = 'rhp'
    header_tag = 'description'
    indent_level = 0
    xml_string = ''
    xml_string += '\n' + ' '*indent*indent_level
    xml_string += '<{}>'.format(root_tag)
    # header
    xml_string += value2xml(header_tag, data[0], indent, indent_level+1)
    # content
    xml_string += dict2xml(data[1], indent, indent_level+1)
    xml_string += '\n' + ' '*indent*indent_level
    xml_string += '</{}>'.format(root_tag)
    return xml_string


def dict2xml(the_dict, indent, indent_level):
    xml_string = ''
    for key, value in the_dict.items():
        item = {}
        xml_string += item2xml(key, value, indent, indent_level)
    return xml_string

def item2xml(the_key, the_value, indent, indent_level):
    xml_string = ''

    if type(the_value) is dict:
        xml_string += '\n' + ' '*indent*indent_level
        xml_string += '<{}>'.format(the_key)
        xml_string += dict2xml(the_value, indent, indent_level+1)
        xml_string += '\n' + ' '*indent*indent_level
        xml_string += '</{}>'.format(the_key)
    elif type(the_value) is list:
        for value in the_value:
            xml_string += value2xml(the_key, value, indent, indent_level+1)
    else:
        # it must be a single value
        xml_string += value2xml(the_key, the_value, indent, indent_level+1)

    return xml_string

def value2xml(the_tag, the_value, indent, indent_level):
    xml_string = ''
    xml_string += '\n' + ' '*indent*indent_level
    xml_string += '<{}>'.format(the_tag)

    xml_string += '\n' + ' '*indent*(indent_level+1)
    xml_string += the_value

    xml_string += '\n' + ' '*indent*indent_level
    xml_string += '</{}>'.format(the_tag)
    return xml_string


def xml_dump(data, the_file, default_flow_style=False, indent=4):
    # TODO: Use ElementTree
    if indent == None:
        indent = 0
    xml_string = data2xml(data, default_flow_style=default_flow_style, indent=indent)
    print xml_string
    the_file.write(xml_string)

def rhp_to_xml(rhp_file, xml_file, compressed):
    try:
        data = rhp.load(file(rhp_file, 'r'))
    except IOError, e:
        print e
        sys.exit(1)
    if compressed:
        indent = None
        default_flow_style = True
    else:
        indent = 2
        default_flow_style = False
    xml_dump(data, file(xml_file, 'w'), default_flow_style=default_flow_style, indent=indent)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Read Rhapsody archive file and write equivalent .xml file')
    parser.add_argument('-c', '--c', action='store_true', help='compressed xml output')
    parser.add_argument('rhp_file', help='Rhapsody archive filepath')
    parser.add_argument('xml_file', nargs='?', help='xml filepath')
    args = parser.parse_args()
    rhp_file = args.rhp_file
    if args.xml_file == None:
        xml_file = os.path.splitext(args.rhp_file)[0] + '.xml'
    else:
        xml_file = args.xml_file

    rhp_to_xml(rhp_file, xml_file, args.c)

