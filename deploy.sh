#!/bin/bash
#
# usage: venv/bin/dotenv run svaudio/deploy.sh

source venv/bin/activate
set -ex
cd svaudio
git reset --hard HEAD
git checkout "${BRANCH}"
git fetch
git reset --hard "origin/${BRANCH}"
pip install -Ur requirements/production.txt
npm run build
dotenv run ./manage.py collectstatic --noinput
dotenv run ./manage.py compress
dotenv run ./manage.py migrate
touch config/wsgi.py
cd ..
supervisorctl -c supervisor/supervisor.conf restart celery