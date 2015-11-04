#!/bin/bash

# You need to set execute permission for this script:
#   chmod +x autoinstall_rules.sh
# You need to run the script as root
#   sudo ./autoinstall_rules.sh

new_rules=("puppet" "netscaler")

date=`date +%Y%m%d`
backup="$date"".bk"

ossec_path="/var/ossec/"
path_decoder=$ossec_path"etc/decoder.xml"
path_rules=$ossec_path"rules/"
path_ossec_conf=$ossec_path"etc/ossec.conf"
log_file=$ossec_path"install_log."$backup

#Exit immediately if a command exits with a non-zero status
set -e


if [[ $1 != "update" ]] ; then
    # ** Check OSSEC path **
    read -p "OSSEC path is \"$ossec_path\"? (Y/n)" -n 1

    if [[ $REPLY =~ ^[nN]$ ]]; then
        echo
        read -p "Path to OSSEC: " 
        ossec_path=$REPLY
        path_decoder=$ossec_path"etc/decoder.xml"
        path_rules=$ossec_path"rules/"
        path_ossec_conf=$ossec_path"etc/ossec.conf"
        log_file=$ossec_path"install_log."$backup
    fi
    
    # ** Dialog **
    cmd=(dialog --separate-output --checklist "What rules do you want to install?:" 22 76 16)
    options=(1 "ossec" on
                   2 "puppet" off
                   3 "netscaler" off)
    choices=$("${cmd[@]}" "${options[@]}" 2>&1 >/dev/tty)
    clear
    for choice in $choices
    do
        case $choice in
            1) #OSSEC = 1
            install+=(${options[1]})
            ;;
            2) #Puppet = 4
            install+=(${options[4]})
            ;;
            3) #Netscaler = 7
             install+=(${options[7]})
            ;;
        esac
    done
else
    # Get all rules
    rules=`grep -Po "<include>\K.*?(?=_rules)" $path_ossec_conf`

    install+=("ossec")
    
    # Get new rules if exist
    for new in ${new_rules[@]}
    do
        for rule in ${rules[@]}
        do
            if [[ $new == $rule ]]; then
                install+=($rule)
            fi            
        done
    done
fi

# ** Install **
echo "The following rules will be installed: " | tee $log_file
printf '%s\n' "${install[@]}" | tee -a $log_file
echo | tee -a $log_file


echo "Installing..." | tee -a $log_file
save_conf=true
for item in ${install[@]}
do
    if [[ $item == "ossec" ]]
    then
        # Decoders
        path="decoder.xml"
        echo "[Decoder] $item" | tee -a $log_file
        cp $path_decoder $path_decoder.$backup
        echo "  Backup: $path_decoder.$backup" | tee -a $log_file
        cp $path $path_decoder
        echo "  Done" | tee -a $log_file
        
        # Rules
        echo "[Rules] $item" | tee -a $log_file
        filename="$ossec_path""rules_$backup.tar"
        #zip -r $filename $path_rules >/dev/null
        tar -cf $filename $path_rules # Extract: tar -xvf $filename
        echo "  Backup: $filename" | tee -a $log_file
        for rule in `ls ./ossec | grep _rules.xml | egrep -v 'local_rules'`
        do
            cp "./ossec/$rule" $path_rules
        done
        echo "  Done" | tee -a $log_file
        
        echo | tee -a $log_file
    else
        # Decoders
        echo "[Decoder] $item" | tee -a $log_file
        
        if grep -iq "<decoder name=\"$item" $path_decoder # check if decoders exists
        then
            echo "  Error: $item already exists in $path_decoder" | tee -a $log_file
            echo "  **MANUAL STEP** Install this decoder manually" | tee -a $log_file
            #ToDo: Automatically
        else
            path="./$item/$item""_decoders.xml"
            cat $path >> $path_decoder
            echo "  Done" | tee -a $log_file
        fi
        
        # Rules
        path="./$item/$item""_rules.xml"
        echo "[Rules] $item" | tee -a $log_file
        cp $path $path_rules
        echo "  Done" | tee -a $log_file
        
        # ossec.conf
        echo  "[ossec.conf] $item" | tee -a $log_file
        
        if [ "$save_conf" = true ] ; then
            cp $path_ossec_conf  $path_ossec_conf.$backup # Backup just first time
            echo "  Backup: $path_ossec_conf.$backup" | tee -a $log_file
            save_conf=false
        fi

        new_rule=$item"_rules.xml"
        if grep -iq "<include>$new_rule</include>" $path_ossec_conf # check if item exists
        then
            echo "  $new_rule already exists in $path_ossec_conf" | tee -a $log_file
        else
            sed -i "s/.*<\/rules>.*/    <include>$new_rule<\/include>\n&/" $path_ossec_conf
        fi
        echo "  Done" | tee -a $log_file

        # Info
        case $item in
            ("puppet") 
            echo "[Info] $item" | tee -a $log_file
            echo "  **MANUAL STEP** Follow the last given instruction in the file instructions.md" | tee -a $log_file
            ;;
        esac
        
        echo | tee -a $log_file
    fi
done

#Restart ossec
echo "Restarting OSSEC..." | tee -a $log_file
/var/ossec/bin/ossec-control restart | tee -a $log_file


# Wazuh
echo -e "\nWazuh.com\n" | tee -a $log_file
