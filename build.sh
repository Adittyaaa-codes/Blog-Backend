set -o errexit

pip install --upgrade pip setuptools wheel

pip install -r requirements.txt

python manage.py collectstatic --no-input

python manage.py migrate

if [[ $CREATE_SUPERUSER == "true" ]]; then
    python manage.py createsuperuser --noinput
fi