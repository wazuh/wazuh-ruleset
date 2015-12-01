#!/usr/bin/env python
# OSSEC Ruleset Updater

# v1.1 2015/11/30
# Created by Wazuh, Inc. <info@wazuh.com>.
# This program is a free software; you can redistribute it and/or modify it under the terms of GPLv2

# Instructions:
#   cd ~ && mkdir ruleset_tmp && cd ruleset_tmp
#   git clone https://github.com/wazuh/ossec-rules.git
#   cd ossec-rules
#   chmod +x ossec_ruleset.py
#   sudo ./ossec_ruleset.py

import os
import sys
import getopt
import shutil
import glob
import re
import fileinput
import signal
from datetime import date
import hashlib
import zipfile
import pwd
import grp
import contextlib

try:
    from urllib2 import urlopen, URLError, HTTPError
except:
    # Python 3
    from urllib.request import urlopen


# Log class
class LogFile(object):
    """Print to stdout and file"""

    def __init__(self, name=None):
        self.stdout = True
        self.log_out = True
        try:
            self.logger = open(name, 'a')
        except:
            print("Error opening log \"{0}".format(name))

    def set_ouput(self, stdout=True, log=True):
        self.stdout = stdout
        self.log_out = log

    def log(self, str_output):
        if self.stdout:
            print(str_output)
        if self.log_out:
            self.logger.write("{0}\n".format(str_output))

    def __del__(self):
        self.logger.close()


# Aux functions
def get_ruleset_version():
    try:
        f_version = open("VERSION")
        rs_version = f_version.read().rstrip('\n')
        f_version.close()
    except:
        rs_version = "0.100"

    return rs_version


def regex_in_file(regex, filepath):
    with open(filepath) as f:
        m = re.search(regex, f.read())
        if m:
            return True
        else:
            return False


def replace_text_in_file(old_text_init, old_text_end, new_text, filepath):
    replace = False

    f = open(filepath)
    text = f.read()
    f.close()

    if old_text_init in text and old_text_end in text:
        for line in fileinput.input(filepath, inplace=True):
            if old_text_init in line.strip():
                replace = True
            elif old_text_end in line.strip():
                replace = False
                print(new_text)
                continue

            if not replace:
                print(line.rstrip("\n"))
        fileinput.close()

        return True
    else:
        return False


def write_before_line(line_search, new_text, filepath):
    for line in fileinput.input(filepath, inplace=True):
        if line_search in line.strip():
            print(new_text)
        print(line.rstrip("\n"))
    fileinput.close()


def write_after_line(line_search, new_text, filepath):
    for line in fileinput.input(filepath, inplace=True):
        print(line.rstrip("\n"))
        if line_search in line.strip():
            print(new_text)
    fileinput.close()


def signal_handler(n_signal, frame):
    sys.exit(0)


def get_item_between_label(label, filepath):
    f = open(filepath)

    label_s = "<{0}>".format(label)
    label_e = "</{0}>".format(label)
    lines = []
    save_lines = False
    for line in f.readlines():
        if save_lines:
            match = re.search(r'\s*<.+>(.+)</.+>', line)
            if match:
                lines.append(match.group(1))

        if label_s in line:
            save_lines = True
        elif label_e in line:
            break

    f.close()

    return lines


def download_file(url, output_file):
    try:
        f = urlopen(url)

        with open(output_file, "wb") as local_file:
            local_file.write(f.read())

    except HTTPError as e:
        logger.log("HTTP Error {0}: {1}".format(e.code, url))
        sys.exit(2)
    except URLError as e:
        logger.log("URL Error - {0}: {1}".format(e.reason, url))
        sys.exit(2)
    except Exception as e:
        logger.log("Download error:{0}.\nExit.".format(e))
        sys.exit(2)


def chown_r(path, uid, gid):
    if os.path.isdir(path):
        os.chown(path, uid, gid)
        for item in os.listdir(path):
            itempath = os.path.join(path, item)
            if os.path.isfile(itempath):
                os.chown(itempath, uid, gid)
            elif os.path.isdir(itempath):
                chown_r(itempath, uid, gid)


