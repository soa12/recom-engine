#!/usr/bin/env sh

pip install -r /var/www/app/requirements.txt --user --upgrade && uvicorn app.main:app --reload --workers 1 --host 0.0.0.0 --port 8000
