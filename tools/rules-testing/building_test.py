# Building rule's test
#
# If you want learn more about lxml package visit
# https://lxml.de/
#

import os
import sys
import re
from lxml import etree


def build_test(path_xml, path_test, rules_write = []):

    try:
        doc = etree.parse(path_xml)
        r = doc.getroot()
    except:
        print("Can't open " + path_xml + " as lxml's tree")
        return False

    try:
        file = open(path_test, "a")
        file.write("\n"+"\n")
    except:
        print("Can't open " + path_test)
        return False

    list = []
    decoder = ""

    for i in r:

        if i.tag == "rule":
            if i.find("decoded_as") != None:
                list.append([i.attrib["id"], i.find("decoded_as").text])
                decoder = i.find("decoded_as").text
            elif i.find("decoded_as") == None and i.find("if_sid") != None:
                parent = i.find("if_sid").text
                for p in list:
                    if(parent in p):
                        decoder = p[1]
                        p.append(i.attrib["id"])
            else:
                decoder = ""

            if i.attrib["id"] not in rules_write:
                file.write("[" + i.find("description").text + "]\n")
                file.write("log 1 pass = \n")
                file.write("rule = " + i.attrib["id"] + "\n")
                file.write("alert = " + i.attrib["level"] + "\n")
                file.write("decoder = " + decoder + "\n")
                file.write("\n")

    file.close
    return True


def check_test(path_xml, path_test):
    file = open(path_test, "r")
    list = []

    for line in file:
        rule = re.search("^rule = \d+", line)
        if rule != None:
            rule = rule.group(0).split('= ')[1]
            list.append(rule)
    
    file.close
    return build_test(path_xml, path_test, list)


## --------------------------------------------------------
## --------------------------------------------------------

if len(sys.argv) < 2:
    print("python building_test.py path_xml path_test")
else:

    if os.path.isfile(sys.argv[1]):
        if os.path.isfile(sys.argv[2]) == False:
            if build_test(sys.argv[1], sys.argv[2]):
                print("OK")
            else:
                print("Built failed")
        else:
            if check_test(sys.argv[1], sys.argv[2]):
                print("OK")
            else:
                print("Built failed")
    else:
        print("XML doesn't exist")