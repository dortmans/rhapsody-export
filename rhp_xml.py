#!/usr/bin/env python
"""rhp_xml.py; Read Rhapsody archive file and write as .xml file

"""

__author__ = "Eric Dortmans"
__copyright__ = "Copyright 2015, Eric Dortmans"

import sys, os, argparse, rhp
from xml.dom.minidom import Document

doc = Document()

def data2xml(data):
    root_tag = 'I-Logix-RPY-Archive'
    header_tag = 'description'
    root = doc.createElement(root_tag)
    root.setAttribute(header_tag, data[0])
    doc.appendChild(root)
    dict2xml(data[1], root)
    return doc

def dict2xml(the_dict, parent):
    for key, value in the_dict.items():
        item2xml(key, value, parent)

def item2xml(the_key, the_value, parent):
    if type(the_value) is dict:
        child = doc.createElement(the_key)
        parent.appendChild(child)
        dict2xml(the_value, child)
    elif type(the_value) is list:
        for value in the_value:
            value2xml(the_key, value, parent)
    else: # it must be a single value
        value2xml(the_key, the_value, parent)

def value2xml(the_tag, the_value, parent):
    child = doc.createElement(the_tag)
    parent.appendChild(child)
    if type(the_value) is dict:
        dict2xml(the_value, child)
    else:
        child_content = doc.createTextNode(str(the_value))
        child.appendChild(child_content)

def xml_dump(data, the_file, pretty=True, indent=4):
    if indent == None:
        indent = 0
    if pretty:
        xml_string = data2xml(data).toprettyxml(indent=' '*indent, encoding='utf-8')
    else:
        xml_string = data2xml(data).toxml(encoding='utf-8')
    the_file.write(xml_string)

def rhp_to_xml(rhp_file, xml_file, compressed):
    try:
        data = rhp.load(file(rhp_file, 'r'))
    except IOError, e:
        print e
        sys.exit(1)
    if compressed:
        indent = None
        pretty = False
    else:
        indent = 2
        pretty = True
    xml_dump(data, file(xml_file, 'w'), pretty=pretty, indent=indent)


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

