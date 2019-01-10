#!/bin/bash
set -e

cd /flask-starter
iamctl db upgrade
iamctl static
cd /flask-starter/app

export APP_VERSION=$(sed -n 1p /default/version)
export APP_COMMIT=$(sed -n 2p /default/version)
export APP_COMMIT_FULL=$(sed -n 3p /default/version)


gunicorn --error-logfile - -w 4 -b 0.0.0.0:8000 uwsgi:app