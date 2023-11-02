param (
    [string]$action,
    [string[]]$libraries
)

# Specify the path to the virtual environment folder
$venvFolder = ".\venv"  # Change this to the path of your virtual environment

if ($action -eq "install") {
    if ($libraries.Count -eq 0) {
        Write-Host "No libraries provided for installation."
        exit 1
    }

    # Activate the virtual environment
    & "$venvFolder\Scripts\Activate.ps1"

    # Install the specified Python libraries
    & pip install $libraries

    # Generate requirements.txt after installation
    & pip freeze | Out-File -FilePath "requirements.txt" -Encoding utf8
    Write-Host "Installed libraries and updated requirements.txt."

    # Deactivate the virtual environment
    & "$venvFolder\Scripts\Deactivate.ps1"
}
elseif ($action -eq "uninstall") {
    if ($libraries.Count -eq 0) {
        Write-Host "No libraries provided for uninstallation."
        exit 1
    }

    # Activate the virtual environment
    & "$venvFolder\Scripts\Activate.ps1"

    # Uninstall the specified Python libraries
    $libraries | ForEach-Object { & pip uninstall -y $_ }

    # Generate requirements.txt after uninstallation
    & pip freeze | Out-File -FilePath "requirements.txt" -Encoding utf8
    Write-Host "Uninstalled libraries and updated requirements.txt."

    # Deactivate the virtual environment
    & "$venvFolder\Scripts\Deactivate.ps1"
}
else {
    Write-Host "Invalid action. Use 'install' or 'uninstall'."
    exit 1
}