# Ruleset functions

def get_ruleset_from_menu(type_ruleset):
    """
    :param type_ruleset: rules, rootchecks, all
    :return: ruleset to install
    """
    directories = []

    ruleset_menu = {"rules": [], "rootchecks": []}

    if type_ruleset == "rules" or type_ruleset == "all":
        directories.append("rules-decoders")
    if type_ruleset == "rootchecks" or type_ruleset == "all":
        directories.append("rootcheck")

    for directory in directories:
        type_directory = "rules" if "rules" in directory else "rootchecks"

        ruleset_select = []

        # Get name of the new rules/rootchecks
        menu_ruleset = [name for name in os.listdir(directory) if os.path.isdir(os.path.join(directory, name))]

        # OSSEC is already installed -> remove from menu_ruleset
        sorted(menu_ruleset)
        if "ossec" in menu_ruleset:
            menu_ruleset.remove("ossec")

        title_str = "OSSEC Wazuh Ruleset, {0}\n\nUse ENTER key to select/unselect {1}:\n".format(today_date,
                                                                                                 type_directory)

        if menu_ruleset:
            toggle = []
            for i in range(len(menu_ruleset)):
                toggle.append(' ')

            read_input = True
            while read_input:
                os.system("clear")
                print(title_str)

                i = 1
                for rule in menu_ruleset:
                    print("{0}. [{1}] {2}".format(i, toggle[i - 1], rule))
                    i += 1
                print("{0}. Confirm and continue.".format(i))

                try:
                    ans = raw_input("\nOption: ")
                except:
                    # Python 3
                    ans = input("\nOption: ")
                try:
                    option = int(ans) - 1
                except Exception:
                    continue

                if 0 <= option < len(menu_ruleset):  # Option 1 -> n
                    if toggle[option] == "X":
                        toggle[option] = " "
                    else:
                        toggle[option] = "X"
                elif option == (i - 1):  # Option Done
                    read_input = False

            for i in range(len(toggle)):
                if toggle[i] == "X":
                    ruleset_select.append(menu_ruleset[i])

            ruleset_menu[type_directory] = ruleset_select

    print("")
    return ruleset_menu


def get_ruleset_from_file(filename, type_r):
    """
    :param filename: File with ruleset to install. Format:
        # comment
        \n
        rules:name_rule
        rootchecks:name_rootcheck
    :param type_r: rules (get rules) rootchecks (get rootchecks)
    :return: ruleset to install
    """

    logger.log("Reading configuration file {0}".format(filename))

    ruleset_file = {"rules": [], "rootchecks": []}
    rules_file = []
    rootchecks_file = []
    try:
        file_config = open(filename)
        i = 1
        for line in file_config:
            if re.match("(^rootchecks|rules):.+", line) is not None:
                if "rules" in line:
                    rules_file.append(line.split(":")[1].rstrip('\n').strip())
                elif "rootchecks" in line:
                    rootchecks_file.append(line.split(":")[1].rstrip('\n').strip())
            elif re.match("^#.*", line) is not None or re.match("^\s*\n", line) is not None:
                continue
            else:
                logger.log("Syntax error in line [{0}]: ->{1}<-".format(i, line))
                sys.exit(2)
            i += 1
        file_config.close()
    except Exception as e:
        logger.log("Error reading config file:{0}.\nExit.".format(e))
        sys.exit(2)

    if rules_file:
        if "ossec" in rules_file:
            logger.log("Error reading config file: \"ossec\" item found")
            logger.log("\tIt is assumed that the default rootchecks are installed.")
            logger.log("\tIf you want to update it, please use the option -u")
            sys.exit(2)

        directory = "rules-decoders"
        new_ruleset = os.listdir(directory)

        for rs_f in rules_file:
            if rs_f not in new_ruleset:
                logger.log("Error: {0} not in folder {1}".format(rs_f, directory))
                sys.exit(2)

    if rootchecks_file:
        if "ossec" in rootchecks_file:
            logger.log("Error reading config file: \"ossec\" item found")
            logger.log("\tIt is assumed that the default rootchecks are installed.")
            logger.log("\tIf you want to update it, please use the option -u")
            sys.exit(2)

        directory = "rootcheck"
        new_ruleset = os.listdir(directory)

        for rs_f in rootchecks_file:
            if rs_f not in new_ruleset:
                logger.log("Error: {0} not in folder {1}".format(rs_f, directory))
                sys.exit(2)

    if type_r == "rules" or type_r == "all":
        ruleset_file["rules"] = rules_file
    if type_r == "rootchecks" or type_r == "all":
        ruleset_file["rootchecks"] = rootchecks_file

    logger.log("\t[Done]\n")
    return ruleset_file


