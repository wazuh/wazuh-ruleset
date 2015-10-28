#!/bin/bash

# You need to set execute permission for this script:
#   chmod +x autoinstall_rules.sh
# You need to run the script as root
#   sudo ./autoinstall_rules.sh

date=`date +%Y%m%d`
backup="bk$date"

ossec_path="/var/ossec/"

#Exit immediately if a command exits with a non-zero status
set -e

read -p "OSSEC path is \"$ossec_path\"? (Y/n)" -n 1

if [[ $REPLY =~ ^[nN]$ ]]; then
    echo
    read -p "Path to OSSEC: " 
    ossec_path=$REPLY
fi

path_decoder=$ossec_path"etc/decoder.xml"
path_rules=$ossec_path"rules/"

# Decoders
echo "1. Copy decoder.xml to $path_decoder"
cp $path_decoder $path_decoder.$backup
echo "Backup: $path_decoder.$backup"
cp "decoder.xml" $path_decoder
echo "[Done]"

# Rules 
echo "2. Copy all rules to $path_rules"
filename="$ossec_path""rules_$backup.zip"
zip -r $filename $path_rules >/dev/null
echo "Backup: $filename"
cp `ls | grep _rules.xml | egrep -v 'local_rules'` $path_rules
echo "[Done]"



# Wazuh
echo -e "\nWazuh, Inc\n"
