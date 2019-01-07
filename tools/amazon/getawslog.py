#!/usr/bin/env python
#
# Import AWS CloudTrail data to a local flat file
#
# Author: Xavier Mertens <xavier@rootshell.be>
# Copyright: GPLv3 (http://gplv3.fsf.org/)
# Feel free to use the code, but please share the changes you've made
#
# Install: boto is required to connect to S3 (http://code.google.com/p/boto/)
#

import ConfigParser
import argparse
import boto
import gzip
import json
import os
import os
import re
import signal
import sys
from optparse import OptionParser


def handler(signal, frame):
    print "SIGINT received, bye!"
    sys.exit(1)

def already_processed(newFile, state_tracker):
    if state_tracker:
        cursor = state_tracker.execute('select count(*) from log_progress where log_name="{log_name}"'.format(log_name=newFile))
        if cursor.fetchall()[0][0]:
            return True
    return False

def mark_complete(newFile, state_tracker):
    if state_tracker:
        state_tracker.execute("insert into log_progress (log_name, processed_date) values ('{log_name}', DATE('now'))".format(log_name=newFile))
        state_tracker.commit()



def main(argv):

    parser = OptionParser(usage="usage: %prog [options]", version="%prog 1.0")
    parser.add_option('-b', '--bucket', dest='logBucket', type='string', \
            help='Specify the S3 bucket containing AWS logs')
    parser.add_option('-d', '--debug', action='store_true', dest='debug', \
            help='Increase verbosity')
    parser.add_option('-l', '--log', dest='logFile', type='string', \
            help='Local log file')
    parser.add_option('-j', '--json', action='store_true', dest='dumpJson', \
            help='Reformat JSON message (default: raw)')
    #Beware, once you delete history it's gone.
    parser.add_option('-D', '--delete', action='store_true', dest='deleteFile', \
            help='Delete processed files from the AWS S3 bucket')
    parser.add_option('-s', '--state', dest='state', type='string', \
            help="State file for keeping track of what logs you already processed.")
    (options, args) = parser.parse_args()
    state_tracker = None

    if options.debug:
        print '+++ Debug mode on'

    if options.logBucket == None:
        print 'ERROR: Missing an AWS S3 bucket! (-b flag)'
        sys.exit(1)
    if options.logFile == None:
        print 'ERROR: Missing a local log file! (-l flag)'
        sys.exit(1)
    if options.state:
        import sqlite3
        try:
            state_tracker = sqlite3.connect(options.state)
            state_tracker.execute("select count(*) from log_progress")
        except sqlite3.OperationalError:
            state_tracker.execute("create table log_progress  (log_name 'text' primary key, processed_date 'TEXT')")


    if options.debug: print '+++ Connecting to Amazon S3'
    s3 = boto.connect_s3()
    c = s3.get_bucket(options.logBucket)
    try:
        c = s3.get_bucket(options.logBucket)
    except boto.exception.S3ResponseError as e:
        print "Bucket %s access error: %s" % (options.logBucket, e)
        sys.exit(3)
    for f in c.list():
        newFile = os.path.basename(str(f.key))
        if re.match('.+_CloudTrail-Digest_.+', newFile):
            if options.debug: print "Skipping digest file: %s" % newFile
            continue
        if newFile != "":
            if already_processed(newFile, state_tracker):
                if options.debug:
                    print "Skipping previously seen file {file}".format(file=newFile)
                continue
            if options.debug:
                print "+++ Found new log: ", newFile
            f.get_contents_to_filename(newFile)
            data = gzip.open(newFile, 'rb')
            try:
                log = open(options.logFile, 'ab')
            except IOError as e:
                print "ERROR: Cannot open %s (%s)" % (options.logFile, e.strerror)
                sys.exit(1)

            if options.dumpJson == None:
                log.write(data.read())
                log.write("\n")
            else:
                j = json.load(data)
                if "Records" not in j:
                    continue
                for json_event in j["Records"]:
                    new_dict = {}
                    for key in json_event:
                        if json_event[key]:
                            new_dict[key] = json_event[key]
                    new_dict['log_file'] = newFile
                    aws_log = {'aws': new_dict}
                    # Copy 'aws.sourceIPAddress' and 'aws.userIdentity.userName' to standard fields 'srcip' and 'user' so 'srcip' can be used in Wazuh GeoIP lookups and <same_user /> and <same_source_ip /> can be used in composite rules.
                    if 'sourceIPAddress' in aws_log["aws"]:
                        aws_log["srcip"]=aws_log["aws"]["sourceIPAddress"]
                    if 'userIdentity' in aws_log["aws"] and 'userName' in aws_log["aws"]["userIdentity"]:
                        aws_log["user"]=aws_log["aws"]["userIdentity"]["userName"]
                    log.write("{0}\n".format(json.dumps(aws_log)))
            log.close()

            try:
                os.remove(newFile)
            except IOError as e:
                print "ERROR: Cannot delete %s (%s)" % (newFile, e.strerror)
            if options.deleteFile:
                c.delete_key(f.key)
            mark_complete(newFile, state_tracker)

if __name__ == '__main__':
    signal.signal(signal.SIGINT, handler)
    main(sys.argv[1:])
    sys.exit(0)