def get_ruleset_from_update(type_ruleset):
    ruleset_update = {"rules": [], "rootchecks": []}

    logger.log("Downloading new ruleset ...")

    # FixMe: New structure
    print("FixMe: New structure")
    return ruleset_update

    # Get installed ruleset
    ossec_conf = "{0}/etc/ossec.conf".format(ossec_path)
    if type_ruleset == "rules" or type_ruleset == "all":
        installed_rules = get_item_between_label("rules", ossec_conf)

    if type_ruleset == "rootchecks" or type_ruleset == "all":
        installed_rootchecks = get_item_between_label("rootcheck", ossec_conf)

    # Download new ruleset and extract all files
    downloads_directory = "./downloads"
    output = "{0}/ruleset.zip".format(downloads_directory)
    last_update = "last_update"

    if not os.path.exists(downloads_directory):
        os.makedirs(downloads_directory)

    # Check sha
    try:
        f_last_update = open(last_update)
        type_r_old, zip_sha_old = f_last_update.readlines()[0].split(":")
        f_last_update.close()
    except:
        type_r_old = ""
        zip_sha_old = ""

    # Download file and create sha
    download_file(url_ruleset, output)

    zip_sha = hashlib.sha256(open(output, 'rb').read()).hexdigest()

    if zip_sha != zip_sha_old or type_ruleset != type_r_old:
        old_extracted_files = "{0}/ossec-rules/".format(downloads_directory)
        if os.path.exists(old_extracted_files):
            shutil.rmtree(old_extracted_files)

        with contextlib.closing(zipfile.ZipFile(output)) as z:
            z.extractall(downloads_directory)

        # Get ruleset to update
        # FixMe:
        # Update only those rules/rootchecks that have changed.
        rules_update = []
        rootchecks_update = []
        if type_ruleset == "rules" or type_ruleset == "all":
            new_rules_path = "{0}/ossec-rules/rules-decoders/".format(downloads_directory)
            rules_update.append("ossec")
            for new_rule in os.listdir(new_rules_path):
                if new_rule == "ossec":
                    continue

                new_rule_ossec_conf = "{0}_rules.xml".format(new_rule)
                if new_rule_ossec_conf in installed_rules:
                    rules_update.append(new_rule)

        if type_ruleset == "rootchecks" or type_ruleset == "all":
            new_rootchecks_path = "{0}/ossec-rules/rootcheck/".format(downloads_directory)
            rootchecks_update.append("ossec")
            for new_rc in os.listdir(new_rootchecks_path):
                if new_rc == "ossec":
                    continue

                new_rc_ossec_conf = "{0}/etc/shared/{1}/.+\.txt".format(ossec_path, new_rc)

                for ins_rc in installed_rootchecks:
                    match = re.search(new_rc_ossec_conf, ins_rc)
                    if match:
                        rootchecks_update.append(new_rc)
                        break

        # Update main directory and remove Downloads
        move_dirs = ["rules-decoders", "rootcheck"]
        for dest_dir in move_dirs:
            src_dir = "{0}/ossec-rules/{1}".format(downloads_directory, dest_dir)
            if os.path.exists(dest_dir):
                shutil.rmtree(dest_dir)
            shutil.copytree(src_dir, dest_dir)

        shutil.copyfile("{0}/ossec-rules/VERSION".format(downloads_directory), "VERSION")

        new_python_script = "{0}/ossec-rules/ossec_ruleset.py".format(downloads_directory)
        if os.path.isfile(new_python_script):
            logger.log("Updating ossec_ruleset.py...")
            shutil.copyfile(new_python_script, "ossec_ruleset.py")

        if os.path.exists(downloads_directory):
            shutil.rmtree(downloads_directory)

        global ruleset_version
        ruleset_version = get_ruleset_version()

        # Save ruleset
        ruleset_update["rules"] = rules_update
        ruleset_update["rootchecks"] = rootchecks_update

        f_last_update = open(last_update, 'w')
        f_last_update.write("{0}:{1}".format(type_ruleset, zip_sha))
        f_last_update.close()
    else:
        msg = "\tRuleset({0}) up to date".format(ruleset_version)
        logger.log(msg)

    logger.log("\t[Done]\n")
    return ruleset_update


