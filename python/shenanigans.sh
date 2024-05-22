#!/bin/bash

# Path to your python script
PYTHON_SCRIPT="/home/ec2-user/environment/huggingface/scripts/start.py"


VENV_PATH="/home/ec2-user/environment/huggingface/venv/bin/activate"

# Interval in seconds
INTERVAL=10

# Activate the virtual environment
source $VENV_PATH/bin/activate


# Infinite loop
while true
do
    # Run the Python script
    python3 $PYTHON_SCRIPT

    # Wait for X seconds
    sleep $INTERVAL
done

deactivate 