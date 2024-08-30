#!/bin/bash

rm -rf instance
rm -rf contents/images
rm -rf contents/videos

command_exists() {
    command -v "$1" >/dev/null 2>&1
}

if ! command_exists pip; then
    echo "pip is not installed. Please install pip to continue."
    exit 1
fi

if ! command_exists sqlite3; then
    echo "sqlite3 is not installed. Please install sqlite3 to continue."
    exit 1
fi


rm -rf .venv
virtualenv .venv

source .venv/bin/activate

pip install -r requirements.txt

if ! flask shell <<EOF
exec(open('init.py').read())
exit()
EOF
then
    echo "Error: Failed to execute init.py. Please ensure you have a .env file configured properly."
    exit 1
fi

sqlite3 instance/blog-flask.db < seed/categories.sql

echo "successfully initialized"