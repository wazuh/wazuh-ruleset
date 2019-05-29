#! /usr/bin/python
# -*- coding: utf8 -*-

import argparse
import re
import os
import glob
import json


_sca_file_groups = re.compile(r'compliance:\n\-(.*):(.*)\"\ncondition')


def pci_to_any(path, schema):
    if list(path)[-1] != '/':
        path += '/'
    with open(schema) as f:
        json_data = json.load(f)
    os.chdir(path)
    for file in glob.glob('*.yml'):
        print('[INFO] Processing {}'.format(file))
        with open(file, 'r+') as f:
            lines = f.readlines()
        new_file = ''
        for line in lines:
            match = re.search(_sca_file_groups, line)
            if match:
                added = list()
                standard = json_data[json_data.keys()[0]]
                standard = ''.join(standard.split('_')[0:2])
                if standard == match.groups()[0]:
                    


                ##
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

    parser.add_argument('-p', '--path', type=str, default='../../sca/', help='Sca path')
    parser.add_argument('-m', '--mapping', type=str, default='mapping.json', help='Mapping path')

    args = parser.parse_args()

    pci_to_any(args.path, args.mapping)
