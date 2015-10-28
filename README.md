# ossec-rules
OSSEC Free Open Source community rule set put together by WAZUH

Directory structure:

    ├── ossec-rules             
    │ ├── rootcheck            
    │   ├── ossec            # OSSEC Rootchecks updated by Wazuh
    │   ├── <new_rootcheck>  # New rootchecks
    |
    │ ├── rules-decoders      
    │   ├── ossec            # OSSEC Rules & Decoders updated by Wazuh
    │     ├── decoder.xml
    │     ├── *_rules.xml
    │     ├── ossec_instructions.md
    │     ├── autoinstall_rules.sh
    │   ├── <new_software>   # New rules & decoders
    |     ├── new_software_decoders.xml
    |     ├── new_software_rules.xml  
    |     ├── new_software_instructions.md  
    |     ├── autoinstall_rules.sh  
    |
    │ ├── README.md  