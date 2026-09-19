#!/usr/bin/env bash
# Render runs this on every deploy
set -o errexit

pip install -r requirements.txt
python manage.py collectstatic --noinput
python manage.py migrate

# First deploy only: load the sections/products exported from the old SQLite database
if python manage.py shell -c "from shoppingapp.models import section; import sys; sys.exit(0 if section.objects.exists() else 1)"; then
    echo "Shop data already present, skipping fixture"
else
    python manage.py loaddata shop_data.json
fi

# Creates the admin login from DJANGO_SUPERUSER_* env vars (skipped if it already exists)
python manage.py createsuperuser --noinput || true
