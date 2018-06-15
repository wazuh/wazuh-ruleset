# Change Log
All notable changes to this project will be documented in this file.

## [v3.4.0]

### Added
  - CIS rootchecks for Windows 2012 R2 (by @Bob-Andrews).
  - Extract port name for Sysmon event 3. ([#127](https://github.com/wazuh/wazuh-ruleset/pull/127))
  - Improve Shellshock detection. ([#115](https://github.com/wazuh/wazuh-ruleset/pull/115))

### Fixed
  - Windows rules: Fix SID syntax for group membership changes. ([#125](https://github.com/wazuh/wazuh-ruleset/pull/125)).
  - Windows decoders: Match "Subject :" format ([#128](https://github.com/wazuh/wazuh-ruleset/pull/128)).

## [v3.3.1]

### Added

  - Rule to detect when agents are unable to unmerge shared files. ([#143](https://github.com/wazuh/wazuh-ruleset/pull/143))

## [v3.3.0]

There are no changes for Wazuh Ruleset in this version.


## [v3.2.4]

There are no changes for Wazuh Ruleset in this version.


## [v3.2.3]

### Added
  - GDPR (General Data Protection Regulation) mapping.
  - Improve GeoIP and composite rule support for AWS events.
  - Pfsense rules.

### Fixed
  - Error handling in update ruleset script using python3.


## [v3.2.2]
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


## [v3.2.1]
### Fixed
  - Silence rules about OpenSCAP and CIS-CAT scan status.
  - Add compatibility between versions for CIS-CAT rules.
  - Sudo decoders extract commands with spaces.


## [v3.2.0]
### Added
  - Added new rules for _Vulnerability detector_.

### Removed
  - Removed svchost.exe and inetsrv.exe processes checking outside SysNative due to false positive.

### Fixed
  - Fixed `update_ruleset` script.


## [v3.1.0]
### Added
  - New rules for VULS integration
  - New rules for CIS-CAT integration

## [v3.0.0]
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
