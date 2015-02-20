#!/usr/bin/env python
"""Python example.

Rhapsody SBS file processing.
"""

import os, argparse, re, json

def tokenize(text):
    tokenstream = []
    for i, line in enumerate(text):
        line_stripped = line.strip()
        if line_stripped == '': break
        print i, line
        tokenize_line(tokenstream, line_stripped)
    return tokenstream


def tokenize_line(tokenstream, line):
        if line[0] == '{':
            tokenstream.append('{')
            tokenstream.append(line[1:].strip())
        elif line[0] == '-':
            assignment = re.split(' =|;',line[2:])
            left = assignment[0].strip()
            tokenstream.append('=')
            tokenstream.append(left)
            right = assignment[1].strip()
            if right != '' and right[0] == '{':
                tokenstream.append('{')
                tokenstream.append(right[1:].strip())
            else:
                tokenstream.append(right)
        elif line[0] == '}':
            tokenstream.append('}')
        else:
            tokenstream.append('#')
            tokenstream.append(line)


def parse(tokenstream):
    # Parse the sbs tokenstream
    sbs=[]
    tokenstream.pop(0)
    sbs.append(parse_comment(tokenstream))
    tokenstream.pop(0)
    sbs.append(parse_object(tokenstream))
    return sbs

def parse_object(tokenstream):
    type = tokenstream.pop(0)
    properties = parse_properties(tokenstream)
    object = type, properties
    return object

def parse_properties(tokenstream):
    properties = {}
    while tokenstream.pop(0) != '}':
        key = tokenstream.pop(0)
        value = parse_value(tokenstream)
        properties[key] = value
    return properties

def parse_value(tokenstream):
    token = tokenstream.pop(0)
    if token == '{':
        # object
        value = parse_object(tokenstream)
    else:
        # simple value
        value = token
    return value

def parse_comment(tokenstream):
    return '# ' + tokenstream.pop(0)

def sbs_load(sbs_file):
    text = sbs_file.readlines()
    tokenstream = tokenize(text)
    print tokenstream
    sbs = parse(tokenstream)
    return tokenstream
    #return sbs

def sbs_to_json(sbs_file, compressed):
    data = sbs_load(file(sbs_file, 'r'))
    if compressed:
        separators = (',', ':')
        indent = None
    else:
        separators = None
        indent = 2
    json_file = os.path.splitext(sbs_file)[0] + '.json'
    json.dump(data, file(json_file, 'w'), separators=separators, indent=indent)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Read .sbs file and write equivalent .json file')
    parser.add_argument('-c', '--c', action='store_true', help='compressed json output')
    parser.add_argument('sbs_file', help='The .sbs file to convert')
    args = parser.parse_args()
    sbs_to_json(args.sbs_file, args.c)
