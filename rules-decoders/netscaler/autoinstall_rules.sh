#!/bin/bash

# You need to set execute permission for this script:
#   chmod +x autoinstall_rules.sh
# You need to run the script as root
#   sudo ./autoinstall_rules.sh

backup="backup_netscaler"
x_decoder="netscaler_decoders.xml"
x_rules="netscaler_rules.xml"

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
path_ossec=$ossec_path"etc/ossec.conf"

# Decoders
echo "1. Append $x_decoder to $path_decoder"
cp $path_decoder  $path_decoder.$backup
cat $x_decoder >> $path_decoder
echo "[Done]"

# Rules 
echo "2. Copy $x_rules to $path_rules"
cp $x_rules $path_rules
echo "[Done]"

# ossec.conf
echo  "3. Add <include>$x_rules</include> to $path_ossec"
cp $path_ossec  $path_ossec.$backup
sed -i "s/.*<\/rules>.*/    <include>$x_rules<\/include>\n&/" $path_ossec
echo "[Done]"

# Wazuh
echo -e "\nWazuh, Inc\n"
