# Wazuh Ruleset

[![Slack](https://img.shields.io/badge/slack-join-blue.svg)](https://goo.gl/forms/M2AoZC4b2R9A9Zy12)
[![Email](https://img.shields.io/badge/email-join-blue.svg)](https://groups.google.com/forum/#!forum/wazuh)
[![Documentation](https://img.shields.io/badge/docs-view-green.svg)](https://documentation.wazuh.com)
[![Documentation](https://img.shields.io/badge/web-view-green.svg)](https://wazuh.com)

Wazuh ruleset is used to detect attacks, intrusions, software misuse, configuration problems, application errors, malware, rootkits, system anomalies or security policy violations.

The ruleset includes compliance mapping with [PCI DSS v3.2](https://www.pcisecuritystandards.org/), [GDPR](https://gdpr-info.eu/), [CIS](https://www.cisecurity.org/) and [MITRE ATT&CK](https://attack.mitre.org/)

![image](https://user-images.githubusercontent.com/10210567/90039680-4441ff80-dcc7-11ea-8c2d-2e137652a41c.png)

This ruleset currently has more than 3000 rules, and it applies to a huge list of additional technologies such:

- Syslog
- SonicWall
- Cisco Systems
- Postfix
- Mailscanner
- Microsoft Exchange
- Courier
- PIX
- NetScreen technologies
- McAfee
- NextCloud
- Palo Alto
- VirusTotal
- Suricata
- MongoDB

And much more, take a look at the full list [here](https://documentation.wazuh.com/current/user-manual/ruleset/getting-started.html).

## Updating the Wazuh Ruleset

Run the `update_ruleset` script to update the Wazuh ruleset. You should not need to make any other changes to accommodate the updated rules.

### Usage examples

- Update Decoders, Rules and Rootchecks:

```
# /var/ossec/bin/update_ruleset
```

Check the script options following [our documentation](https://documentation.wazuh.com/3.13/user-manual/reference/tools/update_ruleset.html#update-ruleset).


## Directory structure

    wazuh-ruleset/
    ├── decoders
    ├── lists               # CDB lists
    │   └── amazon
    ├── rootchecks
    ├── rules
    │   ├── log-entries
    │   └── translated
    ├── sca                # security configuration assesments policies
    │   ├── applications
    │   ├── darwin
    │   ├── debian
    │   ├── generic
    │   ├── rhel
    │   ├── sles
    │   ├── sunos
    │   └── windows
    ├── scap_content       # OVAL, XCCDF, DS
    └── tools
    │   ├── amazon
    │   ├── cve-xccdf
    │   ├── file-testing
    │   ├── map-security-standard
    │   └── rules-testing
    ├── update_ruleset     # Install/update ruleset
    └── VERSION

## Full documentation

Full documentation at [documentation.wazuh.com](https://documentation.wazuh.com/current/user-manual/ruleset/index.html)

## Branches

* `stable` branch on correspond to the last OSSEC Ruleset stable version.
* `master` branch contains the latest code, be aware of possible bugs on this branch.
* `develop` branch includes all the new features we are adding and testing.

## Contribute

If you have created new rules, decoders or SCA policies and you'd like to contribute to this repository, please fork it and submit a new Pull Request. To do so, follow these instructions:

1. If your rules and decoders are related to existent ones in the ruleset, you should add them at the end of the corresponding file. If they are made for a new application or device that Wazuh does not currently support, you must create a new `XML` following the title format. For example, if the last `XML` file is `0620-last-xml_rules.xml`, the next one should be named `0625-new_integration.xml`. Please, make sure your rules do not use an existent `rule id`.

2. Make sure to create your `test.ini` file. You may find examples under the `wazuh/wazuh-ruleset/tools/rules-testing/tests` folder. Then add it to the repository along with the rest of the tests.

3. Open the Pull Request.

If you are not familiar with GitHub, you can also share them through [our users mailing list](https://groups.google.com/d/forum/wazuh), to which you can subscribe by sending an email to `wazuh+subscribe@googlegroups.com`. As well do not hesitate to request new rules or SCA policies that you would like to see running in Wazuh and the team will do their best to make it happen.

## Web references

* [Wazuh website](http://wazuh.com)
