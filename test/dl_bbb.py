from urllib.request import urlretrieve
from urllib.error import HTTPError, URLError
import os

url = "https://download.blender.org/demo/movies/BBB/bbb_sunflower_1080p_60fps_normal.mp4"
destination_filename = "test-1080p.mp4"

while True:
    try:
        # Inform the user about the start of the download process
        print(f"Starting download from {url}...")

        # Downloading the file
        urlretrieve(url, destination_filename)
        
        # Inform the user that the download was successful
        print(f"File downloaded and renamed to {destination_filename}")
        break

    except HTTPError as e:
        # Detailed error handling for HTTP errors
        if e.code == 429:
            print("HTTP error 429: Too many requests. Please try again later.")
        else:
            print(f"HTTP error occurred: HTTP Status Code {e.code}")
    except URLError as e:
        # Detailed error handling for URL errors
        print(f"URL error occurred: {e.reason}")
    except Exception as e:
        # Generic error message for other types of exceptions
        print(f"An unknown error occurred while downloading the file: {e}")

    # Checking if the file exists in the current directory and informing the user
    if os.path.isfile(destination_filename):
        print(f"The file {destination_filename} has been saved to the current directory.")
        break
    else:
        print(f"The file could not be found in the current directory. Please ensure the URL is correct and try again.")
        retry = input("Do you want to retry? (y/n): ").strip().lower()
        if retry != 'y':
            break

# Prompting the user to press enter to exit
input("Press Enter to exit...")
