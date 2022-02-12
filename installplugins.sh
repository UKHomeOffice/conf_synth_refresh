#!/bin/bash

timestamp() {
  date +"%Y-%m-%d %H:%M:%S"
}

# Icons
ERROR="\xe2\x9d\x97"
INFO="\xe2\x84\xb9\xef\xb8\x8f"
SUCCESS="\xe2\x9c\x85"


ADMIN_USRNAME=$USERNAME
ADMIN_PWD=$PASSWORD
CONFLUENCE_BASE_URL=https://confluence.shs-dev.dsa-notprod.homeoffice.gov.uk

declare -a APP_FILE_PATH=('drawio-confluence-plugin-9.4.22.obr' 'elements-spreadsheet-3.6.2.jar' 'gliffy-confluence-plugin-8.6.5.obr' 'tablefilter-5.3.21.jar')

for value in "${APP_FILE_PATH[@]}"
do
    UPM_TOKEN=$(curl -I --user $ADMIN_USRNAME:$ADMIN_PWD -H 'Accept: application/vnd.atl.plugins.installed+json' $CONFLUENCE_BASE_URL'/rest/plugins/1.0/?os_authType=basic' 2>/dev/null | grep 'upm-token' | cut -d " " -f 2 | tr -d '\r')
    command=$(curl -f -s --user ${ADMIN_USRNAME}:${ADMIN_PWD} -H 'Accept: application/json' ${CONFLUENCE_BASE_URL}'/rest/plugins/1.0/?token='${UPM_TOKEN} -F plugin=@./conf_plugins/$value)
    mycmd=$?
    if [ $mycmd -eq 0 ]; then
        timestamp
        echo -e "$SUCCESS Successfully Installed ${value} \n"
    else
        timestamp
        echo -e "$ERROR Error Installing ${value}"
    fi
done