def setup_decoders(decoder):
    if decoder == "ossec":
        src_dir = "./rules-decoders/ossec/decoders"
        dest_dir = "{0}/etc/ossec_decoders".format(ossec_path)

        if os.path.exists(dest_dir):
            shutil.rmtree(dest_dir)

        logger.log("\t\t**Overwriting** {0}".format(dest_dir))

        shutil.copytree(src_dir, dest_dir)
        chown_r(dest_dir, root_uid, ossec_gid)
    else:
        decoders_wazuh_directory = "{0}/etc/wazuh_decoders".format(ossec_path)
        if not os.path.exists(decoders_wazuh_directory):
            os.makedirs(decoders_wazuh_directory)

        new_decoder = "./rules-decoders/{0}/{0}_decoders.xml".format(decoder)
        dest_new_decoder = "{0}/etc/wazuh_decoders/{1}_decoders.xml".format(ossec_path, decoder)
        shutil.copyfile(new_decoder, dest_new_decoder)

        chown_r(decoders_wazuh_directory, root_uid, ossec_gid)


def setup_rules(rule):
    if rule == "ossec":
        new_rules_path = "./rules-decoders/ossec/rules/*_rules.xml"
        ossec_rules = sorted(glob.glob(new_rules_path))

        for ossec_rule in ossec_rules:
            # Do not copy local_rules.xml
            if os.path.isfile(ossec_rule) and "local_rules.xml" not in ossec_rule:
                split = ossec_rule.split("/")
                filename = split[len(split) - 1]
                dest_file = "{0}/rules/{1}".format(ossec_path, filename)
                shutil.copyfile(ossec_rule, dest_file)
                os.chown(dest_file, root_uid, ossec_gid)

    else:
        src_file = "./rules-decoders/{0}/{0}_rules.xml".format(rule)
        dest_file = "{0}/rules/{1}_rules.xml".format(ossec_path, rule)
        shutil.copyfile(src_file, dest_file)
        os.chown(dest_file, root_uid, ossec_gid)


def setup_roochecks(rootcheck):
    src_dir = "./rootcheck/{0}".format(rootcheck)
    dest_dir = "{0}/etc/shared/{1}".format(ossec_path, rootcheck)
    if os.path.exists(dest_dir):
        shutil.rmtree(dest_dir)
    shutil.copytree(src_dir, dest_dir)
    chown_r(dest_dir, root_uid, ossec_gid)


