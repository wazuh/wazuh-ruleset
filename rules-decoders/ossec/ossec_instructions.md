#Instructions for OSSEC rules
**Updated by Wazuh, Inc. <ossec@wazuh.com>**

You can run the script ***ossec_ruleset.py***, or follow the next instructions:

 1. Configure decoders path adding the next lines after tag ``<rules>``at ``/var/ossec/etc/ossec.conf``:

    ``<decoder>etc/decoder.xml</decoder>``
    ``<decoder>etc/local_decoder.xml</decoder>``
    ``<decoder_dir>etc/wazuh_decoders</decoder_dir>``
 2. Copy */rules-decoders/decoder.xml* to */var/ossec/etc/*
 3. Copy */rules-decoders/ossec/*_rules.xml* to */var/ossec/rules/*, except local_rules.xml
 4. Restart your OSSEC Manager