#! bin/bash

ZABBIX_SERVER="127.0.0.1"

PYTHON_SCRIPT="/sciezka/do/skryptu/opcua_automated.py"

UPS_LIST=(
        "<IP z Zabbixa> <HOSTNAME z Zabbixa> <PASSWORD do opcua>"
        "<IP z Zabbixa> <HOSTNAME z Zabbixa> <PASSWORD do opcua>"
        "<IP z Zabbixa> <HOSTNAME z Zabbixa> <PASSWORD do opcua>"
        )

echo "Starting UPS monitoring script for all devices..."

for ups_entry in "${UPS_LIST[@]}"; do
    read -r UPS_IP_ADDRESS ZABBIX_HOST_NAME UPS_PASSWORD <<< "$ups_entry"

    echo "Processing UPS: $UPS_IP_ADDRESS (Zabbix Host: $ZABBIX_HOST_NAME)"

    sudo /usr/bin/python3 "$PYTHON_SCRIPT" "$UPS_IP_ADDRESS" "$ZABBIX_HOST_NAME" "$UPS_PASSWORD"

    sleep 2

done

echo "Zakonczono przetwarzanie UPS'ow"