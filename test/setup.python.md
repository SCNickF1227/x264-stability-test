# Python Setup Script for Windows - THIS IS UNTESTED

This PowerShell script automates the setup of Python on a Windows machine by performing the following actions:

1. Directs the user to install Python from the Windows Store.
2. Adds Python to the user's PATH environment variable.
3. Sets up file associations for `.py` files, allowing them to be executed by double-clicking.

## Prerequisites

- Windows 10 or newer.
- PowerShell with administrative privileges.

## Usage

1. Save the script to a file named `SetupPython.ps1`.
2. Open PowerShell as an administrator.
3. Navigate to the directory where `SetupPython.ps1` is located.
4. Run the script using the following command:

    ```shell
    .\SetupPython.ps1
    ```

5. Follow the on-screen prompts to install Python from the Windows Store.
6. Press any key to proceed to the next step or press Enter to exit the script at any prompt.

## Troubleshooting

If you encounter errors while running the script, ensure that:

- You are running PowerShell with administrative privileges.
- You have a stable internet connection to access the Windows Store and download Python.

## Notes

- The script assumes Python 3.9 as the version to be installed. If a different version is installed, modify the `$PythonExePath` variable in the `Set-PyFileAssociation` function accordingly.
- The script adds Python to the user's PATH environment variable, allowing Python to be accessed from any command prompt or PowerShell window.
- After running the script, open a new command prompt or PowerShell window to ensure the updated PATH environment variable is loaded.

## License

This script is provided "as is" without any warranty. Use it at your own risk.

