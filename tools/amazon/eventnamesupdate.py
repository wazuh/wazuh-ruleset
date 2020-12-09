#!/usr/bin/env python
#
# Fetch AWS API Actions from docs page and update Wazuh aws-eventnames list
#
# Author: Franco Hielpos <franco.hielpos@wazuh.com>
#
# Some URL examples:
# EC2: https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_Operations.html
# IAM: https://docs.aws.amazon.com/IAM/latest/APIReference/API_Operations.html
# LAMBDA: https://docs.aws.amazon.com/lambda/latest/dg/API_Operations.html
#

from bs4 import BeautifulSoup
import requests
import argparse


def main(url, service, path):
    dic = {}

    # Make a GET request to fetch the raw HTML content
    html_content = requests.get(url).text

    # Parse the html content
    soup = BeautifulSoup(html_content, "html.parser")

    # Open event name file
    with open(path, "r+") as f:
        # Get actual eventName dictionary
        for line in f:
            (key, val) = line.split(":")
            dic[key] = val

        count = 0

        # Fetch Action list from AWS API reference guide
        for item in soup.find_all('li', "listitem"):
            for action in item.find_all('a'):
                if action.text not in dic:
                    # Add pair to eventName list
                    new_pair = f"{action.text}:{service} \n"
                    # Write to file
                    f.write(new_pair)
                    print("New pair added: " + new_pair)
                    count += 1

    print(f"Script finished. {count} new pairs added.")


if __name__ == '__main__':
    # Args
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', '--url', type=str, default='',
                        help='AWS API reference URL to fetch API Actions. You can find them at: https://docs.aws.amazon.com/index.html', required=True)
    parser.add_argument('-s', '--service', type=str, default='',
                        help='name of the AWS service (eg: EC2, IAM, etc)', required=True)
    parser.add_argument('-p', '--path', type=str, default='/var/ossec/etc/lists/amazon/aws-eventnames',
                        help='path to the aws-eventnames list file', required=False)
    args = parser.parse_args()

    main(args.url, args.service.upper(), args.path)
