#!/bin/bash

# You need to set execute permission for this script:
#   chmod +x autoinstall_rules.sh
# You need to run the script as root
#   sudo ./autoinstall_rules.sh

x_decoder="netscaler_decoders.xml"
x_rules="netscaler_rules.xml"
path_decoder="/var/ossec/etc/decoder.xml"
path_rules="/var/ossec/rules/"

#Exit immediately if a command exits with a non-zero status
set -e

# Decoders
read -p "1. Append $x_decoder to $path_decoder? (Y/n) " -n 1

if [[ $REPLY =~ ^[nN]$ ]]; then
    echo
    read -p "Path to OSSEC decoders.xml: " 
    path_decoder=$REPLY
fi

if [ -f "$path_decoder" ]
then
	cat $x_decoder >> $path_decoder
else
	echo "Error: $path_decoder does not exist"
    exit
fi

# Rules 
read -p "2. Copy $x_rules to $path_rules? (Y/n) " -n 1

if [[ $REPLY =~ ^[nN]$ ]]; then
    echo
    read -p "Path to OSSEC rules: " 
    path_rules=$REPLY
fi

if [ -d "$path_rules" ]
then
	cp $x_rules $path_rules
else
	echo "Error: $path_rules does not exist"
    exit
fi


# Info
echo "3. **MANUAL STEP**"
echo "Follow the third instruction indicated in the file instructions.md"


# Wazuh
echo -e "\nWazuh, Inc\n"
