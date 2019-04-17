# Building rule's test
#
# I you want learn more about lxml package visit
# https://lxml.de/
#

import os
import sys
import re
from lxml import etree


def build_test(path_xml, path_test):
    doc = etree.parse(path_xml)
    r = doc.getroot()
    file = open(path_test, "w")
    list_decoders = []
    list_parents = []

    for i in r:
        if i.tag == "rule":
            file.write("[" + i.find("description").text + "]\n")
            file.write("log 1 pass = \n")
            file.write("rule = " + i.attrib["id"] + "\n")
            file.write("alert = " + i.attrib["level"] + "\n")
            
            if i.find("decoded_as") != None:
                list_decoders.append((i.attrib["id"], i.find("decoded_as").text))
                file.write("decoder = " + i.find("decoded_as").text + "\n")
            elif i.find("if_sid") != None and i.find("decoded_as") == None:
                parent = i.find("if_sid").text
                for p in list_parents:
                    if(parent in p): parent = p[0]
                for p in list_decoders:
                    if(parent in p): file.write("decoder = " + p[1] + "\n")
                list_parents.append((parent, i.attrib["id"]))
            else:
                file.write("decoder = \n")
            
            file.write("\n")

    file.close


def check_test(path_xml, path_test):
    doc = etree.parse(path_xml)
    r = doc.getroot()
    file = open(path_test, "r")
    list = []

    for line in file:
        rule = re.search("^rule = \d+", line)
        if rule != None:
            rule = rule.group(0).split('= ')[1]
            list.append(rule)
    
    file.close
    print(list)
    file = open(path_test, "a")
    file.write("\n")
    
    for i in r:
        if i.tag == "rule" and i.attrib["id"] not in list:
            file.write("[" + i.find("description").text + "]\n")
            file.write("log 1 pass = \n")
            file.write("rule = " + i.attrib["id"] + "\n")
            file.write("alert = " + i.attrib["level"] + "\n")
            file.write("decoder = \n")
            file.write("\n")
    
    file.close


## --------------------------------------------------------
## --------------------------------------------------------

if len(sys.argv) < 2:
    print("python building_test.py path_xml path_test")
else:

    if os.path.isfile(sys.argv[1]):
        if os.path.isfile(sys.argv[2]) == False:
            build_test(sys.argv[1], sys.argv[2])
        #else:
            #check_test(sys.argv[1], sys.argv[2])
    else:
        print("XML doesn't exist")