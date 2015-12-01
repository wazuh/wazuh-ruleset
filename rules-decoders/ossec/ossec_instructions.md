#Instructions for OSSEC rules
**Updated by Wazuh, Inc. <ossec@wazuh.com>**

You can run the script ***ossec_ruleset.py***, or follow the next instructions:

 1. Configure decoders path adding the next lines after tag ``<rules>``at ``/var/ossec/etc/ossec.conf``:
 
	 - ``<decoder_dir>etc/ossec_decoders</decoder_dir>``
	 - ``<decoder>etc/local_decoder.xml</decoder>`` (when you are using local decoders)
	 - ``<decoder_dir>etc/wazuh_decoders</decoder_dir>``
 2. Copy */rules-decoders/ossec/decoders/*_decoders.xml* to */var/ossec/etc/ossec_decoders*
 3. Copy */rules-decoders/ossec/rules/*_rules.xml* to */var/ossec/rules/*, except local_rules.xml
 4. Restart your OSSEC Manager