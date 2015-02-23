#!/usr/bin/env python
"""rhp_json.py; Read Rhapsody archive file and write as .json file

"""

__author__ = "Eric Dortmans"
__copyright__ = "Copyright 2015, Eric Dortmans"

import sys, os, argparse, rhp, json


def rhp_to_json(rhp_file, json_file, compressed):
    try:
        data = rhp.load(file(rhp_file, 'r'))
    except IOError, e:
        print e
        sys.exit(1)
    if compressed:
        separators = (',', ':')
        indent = None
    else:
        separators = None
        indent = 2
    json.dump(data, file(json_file, 'w'), separators=separators, indent=indent)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Read Rhapsody archive file and write equivalent .json file')
    parser.add_argument('-c', '--c', action='store_true', help='compressed json output')
    parser.add_argument('rhp_file', help='Rhapsody archive filepath')
    parser.add_argument('json_file', nargs='?', help='json filepath')
    args = parser.parse_args()
    rhp_file = args.rhp_file
    if args.json_file == None:
        json_file = os.path.splitext(args.rhp_file)[0] + '.json'
    else:
        json_file = args.json_file

    rhp_to_json(rhp_file, json_file, args.c)
