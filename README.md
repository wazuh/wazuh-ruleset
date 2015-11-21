# OSSEC Wazuh Ruleset mantained by Wazuh

OSSEC rules are used to detect attacks, intrusions, software misuse, configuration problems, application errors, malware, rootkits, system anomalies or security policy violations. OSSEC provides an out-of-the-box set of rules that we update by modifying them or including new ones, in order to increase OSSEC detection capabilities.

The ruleset includes compliance mapping with PCI DSS v3.1, CIS and additional decoders and rules.

## Installation

* [Manual installation instructions](http://documentation.wazuh.com/en/latest/ossec_ruleset.html#manual-installation)
* [Automatic installation instructions](http://documentation.wazuh.com/en/latest/ossec_ruleset.html#automatic-installation): Using `ossec_ruleset.py`

## Directory structure

    ├── ossec-rules             
    │ ├── rootcheck            
    │   ├── ossec            # OSSEC Rootchecks updated by Wazuh
    │   ├── <new_rootcheck>  # New rootchecks
    |
    │ ├── rules-decoders 
    │   ├── decoder.xml      # OSSEC Decoders updated by Wazuh
    │   ├── ossec            # OSSEC Rules updated by Wazuh
    │     ├── *_rules.xml
    │     ├── ossec_instructions.md
    │   ├── <new_software>   # New rules & decoders
    |     ├── new_software_decoders.xml
    |     ├── new_software_rules.xml  
    |     ├── new_software_instructions.md  
    |
    │ ├── INSTRUCTIONS
    │ ├── README.md
    │ ├── VERSION
    │ ├── ossec_ruleset.py # Ruleset installer/updater
    
## Full documentation

Full documentation at [documentation.wazuh.com](http://documentation.wazuh.com/en/latest/ossec_ruleset.html)

## Contribute

Users can contribute to this rule set by submitting pull requests. Our team will continue maintaining and updating it periodically.
If you want to contribute to this ruleset or our projects please don't hesitate to send a pull request. You can also join our users [mailing list](https://groups.google.com/d/forum/wazuh), by sending an email to [wazuh+subscribe@googlegroups.com](mailto:wazuh+subscribe@googlegroups.com), to ask questions and participate in discussions.
    

