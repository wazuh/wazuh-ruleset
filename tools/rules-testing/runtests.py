#!/usr/bin/env python
# Copyright (C) 2015-2019, Wazuh Inc.
#
# This program is a free software; you can redistribute it
# and/or modify it under the terms of the GNU General Public
# License (version 2) as published by the FSF - Free Software
# Foundation

import ConfigParser
import subprocess
import os
import sys
import os.path
from collections import OrderedDict
import shutil

class MultiOrderedDict(OrderedDict):
    def __setitem__(self, key, value):
        if isinstance(value, list) and key in self:
            self[key].extend(value)
        else:
            super(MultiOrderedDict, self).__setitem__(key, value)

def checkConfig(initconf,path):
    if os.path.isfile(path):
        with open(path) as f:
            for line in f.readlines():
                key, value = line.rstrip("\n").split("=")
                value = value.replace("\"","")
                initconf[key] = value
        if initconf["NAME"] != "Wazuh":
            print "Name is incorrect"
            sys.exit(1)
    else:
        print "Seems like there is no Wazuh installation."
        sys.exit(1)

class OssecTester(object):
    def __init__(self, bdir):
        self._error = False
        self._debug = False
        self._quiet = False
        self._ossec_conf = bdir + "/etc/ossec.conf"
        self._base_dir = bdir
        self._ossec_path = bdir + "/bin/"
        self._test_path = "./tests"

    def buildCmd(self, rule, alert, decoder):
        cmd = ['%s/ossec-logtest' % (self._ossec_path), ]
        cmd += ['-q']
        if self._ossec_conf:
            cmd += ["-c", self._ossec_conf]
        if self._base_dir:
            cmd += ["-D", self._base_dir]
        cmd += ['-U', "%s:%s:%s" % (rule, alert, decoder)]
        return cmd
    def runTest(self, log, rule, alert, decoder, section, name, negate=False):
        p = subprocess.Popen(
                self.buildCmd(rule, alert, decoder),
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                stdin=subprocess.PIPE,
                shell=False)
        std_out = p.communicate(log)[0]
        if (p.returncode != 0 and not negate) or (p.returncode == 0 and negate):
            self._error = True
            print ""
            print "-" * 60
            print "Failed: Exit code = %s" % (p.returncode)
            print "        Alert     = %s" % (alert)
            print "        Rule      = %s" % (rule)
            print "        Decoder   = %s" % (decoder)
            print "        Section   = %s" % (section)
            print "        line name = %s" % (name)
            print " "
            print std_out
        elif self._debug:
            print "Exit code= %s" % (p.returncode)
            print std_out
        else:
            sys.stdout.write(".")

    def run(self, selective_test=False):
        for aFile in os.listdir(self._test_path):
            aFile = os.path.join(self._test_path, aFile)
            if aFile.endswith(".ini"):
                if selective_test and not aFile.endswith(selective_test):
                    continue
                print "- [ File = %s ] ---------" % (aFile)
                tGroup = ConfigParser.RawConfigParser(dict_type=MultiOrderedDict)
                tGroup.read([aFile])
                tSections = tGroup.sections()
                for t in tSections:
                    rule = tGroup.get(t, "rule")
                    alert = tGroup.get(t, "alert")
                    decoder = tGroup.get(t, "decoder")
                    for (name, value) in tGroup.items(t):
                        if name.startswith("log "):
                            if self._debug:
                                print "-" * 60
                            if name.endswith("pass"):
                                neg = False
                            elif name.endswith("fail"):
                                neg = True
                            else:
                                neg = False
                            self.runTest(value, rule, alert, decoder,
                            t, name, negate=neg)
                print ""
        if self._error:
            sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) == 2:
        selective_test = sys.argv[1]
        if not selective_test.endswith('.ini'):
            selective_test += '.ini'
    else:
        selective_test = False
        ossec_init = {}
        initconfigpath = "/etc/ossec-init.conf"
        checkConfig(ossec_init, initconfigpath)
        shutil.copy2("./rules/test_rules.xml", ossec_init["DIRECTORY"] + "/etc/rules")
        shutil.copy2("./decoders/test_decoders.xml", ossec_init["DIRECTORY"] + "/etc/decoders")
        OT = OssecTester(ossec_init["DIRECTORY"])
        OT.run(selective_test)
        os.remove(ossec_init["DIRECTORY"] + "/etc/rules/test_rules.xml")
        os.remove(ossec_init["DIRECTORY"] + "/etc/decoders/test_decoders.xml")
