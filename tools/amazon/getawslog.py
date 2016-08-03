#!/usr/bin/python
#
# Import AWS CloudTrail data to a local flat file
#
# Author: Xavier Mertens <xavier@rootshell.be>
# Copyright: GPLv3 (http://gplv3.fsf.org/)
# Feel free to use the code, but please share the changes you've made
#
# Install: boto is required to connect to S3 (http://code.google.com/p/boto/)
#


import os
import argparse
import ConfigParser
import boto
import gzip
import os
import sys
import signal
import json
from optparse import OptionParser


def handler(signal, frame):
    print "SIGINT received, bye!"
    sys.exit(1)

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
    parser.add_option('-D', '--delete', action='store_true', dest='deleteFile', \
            help='Delete processed files from the AWS S3 bucket')
    (options, args) = parser.parse_args()

    if options.debug:
        print '+++ Debug mode on'

    if options.logBucket == None:
        print 'ERROR: Missing an AWS S3 bucket! (-b flag)'
        sys.exit(1)
    if options.logFile == None:
        print 'ERROR: Missing a local log file! (-l flag)'
        sys.exit(1)

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
        if newFile != "":
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
                if "Records" in j:
                    records = j["Records"]
                    for item in records:
                        newline = 0
                        for field in item:
                            if newline > 0:
                                log.write(",")
                            newline = 1
                            log.write("\"%s\":\"%s\"" % (field, item[field]))
                        log.write("\n\"AmazonAWS\":")
            log.close()

            try:
                os.remove(newFile)
            except IOError as e:
                print "ERROR: Cannot delete %s (%s)" % (newFile, e.strerror)

            if options.deleteFile:
                c.delete_key(f.key)

if __name__ == '__main__':
    signal.signal(signal.SIGINT, handler)
    main(sys.argv[1:])
    sys.exit(0)
