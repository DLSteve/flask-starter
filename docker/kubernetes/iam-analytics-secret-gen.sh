#!/bin/sh

echo "Enter Application secret..."
read -s SECRET_KEY
echo "Enter Azure AD client secret..."
read -s AZURE_CLIENT_SECRET
echo "Enter Azure Storage account key..."
read -s AZURE_STORAGE_ACCOUNT_KEY
echo "Enter the database URI..."
read -s SQLALCHEMY_DATABASE_URI
echo "Enter Celery broker URL..."
read -s BROKER_URL
echo "Enter Celery results backent URL..."
read -s RESULT_BACKEND


SECRET_KEY_BASE64_ENC=$(echo ${SECRET_KEY} | base64 | tr -d '\n')
AZURE_CLIENT_SECRET_BASE64_ENC=$(echo ${AZURE_CLIENT_SECRET} | base64 | tr -d '\n')
AZURE_STORAGE_ACCOUNT_KEY_BASE64_ENC=$(echo ${AZURE_STORAGE_ACCOUNT_KEY} | base64 | tr -d '\n')
SQLALCHEMY_DATABASE_URI_BASE64_ENC=$(echo ${SQLALCHEMY_DATABASE_URI} | base64 | tr -d '\n')
BROKER_URL_BASE64_ENC=$(echo ${BROKER_URL} | base64 | tr -d '\n')
RESULT_BACKEND_BASE64_ENC=$(echo ${RESULT_BACKEND} | base64 | tr -d '\n')


sed -e "s#{{secret_key_data}}#${SECRET_KEY_BASE64_ENC}#g" \
    -e "s#{{azure_client_secret_data}}#${AZURE_CLIENT_SECRET_BASE64_ENC}#g" \
    -e "s#{{azure_storage_account_key_data}}#${AZURE_STORAGE_ACCOUNT_KEY_BASE64_ENC}#g" \
    -e "s#{{sqlalchemy_database_uri_data}}#${SQLALCHEMY_DATABASE_URI_BASE64_ENC}#g" \
    -e "s#{{broker_url_data}}#${BROKER_URL_BASE64_ENC}#g" \
    -e "s#{{result_backend_data}}#${RESULT_BACKEND_BASE64_ENC}#g" ./templates/flask-starter-secret-template.yaml > ./flask-starter-secret.yaml

echo "Task completed! flask-starter-secret.yaml file created. Remember to delete the file once it has been uploaded to Kubernetes."