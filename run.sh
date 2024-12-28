#!/bin/bash

# Function to deactivate virtualenv and exit
cleanup() {
    if [ -n "$VIRTUAL_ENV" ]; then
        echo "Deactivating virtual environment"
        deactivate
    fi
    exit 0
}

# Load .env file
export $(grep -v '^#' .env | xargs)

# Trap SIGINT (Ctrl + C) and call cleanup
trap cleanup SIGINT

# Start the workflow server
 
# Check if running inside Docker
if [ -f /.dockerenv ]; then
    echo "Running inside Docker"
    gunicorn --log-level info --access-logfile - -w 4 -b 0.0.0.0:$PORT server:app
else
    echo "Running on local machine"
    source .venv/bin/activate

    # Run Gunicorn server
    gunicorn --log-level info --access-logfile - -w 4 -b 0.0.0.0:$PORT server:app
    deactivate
fi