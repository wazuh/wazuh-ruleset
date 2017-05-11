# Wazuh Ruleset

Wazuh ruleset is used to detect attacks, intrusions, software misuse, configuration problems, application errors, malware, rootkits, system anomalies or security policy violations.

The ruleset includes compliance mapping with PCI DSS v3.1 and CIS.

## Installation

* [Installation instructions](https://documentation.wazuh.com/current/user-manual/ruleset/update.html)

## Directory structure

    ├── wazuh-ruleset
    │ ├── decoders            # OSSEC decoders created/updated by Wazuh
    │ ├── rules               # OSSEC rules created/updated by Wazuh
    │ ├── rootchecks          # OSSEC rootchecks created/updated by Wazuh
    │ ├── scap_content        # OVAL, XCCDF, DS created/updated by Wazuh
    │ ├── lists               # CDB lists created/updated by Wazuh
    |
    │ ├── tools
    |
    │ ├── README.md
    │ ├── VERSION
    │ ├── update_ruleset.py   # Install/update ruleset

## Full documentation

Full documentation at [documentation.wazuh.com](https://documentation.wazuh.com/current/user-manual/ruleset/index.html)

## Branches

* `stable` branch on correspond to the last OSSEC Ruleset stable version.
* `master` branch contains the latest code, be aware of possible bugs on this branch.
* `development` branch includes all the new features we are adding and testing.


## Contribute

If you have created new rules, decoders or rootchecks and you would like to contribute to our repository, please fork our Github repository and submit a pull request.

If you are not familiar with Github, you can also share them through [our users mailing list](https://groups.google.com/d/forum/wazuh), to which you can subscribe by sending an email to `wazuh+subscribe@googlegroups.com`. As well do not hesitate to request new rules or rootchecks that you would like to see running in Wazuh and our team will do our best to make it happen.

## Web references

* [Wazuh website](http://wazuh.com)
* [OSSEC project website](http://ossec.github.io)