def setup_ossec_conf(item, type_item):
    ossec_conf = "{0}/etc/ossec.conf".format(ossec_path)

    # Check decoders
    # OSSEC Decoders
    old_decoder = "{0}/etc/decoder.xml".format(ossec_path)
    try:
        if os.path.exists(old_decoder):
            os.remove(old_decoder)
    except Exception as e:
            logger.log("Error:{0}.\n".format(e))
            logger.log("Please, remove {0} because it is no longer used".format(old_decoder))

    str_decoder = "<decoder_dir>etc/ossec_decoders</decoder_dir>"
    if not regex_in_file(str_decoder, ossec_conf):
        write_after_line("<rules>", "    {0}".format(str_decoder), ossec_conf)
        logger.log("\t\t{0} added in ossec.conf".format(str_decoder))

    # Local decoder
    path_decoder_local = "{0}/etc/local_decoder.xml".format(ossec_path)
    if not os.path.exists(path_decoder_local):
        # Create local decoder
        text = ("<!-- Local Decoders -->\n"
                "<decoder name=\"local_decoder_example\">\n"
                "    <program_name>local_decoder_example</program_name>\n"
                "</decoder>\n")
        f_local_decoder = open(path_decoder_local, 'a')
        f_local_decoder.write(text)
        f_local_decoder.close()
        os.chown(path_decoder_local, root_uid, ossec_gid)

    str_decoder_local = "<decoder>etc/local_decoder.xml</decoder>"
    if not regex_in_file(str_decoder_local, ossec_conf):
        write_after_line(str_decoder, "    {0}".format(str_decoder_local), ossec_conf)
        logger.log("\t\t{0} added in ossec.conf".format(str_decoder_local))

    # Wazuh decoders
    str_decoder_wazuh = "<decoder_dir>etc/wazuh_decoders</decoder_dir>"
    if not regex_in_file(str_decoder_wazuh, ossec_conf):
        write_after_line(str_decoder_local, "    {0}".format(str_decoder_wazuh), ossec_conf)
        logger.log("\t\t{0} added in ossec.conf".format(str_decoder_wazuh))

    # Include Rules & Rootchecks
    if type_item == "rule":
        # Include new rules
        if item != "ossec":
            if regex_in_file("\s*<include>{0}_rules.xml</include>".format(item), ossec_conf):
                logger.log("\t\tRules \"{0}\" already exist in ossec.conf".format(item))
            else:
                logger.log("\t\tIncluding \"{0}\" in ossec.conf ...".format(item))
                write_before_line("</rules>", '    <include>{0}_rules.xml</include>'.format(item), ossec_conf)
                # else:
                # Note: ossec rules are included in ossec.conf by default
                # logger.log("\t\t**It is assumed that the default rules are included in ossec.conf**")

    elif type_item == "rootcheck":
        if item != "ossec":
            types_rc = ["rootkit_files", "rootkit_trojans", "system_audit", "win_applications", "win_audit",
                        "win_malware"]

            dest_dir = "{0}/etc/shared/{1}".format(ossec_path, item)

            for new_rc in os.listdir(dest_dir):
                new_rc = "{0}/{1}".format(dest_dir, new_rc)
                logger.log("\t\t{0}".format(new_rc))

                rc_include = None
                for type_rc in types_rc:
                    if type_rc in new_rc:
                        rc_include = "<{0}>{1}</{0}>".format(type_rc, new_rc)

                if not rc_include:
                    logger.log("\t\t\tError in file {0}: Wrong filename".format(new_rc))
                    logger.log("\t\t\tFilename must start with:")
                    for t_rc in types_rc:
                        logger.log("\t\t\t\t{0}".format(t_rc))
                    sys.exit(2)

                rc_include_search = "\s*{0}".format(rc_include)
                rc_include_new = "    {0}".format(rc_include)

                if regex_in_file(rc_include_search, ossec_conf):
                    logger.log("\t\t\tRootchecks \"{0}\" already exist in ossec.conf".format(new_rc))
                else:
                    logger.log("\t\t\tIncluding \"{0}\" in ossec.conf ...".format(new_rc))
                    write_before_line("</rootcheck>", rc_include_new, ossec_conf)
                    # else:
                    # Note: ossec rootchecks are included in ossec.conf by default
                    # logger.log("\t\t**It is assumed that the default rootchecks are included in ossec.conf**")

    os.chown(ossec_conf, root_uid, ossec_gid)


