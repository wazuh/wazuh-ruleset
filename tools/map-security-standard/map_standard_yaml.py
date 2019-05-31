#! /usr/bin/python
# -*- coding: utf8 -*-

import argparse
import os
import json
import glob
import ruamel.yaml


# Return a dict with key (cis, pci, pci_dss...) and version

def get_standards(schema):
    with open(schema) as f:
        json_data = json.load(f)

    dict_standards = dict()
    for s in json_data.keys():
        if s not in dict_standards.keys():
            splitted = s.split('_')
            if len(splitted) < 3:
                if splitted[0] not in list(dict_standards.keys()):
                    dict_standards[splitted[0]] = list()
                dict_standards[splitted[0]].append(splitted[1])
            else:
                union = '_'.join(splitted[0:2])
                if union not in list(dict_standards.keys()):
                    dict_standards[union] = list()
                dict_standards[union].append(splitted[2])

    return dict_standards


def parse_standard(standard):
    st = standard.strip().split(',')
    for index, s in enumerate(st):
        st[index] = s.split('_')

    return st


def add_standard(standard, schema, schema_total):
    for key, value in standard.items():
        if key in schema.keys():
            for v in schema[key]:
                for va in value.split(', '):
                    if va == v:
                        if key+'_'+va in schema_total.keys():
                            parse_st = parse_standard(schema_total[key + '_' + va])
                            if not parse_st:
                                continue
                            if len(schema_total[key+'_'+va].split(',')) == 1:
                                if parse_st:
                                    if parse_st[0][0] not in standard.keys():
                                        standard[parse_st[0][0]] = \
                                            ruamel.yaml.scalarstring.DoubleQuotedScalarString(parse_st[0][1])
                                    if parse_st[0][1] not in standard[parse_st[0][0]]:
                                        standard[parse_st[0][0]] += \
                                            ', '+ruamel.yaml.scalarstring.DoubleQuotedScalarString(parse_st[0][1])
                            else:
                                for pa in parse_st:
                                    if pa[0] not in standard.keys():
                                        standard[pa[0]] = ruamel.yaml.scalarstring.DoubleQuotedScalarString(pa[1])
                                    else:
                                        if pa[1] not in standard[pa[0]]:
                                            standard[pa[0]] += ', '+pa[1]


# yaml_file['checks'][0]['compliance'][0]['cis']


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
            yaml_file = ruamel.yaml.round_trip_load(f, preserve_quotes=True)
            for id in yaml_file['checks']:
                for compliance in id['compliance']:
                    add_standard(compliance, list_standards, json_data)

        with open(file, 'w') as f:
            yaml = ruamel.yaml.YAML()
            yaml.width = 4096
            yaml.dump(yaml_file, f)

        break


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument('-p', '--path', type=str, default='../../sca/', help='Sca path')
    parser.add_argument('-m', '--mapping', type=str, default='mapping.json', help='Mapping path')

    args = parser.parse_args()

    pci_to_any(args.path, args.mapping)








# import argparse
# import os
# import json
# import glob
#
#
# def get_standards(schema):
#     with open(schema) as f:
#         json_data = json.load(f)
#
#     keys = list()
#     for s in json_data.keys():
#         if s not in keys:
#             splitted = s.split('_')
#             if len(splitted) < 3:
#                 if splitted not in keys:
#                     keys.append(splitted[0])
#             else:
#                 union = '_'.join(splitted[0:2])
#                 if union not in keys:
#                     keys.append(union)
#
#     return keys
#
#
# def add_standard(standard, actual):
#     splitted = actual.strip().split(',')
#     splitted.append(standard)
#     for index, split in enumerate(splitted):
#         splitted[index] = '"'+split+'"'
#     splitted.append('\n')
#     string = ', '.join(splitted)
#     string = list(string)
#     string.pop(-3)
#     return ''.join(string)
#
#
# def get_new_line(standard, schema):
#     for key in standard.keys():
#         version = standard[key]
#         st_key = key
#         to_search = (st_key+'_'+version).strip()
#     if to_search in schema.keys():
#         schema_split = schema[to_search].strip().split(',')
#         for st in schema_split:
#             if st != '' and st not in standard:
#                 return schema[to_search]
#
#     return False
#
#
# def pci_to_any(path, schema):
#     if list(path)[-1] != '/':
#         path += '/'
#     with open(schema) as f:
#         json_data = json.load(f)
#     list_standards = get_standards(schema)
#     os.chdir(path)
#     for file in glob.glob('**/*.yml', recursive=True):
#         print('[INFO] Processing {}'.format(file))
#         with open(file) as f:
#             with open(file, 'r+') as f:
#                 lines = f.readlines()
#             new_file = ''
#             for line in lines:
#                 edited = False
#                 for standard in list_standards:
#                     if '- '+standard+':' in line:
#                         actual_line = line
#                         splitted_line = line.split('-')
#                         whitespaces = splitted_line[0]
#                         standard = splitted_line[1].strip().split(':')
#                         standard_name = standard[0]
#                         standard[1] = standard[1].replace('"', '').strip()
#                         standard_versions = standard[1]
#                         dict_standard = dict()
#                         dict_standard[standard_name] = standard_versions
#                         new_standard = get_new_line(standard=dict_standard, schema=json_data)
#                         if new_standard:
#                             new_file += whitespaces+'-'+' '+standard_name+': '+add_standard(replacement, standard_versions)
#                             edited = True
#                         break
#                 if not edited:
#                     new_file += line
#             with open(file, 'w') as f:
#                 f.write(new_file)
#
#
# if __name__ == '__main__':
#     parser = argparse.ArgumentParser()
#
#     parser.add_argument('-p', '--path', type=str, default='../../sca/', help='Sca path')
#     parser.add_argument('-m', '--mapping', type=str, default='mapping.json', help='Mapping path')
#
#     args = parser.parse_args()
#
#     pci_to_any(args.path, args.mapping)
