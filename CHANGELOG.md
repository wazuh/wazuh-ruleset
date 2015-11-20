# Change Log
All notable changes to this project will be documented in this file.

## [Unreleased]
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

### Removed


## [v1.0] - 2015-08-24
- Inital version: OSSEC out-of-the-box rules, decoders and rootchecks.