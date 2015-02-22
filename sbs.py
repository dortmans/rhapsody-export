#!/usr/bin/env python
"""sbs.py; parse Rhapsody archive file

"""

__author__ = "Eric Dortmans"
__copyright__ = "Copyright 2015, Eric Dortmans"

import sys, os, argparse, re


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
        assignment = line[1:].split('=', 1)
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
            pass  # continued on next line
    elif line[0] == '}':
        # object close
        tokenstream.append('}')
    else:
        if not tokenstream:
            # first line
            tokenstream.append(line)
        else:
            # remainder of previous line
            # tokenstream[-1] += '\\n'
            tokenstream[-1] += line.strip('')


def parse(tokenstream):
    # Parse the sbs tokenstream
    sbs = []
    sbs.append(parse_header(tokenstream))
    tokenstream.pop(0)  # {
    sbs.append(parse_object(tokenstream))
    return sbs


def parse_header(tokenstream):
    token = tokenstream.pop(0)
    tag = token[:19]
    if tag != 'I-Logix-RPY-Archive':
        raise Exception("ERROR: Wrong file header tag: {}".format(tag))
    return token


def parse_object(tokenstream):
    type = tokenstream.pop(0)
    properties = parse_properties(tokenstream)
    object = {type: properties}
    return object


def parse_properties(tokenstream):
    # properties = []
    properties = {}
    token = tokenstream.pop(0)
    while token != '}':
        if token == '=':
            key = tokenstream.pop(0)
            value = parse_value(tokenstream)
            # properties.append({key:value})
            properties.update({key: value})
        elif token == '{':
            # properties.append(parse_object(tokenstream))
            properties.update(parse_object(tokenstream))
        else:
            raise Exception("ERROR: Unexpected token': {}".format(token))
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
        tokenstream.insert(0, token)
        if len(value) == 1:
            # or just one object
            value = value[0]
    else:
        # or a list of values
        parts = token.split('"')
        if parts[-1].strip() == ';':
            value = '"'.join(parts[1:-1])
        else:
            value = [x.strip() for x in token.split(";")[:-1]]
        if len(value) == 1:
            # or a single value
            value = value[0]
    return value


def load(file):
    try:
        text = file.readlines()
        tree = parse(tokenize(text))
    except Exception, e:
        print e
        sys.exit(1)
    return tree


if __name__ == "__main__":
    # TODO: Someday put some test here
    pass
