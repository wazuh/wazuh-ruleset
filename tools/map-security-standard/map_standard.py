#! /usr/bin/python
# -*- coding: utf8 -*-

import argparse
import re
import os
import glob
import json


_rules_file_group = re.compile(r'<group>(.*),<\/group>')


def pci_to_hipaa(path, schema):
    if list(path)[-1] != '/':
        path += '/'
    with open(schema) as f:
        json_data = json.load(f)
    os.chdir(path)
    for file in glob.glob('*.xml'):
        print('[INFO] Processing {}'.format(file))
        with open(file, 'r+') as f:
            lines = f.readlines()
        new_file = ''
        for line in lines:
            match = re.search(_rules_file_group, line)
            if match:
                added = list()
                for group in match.groups():
                    for pci in group.split(','):
                        if pci in list(json_data.keys()):
                            if json_data[pci] not in group.split(','):
                                if json_data[pci] not in added:
                                    added.append(json_data[pci])
                                    added.append(',')
                if len(added) > 1:
                    new_line = line.split(',')
                    new_line.insert(-1, "".join(added[0:-1]))
                    new_line = ",".join(new_line)
                    new_file += new_line
                else:
                    new_file += line
            else:
                new_file += line
        with open(file, 'w') as f:
            f.write(new_file)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument('-p', '--path', type=str, default='../../rules/', help='Rules path')
    parser.add_argument('-s', '--schema', type=str, default='schema.txt', help='Schema path')

    args = parser.parse_args()

    pci_to_hipaa(args.path, args.schema)
