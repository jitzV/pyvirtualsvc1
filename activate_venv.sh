#!/bin/bash
# filepath: d:\_MyLearnings\PycharmProjects\18_FassAPI_ModuleExample\activate_venv.sh

# Check if the virtual environment directory exists
if [ -d "venv" ]; then
    # Activate the virtual environment
    source venv/bin/activate
    echo "Virtual environment activated."
else
    echo "Error: Virtual environment not found. Please create it first."
fi