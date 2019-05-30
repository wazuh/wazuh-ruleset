#! /usr/bin/python
# -*- coding: utf8 -*-

import argparse
import os
import json
import glob


def get_standards(schema):
    with open(schema) as f:
        json_data = json.load(f)

    keys = list()
    for s in json_data.keys():
        if s not in keys:
            splitted = s.split('_')
            if len(splitted) < 3:
                if splitted not in keys:
                    keys.append(splitted[0])
            else:
                union = '_'.join(splitted[0:2])
                if union not in keys:
                    keys.append(union)

    return keys


def add_standard(standard, actual):
    splitted = actual.strip().split(',')
    splitted.append(standard)
    for index, split in enumerate(splitted):
        splitted[index] = '"'+split+'"'
    splitted.append('\n')
    string = ', '.join(splitted)
    string = list(string)
    string.pop(-3)
    return ''.join(string)


def get_replacement(standard, schema):
    for key in standard.keys():
        version = standard[key]
        st_key = key
        to_search = (st_key+'_'+version).strip()
    if to_search in schema.keys():
        if schema[to_search] != '' and schema[to_search] not in standard:
            return schema[to_search]

    return False


def pci_to_any(path, schema):
    if list(path)[-1] != '/':
        path += '/'
    with open(schema) as f:
        json_data = json.load(f)
    list_standards = get_standards(schema)
    os.chdir(path)
    for file in glob.glob('**/*.yml', recursive=True):
        print('[INFO] Processing {}'.format(file))
        with open(file) as f:
            with open(file, 'r+') as f:
                lines = f.readlines()
            new_file = ''
            for line in lines:
                edited = False
                for standard in list_standards:
                    if '- '+standard+':' in line:
                        splitted_line = line.split('-')
                        whitespaces = splitted_line[0]
                        standard = splitted_line[1].strip().split(':')
                        standard_name = standard[0]
                        standard[1] = standard[1].replace('"', '').strip()
                        standard_versions = standard[1]
                        dict_standard = dict()
                        dict_standard[standard_name] = standard_versions
                        replacement = get_replacement(standard=dict_standard, schema=json_data)
                        if replacement:
                            new_file += whitespaces+'-'+' '+standard_name+': '+add_standard(replacement, standard_versions)
                            edited = True
                        break
                if not edited:
                    new_file += line
            with open(file, 'w') as f:
                f.write(new_file)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument('-p', '--path', type=str, default='../../sca/', help='Sca path')
    parser.add_argument('-m', '--mapping', type=str, default='mapping.json', help='Mapping path')

    args = parser.parse_args()

    pci_to_any(args.path, args.mapping)
