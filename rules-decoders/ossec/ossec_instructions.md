#Instructions for OSSEC rules
**Updated by Wazuh, Inc. <ossec@wazuh.com>**

You can run the script ***ossec_ruleset.py***, or follow the next instructions:

 1. Copy */rules-decoders/decoder.xml* to */var/ossec/etc/*
 2. Copy */rules-decoders/ossec/*_rules.xml* to */var/ossec/rules/*, except local_rules.xml
 3. Restart your OSSEC Manager
