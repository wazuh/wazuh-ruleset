#! /usr/bin/python
# -*- coding: utf8 -*-

import argparse
import os
import json
import glob
import ruamel.yaml
from collections import OrderedDict


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


def add_standard(actual_compliances, schema, schema_total):
    for actual_compliance in actual_compliances:
        for key, values in actual_compliance.items():
            try:
                for value in values.split(', '):
                    for version in schema[key]:
                        if version == value:
                            new_key = OrderedDict()
                            new_key_v = schema_total[key + '_' + value].split('_')[0]
                            new_values = ruamel.yaml.scalarstring.DoubleQuotedScalarString('')
                            for index_c, ver_c in enumerate(schema_total[key + '_' + value].split(',')):
                                for index, ver in enumerate(ver_c.split('_')):
                                    if index % 2 != 0:
                                        new_values += ','+ruamel.yaml.scalarstring.DoubleQuotedScalarString(ver)
                            for split in new_values.split(','):
                                try:
                                    if new_key[new_key_v] != '':
                                        new_key[new_key_v] += ruamel.yaml.scalarstring.DoubleQuotedScalarString(', ' +
                                                                                                                split)
                                    else:
                                        new_key[new_key_v] = ruamel.yaml.scalarstring.DoubleQuotedScalarString(split)
                                except:
                                    new_key[new_key_v] = ruamel.yaml.scalarstring.DoubleQuotedScalarString(split)
                            try:
                                if actual_compliances[-1].keys() == new_key.keys():
                                    for ke in actual_compliances[-1].keys():
                                        for new_vaa in new_key[ke].split(', '):
                                            if new_vaa not in actual_compliances[-1][ke]:
                                                actual_compliances[-1][ke] = \
                                                    ruamel.yaml.scalarstring.DoubleQuotedScalarString(
                                                        actual_compliances[-1][ke]+', '+new_vaa)
                                else:
                                    actual_compliances.append(new_key)
                            except:
                                pass
            except:
                pass


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
            for element in yaml_file['checks']:
                add_standard(element['compliance'], list_standards, json_data)

        with open(file, 'w') as f:
            yaml = ruamel.yaml.YAML()
            yaml.width = 4096
            yaml.Representer.add_representer(OrderedDict, yaml.Representer.represent_dict)
            yaml.dump(yaml_file, f)

        break


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument('-p', '--path', type=str, default='../../sca/', help='Sca path')
    parser.add_argument('-m', '--mapping', type=str, default='mapping.json', help='Mapping path')

    args = parser.parse_args()

    pci_to_any(args.path, args.mapping)
