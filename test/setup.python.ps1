# Function to install Python from Windows Store
function Install-PythonFromStore {
    try {
        # Open Python app page on the Windows Store
        Invoke-Expression 'start ms-windows-store://pdp/?productid=9P7QFQBJD4NP'
        
        # Inform the user to install Python manually
        Write-Host "Please install Python from the Windows Store. Once installed, press any key to continue or 'Enter' to exit."
        
        # Read user input to continue or exit
        if ([string]::IsNullOrWhiteSpace($(Read-Host))) {
            exit
        }
    } catch {
        Write-Host "An error occurred: $_"
        exit
    }
}

# Function to add Python to the PATH environment variable
function Add-PythonToPath {
    try {
        $PythonPath = [System.IO.Path]::Combine($env:USERPROFILE, 'AppData\Local\Microsoft\WindowsApps')
        $env:Path += ";$PythonPath"
        [System.Environment]::SetEnvironmentVariable('Path', $env:Path, [System.EnvironmentVariableTarget]::User)
        
        Write-Host "Python has been added to the PATH environment variable."
    } catch {
        Write-Host "An error occurred while adding Python to PATH: $_"
        exit
    }
}

# Function to associate .py files with Python executable
function Set-PyFileAssociation {
    try {
        $PythonExePath = [System.IO.Path]::Combine($env:USERPROFILE, 'AppData\Local\Microsoft\WindowsApps', 'python3.9.exe')
        assoc .py=PythonFile
        ftype PythonFile="$PythonExePath %1 %*"
        
        Write-Host ".py files have been associated with the Python executable."
    } catch {
        Write-Host "An error occurred while setting file association: $_"
        exit
    }
}

# Main script body
while ($true) {
    # Step 1: Install Python from Windows Store
    Install-PythonFromStore
    
    # Step 2: Add Python to the PATH environment variable
    Add-PythonToPath
    
    # Step 3: Associate .py files with Python executable
    Set-PyFileAssociation
    
    # Ask the user if they would like to retry or exit
    Write-Host "Setup completed successfully. Would you like to retry the setup? (Press any key to retry or 'Enter' to exit)"
    
    # Read user input to retry or exit
    if ([string]::IsNullOrWhiteSpace($(Read-Host))) {
        exit
    }
}
