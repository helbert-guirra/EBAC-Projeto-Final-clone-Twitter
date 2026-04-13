#!/usr/bin/env bash
# O Render executa esse script na fase de build

set -o errexit   # para tudo se algum comando falhar

pip install --upgrade pip
pip install -r requirements.txt

python manage.py collectstatic --noinput
python manage.py migrate