def do_backups(bk_ossec_conf=False, bk_decoders=False, bk_rules=False, bk_rootchecks=False):
    bk_directory = "backups"

    try:
        # Create folder backups
        if not os.path.exists(bk_directory):
            os.makedirs(bk_directory)

        # Create folder /backups/YYYYMMDD_i
        i = 0
        bk_subdirectory = "{0}/{1}_{2}".format(bk_directory, today_date, str(i).zfill(2))
        while os.path.exists(bk_subdirectory):
            i += 1
            bk_subdirectory = "{0}/{1}_{2}".format(bk_directory, today_date, str(i).zfill(2))

        os.makedirs(bk_subdirectory)

        if bk_ossec_conf:
            src_file = "{0}/etc/ossec.conf".format(ossec_path)
            dest_file = "{0}/ossec.conf".format(bk_subdirectory)
            shutil.copyfile(src_file, dest_file)

        if bk_decoders:
            # decoder.xml
            src_file = "{0}/etc/decoder.xml".format(ossec_path)
            if os.path.exists(src_file):
                dest_file = "{0}/decoder.xml".format(bk_subdirectory)
                shutil.copyfile(src_file, dest_file)
            # ossec_decoders
            src_dir = "{0}/etc/ossec_decoders".format(ossec_path)
            if os.path.exists(src_dir):
                dest_dir = "{0}/ossec_decoders".format(bk_subdirectory)
                if os.path.exists(dest_dir):
                    shutil.rmtree(dest_dir)
                shutil.copytree(src_dir, dest_dir)

        if bk_rules:
            src_dir = "{0}/rules".format(ossec_path)
            dest_dir = "{0}/rules".format(bk_subdirectory)
            if os.path.exists(dest_dir):
                shutil.rmtree(dest_dir)
            shutil.copytree(src_dir, dest_dir)

        if bk_rootchecks:
            src_dir = "{0}/etc/shared".format(ossec_path)
            dest_dir = "{0}/rootchecks".format(bk_subdirectory)
            if not os.path.exists(dest_dir):
                os.makedirs(dest_dir)

            files = glob.iglob(os.path.join(src_dir, "*.txt"))

            for rootcheck_file in files:
                if os.path.isfile(rootcheck_file):
                    split = rootcheck_file.split("/")
                    filename = split[len(split) - 1]

                    dest_file = "{0}/{1}".format(dest_dir, filename)
                    shutil.copyfile(rootcheck_file, dest_file)

    except Exception as e:
        logger.log("Backup error:{0}.\nExit.".format(e))
        sys.exit(2)

    return bk_subdirectory


def get_ruleset(type_ruleset, r_action):
    """
    :param type_ruleset: "rules" or "rootchecks"
    :param r_action: "manual", "file:filepath.ext" or "update"
    :return: List of ruleset to install / update
    """
    if r_action == "manual":
        n_ruleset = get_ruleset_from_menu(type_ruleset)
    elif "file:" in r_action:
        filename = r_action.split(":")[1].rstrip('\n')
        n_ruleset = get_ruleset_from_file(filename, type_ruleset)
    elif r_action == "update":
        n_ruleset = get_ruleset_from_update(type_ruleset)
    else:
        n_ruleset = []

    return n_ruleset


def setup_ruleset_r(target_rules, r_action):
    """
    :param r_action: manual, file, update
    :param target_rules: rules to install
    :rtype: list
    """

    str_title = "updated" if r_action == "update" else "installed"

    logger.log("\nThe following rules will be {0}:".format(str_title))
    for rule in target_rules:
        logger.log("\t{0}".format(rule))
    logger.log("")

    instructions = []
    for item in target_rules:
        logger.log("{0}:".format(item))

        # Decoders
        logger.log("\tDecoder:")
        setup_decoders(item)
        logger.log("\t\t[Done]")

        # Rules
        logger.log("\tRules:")
        logger.log("\t\tCopying rules...")
        setup_rules(item)
        logger.log("\t\t[Done]")

        # ossec.conf
        logger.log("\tossec.conf:")
        setup_ossec_conf(item, "rule")
        logger.log("\t\t[Done]")

        # Info
        if r_action != "update":
            if item == "puppet":
                msg = "The rules of Puppet are installed but some rules need to read the output of a command." \
                      " Follow the fourth step detailed in file \"./rules-decoders/puppet/puppet_instructions.md\" to allow OSSEC execute this command and read its output."
                logger.log("\t**Manual steps**:\n\t\t{0}".format(msg))
                instructions.append("{0}: {1}".format(item, msg))

    return instructions


