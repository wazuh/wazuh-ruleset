#!/usr/bin/env python
# Wazuh Ruleset Tools: File Test

# v1.0 2016/01/08
# Copyright (C) 2015-2020, Wazuh Inc.
# Created by Wazuh, Inc. <info@wazuh.com>.
# jesus@wazuh.com
# This program is a free software; you can redistribute it and/or modify it under the terms of GPLv2

# Requirements:
#  Python 2.6 or later
#  OSSEC 2.8 or later
#  root privileges

# Instructions:
#   cd ~ && mkdir ruleset_tmp && cd ruleset_tmp
#   git clone https://github.com/wazuh/wazuh-ruleset.git
#   cd wazuh-ruleset/tools/file-testing
#   chmod +x file_test.py
#   sudo ./file_test.py

from subprocess import PIPE, Popen
import os
import sys
import getopt
import logging
import signal


def signal_handler(n_signal, frame):
    sys.exit(0)


def usage():
    msg = """
OSSEC Wazuh Ruleset Tools: File Test
Github repository: https://github.com/wazuh/wazuh-ruleset
Full documentation: http://documentation.wazuh.com/en/latest/ossec_ruleset.html

Usage: ./file_test.py -d decoder1,decoder2,decoderN -r [ruleID_Min:ruleID_Max|ruleID1,ruleID2,ruleIDN|ruleID] -f file.log [-v]

\t-d, --decoder\tA decoder or several decoders separated by ','
\t-r, --rule\tA rule, several rules separated by ',' or a rule interval (ruleID1:ruleID2)
\t-f, --file\tFile to check
\t-v, --verbose

Example: ./file_test.py -d auditd -r 80700:80760 -f audit.log
"""
    print(msg)


if __name__ == "__main__":
    R_TYPE_INTERVAL = 0
    R_TYPE_LIST = 1
    R_TYPE_RULE = 2

    logtest_path = "/var/ossec/bin/ossec-logtest"

    logger = logging.getLogger('logger_verbose')

    mandatory_args = 0
    verbose = False

    # Capture Cntrl + C
    signal.signal(signal.SIGINT, signal_handler)

    # Check sudo
    if os.geteuid() != 0:
        sys.exit("You need root privileges to run this script. Please try again, using 'sudo'. Exiting.")

    # Check arguments
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hvd:r:f:",
                                   ["decoder=", "rule=", "file=", "help", "verbose"])
        if not opts or not (1 == len(opts) or 3 == len(opts) or 4 == len(opts)):
            print("Incorrect number of arguments. \nTry './file_test.py --help' for more information.")
            sys.exit()
    except getopt.GetoptError as err:
        print(str(err))
        print("Try './file_test.py --help' for more information.")
        sys.exit(2)

    for o, a in opts:
        if o in ("-d", "--decoder"):
            match_decoders = a.split(",")
            mandatory_args += 1
        elif o in ("-r", "--rule"):
            if ":" in a:
                match_id_rule_min = int(a.split(":")[0])
                match_id_rule_max = int(a.split(":")[1])
                rule_type = R_TYPE_INTERVAL
            elif "," in a:
                rule_type = R_TYPE_LIST
                match_id_rules = [int(x) for x in a.split(",")]
            else:
                rule_type = R_TYPE_RULE
                match_id_rule = int(a)
            mandatory_args += 1
        elif o in ("-f", "--file"):
            filename = a
            mandatory_args += 1
        elif o in ("-v", "--verbose"):
            logger.setLevel(logging.DEBUG)
            ch = logging.StreamHandler()
            ch.setLevel(logging.DEBUG)
            formatter = logging.Formatter('%(message)s')
            ch.setFormatter(formatter)
            logger.addHandler(ch)
        elif o in ("-h", "--help"):
            usage()
            sys.exit()
        else:
            usage()
            sys.exit()

    if mandatory_args != 3:
        print("Mandatory arguments: -d -r -f")
        usage()
        sys.exit()

    str_rules = "?"
    if rule_type == R_TYPE_INTERVAL:
        str_rules = "Interval rules: {0} - {1}".format(match_id_rule_min, match_id_rule_max)
    elif rule_type == R_TYPE_LIST:
        str_rules = "List rules: {0}".format(match_id_rules)
    elif rule_type == R_TYPE_RULE:
        str_rules = "Rule: {0}".format(match_id_rule)

    print("\nChecking '{0}'\n\tDecoder match: {1}\n\t{2}\n".format(filename, match_decoders, str_rules))

    log_file = open(filename)

    filename_decoder_ko = "{0}.decoder.ko".format(filename)
    filename_rules_ko = "{0}.rules.ko".format(filename)
    log_file_decoder_ko = open(filename_decoder_ko, 'w')
    log_file_rules_ko = open(filename_rules_ko, 'w')
    n_line = 0
    n_decoder_ko = 0
    n_rules_ko = 0

    tam = 0
    for line in open(filename).xreadlines():
        tam += 1

    for line in log_file:
        # Get log
        n_line += 1
        log_line = line.rstrip()
        logger.debug("\nLine [{0}]: '{1}'".format(n_line, log_line))

        # Get logtest output: Decoder and rule id
        p = Popen([logtest_path], stdin=PIPE, stdout=PIPE, stderr=PIPE)
        std_out, std_err = p.communicate(log_line)
        decoder = None
        rule = None
        for line_output in std_err.split(os.linesep):
            if "decoder: '" in line_output:
                decoder = line_output.split("'")[1]
            elif "Rule id: '" in line_output:
                rule = int(line_output.split("'")[1])

        # Check Decoder
        logger.debug("\tDecoder: {0}".format(decoder))
        decoders_ok = False
        for match_decoder in match_decoders:
            if decoder == match_decoder:
                logger.debug("\t\t== {0}? [OK]".format(match_decoder))
                decoders_ok = True
                break
            else:
                logger.debug("\t\t== {0}? [KO]".format(match_decoder))

        if not decoders_ok:
            n_decoder_ko += 1
            log_file_decoder_ko.write("Line {0}:{1}\n".format(n_line, log_line))

        # Check Rule ID
        if rule_type == R_TYPE_INTERVAL:
            match_rules = list(range(match_id_rule_min, match_id_rule_max))
        elif rule_type == R_TYPE_LIST:
            match_rules = match_id_rules
        elif rule_type == R_TYPE_RULE:
            match_rules = [match_id_rule]

        logger.debug("\tRule: {0}".format(rule))
        rules_ok = False
        for match_rule in match_rules:
            if rule == match_rule:
                logger.debug("\t\t== {0}? [OK]".format(match_rule))
                rules_ok = True
                break
            else:
                logger.debug("\t\t== {0}? [KO]".format(match_rule))

        if not rules_ok:
            n_rules_ko += 1
            log_file_rules_ko.write("Line {0}:{1}\n".format(n_line, log_line))

        p = (n_line * 100) / float(tam)
        sys.stdout.write("Progress: %.2f%%   \r" % p)
        sys.stdout.flush()

    print("\n\nResult:")

    p_decoder_ko = (n_decoder_ko/float(n_line))*100
    p_rules_ko = (n_rules_ko/float(n_line))*100

    print("\tDecoders KO: %.2f%%   \r" % p_decoder_ko)
    print("\tRules KO: %.2f%%   \r" % p_rules_ko)
    print("\nOutput files:\n\t{0}\n\t{1}".format(filename_decoder_ko, filename_rules_ko))

    log_file.close()
    log_file_decoder_ko.close()
    log_file_rules_ko.close()
