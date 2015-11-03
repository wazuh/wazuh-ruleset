#!/bin/bash

# You need to set execute permission for this script:
#   chmod +x autoinstall_rules.sh
# You need to run the script as root
#   sudo ./autoinstall_rules.sh

new_rules=("puppet" "netscaler")

date=`date +%Y%m%d`
backup="$date""bk"

ossec_path="/var/ossec/"
path_decoder=$ossec_path"etc/decoder.xml"
path_rules=$ossec_path"rules/"
path_ossec_conf=$ossec_path"etc/ossec.conf"

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
echo "The following rules will be installed: "
printf '%s\n' "${install[@]}"
echo


echo "Installing..."
save_conf=true
for item in ${install[@]}
do
    if [[ $item == "ossec" ]]
    then
        # Decoders
        path="decoder.xml"
        echo "[Decoder] $item"
        cp $path_decoder $path_decoder.$backup
        echo "  Backup: $path_decoder.$backup"
        cp $path $path_decoder
        echo "  Done"
        
        # Rules
        echo "[Rules] $item"
        filename="$ossec_path""rules_$backup.zip"
        zip -r $filename $path_rules >/dev/null
        echo "  Backup: $filename"
        for rule in `ls ./ossec | grep _rules.xml | egrep -v 'local_rules'`
        do
            cp "./ossec/$rule" $path_rules
        done
        echo "  Done"
        
        echo
    else
        # Decoders
        echo "[Decoder] $item"
        
        if grep -iq "<decoder name=\"$item" $path_decoder # check if decoders exists
        then
            echo "  Error: $item already exists in $path_decoder"
            echo "  **MANUAL STEP** Install this decoder manually"
            #ToDo: Automatically
        else
            path="./$item/$item""_decoders.xml"
            cat $path >> $path_decoder
            echo "  Done"
        fi
        
        # Rules
        path="./$item/$item""_rules.xml"
        echo "[Rules] $item"
        cp $path $path_rules
        echo "  Done"
        
        # ossec.conf
        echo  "[ossec.conf] $item"
        
        if [ "$save_conf" = true ] ; then
            cp $path_ossec_conf  $path_ossec_conf.$backup # Backup just first time
            echo "  Backup: $path_ossec_conf.$backup"
            save_conf=false
        fi

        new_rule=$item"_rules.xml"
        if grep -iq "<include>$new_rule</include>" $path_ossec_conf # check if item exists
        then
            echo "  $new_rule already exists in $path_ossec_conf"
        else
            sed -i "s/.*<\/rules>.*/    <include>$new_rule<\/include>\n&/" $path_ossec_conf
        fi
        echo "  Done"

        # Info
        case $item in
            ("puppet") 
            echo "[Info] $item"
            echo "  **MANUAL STEP** Follow the last given instruction in the file instructions.md"
            ;;
        esac
        
        echo
    fi
done


#Restart ossec
echo "Restarting OSSEC..."
/var/ossec/bin/ossec-control restart


# Wazuh
echo -e "\nWazuh.com\n"
