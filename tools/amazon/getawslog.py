#!/usr/bin/env python
#
# Import AWS CloudTrail data to a local flat file
#
# Authors:
# * Xavier Mertens <xavier@rootshell.be>
# * Marcel Puchol <marcel.puchol@sequra.es>
#
# Copyright: GPLv3 (http://gplv3.fsf.org/)
# Feel free to use the code, but please share the changes you've made
#
# Install: boto3 is required to connect to S3
#

import ConfigParser
import argparse
import boto3
import botocore
import zlib
import json
import os
import os
import re
import signal
import sys
import logging
import logging.handlers
from optparse import OptionParser


def already_processed(newFile, state_tracker):
    if state_tracker:
        cursor = state_tracker.execute("""SELECT count(1)
                                       FROM log_progress
                                       WHERE log_name="{log_name}"
                                       """.format(log_name=newFile))
        if cursor.fetchall()[0][0]:
            return True
    return False


def mark_complete(newFile, state_tracker):
    if state_tracker:
        state_tracker.execute("""INSERT INTO log_progress(log_name, processed_date)
                              VALUES ('{log_name}', DATE('now'))""".
                              format(log_name=newFile))
        state_tracker.commit()


def main(argv):
    parser = OptionParser(usage="usage: %prog [options]", version="%prog 1.0")
    parser.add_option('-b', '--bucket', dest='logBucket', type='string',
                      help='Specify the S3 bucket containing AWS logs')
    parser.add_option('-d', '--debug', action='store_true', dest='debug',
                      help='Increase verbosity')
    parser.add_option('-o', '--output', dest='outputFile', type='string',
                      help='Output file')
    parser.add_option('-l', '--log', dest='logFile', type='string',
                      help='File in which to dump logs (default: stdout)')
    parser.add_option('-j', '--json', action='store_true', dest='dumpJson',
                      help='Reformat JSON message (default: raw)')
    # Beware, once you delete history it's gone.
    parser.add_option('-D', '--delete', action='store_true', dest='deleteFile',
                      help='Delete processed files from the AWS S3 bucket')
    parser.add_option('-s', '--state', dest='state', type='string',
                      help="State file for keeping track of what logs you \
                      already processed.")
    (options, args) = parser.parse_args()
    state_tracker = None

    logger = logging.getLogger('getawslog')

    if options.logFile:
        logger_handler = logging.handlers.WatchedFileHandler(options.logFile)
    else:
        logger_handler = logging.StreamHandler()

    logger_handler.setFormatter(logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'))

    logger_level = logging.DEBUG if options.debug else logging.INFO
    logger.setLevel(logger_level)
    logger_handler.setLevel(logger_level)

    logger.addHandler(logger_handler)

    def signal_handler(*args):
        logger.error("SIGINT received, closing process")
        sys.exit(1)

    signal.signal(signal.SIGINT, signal_handler)

    if options.logBucket is None:
        logger.critical('Missing an AWS S3 bucket! (-b flag)')
        sys.exit(1)
    if options.outputFile is None:
        logger.critical('Missing a local log file! (-l flag)')
        sys.exit(1)
    if options.state:
        import sqlite3
        try:
            state_tracker = sqlite3.connect(options.state)
            state_tracker.execute("SELECT 1 FROM log_progress")
        except sqlite3.OperationalError:
            state_tracker.execute("""CREATE TABLE log_progress(
                                  log_name 'text' PRIMARY KEY,
                                  processed_date 'TEXT')""")

    logger.info('Starting process')
    logger.debug('Connecting to Amazon S3')
    s3 = boto3.resource('s3')
    bucket = None
    try:
        bucket = s3.Bucket(options.logBucket)
        s3.meta.client.head_bucket(Bucket=options.logBucket)
    except botocore.exceptions.ClientError as e:
        logger.critical("Bucket %s access error: %s" % (options.logBucket, e))
        sys.exit(3)

    stats_total_objs = 0
    stats_already_processed_objs = 0
    stats_processed_objs = 0
    for obj in bucket.objects.all():
        stats_total_objs = stats_total_objs + 1
        if obj.key.endswith('/'):
            logger.debug("Skipping path key: %s" % obj.key)
            continue

        if '_CloudTrail-Digest_' in obj.key:
            logger.debug("Skipping digest file: %s" % obj.key)
            continue

        if already_processed(obj.key, state_tracker):
            logger.debug("Skipping previously seen file {file}".
                         format(file=obj.key))
            stats_already_processed_objs = stats_already_processed_objs + 1
            continue

        stats_processed_objs = stats_processed_objs + 1
        logger.debug("Found new log: %s" % (obj.key))
        data = zlib.decompress(obj.get()['Body'].read(), zlib.MAX_WBITS | 32)
        try:
            log = open(options.outputFile, 'ab')
        except IOError as e:
            logger.critical("Cannot open %s (%s)" %
                            (options.outputFile, e.strerror))
            sys.exit(1)

        if options.dumpJson is None:
            log.write(data)
            log.write("\n")
        else:
            j = json.loads(data)
            if "Records" in j:
                records = j["Records"]
                for item in records:
                    log.write("\"AmazonAWS\":")
                    newline = 0
                    for field in item:
                        if newline > 0:
                            log.write(",")
                        newline = 1
                        log.write("\"%s\":\"%s\"" % (field, item[field]))
                    log.write("\n")
        log.close()

        if options.deleteFile:
            obj.delete()
        mark_complete(obj.key, state_tracker)

    logger.info('Process finished correctly. Total objects=%d, already \
                processed objects=%d, new processed objects=%d' % (
                    stats_total_objs, stats_already_processed_objs,
                    stats_processed_objs
                ))


if __name__ == '__main__':
    main(sys.argv[1:])
    sys.exit(0)