def setup_ruleset_rc(target_rootchecks, r_action):
    """
    :param r_action: manual, file, update
    :param target_rootchecks: rootchecks to install
    Important: Filenames must contain the following strings at the beginning:
        rootkit_files
        rootkit_trojans
        system_audit
        win_applications
        win_audit
        win_malware

        *except for default ossec rootchecks
    """

    str_title = "updated" if r_action == "update" else "installed"
    logger.log("\nThe following rootchecks will be {0}:".format(str_title))
    for t_rootcheck in target_rootchecks:
        logger.log("\t{0}".format(t_rootcheck))
    logger.log("")

    for item in target_rootchecks:
        logger.log("{0}:".format(item))

        # Rootchecks
        logger.log("\tCopy rootcheck:")
        setup_roochecks(item)
        logger.log("\t\t[Done]")

        # ossec.conf
        logger.log("\tossec.conf:")
        setup_ossec_conf(item, "rootcheck")
        logger.log("\t\t[Done]")


# Main

def usage():
    msg = """
OSSEC Wazuh Ruleset installer & updater
Github repository: https://github.com/wazuh/ossec-rules
Full documentation: http://documentation.wazuh.com/en/latest/ossec_ruleset.html

Usage: ./ossec_ruleset.py -r [-u | -f conf.txt] [-s]
       ./ossec_ruleset.py -c [-u | -f conf.txt] [-s]
       ./ossec_ruleset.py -a [-u | -f conf.txt] [-s]

Select ruleset:
\t-r, --rules
\t-c, --rootchecks
\t-a, --all

Select action:
\tno arguments\tInteractive menu for selection of rules and rootchecks to install.
\t-f, --file\tUse a configuration file to select rules and rootchecks to install.
\t-u, --update\tUpdate existing ruleset.

Aditional params:
\t-s, --silent\tForce OSSEC restart

Configuration file syntax using option -f:
\t# Commented line
\trules:new_rule_name
\trootchecks:new_rootcheck_name

Examples:
Manually choose rules to install: ./ossec_ruleset.py -r
Use a configuration file to select rules to install: ./ossec_ruleset.py -r -f new_rules.conf
\tnew_rules.conf content example:\n\trules:puppet\n\trules:netscaler
Update rules: ./ossec_ruleset.py -r -u
"""
    print(msg)


