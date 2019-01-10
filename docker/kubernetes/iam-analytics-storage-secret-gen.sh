#!/bin/sh

echo "Enter Azure Storage account name..."
read -s ACCOUNT_NAME
echo "Enter Azure Storage key..."
read -s STORAGE_KEY


ACCOUNT_NAME_BASE64_ENC=$(echo ${ACCOUNT_NAME} | sed -e 's/[[:space:]]*$//' | tr -d '\n' | base64)
STORAGE_KEY_BASE64_ENC=$(echo ${STORAGE_KEY} | sed -e 's/[[:space:]]*$//' | tr -d '\n' | base64)


sed -e "s#{{account_name_data}}#${ACCOUNT_NAME_BASE64_ENC}#g" \
    -e "s#{{storage_key_data}}#${STORAGE_KEY_BASE64_ENC}#g" ./templates/flask-starter-storage-secret-template.yaml > ./flask-starter-storage-secret.yaml

echo "Task completed! flask-starter-storage-secret.yaml file created. Remember to delete the file once it has been uploaded to Kubernetes."