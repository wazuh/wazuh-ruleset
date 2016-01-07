# Change Log
All notable changes to this project will be documented in this file.

## [Unreleased]
### Added
- Amazon Decoders & Rules:
  - EC2
  - IAM
- web-accesslog-iis-default decoder
- New rules for sudo
- New rules for systemd
- Auditd Rules
- Folder tools
- Shellshock rules

### Changed
- Minor changes in some decoders and rules.
- Auditd Decoders
- Netscaler updated
- Script fixes

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