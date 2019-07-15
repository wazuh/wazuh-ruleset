#! /usr/bin/python
# -*- coding: utf8 -*-

import argparse
import os
import json
import glob
import re
import ruamel.yaml
from collections import OrderedDict


# Return a dict with key (cis, pci, pci_dss...) and version

class FlowList(list):
    pass



def represent_flow_seq(dumper, data):
    """
    Dump sequences in flow style
    """
    return dumper.represent_sequence(u'tag:yaml.org,2002:seq', data, flow_style=True)


def get_standards(schema):
    with open(schema) as f:
        json_data = json.load(f)

    dict_standards = dict()
    for s in json_data.keys():
        if s not in dict_standards.keys():
            splitted = s.split('_')
            if len(splitted) == 1:
                dict_standards[splitted] = splitted
            else:
                union = '_'.join(splitted[0:-1])
                if union not in list(dict_standards.keys()):
                    dict_standards[union] = list()
                dict_standards[union].append(splitted[2])

    return dict_standards


def add_standard(actual_compliances, schema, schema_total):
    comma_sep = re.compile('\s*,\s*')

    for actual_compliance in actual_compliances:
        for key, values in actual_compliance.items():
            try:
                for value in values:
                    for version in schema[key]:
                        if version == value:
                            new_key = OrderedDict()
                            new_key_v = None
                            for v in comma_sep.split(schema_total[key + '_' + value].strip()):
                                new_key_v = v.split('_')[0:len(v.split('_'))-1]
                                new_key_v = '_'.join(new_key_v)
                            new_values = []
                            for index_c, ver_c in enumerate(comma_sep.split(schema_total[key + '_' + value])):
                                new_values += \
                                    [ruamel.yaml.scalarstring.DoubleQuotedScalarString(ver_c.split('_')[-1])]

                            try:
                                if isinstance(new_key[new_key_v], list):
                                    new_key[new_key_v] += new_values
                                else:
                                    new_key[new_key_v] = new_values
                            except KeyError:
                                new_key[new_key_v] = new_values

                            new_key[new_key_v] = FlowList(new_key[new_key_v])

                            try:
                                if actual_compliances[-1].keys() == new_key.keys():
                                    for ke in actual_compliances[-1].keys():
                                        for new_vaa in new_key[ke]:
                                            if new_vaa not in actual_compliances[-1][ke]:
                                                actual_compliances[-1][ke] += \
                                                    [ruamel.yaml.scalarstring.DoubleQuotedScalarString(new_vaa)]

                                else:
                                    #for k, v in new_key.items():
                                    #    new_key[k] = v
                                    pass

                                    actual_compliances.append(new_key)
                            except Exception as e:
                                pass
            except Exception as e:
                pass


def standard_to_any(path, schema):
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
                try:
                    add_standard(element['compliance'], list_standards, json_data)
                except:
                    pass

        with open(file, 'w') as f:
            yaml = ruamel.yaml.YAML()
            yaml.width = 4096
            yaml.Representer.add_representer(OrderedDict, yaml.Representer.represent_dict)
            yaml.Representer.add_representer(FlowList, represent_flow_seq)
            yaml.indent(mapping=2, sequence=4, offset=2)
            yaml.dump(yaml_file, f)


def delete_standard(path, standard):
    if list(path)[-1] != '/':
        path += '/'
    os.chdir(path)
    for file in glob.glob('**/*.yml', recursive=True):
        changed = False
        with open(file) as f:
            yaml_file = ruamel.yaml.round_trip_load(f, preserve_quotes=True)
            for element in yaml_file['checks']:
                try:
                    for index, key in enumerate(element['compliance']):
                        for k in key:
                            if k == standard:
                                element['compliance'].pop(index)
                                changed = True
                except:
                    pass

        with open(file, 'w') as f:
            yaml = ruamel.yaml.YAML()
            yaml.width = 4096
            yaml.Representer.add_representer(OrderedDict, yaml.Representer.represent_dict)
            yaml.Representer.add_representer(FlowList, represent_flow_seq)
            yaml.indent(mapping=2, sequence=4, offset=2)
            yaml.dump(yaml_file, f)

        if changed:
            print('[DELETE] Deleted {} in file {}'.format(standard, file))


if __name__ == '__main__':

    parser = argparse.ArgumentParser()

    parser.add_argument('-p', '--path', type=str, default='../../sca/', help='Sca path')
    parser.add_argument('-m', '--mapping', type=str, default='mapping.json', help='Mapping path')
    parser.add_argument('-d', '--delete', type=str, default='', help='Standard to be delete')

    args = parser.parse_args()

    if args.delete == '':
        standard_to_any(args.path, args.mapping)
    else:
        delete_standard(args.path, args.delete)

