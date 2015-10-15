#Instructions for Puppet rules
**Created by Wazuh, Inc. <ossec@wazuh.com>**

 1. Append *puppet_decoders.xml* to */var/ossec/etc/decoders.xml*
 2. Copy *puppet_rules.xml* to */var/ossec/rules/*
 3. Some rules need to read a command output, so it is necessary to copy the code below to */var/ossec/etc/ossec.conf* (in **every agent**)
```xml
<localfile>
    <log_format>full_command</log_format>
    <command>timestamp_puppet=`cat /var/lib/puppet/state/last_run_summary.yaml | grep last_run | cut -d: -f 2 | tr -d '[[:space:]]'`;timestamp_current_date=$(date +"%s");diff_min=$((($timestamp_current_date-$timestamp_puppet)/60));if [ "$diff_min" -le "30" ];then echo "Puppet: OK. It runs in the last 30 minutes";else puppet_date=`date -d @"$timestamp_puppet"`;echo "Puppet: KO. Last run: $puppet_date";fi</command>
    <frequency>2100</frequency>
</localfile>
```

\*Also you can copy the code to */var/ossec/etc/shared/agent.conf* in **OSSEC Master** and configure in every agent the logcollector option to accept remote commands from the manager: 
*/var/ossec/etc/internal_options.conf*:

    # Logcollector - If it should accept remote commands from the manager
    logcollector.remote_commands=1