if __name__ == "__main__":
    # Vars
    ossec_path = "/var/ossec"
    url_ruleset = "http://ossec.wazuh.com/ruleset/ruleset.zip"
    today_date = date.today().strftime('%Y%m%d')
    ruleset_version = "0.100"  # Default
    ruleset_type = ""
    action = "manual"
    silent = False
    mandatory_args = 0

    # Capture Cntrl + C
    signal.signal(signal.SIGINT, signal_handler)

    # Check sudo
    if os.geteuid() != 0:
        sys.exit("You need root privileges to run this script. Please try again, using 'sudo'. Exiting.")

    # Check arguments
    try:
        opts, args = getopt.getopt(sys.argv[1:], "rcauhsf:",
                                   ["rules", "rootchecks", "all", "update", "help", "silent", "file="])
        if not opts or not (1 <= len(opts) <= 3):
            print("Incorrect number of arguments. Expected 1 or 2 arguments.")
            usage()
            sys.exit()
    except getopt.GetoptError as err:
        print(str(err))
        usage()
        sys.exit(2)

    for o, a in opts:
        if o in ("-r", "--rules"):
            ruleset_type = "rules"
            mandatory_args += 1
        elif o in ("-c", "--rootchecks"):
            ruleset_type = "rootchecks"
            mandatory_args += 1
        elif o in ("-a", "--all"):
            ruleset_type = "all"
            mandatory_args += 1
        elif o in ("-u", "--update"):
            action = "update"
        elif o in ("-h", "--help"):
            usage()
            sys.exit()
        elif o in ("-s", "--silent"):
            silent = True
        elif o in ("-f", "--file"):
            action = "file:{0}".format(a)
        else:
            usage()
            sys.exit()

    if mandatory_args != 1:
        print("Mandatory arguments: -r | -c | -a")
        usage()
        sys.exit()

    str_mode = "updated" if action == "update" else "installed"

    # Log
    logger = LogFile("log")

    # Get uid:gid = root:ossec
    try:
        root_uid = pwd.getpwnam("root").pw_uid
        ossec_gid = grp.getgrnam("ossec").gr_gid
    except:
        logger.log("Error get uid - gid")
        sys.exit(2)

    # Get ruleset version from file VERSION
    ruleset_version = get_ruleset_version()

    # Title
    logger.log("\nOSSEC Wazuh Ruleset [{0}], {1}\n".format(ruleset_version, today_date))

    # Get new ruleset
    if ruleset_type != "all":
        ruleset = get_ruleset(ruleset_type, action)[ruleset_type]

        if not ruleset:
            logger.log("No new {0} to be {1}".format(ruleset_type, str_mode))
            sys.exit()
    else:
        ruleset = get_ruleset("all", action)
        rules = ruleset["rules"]
        rootchecks = ruleset["rootchecks"]

        if not rules:
            logger.log("No new rules to be {0}".format(str_mode))
        if not rootchecks:
            logger.log("No new rootchecks to be {0}".format(str_mode))

        if not rules and not rootchecks:
            sys.exit()

    # Backups
    logger.log("Backup: ossec.conf, decoder.xml, rules, rootchecks")
    dir_bk = do_backups(True, True, True, True)
    logger.log("\tBackups folder: {0}".format(dir_bk))
    logger.log("\t[Done]")

    # Setup ruleset
    manual_steps = []
    if ruleset_type == "all":
        manual_steps = setup_ruleset_r(rules, action)
        setup_ruleset_rc(rootchecks, action)
    elif ruleset_type == "rules":
        manual_steps = setup_ruleset_r(ruleset, action)
    elif ruleset_type == "rootchecks":
        setup_ruleset_rc(ruleset, action)

    # PATCH for OSSEC version 2.8
    # If decoder.xml does not contain the tag accumulate it means is a old version of OSSEC
    # if not regex_in_file("accumulate", "{0}/etc/ossec_decoders/openldap_decoders.xml".format(ossec_path)):
    print("ToDo: Check OLD Version")

    # Restart ossec
    if not silent:
        logger.log("\nOSSEC requires a restart to apply changes")
        try:
            ans_restart = raw_input("Do you want to restart OSSEC now? [y/N]: ")
        except:
            # Python 3
            ans_restart = input("Do you want to restart OSSEC now? [y/N]: ")
    else:
        ans_restart = "y"

    ret = 0
    if ans_restart == "y":
        logger.log("\nRestarting OSSEC...")
        ret = os.system("{0}/bin/ossec-control restart".format(ossec_path))
        if ret != 0:
            logger.log("\n**Something went wrong**")
            logger.log("Please check your config. logtest can be useful: {0}/bin/ossec-logtest".format(ossec_path))
            logger.log("\n\n**Ruleset error**")
        else:
            logger.log("\n\n**Ruleset({0}) {1} successfully**".format(ruleset_version, str_mode))
    else:
        logger.log("Do not forget to restart OSSEC to apply changes.")
        logger.log("\n\n**Ruleset({0}) {1} successfully**".format(ruleset_version, str_mode))

    if manual_steps:
        logger.log("\nDo not forget the manual steps:")
        for step in manual_steps:
            logger.log("\t{0}".format(step))

    logger.log("\n\nWazuh.com")
