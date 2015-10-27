#Instructions for Netscaler rules
**Created by Wazuh, Inc. <ossec@wazuh.com>**

You can run the script ***./autoinstall_rules.sh***, or follow the instructions:

 1. Append *netscaler_decoders.xml* to */var/ossec/etc/decoders.xml*
 2. Copy *netscaler_rules.xml* to */var/ossec/rules/*
 3. Add *<include>netscaler_rules.xml</include>* to */var/ossec/etc/ossec.conf*