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
        # print i, line
        tokenize_line(tokenstream, line_stripped)
    return tokenstream


def tokenize_line(tokenstream, line):
    line = line.strip(';')
    if line[0] == '{': # object open
        tokenstream.append('{')
        tokenstream.append(line[1:].strip())
    elif line[0] == '-': # property
        assignment = re.split(' =', line[2:])
        left = assignment[0].strip()
        tokenstream.append('=')
        tokenstream.append(left)
        right = assignment[1].strip()
        if right != '':
            if right[0] == '{':
                tokenstream.append('{')
                tokenstream.append(right[1:].strip())
            else:
                tokenstream.append(right)
        else:
            pass # continued on next line
    elif line[0] == '}': # object close
        tokenstream.append('}')
    else:
        if not tokenstream:  # first line
            tokenstream.append(line)
        else:  # remainder of previous line
            tokenstream[-1] += line


def parse(tokenstream):
    # Parse the sbs tokenstream
    sbs = []
    sbs.append(parse_comment(tokenstream))
    tokenstream.pop(0)
    sbs.append(parse_object(tokenstream))
    return sbs


def parse_object(tokenstream):
    print "BEGIN_OF_OBJECT"
    type = tokenstream.pop(0)
    properties = parse_properties(tokenstream)
    object = type, properties
    print "END_OF_OBJECT"
    return object


def parse_properties(tokenstream):
    print "BEGIN_OF_PROPERTIES"
    properties = {}
    token = tokenstream.pop(0)
    while token != '}':
        if token != '=': raise Exception("UNEXPECTED TOKEN:", token)
        key = tokenstream.pop(0)
        value = parse_value(tokenstream)
        print key, "=", value
        properties[key] = value
        token = tokenstream.pop(0)
    print "END_OF_PROPERTIES"
    return properties


def parse_value(tokenstream):
    token = tokenstream.pop(0)
    # TODO: empty value like in - m_pParent = ;
    if token != '{':
        # simple value
        value = token
    else:
        # list of objects
        value = []
        while token == '{':
            value = parse_object(tokenstream)
            token = tokenstream.pop(0)
        tokenstream.insert(0,token) # push back token
    return value


def parse_comment(tokenstream):
    return tokenstream.pop(0)


def sbs_load(sbs_file):
    text = sbs_file.readlines()
    tokenstream = tokenize(text)
    print tokenstream
    sbs = parse(tokenstream)
    print sbs
    return sbs


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
