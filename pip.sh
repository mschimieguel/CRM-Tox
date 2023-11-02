#!/bin/bash
#Use para automatizar o processo de adicionar uma biblioteca

# Check if the user provided the action (install or uninstall) as the first argument
if [ $# -lt 1 ]; then
    echo "Usage: $0 <install/uninstall> [library1 library2 ...]"
    exit 1
fi

# The first argument is the action (install/uninstall)
action="$1"
shift

# Check if the virtual environment folder is specified
venv_folder="./venv"  # Change this to the path of your virtual environment

# Check if the virtual environment folder exists
if [ ! -d "$venv_folder" ]; then
    echo "Virtual environment folder '$venv_folder' not found. Please specify the correct path."
    exit 1
fi

# Activate the virtual environment
source "$venv_folder/bin/activate"

if [ "$action" == "install" ]; then
    if [ $# -eq 0 ]; then
        echo "No libraries provided for installation."
        exit 1
    fi

    # Install the specified Python libraries
    pip install "$@"

    # Generate requirements.txt after installation
    pip freeze > requirements.txt
    echo "Installed libraries and updated requirements.txt."

elif [ "$action" == "uninstall" ]; then
    if [ $# -eq 0 ]; then
        echo "No libraries provided for uninstallation."
        exit 1
    fi

    # Uninstall the specified Python libraries
    pip uninstall -y "$@"

    # Generate requirements.txt after uninstallation
    pip freeze > requirements.txt
    echo "Uninstalled libraries and updated requirements.txt."

else
    echo "Invalid action. Use 'install' or 'uninstall'."
    exit 1
fi

# Deactivate the virtual environment
deactivate

exit 0
