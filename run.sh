python3 -m venv venv
pip install -r requirements.txt
gunicorn --bind=0.0.0.0 --timeout 600 startup:app