#!/usr/bin/env python
"""sbs_yaml.py; Read Rhapsody archive file and write equivalent .yaml file

argument: filepath of a Rhapsody archive file
"""

__author__ = "Eric Dortmans"
__copyright__ = "Copyright 2015, Eric Dortmans"

import os, argparse, yaml


def tokenize(text):
    tokenstream = []
    for i, line in enumerate(text):
        line_stripped = line.strip()
        if line_stripped != '':
            tokenize_line(tokenstream, line_stripped)
    return tokenstream


def tokenize_line(tokenstream, line):
    if line[0] == '{':
         # object open
        tokenstream.append('{')
        tokenstream.append(line[1:].strip())
    elif line[0] == '-':
        # property
        assignment = line[1:].split('=',1)
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
    elif line[0] == '}':
        # object close
        tokenstream.append('}')
    else:
        if not tokenstream:
            # first line
            tokenstream.append(line)
        else:
            # remainder of previous line
            tokenstream[-1] += line.strip(';')


def parse(tokenstream):
    # Parse the sbs tokenstream
    sbs = []
    sbs.append(parse_header(tokenstream))

    if tokenstream.pop(0) == '{':
        sbs.append(parse_object(tokenstream))
    else:
        raise Exception("ERROR: Unexpected token in 'parse': ",token)
    return sbs


def parse_header(tokenstream):
    return tokenstream.pop(0)


def parse_object(tokenstream):
    type = tokenstream.pop(0)
    properties = parse_properties(tokenstream)
    object = {type:properties}
    return object


def parse_properties(tokenstream):
    #properties = []
    properties = {}
    token = tokenstream.pop(0)
    while token != '}':
        if token == '=':
            key = tokenstream.pop(0)
            value = parse_value(tokenstream)
            #properties.append({key:value})
            properties.update({key:value})
        elif token == '{':
            #properties.append(parse_object(tokenstream))
            properties.update(parse_object(tokenstream))
        else:
            raise Exception("ERROR: Unexpected token in 'parse_properties': ",token)
        token = tokenstream.pop(0)
    return properties


def parse_value(tokenstream):
    token = tokenstream.pop(0)
    if token == '{':
        # value is list of objects
        value = []
        while token == '{':
            value.append(parse_object(tokenstream))
            token = tokenstream.pop(0)
        tokenstream.insert(0,token)
        if len(value) == 1:
            # or just one object
            value = value[0]
    else:
        # or just a list of values
        parts = token.split('"')
        if len(parts) == 1:
            value = [x.strip() for x in token.split(";")[:-1]]
        else:
            value = parts[1]
        if len(value) == 1:
            # or just one value
            value = value[0]
    return value

def sbs_load(sbs_file):
    text = sbs_file.readlines()
    tokenstream = tokenize(text)
    # print tokenstream
    sbs = parse(tokenstream)
    # print sbs
    return sbs


def sbs_to_yaml(sbs_file, compressed):
    data = sbs_load(file(sbs_file, 'r'))
    if compressed:
        indent = None
        default_flow_style=True
    else:
        indent = 2
        default_flow_style=False
    yaml_file = os.path.splitext(sbs_file)[0] + '.yaml'
    yaml.dump(data, file(yaml_file, 'w'), default_flow_style=default_flow_style, indent=indent)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Read Rhapsody archive file and write equivalent .yaml file')
    parser.add_argument('-c', '--c', action='store_true', help='compressed yaml output')
    parser.add_argument('sbs_file', help='The .sbs file to convert')
    args = parser.parse_args()
    sbs_to_yaml(args.sbs_file, args.c)
