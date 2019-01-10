#!/bin/bash

su celery -c "export PATH=\"/home/celery/.local/bin:$PATH\" && celery worker --workdir=/flask-starter/ --loglevel=INFO --app=app.worker.celery --time-limit=10800"
