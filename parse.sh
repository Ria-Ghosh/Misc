#!/bin/bash

echo -e "###Fetching edge details"
# serial_number=$(lshw | grep serial)
# echo $serial_number
edge_details=$(curl -X GET --header "serial-number: 1423622024849" "http://4.236.140.95:8005/api/kc/getEdgeDeviceConfig")
IFS='"'

SUB1='X_Tenant_id'
prefix1=${edge_details%%$SUB1*}
index1=${#prefix1}
if [[ "$edge_details" == *"$SUB1"* ]]; then
  ch1=${edge_details:index1:55}
  read -ra values1 <<< "$ch1"
  for value in "${values1[@]}"; do
    length=${#value}
    if [[ "$length" == 36  ]]; then
        tenant_ID=$value
        echo "$tenant_ID"
        # echo "$value"
    fi
  done
fi

SUB2='kcedgedevice_id'
prefix2=${edge_details%%$SUB2*}
index2=${#prefix2}
if [[ "$edge_details" == *"$SUB2"* ]]; then
  ch2=${edge_details:index2:30}
  read -ra values2 <<< "$ch2"
  for value in "${values2[@]}"; do
    length=${#value}
    if [[ "$length" == 9 ]]; then
        edge_ID=$value
        echo "$edge_ID"
    fi
  done
fi
# echo $edge_details
export TENANT_ID=$tenant_ID
export EDGE_ID=$edge_ID