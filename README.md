# OSSEC Wazuh Ruleset

OSSEC rules are used to detect attacks, intrusions, software misuse, configuration problems, application errors, malware, rootkits, system anomalies or security policy violations. OSSEC provides an out-of-the-box set of rules that we update by modifying them or including new ones, in order to increase OSSEC detection capabilities.

The ruleset includes compliance mapping with PCI DSS v3.1, CIS and additional decoders and rules.

## Installation

* [Manual installation instructions](http://documentation.wazuh.com/en/latest/ossec_ruleset.html#manual-installation)
* [Automatic installation instructions](http://documentation.wazuh.com/en/latest/ossec_ruleset.html#automatic-installation)

## Directory structure

    ├── ossec-rules             
    │ ├── rootcheck        # OSSEC Rootchecks created/updated by Wazuh
    |
    │ ├── rules-decoders 
    │   ├── ossec            # OSSEC Decoders & Rules updated by Wazuh
    │     ├── decoders
    │     ├── rules
    │     ├── ossec_instructions.md
    │   ├── <new_software>   # New rules & decoders
    |     ├── new_software_decoders.xml
    |     ├── new_software_rules.xml  
    |     ├── new_software_instructions.md  
    |
    │ ├── tools
    |
    │ ├── README.md
    │ ├── VERSION
    │ ├── ossec_ruleset.py   # Ruleset installer/updater
    
## Full documentation

Full documentation at [documentation.wazuh.com](http://documentation.wazuh.com/en/latest/ossec_ruleset.html)

## Branches

* `stable` branch on correspond to the last OSSEC Ruleset stable version.
* `master` branch contains the latest code, be aware of possible bugs on this branch.
* `development` branch includes all the new features we are adding and testing.


## Contribute

If you have created new rules, decoders or rootchecks and you would like to contribute to our repository, please fork our Github repository and submit a pull request.

If you are not familiar with Github, you can also share them through [our users mailing list](https://groups.google.com/d/forum/wazuh), to which you can subscribe by sending an email to `wazuh+subscribe@googlegroups.com`. As well do not hesitate to request new rules or rootchecks that you would like to see running in OSSEC and our team will do our best to make it happen.

## Web references

* [Wazuh website](http://wazuh.com)
* [OSSEC project website](http://ossec.github.io)
