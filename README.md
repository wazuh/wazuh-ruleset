# OSSEC HIDS Ruleset mantained by Wazuh

This rule set updates OSSEC rules by modifying them or including new ones to increase detection capabilities, add functionality and expand OSSEC scope. 

It includes, among many others, compliance mapping with PCI DSS v3.1, CIS and additional decoders and rules.

OSSEC Rule set is fed with the effort of a dedicated team and the help of the community. We encourage users to contribute to the repository and/or request new rules and decoders.

## How to use

Use ```ossec_ruleset.py ``` to install and update new rules, decoders and rootcheck. Some features:

* Check current installation
* Install new rules and rootchecks
* Decoders management
* Automatic ```ossec.conf``` configuration
* Update ruleset from Wazuh website
* Silent mode

**Some examples**

Menu to install new rules/rootchecks
``` bash
./ossec_ruleset.py -a
```
Install new rules/rootchecks from config file
``` bash
./ossec_ruleset.py -a -f file.conf
```

Silent update
``` bash
./ossec_ruleset.py -a -u -s
```

Don't hesitate to set up the script to fetch periodically new rules, decoders and rootcheck.
Find out how to do it at [Script Documentation](http://documentation.wazuh.com/en/latest/ossec_rule_set.html)


## Documentation

* Full documentation at [documentation.wazuh.com](http://documentation.wazuh.com/en/latest/ossec_rule_set.html)

## Contribute

Users can contribute to this rule set by submitting pull requests. Our team will continue maintaining and updating it periodically.
If you want to contribute to this ruleset or our projects please don't hesitate to send a pull request. You can also join our users [mailing list](https://groups.google.com/d/forum/wazuh), by sending an email to [wazuh+subscribe@googlegroups.com](mailto:wazuh+subscribe@googlegroups.com), to ask questions and participate in discussions.




Directory structure:

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
    

