# ossec-rules
OSSEC HIDS Open Source community rule set put together by WAZUH

Includes compliance mapping with PCI DSS v3.1 or CIS and additional decoders and rules. Users can contribute to this rule set by submitting pull requests. Our team will continue to maintain and update it periodically.

We are creating an automatic updating service, meantime you can install the rules using a bash script. 

Find more detailed information at [Ruleset Documentation](http://documentation.wazuh.com/en/latest/ossec_rule_set.html)


Directory structure:

    ├── ossec-rules             
    │ ├── rootcheck            
    │   ├── ossec            # OSSEC Rootchecks updated by Wazuh
    │   ├── <new_rootcheck>  # New rootchecks
    |
    │ ├── rules-decoders 
    │   ├── install_rules.sh # Rules script updater 
    │   ├── decoder.xml      # OSSEC Decoders updated by Wazuh
    │   ├── ossec            # OSSEC Rules updated by Wazuh
    │     ├── *_rules.xml
    │     ├── ossec_instructions.md
    │   ├── <new_software>   # New rules & decoders
    |     ├── new_software_decoders.xml
    |     ├── new_software_rules.xml  
    |     ├── new_software_instructions.md  
    |
    │ ├── README.md  

