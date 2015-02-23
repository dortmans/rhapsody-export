#!/usr/bin/env python
"""rhp_yaml.py; Read Rhapsody archive file and write as .yaml file

"""

__author__ = "Eric Dortmans"
__copyright__ = "Copyright 2015, Eric Dortmans"

import sys, os, argparse, rhp, yaml


def rhp_to_yaml(rhp_file, yaml_file, compressed):
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
    yaml.dump(data, file(yaml_file, 'w'), default_flow_style=default_flow_style, indent=indent)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Read Rhapsody archive file and write equivalent .yaml file')
    parser.add_argument('-c', '--c', action='store_true', help='compressed yaml output')
    parser.add_argument('rhp_file', help='Rhapsody archive filepath')
    parser.add_argument('yaml_file', nargs='?', help='yaml filepath')
    args = parser.parse_args()
    rhp_file = args.rhp_file
    if args.yaml_file == None:
        yaml_file = os.path.splitext(args.rhp_file)[0] + '.yaml'
    else:
        yaml_file = args.yaml_file

    rhp_to_yaml(rhp_file, yaml_file, args.c)

