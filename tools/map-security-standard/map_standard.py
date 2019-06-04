#! /usr/bin/python
# -*- coding: utf8 -*-

import argparse
import re
import os
import glob
import json


_rules_file_group = re.compile(r'<group>(.*),<\/group>')


def delete_standard(path, standard):
    if list(path)[-1] != '/':
        path += '/'
    os.chdir(path)
    for file in glob.glob('*.xml'):
        with open(file, 'r+') as f:
            lines = f.readlines()
        new_file = ''
        new_line = ''
        changed = False
        for line in lines:
            match = re.search(_rules_file_group, line)
            if match:
                new_line = line.split('<')[0]+'<group>'
                for group in match.groups():
                    groups = group.split(',')
                    for index, pci in enumerate(groups):
                        if pci != standard:
                            new_line += pci + ','
                        else:
                            changed = True
                new_line += '</group>\n'
            if new_line != '':
                new_file += new_line
                new_line = ''
            else:
                new_file += line
        if changed:
            print('[DELETE] Deleted {} in file {}'.format(standard, file))
        with open(file, 'w') as f:
            f.write(new_file)


def pci_to_any(path, schema):
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
    parser.add_argument('-m', '--mapping', type=str, default='mapping.json', help='Mapping path')
    parser.add_argument('-d', '--delete', type=str, default='', help='Standard to be delete')

    args = parser.parse_args()

    if args.delete == '':
        pci_to_any(args.path, args.mapping)
    else:
        delete_standard(args.path, args.delete)
