#!/bin/bash

file_name="quizmaster_23f2001161"

if ! command -v python3 &> /dev/null
then
    echo "Python3 is not installed."
    exit 1
fi

echo "Creating venv for the app..."
python3 -m venv "./$file_name"

echo "Activating the virtual environment..."
source ".$file_name/bin/activate"


echo "Installing dependencies from requirements.txt..."
pip install -r requirements.txt


echo "Setup complete!!"
echo "to start the server run python3 app.py"
echo "Starting for the first time"

python3 app.py



