# Big Buck Bunny Download/Renamer for x264 Stability Testing

This Python script facilitates the downloading of files from a specified URL to your local machine. It currently is configured to download a Big Buck Bunny movie clip in 1080p resolution.

## Features

- Error handling: If any HTTP or URL errors occur during the download, they will be caught and detailed messages will be displayed.
- Retry mechanism: In the case of an error, you have the option to retry the download process.
- Informative messages: The script provides updates on the status of the download process, including the initiation of the download and whether the file has been saved successfully.

## Prerequisites

- Python 3.x

## Usage

1. Save the script to a Python file (e.g., `file_downloader.py`).
2. Open a terminal or command prompt.
3. Navigate to the directory where `file_downloader.py` is saved.
4. Run the script using the following command:

    ```shell
    python file_downloader.py
    ```

5. Follow the on-screen messages to know the status of the download process.
6. In case of failure, you can choose to retry the download by entering 'y' when prompted.

## Customization

To download a different file, modify the `url` variable in the script with the desired file's URL. Also, update the `destination_filename` variable to specify the name under which the file should be saved locally. We are assuming `test-1080p.mp4`.
## Troubleshooting

- Ensure that the URL specified in the `url` variable is correct and accessible.
- If you encounter HTTP error 429, it means there have been too many requests to the server. Try again after some time.
- If the script reports a file not found error, check the URL or try changing the destination filename.

## License

This script is provided "as is" without any warranty. Use it at your own risk.

