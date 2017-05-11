# Wazuh Rules Reference


| Rule                       | Description           |
| -------------------------- |-----------------------|
| rules_config.xml           | Main rules. |
| pam_rules.xml              | A pluggable authentication module (PAM) is a mechanism to integrate multiple low-level authentication schemes into a high-level API. |
| sshd_rules.xml             | sshd (SSH Daemon) is the daemon program for ssh. |
| telnetd_rules.xml          | Telnet protocol daemon. |
| syslog_rules.xml           | Rules to analyze syslog messages. |
| arpwatch_rules.xml         | ARPWatch is a computer software tool for monitoring Address Resolution Protocol traffic on a computer network. |
| symantec-av_rules.xml      | Symantec is an antivirus program. |
| symantec-ws_rules.xml      | Symantec Web Security. |
| pix_rules.xml              | Cisco PIX (Private Internet eXchange) is a popular IP firewall and network address translation (NAT) appliance. |
| named_rules.xml            | named is a Domain Name System (DNS) server. |
| smbd_rules.xml             | SMBD is a server that can provide most SMB services. The server provides filespace and printer services to clients using the SMB protocol. |
| vsftpd_rules.xml           | vsftpd is an FTP server for Unix-like systems, including Linux. |
| pure-ftpd_rules.xml        | Pure-FTPd is a free (BSD license) FTP Server. |
| proftpd_rules.xml          | ProFTPD is an FTP server. |
| ms_ftpd_rules.xml          | Microsoft FTP rules. |
| ftpd_rules.xml             | Simple FTP server. |
| hordeimp_rules.xml         | IMP is the Internet Messaging Program and provides webmail access to IMAP and POP3 accounts. |
| roundcube_rules.xml        | Roundcube is a web-based IMAP email client. |
| wordpress_rules.xml        | WordPress is a free and open-source content management system (CMS) based on PHP and MySQL. |
| cimserver_rules.xml        | Compaq Insight Manager Server. |
| vpopmail_rules.xml         | vpopmail is a free GPL software, to provide a way to manage virtual e-mail domains and non /etc/passwd e-mail accounts on qmail mail servers. |
| vmpop3d_rules.xml          | vm-pop3d is a POP3 server. |
| courier_rules.xml          | IMAP/POP3 server. |
| web_rules.xml              | Web access rules. |
| web_appsec_rules.xml       | Rules for vulnerabilities and attacks related with web. |
| apache_rules.xml           | Apache is the world's most used web server software. |
| nginx_rules.xml            | Nginx is a web server with a strong focus on high concurrency, performance and low memory usage. |
| php_rules.xml              | PHP is a server-side scripting language designed for web development but also used as a general-purpose programming language. |
| mysql_rules.xml            | MySQL is an open-source relational database management system (RDBMS). |
| postgresql_rules.xml       | PostgreSQL is an object-relational database management system (ORDBMS) with an emphasis on extensibility and on standards-compliance. |
| ids_rules.xml              | IDS events detected by OSSEC. |
| squid_rules.xml            | Squid is a caching and forwarding web proxy. |
| firewall_rules.xml         | Firewall events detected by OSSEC. |
| apparmor_rules.xml         | AppArmor is a Linux kernel security module that allows the system administrator to restrict programs's capabilities with per-program profiles. |
| cisco-ios_rules.xml        | Cisco IOS is a software used on most Cisco Systems routers and current Cisco network switches. |
| netscreenfw_rules.xml      | Netscreen is a high performance firewall. |
| sonicwall_rules.xml        | SonicWall is a network firewall. |
| postfix_rules.xml          | Postfix is a free and open-source mail transfer agent (MTA) that routes and delivers electronic mail. |
| sendmail_rules.xml         | Sendmail is a general purpose internetwork email routing facility that supports many kinds of mail-transfer and delivery methods, including SMTP. |
| imapd_rules.xml            | imapd is the Courier IMAP server that provides IMAP access to Maildir mailboxes. |
| mailscanner_rules.xml      | MailScanner is a highly respected open source email security system design for Linux-based email gateways. |
| dovecot_rules.xml          | Dovecot is an open-source IMAP and POP3 server for Linux/UNIX-like systems, written primarily with security in mind. |
| ms-exchange_rules.xml      | Microsoft Exchange Server is a calendaring and mail server developed by Microsoft. |
| racoon_rules.xml           | Racoon is a key management daemon used for VPN connections. |
| vpn_concentrator_rules.xml | Cisco VPN Concentrator. |
| spamd_rules.xml            | spamd is a spam-deferral daemon and works directly with smtp connections. |
| msauth_rules.xml           | Microsoft Windows events deteced by OSSEC. |
| mcafee_av_rules.xml        | McAfee is an antivirus program. |
| trend-osce_rules.xml       | Trend Micro OSCE (Office Scan) rules. |
| ms-se_rules.xml            | Microsoft Security Essentials (MSE) is an antivirus software (AV) product that provides protection against different types of malicious software. |
| policy_rules.xml           | Policy rules (login during weekends, non-business hours) |
| zeus_rules.xml             | Zeus is a lite Web Server. |
| solaris_bsm_rules.xml      | Solaris Basic Security Module (BSM) can create an extremely detailed audit trail for all processes on the system. |
| vmware_rules.xml           | VMware is a virtualization software. |
| ms_dhcp_rules.xml          | Microsoft DHCP rules. |
| asterisk_rules.xml         | Asterisk is a software implementation of a telephone private branch exchange (PBX). |
| ossec_rules.xml            | Main rules. |
| attack_rules.xml           | Signatures of different attacks detected by OSSEC. |
| openbsd_rules.xml          | OpenBSD is a Unix-like computer operating system descended from BSD. |
| clam_av_rules.xml          | Clam AntiVirus (ClamAV) is a free and open-source, cross-platform antivirus software tool-kit able to detect many types of malicious software. |
| dropbear_rules.xml         | Dropbear provides a Secure Shell-compatible server and client. It is designed as a replacement for OpenSSH for environments with low resources. |
| sysmon_rules.xml           | Rules to detect Windows Process Anomalies. |
| auditd_rules.xml           | The Linux Audit system provides a way to track security-relevant information on your system. |
| opensmtpd_rules.xml        | OpenSMTPD is a FREE implementation of the server-side SMTP protocol as defined by RFC 5321, with some additional standard extensions. |
| firewalld_rules.xml        | FirewallD provides a managed firewall with support for network/firewall zones to define the trust level of network connections or interfaces. |
| systemd_rules.xml          | Systemd is a software suite for central management and configuration of the GNU/Linux operating system. |
| unbound_rules.xml          | Unbound is a validating, recursive, and caching DNS server software. |
| puppet_rules.xml           | Puppet is an open-source configuration management utility. |
| netscaler_rules.xml        | NetScaler is a hardware device (or network appliance) manufactured by Citrix, which primary role is to provide Level 4 Load Balancing. |
| serv-u_rules.xml           | FTP Server software (FTP, FTPS, SFTP, Web & mobile) for secure file transfer and file sharing on Windows & Linux. |
| usb_rules.xml              | USB rules |
| amazon_rules.xml           | Amazon rules: EC2, IAM, S3, etc. |
| redis_rules.xml            | Redis is an open source (BSD licensed), in-memory data structure store, used as database, cache and message broker. |
| oscap_rules.xml            | OpenSCAP is an open-source software that provides assessment, measurement and enforcement of security baselines. |
| fortigate_rules.xml        | Fortigate (Fortinet) firewalls. |
| hp_rules.xml               | HP Switch rules |
| openvpn_rules.xml          | OpenVPN is an open-source software application that implements virtual private network (VPN) techniques. |
| rsa-auth-manager_rules.xml | RSA Authentication Manager is a platform behind RSA SecurID that allows for centralized management of the RSA SecurID environment. |
| imperva_rules.xml          | Cyber security software and services to protect companies' sensitive data and application software from attacks. |
| sophos_rules.xml           | Sophos Anti-Virus. |
| freeipa_rules.xml          | Open source project for identity management. |
| cisco-estreamer_rules.xml  | Cisco Event Streamer (eStreamer) allows you to stream FireSIGHT System intrusion, discovery, and connection data from the Cisco to external client applications. |
| ms_wdefender_rules.xml     | Windows Defender is an anti-malware component of Microsoft Windows. |
| ms_logs_rules.xml          | Microsoft Windows logs rules. |
| ms_sqlserver_rules.xml     | Microsoft SQL Server is a relational database management system developed by Microsoft. |
| identity_guard_rules.xml   | Identity Guard is a proactive privacy and identity theft protection service. |
| mongodb_rules.xml          | MongoDB is a free and open-source cross-platform document-oriented database program. |
| docker_rules.xml           | Docker is an open-source project that automates the deployment of applications inside software containers. |
| jenkins_rules.xml          | Jenkins is an open source automation server written in Java. The project was forked from Hudson. |
| suricata_rules.xml       | Suricata is an open source network threat detection engine. It is capable of real time intrusion detection (IDS), intrusion prevention (IPS) and network security monitoring (NSM). |
