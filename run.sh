# Load .env file
export $(grep -v '^#' .env | xargs)

# Run Gunicorn server
$(pwd)/.venv/bin/gunicorn --log-level info --access-logfile - -w 4 -b 0.0.0.0:$PORT server:app