#Instructions for Netscaler rules
**Created by Wazuh, Inc. <ossec@wazuh.com>**

You can run the script ***ossec_ruleset.py***, or follow the next instructions:

 1. Configure decoders path adding the next lines after tag ``<rules>``at ``/var/ossec/etc/ossec.conf``:

    ``<decoder>etc/decoder.xml</decoder>``
    ``<decoder>etc/local_decoder.xml</decoder>``
    ``<decoder_dir>etc/wazuh_decoders</decoder_dir>``
 2. Copy *netscaler_decoders.xml* to */var/ossec/etc/wazuh_decoders/*
 3. Copy *netscaler_rules.xml* to */var/ossec/rules/*
 4. Add *```<include>netscaler_rules.xml</include>```* to */var/ossec/etc/ossec.conf* before tag *```</rules>```*
 5. Restart your OSSEC Manager