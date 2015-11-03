# ossec-rules
OSSEC Free Open Source community rule set put together by WAZUH

Directory structure:

    ├── ossec-rules             
    │ ├── rootcheck            
    │   ├── ossec            # OSSEC Rootchecks updated by Wazuh
    │   ├── <new_rootcheck>  # New rootchecks
    |
    │ ├── rules-decoders 
    │   ├── install_rules.sh
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