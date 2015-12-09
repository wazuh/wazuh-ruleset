#Instructions for Puppet rules
**Created by Wazuh, Inc. <ossec@wazuh.com>**

Run `ossec_ruleset.py -r` to install Puppet rules. More information about automatic installation [here](http://documentation.wazuh.com/en/latest/ossec_ruleset.html#automatic-installation).

If you prefer to install the rules manually follow the instructions listed [here](http://documentation.wazuh.com/en/latest/ossec_ruleset.html#manual-installation).

### Last step
Some rules need to read the output of a command. **To complete the installation you must perform the following step**:

Copy the code below to */var/ossec/etc/shared/agent.conf* in your **OSSEC Manager** to allow OSSEC execute this command and read its output:
```xml
<agent_config>
	<localfile>
	    <log_format>full_command</log_format>
	    <command>timestamp_puppet=`cat /var/lib/puppet/state/last_run_summary.yaml | grep last_run | cut -d: -f 2 | tr -d '[[:space:]]'`;timestamp_current_date=$(date +"%s");diff_min=$((($timestamp_current_date-$timestamp_puppet)/60));if [ "$diff_min" -le "30" ];then echo "Puppet: OK. It runs in the last 30 minutes";else puppet_date=`date -d @"$timestamp_puppet"`;echo "Puppet: KO. Last run: $puppet_date";fi</command>
	    <frequency>2100</frequency>
	</localfile>
</agent_config>
```
 Also you must configure in **every agent** the logcollector option to accept remote commands from the manager. To do this, add the following lines to */var/ossec/etc/internal_options.conf*:

    # Logcollector - If it should accept remote commands from the manager
    logcollector.remote_commands=1
