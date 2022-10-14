#!/bin/sh

if [ $# -lt 1 ]; then
    echo "Usage: $* file"
    echo "Passing arguments to $0 file too"
    exit 1
fi

cd $HOME/projects/VidSucker
if [ -d $1 ]; then
    echo "Found file: $1"
fi
source porn/bin/activate
pip install -r requirements.txt
echo "activate project for python"
if [ ! -d "./results" ]; then
    echo "No results found creating results directory."
    mkdir -p ./results
fi

echo "Running scripts..."
echo $1 | python3 script.py
echo "Done!"
