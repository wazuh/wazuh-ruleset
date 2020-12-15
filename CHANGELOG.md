# Change Log
All notable changes to this project will be documented in this file.

## [v4.1.0]

### Added

- Let the Ruleset update tool to bypass the version check with the force option. ([#773](https://github.com/wazuh/wazuh-ruleset/pull/773))
- Added new AWS Config-History rules to make it more granular by including every item status supported. ([#775](https://github.com/wazuh/wazuh-ruleset/pull/775))

### Changed

- FIM rules have been adapted to the improvements for Windows Registry monitoring. ([#768](https://github.com/wazuh/wazuh-ruleset/pull/768))

### Fixed

- Updated MITRE techniques in web rules. ([#810](https://github.com/wazuh/wazuh-ruleset/pull/810))
- Fixed Sonicwall predecoder to accept whitespaces at the beginning. ([#503](https://github.com/wazuh/wazuh-ruleset/pull/503))


## [v4.0.1]

### Fixed

- Removed duplicated Windows rules for EventChannel. ([#771](https://github.com/wazuh/wazuh-ruleset/pull/771))


## [v4.0.0]

### Changed

- Changed compliance rules groups and removed `alert_by_email` option by default. ([#559](https://github.com/wazuh/wazuh-ruleset/pull/559))
- Let the Ruleset update tool pick up the current version branch by default. ([#753](https://github.com/wazuh/wazuh-ruleset/pull/753))


## [v3.13.0]

### Added

- Added rules and decoders for macOS sshd logs ([#593](https://github.com/wazuh/wazuh-ruleset/pull/593))
- Added TSC/SOC compliance mapping ([#613](https://github.com/wazuh/wazuh-ruleset/pull/613))
- Added rules and decoders for PaloAlto logs ([#658](https://github.com/wazuh/wazuh-ruleset/pull/658))
- Added rules and decoder to monitor the FIM database status. ([#4717](https://github.com/wazuh/wazuh/pull/4717))
- Added rules for WAF. ([#687](https://github.com/wazuh/wazuh-ruleset/pull/687))

### Changed

- Changed description of Vulnerability Detector rules ([#638](https://github.com/wazuh/wazuh-ruleset/pull/638))
- Changed squid decoders ([#672](https://github.com/wazuh/wazuh-ruleset/pull/672))

### Fixed

- Fix the provider name so that Windows Eventlog logs match with the Wazuh rules. ([#662](https://github.com/wazuh/wazuh-ruleset/pull/662))
- Fixed static filters related to the system_name field. ([#684](https://github.com/wazuh/wazuh-ruleset/pull/684))
- Remove trailing whitespaces in the group name section of the ruleset. Thanks to Kevin Branch (@branchnetconsulting). ([#667](https://github.com/wazuh/wazuh-ruleset/pull/667))
- Remove invalid zeroes from rules id. Thanks to @lucanus81. ([#691](https://github.com/wazuh/wazuh-ruleset/pull/691))


## [v3.12.1]

### Fixed

- Fixed the Dropbear brute force rule entrypoint. ([#589](https://github.com/wazuh/wazuh-ruleset/pull/589))


## [v3.12.0]

### Added

- Extend the rules to detect shellshock attacks (by @iasdeoupxe). ([#459](https://github.com/wazuh/wazuh-ruleset/pull/479))
- Update Roundcube decoder to support versions greater than 1.4 (by @iasdeoupxe). ([#537](https://github.com/wazuh/wazuh-ruleset/pull/537))
- Added Junos rules and decoders ([#581](https://github.com/wazuh/wazuh-ruleset/pull/581))

### Fixed

- Fix GPG requirement in Windows rules. ([#562](https://github.com/wazuh/wazuh-ruleset/pull/562))
- Improve Cisco decoders and fix Owlh rule's IDs conflict. ([#570](https://github.com/wazuh/wazuh-ruleset/pull/570))
- Fixed checkpoint decoders to read events with a different format. ([#156](https://github.com/wazuh/wazuh-ruleset/pull/156))

## [v3.11.2]

### Fixed

- Fixed permissions of the VERSION file. ([#545](https://github.com/wazuh/wazuh-ruleset/pull/545))


## [v3.11.0]

### Added

- Add rules and decoders for McAfee EPO. ([#467](https://github.com/wazuh/wazuh-ruleset/pull/467))
- Add PCI-DSS mapping to vulnerability detector rules. ([#525](https://github.com/wazuh/wazuh-ruleset/pull/525))
- Add a new base rule for Microsoft Windows Firewall With Advanced Security/Firewalls. ([#532](https://github.com/wazuh/wazuh-ruleset/pull/532))

### Changed

- Let osquery daemon messages appear in alerts as the full log. ([#531](https://github.com/wazuh/wazuh-ruleset/pull/531))
- Make double-point termination optional in the postfix decoder (by @iasdeoupxe). ([#245](https://github.com/wazuh/wazuh-ruleset/pull/245))

### Fixed

- Fix typo in network checks for SCA Debian 8 and 9 policies. ([#514](https://github.com/wazuh/wazuh-ruleset/pull/514))
- Fix path in audit checks for SCA Debian 8 and 9 policies. ([#527](https://github.com/wazuh/wazuh-ruleset/pull/527))
- Fix last space in regular expression for SCA check about NTP. ([#521](https://github.com/wazuh/wazuh-ruleset/pull/521))
- Unify SCA regular expressions about installed packages by dpkg. ([#522](https://github.com/wazuh/wazuh-ruleset/pull/522))

## [v3.10.0]

### Added

- Add rules for VIPRE antivirus. ([#327](https://github.com/wazuh/wazuh-ruleset/pull/327))
- Add decoders and rules for Panda-PAPS. ([#437](https://github.com/wazuh/wazuh-ruleset/pull/437))
- Add decoders and rules for CheckPoint Smart-1 firewalls. ([#440](https://github.com/wazuh/wazuh-ruleset/pull/440))
- Add Windows Software Restriction Policy rules. ([#461](https://github.com/wazuh/wazuh-ruleset/pull/461))
- Add perdition (imap/pop3 proxy) rules (by @gkissand). ([#407](https://github.com/wazuh/wazuh-ruleset/pull/407))
- Extend event detection for Windows Defender decoders (by @MarauderDueling). ([#220](https://github.com/wazuh/wazuh-ruleset/pull/220))
- Add support for NAXSI web application firewall (by @kravietz). ([#354](https://github.com/wazuh/wazuh-ruleset/pull/354))
- Improved postfix decoder (by @iasdeoupxe). ([#410](https://github.com/wazuh/wazuh-ruleset/pull/410))
- Add rule to alert about changes in system time. ([#239](https://github.com/wazuh/wazuh-ruleset/pull/239))
- Add rule to detect sudo actions from users other than root. ([#149](https://github.com/wazuh/wazuh-ruleset/pull/149))
- Add Cisco-ASA rules and decoders. ([#425](https://github.com/wazuh/wazuh-ruleset/pull/425))
- Add HIPAA compliance groups to ruleset. ([#400](https://github.com/wazuh/wazuh-ruleset/pull/400))
- Add mapping for HIPAA and NIST_800_53 compliance to SCA policies. ([#421](https://github.com/wazuh/wazuh-ruleset/pull/421))
- SCA policies have been improved and refactored. ([#406](https://github.com/wazuh/wazuh-ruleset/pull/406))
- Add recon group to SSH rule (by @kravietz). ([#323](https://github.com/wazuh/wazuh-ruleset/pull/323))
- Add rule to detect untrusted kernel modules being loaded (by @kravietz). ([#323](https://github.com/wazuh/wazuh-ruleset/pull/323))
- Add rule for rndg failure (by @kravietz). ([#323](https://github.com/wazuh/wazuh-ruleset/pull/323))
- Add rules for RAID and disk failure (by @kravietz). ([#323](https://github.com/wazuh/wazuh-ruleset/pull/323))
- Add rule for ZFS error message (by @kravietz). ([#323](https://github.com/wazuh/wazuh-ruleset/pull/323))
- Add rule for systemd status=1/FAILURE (by @kravietz). ([#323](https://github.com/wazuh/wazuh-ruleset/pull/323))

### Fixed

- Fix Sonicwall decoders. ([#274](https://github.com/wazuh/wazuh-ruleset/pull/274))
- Fix for Windows decoder. ([#154](https://github.com/wazuh/wazuh-ruleset/pull/154))
- Fix regex to detect rootkit trojans (by @erinish). ([#144](https://github.com/wazuh/wazuh-ruleset/pull/144))
- Fix rules about shellshock attack. ([#458](https://github.com/wazuh/wazuh-ruleset/pull/458))

## [v3.9.3] 2019-07-09

### Fixed

- NGINX Decoder: make "server" field optional. Thanks to @iasdeoupxe. ([#243](https://github.com/wazuh/wazuh-ruleset/pull/243))
- Remove tailing quote from field "res" in Auditd decoder. Thanks to @branchnetconsulting. ([#412](https://github.com/wazuh/wazuh-ruleset/pull/412))
- Fix conflict between fields "uid" and "auid" in Auditd decoder. Thanks to @tokibi. ([#246](https://github.com/wazuh/wazuh-ruleset/pull/246))
- Prevent rules for AWS, Suricata, VirusTotal, OwnCloud, Vuls, CIS-CAT, Vulnerability Detector, MySQL, Osquery, and Azure from including the full log in JSON format. ([#443](https://github.com/wazuh/wazuh-ruleset/pull/443))

## [v3.9.2] 2019-06-10

### Fixed

- Fixed Windows rule about audit log. ([#408](https://github.com/wazuh/wazuh-ruleset/pull/408))
- Fixed check 11522 of Solaris SCA policy. ([#420](https://github.com/wazuh/wazuh-ruleset/pull/420))

## [v3.9.1] 2019-05-21

### Fixed

- Fixed rule for the SCA check 5035 about SSH protocol. ([#385](https://github.com/wazuh/wazuh-ruleset/pull/385))
- Fixed duplicated rules for the SCA policy cis_debianlinux7-8_L2. ([#386](https://github.com/wazuh/wazuh-ruleset/pull/386))
- Fixed Windows Defender rule description. ([#388](https://github.com/wazuh/wazuh-ruleset/pull/388))
- Fixed rules and requirements for SCA CIS policies of Mac OS X. ([#387](https://github.com/wazuh/wazuh-ruleset/pull/387))
- Fixed Windows NT registries in Windows SCA policies. ([#393](https://github.com/wazuh/wazuh-ruleset/pull/393))
- Fixed Windows EventChannel rules for Eventlog and Security Essentials. ([#397](https://github.com/wazuh/wazuh-ruleset/pull/397))
- Fixed Windows rules to avoid filtering by erroneous provider names. ([#403](https://github.com/wazuh/wazuh-ruleset/pull/403))

## [v3.9.0] 2019-05-02

### Added

- Adapt Sysmon rules to new Windows eventchannel format. ([#285](https://github.com/wazuh/wazuh-ruleset/pull/285))
- Added ruleset for the SCA module. ([#288](https://github.com/wazuh/wazuh-ruleset/pull/288))
- Added policy files in YAML format for the SCA module. ([#288](https://github.com/wazuh/wazuh-ruleset/pull/288))
- Added the policy *cis_win2012r2_memberL2_rcl.yml* for SCA. ([#289](https://github.com/wazuh/wazuh-ruleset/pull/289)) (Thanks to @Bob-Andrews)
- Improved rules for the docker listener. ([#293](https://github.com/wazuh/wazuh-ruleset/pull/293)) ([#307](https://github.com/wazuh/wazuh-ruleset/pull/307))
- New options `same_field` and `not_same_field` to correlate dynamic fields in rules. ([#302](https://github.com/wazuh/wazuh-ruleset/pull/302))
- New rule to catch a logon success from a Windows workstation. ([#304](https://github.com/wazuh/wazuh-ruleset/pull/304))
- Added rules about Application and System channels for the Windows eventchannel format. ([#325](https://github.com/wazuh/wazuh-ruleset/pull/325))
- Added *PCI-DSS* and *GDPR* mapping to rules for the docker listener. ([#333](https://github.com/wazuh/wazuh-ruleset/pull/333))

### Changed

- Changed the eventchannel field names in rules. ([#299](https://github.com/wazuh/wazuh-ruleset/pull/299))
- Redistribute the eventchannel rules by incoming channel. ([#325](https://github.com/wazuh/wazuh-ruleset/pull/325))
- Prevent events invoked by AWS Internal from flooding alerts. ([#351](https://github.com/wazuh/wazuh-ruleset/pull/351))
### Fixed

- Fixed the bruteforce attack rules for Windows Eventchannel. ([#302](https://github.com/wazuh/wazuh-ruleset/pull/302))
- Updated links for Windows rules. ([#311](https://github.com/wazuh/wazuh-ruleset/pull/311)) (Credits to @atomicturtle ([#1675](https://github.com/ossec/ossec-hids/pull/1675)))
- Several fixes for Windows rules for the eventlog format. (Thanks to @branchnetconsulting)
  - Fixed SID regexes for eventlog Windows rules. ([#197](https://github.com/wazuh/wazuh-ruleset/pull/197))
  - Fixed the matched string of rule 18270. ([#219](https://github.com/wazuh/wazuh-ruleset/pull/219))
  - Fixed Sysmon rule when the destination port is empty. ([#229](https://github.com/wazuh/wazuh-ruleset/pull/229))
  - Fixed the description for rule 18260. ([#232](https://github.com/wazuh/wazuh-ruleset/pull/232))
  - Generalize description for rule 83201. ([#241](https://github.com/wazuh/wazuh-ruleset/pull/241))
- Fixed the flow for Windows rule 18230. ([#253](https://github.com/wazuh/wazuh-ruleset/pull/253)) (Thanks to @wiredaem0n)

## [v3.8.2] 2019-01-30

### Changed

- Rework of the rules for Windows Eventchannel. ([#277](https://github.com/wazuh/wazuh-ruleset/pull/277))


## [v3.8.1] 2019-01-25

There are no changes for Wazuh Ruleset in this version.


## [v3.8.0] 2019-01-19

### Added

- Added new rules to support the new Windows eventchannel decoder. ([#247](https://github.com/wazuh/wazuh-ruleset/pull/247))
- Extend Auditd decoder to support more fields. ([#256](https://github.com/wazuh/wazuh-ruleset/pull/256))
- Added rule to alert when an agent is removed. ([#2127](https://github.com/wazuh/wazuh/pull/2127))

### Changed

- Now CDB lists are not prebuilt in the repository. ([#249](https://github.com/wazuh/wazuh-ruleset/pull/249))


## [v3.7.2] 2018-12-17

There are no changes for Wazuh Ruleset in this version.

## [v3.7.1] 2018-12-05

### Added

- New Vulnerability detector rules to warn about version comparison issues. ([#237](https://github.com/wazuh/wazuh-ruleset/pull/237))


## [v3.7.0] 2018-11-10

### Added

- osquery: specific alerts for default packs. ([#196](https://github.com/wazuh/wazuh-ruleset/pull/196))
- Azure integration: Decoders and rules. ([#189](https://github.com/wazuh/wazuh-ruleset/pull/189))

### Changed

- osquery: Rename alerts fields reference. ([#196](https://github.com/wazuh/wazuh-ruleset/pull/196))
- update_ruleset is not available in worker nodes. ([#225](https://github.com/wazuh/wazuh-ruleset/pull/225))
- Update composite rules to match only same_source_ip events. ([#161](https://github.com/wazuh/wazuh-ruleset/pull/161))

### Fixed

- Fixed active response decoder in order to match with different dates. ([#223](https://github.com/wazuh/wazuh-ruleset/pull/223))

### Removed

- Removed deprecated rules for Syscheck.


## [v3.6.1] 2018-09-07

### Fixed

- Silence rule about full disk for SNAP partitions. ([#183](https://github.com/wazuh/wazuh-ruleset/pull/183))


## [v3.6.0] 2018-08-29

### Fixed

 - Fixed login abortion log mismatch in Dovecot decoder when optional parameter didn't appear. ([#171](https://github.com/wazuh/wazuh-ruleset/pull/171))
 - Fixed decoder for Debian packages. ([#172](https://github.com/wazuh/wazuh-ruleset/pull/172))
 - Fixed active response decoder. ([#179](https://github.com/wazuh/wazuh-ruleset/pull/179))

### Added

 - Compatibility with TerminalServices-Gateway event type. ([#175](https://github.com/wazuh/wazuh-ruleset/pull/175))
 - New AWS rules. ([#174](https://github.com/wazuh/wazuh-ruleset/pull/174))


## [v3.5.0] 2018-08-10

### Added

  - Rules for the new osquery integration.
  - Rule to ignore syscollector events.
  - CIS-CAT rules improved.
  - Rules and decoders for the new Kaspersky integration.
  - CIS rootchecks for Windows 2012 R2 (by @Bob-Andrews).
  - Extract port name for Sysmon event 3. ([#127](https://github.com/wazuh/wazuh-ruleset/pull/127))
  - Improve Shellshock detection. ([#115](https://github.com/wazuh/wazuh-ruleset/pull/115))

### Changed

  - Decreased agent upgrade failure rules level.

### Fixed

  - Windows rules: Fix SID syntax for group membership changes. ([#125](https://github.com/wazuh/wazuh-ruleset/pull/125)).
  - Windows decoders: Match "Subject :" format ([#128](https://github.com/wazuh/wazuh-ruleset/pull/128)).


## [v3.4.0] 2018-07-24

### Added

  - Decoder for syscheck integration with audit.

### Changed

  - Removed offset of the `frequency` attribute in rules. ([#145](https://github.com/wazuh/wazuh-ruleset/pull/145))


## [v3.3.1] 2018-06-18

### Added

  - Rule to detect when agents are unable to unmerge shared files. ([#143](https://github.com/wazuh/wazuh-ruleset/pull/143))

## [v3.3.0] 2018-06-06

There are no changes for Wazuh Ruleset in this version.


## [v3.2.4] 2018-06-01

There are no changes for Wazuh Ruleset in this version.


## [v3.2.3] 2018-05-28

### Added
  - GDPR (General Data Protection Regulation) mapping.
  - Improve GeoIP and composite rule support for AWS events.
  - Pfsense rules.

### Fixed
  - Error handling in update ruleset script using python3.


## [v3.2.2] 2018-05-07
### Fixed
  - Syntax error in cis_rhel7_linux_rcl.txt.
  - OpenLDAP decoders to extract the IP address properly.
  - Owncloud rules compatible with JSON logs.
  - Postfix decoders and rules.
  - Sendmail decoders to extract the IP address properly.
  - False positives in SLES 11 rootchecks.

### Removed
  - Removed alert_by_email for rule 1002 and 9704.

### Added
  - OpenVAS decoders and rules.
  - Pfsense decoders.
  - Mysql rules for Percona and Mcafee.
  - MariaDB decoders and rules.
  - Added rootcheck file for apache 2.2/2.4 (by @Bob-Andrews).
  - Rules to detect USB devices disconnected.


## [v3.2.1] 2018-03-03
### Fixed
  - Silence rules about OpenSCAP and CIS-CAT scan status.
  - Add compatibility between versions for CIS-CAT rules.
  - Sudo decoders extract commands with spaces.


## [v3.2.0] 2018-02-13
### Added
  - Added new rules for _Vulnerability detector_.

### Removed
  - Removed svchost.exe and inetsrv.exe processes checking outside SysNative due to false positive.

### Fixed
  - Fixed `update_ruleset` script.


## [v3.1.0] 2017-12-22
### Added
  - New rules for VULS integration
  - New rules for CIS-CAT integration

## [v3.0.0] 2017-12-12
### Added
  - New features for "update_ruleset.py": custom URL and branch name
  - New users added to list of known malicious user agents
  - OwnCloud (Rules and decoders)
  - Updated scap content from https://github.com/OpenSCAP/scap-security-guide
  - Rules for VirusTotal integration
  - Add GPG13 mappings to rules (gpg13.com)

### Changed
  - Removed "MJ12bot" from list of known malicious user agents
  - SSH decoders
  - OpenVPN decoders
  - RoundCube (Rules and decoders)


## [v2.1.0]
### Added
- Decoders and rules for anti-flooding mechanism
### Fixed
 - Fixed Windows decoders to extract the proper fields

## [v2.0.1]
### Added
- Rules/decoders:
  - Microsoft Windows Defender
  - Microsoft log related events
  - Microsoft SQL Server
  - Identity guard
  - Sysmon events 11 and 15
  - MongoDB
  - Docker
  - Jenkins
  - AWS S3
- update_ruleset.py accepts a custom download URL

### Changed
 - web-accesslog_decoders.xml
 - Amazon rules
 - Rootcheck references
 - Sysmon uses dynamic fields
 - getawslog.py: Ignore digest files
 - Fortigate decoders
 - Apache decoders

### Fixed
 - Bug in update_ruleset.py
 - Netstat command
 - SSH rootchecks


## [v2.0] - 2017-04-24
### Added
- Rules/decoders:
 - OpenSCAP
 - Switch HP 5500
 - Chrome Remote Desktop
 - Fortigate
 - OpenVPN
 - ModSecurity for Nginx
 - Barracuda
 - OpenWRT
 - RSA Authentication Manager
 - Imperva
 - Sophos
 - FreeIPA
 - Cisco eStreamer
- Rootchecks:
 - CIS SLES 11 and 12
- SCAP content
 - cve-debian-oval.xml
 - cve-redhat-6-ds.xml
 - cve-redhat-7-ds.xml
 - ssg-centos-6-ds.xml
 - ssg-centos-7-ds.xml
 - ssg-debian-8-ds.xml
 - ssg-fedora-ds.xml
 - ssg-rhel-6-ds.xml
 - ssg-rhel-7-ds.xml
 - ssg-ubuntu-1604-ds.xml

### Changed
- ossec_ruleset.py renamed to update_ruleset.py with new features.
- New directory structure.

### Fixed
- Improvements in several decoders/rules.
- RH7 rootchecks.
- Improved getgetawslog.py.
- IP version-independent regexs.


## [v1.09] - 2016-05-12
### Added
- Decoders and rules for Amazon

### Changed
- Amazon directory structure.
- Minor changes:
 - Apache and Nginx rules.
 - RH7 rootchecks.

## [v1.08] - 2016-05-05
### Added
- Redis decoders and rules.
- Rootchecks for RedHat 7.
- SUDO and SSH decoders.

### Changed
- SSH and OSSEC rules.
- Minor changes in ossec_ruleset.py.


## [v1.07] - 2016-04-05
### Added
- Decoders and rules:
 - ossec-auth
 - OpenBSD SMTP
 - SSH
 - Postfix
- ossec_ruleset.py: Option -d to update the ruleset from local files.

### Changed
- Apache Decoders
- getawslogs.py: Executing with standard users.


## [v1.06] - 2016-02-12
### Added
- Rules for Amazon VPC
- USB Decoder and Rules
- PCI Tagging for SSH rootchecks

### Changed
- *ossec_ruleset.py*: New interface.
- Directory structure of Rootcheck
- Netscreen Firewall decoder

### Fixed
- Syntax error in rootchecks.


## [v1.05] - 2016-01-27
### Fixed
- *ossec_ruleset.py*:
  - Problem with installation path
  - New path: /var/ossec/**update/ruleset/**ossec_ruleset.py


## [v1.04] - 2016-01-25
### Added
- New Rootcheck: SSH Hardening
- New rules: *ossec_ruleset.py* rules
  - Alerts related to the execution of script *ossec_ruleset.py*
- New rules and PCI Tagging for:
  - Amazon IAM
  - Amazon EC2

### Changed
- *ossec_ruleset.py*:
  - New format for *ossec_ruleset.log*
  - New path: */var/ossec/updater/ruleset*
     - All files generated by the script are stored in this directory.
     - We recommend this path to the script: /var/ossec/updater/ruleset/ossec_ruleset.py


## [v1.03] - 2016-01-08
### Added
- Amazon Decoders & Rules:
  - EC2
  - IAM
- Auditd Rules
- Shellshock rules
- New rules for sudo
- New rules for system
- New decoder: web-accesslog-iis-default decoder
- Folder tools:
  - amazon: Script getawslog.py to download the JSON file from S3 Bucket.
  - file-testing: Script file_test.py to check if a log file generates alerts
  - rules-testing: Script runtests.py to run unitary tests. Created by OSSEC.

### Changed
- Auditd Decoders
- Minor changes in some decoders and rules.
- Netscaler updated
- *ossec_ruleset.py* fixes

## [v1.02] - 2015-12-09
### Added
- Serv-U Decoders & Rules.

### Changed
- Directory structure: Decoders have been split.
- Script *ossec_ruleset.py* v2:
  - Bug fixes.
  - Python 2.6 compatibility.
  - OSSEC 2.8.x compatibility.
  - Restore backups automatically.

### Fixed
- Some issues with *windows decoder* have been solved.


# [v1.01] - 2015-11-24
### Fixed
- All sysmon decoders have *windows* as parent.

## [v1.00] - 2015-11-21
### Added
- Puppet Decoders & Rules.
- Compliance mapping with PCI DSS v3.1.
- Netscaler Decoders & Rules.
- ClamAV:
    - New decoder: Extract main fields (path, virus name, hash) when a virus is detected.
    - New rule: ClamAV Stopped.
    - New rule: Virus detected multiple times.
- Sysmon decoders:
    - Decoder for the new log format of Event 1
    - Decoders for Events 2 - 8.
- Script *ossec_ruleset.py* for installing and updating rules, decoders and rootcheck.

### Changed
- SSH Decoder modified to extract user name when invalid/illegal users trying to log in.
- Sysmon Decoder for Event 1 modified (It allows use the new decoder added for this event).

## [v0.00] - 2015-08-24
- Inital version: OSSEC out-of-the-box rules, decoders and rootchecks.
