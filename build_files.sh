echo "installing requirements..."
pip install -r requirements.txt

echo "Collecting stataic..."
python3.9 manage.py collectstatic --noinput

echo "Making Migrations..."
python3.9 manage.py makemigrations --noinput

echo "Migrating to Database..."
python3.9 manage.py migrate --noinput