#!/bin/bash
WAZUH_MANAGER_DIR="/var/ossec"
WAZUH_REPO_DIR="/home/vagrant/wazuh-ruleset"
rm -rf ${WAZUH_MANAGER_DIR}/ruleset/rules/*
rm -rf ${WAZUH_MANAGER_DIR}/ruleset/decoders/*
cp -r ${WAZUH_REPO_DIR}/rules/* ${WAZUH_MANAGER_DIR}/ruleset/rules
cp -r ${WAZUH_REPO_DIR}/decoders/* ${WAZUH_MANAGER_DIR}/ruleset/decoders
chown -R root:ossec ${WAZUH_MANAGER_DIR}/ruleset/rules
chown -R root:ossec ${WAZUH_MANAGER_DIR}/ruleset/decoders
chmod 644 ${WAZUH_MANAGER_DIR}/ruleset/rules/0015-ossec_rules.xml
rm -rf ${WAZUH_MANAGER_DIR}/ruleset/rules/log-entries
rm -rf ${WAZUH_MANAGER_DIR}/ruleset/rules/translated
cd ${WAZUH_REPO_DIR}/tools/rules-testing/
./runtests.py
