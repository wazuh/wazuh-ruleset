# ossec-rules
OSSEC Free Open Source community rule set put together by WAZUH

Directory structure:

    ├── ossec-rules             
    │ ├── rootcheck            
    │   ├── ossec            # OSSEC Rootchecks updated by Wazuh
    │   ├── <new_rootcheck>  # New Wazuh rootcheck
    |
    │ ├── rules-decoders      
    │   ├── ossec            # OSSEC Rules & Decoders updated by Wazuh
    │     ├── decoders.xml
    │     ├── *_rules.xml
    │   ├── <new_software>   # New Wazuh rules & decoders
	|     ├── new_software_decoders.xml
	|     ├── new_software_rules.xml  
	|     ├── instructions.txt  
    |
    │ ├── README.md    

