import os
import subprocess
from datetime import datetime
import json

CONFIG_PATH = os.path.join(os.getcwd(), 'config.json')

def display_info():
    try:
        print("="*63)        # Print a line of 63 "=" characters
        print("                  x264-64 Stability test v3.00 BETA 2")        # Print the title of the stability test
        print("                  Now more Configurable")
        print("="*63)        # Print another line of 63 "=" characters
        print()
        subprocess.run(["x264-64", "--version"])  # Run the command "x264-64 --version" as a subprocess
        print()
    except Exception as e:         # If an exception occurs, print the error message
        print(f"Failed to display info: {e}")

import os

import os
import math

def get_max_threads():
    while True:
        try:            
            # Automatically detect the number of available threads
            available_threads = os.cpu_count()
            print(f"The system detected {available_threads} available threads.")
            
            # Prompt the user to enter the maximum number of threads
            recommended_threads = int(math.ceil(available_threads * 1.33))
            # Ensure the recommended number of threads is even
            if recommended_threads % 2 != 0:
                recommended_threads += 1

            print ("You can enter a number of threads to use for the encoding.")
            print ("It is recommended to enter a value 33 percent higher than what you have available.")
            max_threads = int(input(f"Enter the maximum number of threads (recommended: {recommended_threads}): ")) 
            
            # Check if the entered value is less than or equal to 0
            if max_threads <= 0:                 
                # Raise a ValueError if the entered value is invalid
                raise ValueError("Invalid number. Please enter a valid number.")             

            # Break out of the loop if a valid value is entered
            break
        except ValueError as e:             
            # Print the error message if the entered value is not a valid integer
            print(e)     

    # Return the maximum number of threads
    return max_threads



def get_log_name(log_prefix, log_extension):     # Loop indefinitely until a unique log name is obtained
    while True:         # Get the current timestamp in the format "YYYYMMDD_HH_MM"
        timestamp = datetime.now().strftime("%Y%m%d_%H_%M")
        user_input = input("Log name = ").strip()        # Prompt the user to enter a log name and remove any leading/trailing whitespace
        log_name = f"{log_prefix}{user_input or 'twister'}_{timestamp}.{log_extension}"         # Create the log name using the provided log prefix, user input (or 'twister' if empty), timestamp, and log extension
    
        if not os.path.exists(log_name):         # Check if the log name already exists in the file system
            return log_name            # If the log name is unique, return it
        print("File already exists. Please choose a different name.")        # If the log name already exists, print an error message and continue the loop

def get_loops_config():    # A list of tuples containing loop configurations
    configs = [
        ("Maximum Threads", 10),       # Configuration for maximum threads
        ("Half Threads", 10),          # Configuration for half threads
        ("Quarter Threads", 10),       # Configuration for quarter threads
        ("Eighth Threads", 10),        # Configuration for eighth threads
        ("Minimal Threads", 10)        # Configuration for minimal threads
    ]
    user_config = []     # An empty list to store user configurations
    print("Please specify the number of loops for each thread count (between 0-50):")

    for config_name, default_value in configs:        # Loop until valid input is provided
        while True:
            try:                 # Prompt the user for input, displaying the config name and default value
                value = input(f"{config_name} (default is {default_value}): ")
                if value == "":                    # If no input is provided, use the default value
                    value = default_value
                else:                    # Convert the input to an integer
                    value = int(value)                  
                    if value < 0 or value > 50:  # Check if the value is within the valid range of 0 to 50
                        raise ValueError                 
                user_config.append((config_name, value))   # Append the config name and value to the user_config list            
                break # Break out of the while loop and move to the next config
            except ValueError:                # If an invalid input is provided, display an error message
                print("Invalid input. Please enter a number between 0 and 50.")
    total_loops = sum(value for config_name, value in user_config)    # Calculate the total sum of values in the user_config list
    while True:        # Print the user's configurations
        print("\nYour configurations:")        # Iterate over each configuration name and value in user_config
        for config_name, value in user_config:            # Print the configuration name and value
            print(f"{config_name}: {value} loops")
        
        print(f"\nTotal loops configured: {total_loops}")
        confirm = input("Do you want to proceed with this configuration? (yes/no): ").strip().lower()
        

        if confirm == "yes":        # If the user confirms, return the user_config
            return user_config
        elif confirm == "no":        # If the user does not confirm, call the get_loops_config() function to get new configurations
            return get_loops_config()
        else:        # If the user enters an invalid choice, print an error message
            print("Invalid choice. Please enter 'yes' or 'no'.")
            
def write_log_header(log_filename, max_threads, half_threads, quarter_threads, eighth_threads):
    try:
        with open(log_filename, 'a') as log_file:
            log_file.write(f"{log_header2}\n{log_header1}\n{log_header2}\n\n")
            subprocess.run(["x264-64", "--version"], stdout=log_file, text=True)
            log_file.write('\n')
            
            log_file.write("==== Configuration =============================================\n\n")
            log_file.write(f"Log name = {log_filename}\n")
            log_file.write(f"Maximum Threads = {max_threads}\n")
            log_file.write(f"Half Threads = {half_threads}\n")
            log_file.write(f"Quarter Threads = {quarter_threads}\n")
            log_file.write(f"Eighth Threads = {eighth_threads}\n")  # New log entry for eighth threads
            log_file.write(f"Minimal Threads = 2\n\n")  # New log entry for 2 thread test
    except Exception as e:
        print(f"Failed to write log header: {e}")

def encode(log_filename, loops_list, threads_list):
    for i, (loops, current_thread) in enumerate(zip(loops_list, threads_list)):
        for j in range(loops):
            current_time = datetime.now().strftime('%H:%M:%S')
            print(f"Loop {j + 1} with {current_thread} threads: {current_time}")
            
            with open(log_filename, 'a') as log_file:
                log_file.write(f"Loop {j + 1} with {current_thread} threads: {current_time}\n")
                
                try:
                    process = subprocess.Popen([
                        "x264-64",  # No change: Specifies the x264 64-bit encoder executable
                        "--quiet",  # No change: Suppresses the printing of log messages to the console
                        "--preset", "slower",  # No change: tried from "slower" to "veryslow": to utilize the slowest preset, but CPU load was decreased.
                        "--crf", "0",  # Changed from "16" to "0": to instruct the encoder to attempt lossless compression, greatly increasing CPU load
                        "--threads", str(current_thread),  # No change: Specifies the number of threads for encoding, defined by "current_thread" variable
                        "--rc-lookahead", "72",  # Changed from "40" to "72": to increase the number of frames analyzed before encoding a frame, increasing CPU usage
                        "--aq-strength", "1.5",  # No change: Maintains a strong adaptive quantization to balance bit allocation within each frame
                        "--aq-mode", "3",  # New Addition: Setting AQ mode to 3, enables a more detailed analysis for bit distribution, increasing CPU usage
                        "--merange", "64",  # Changed from "24" to "64": to increase the motion estimation search range, requiring more CPU resources
                        "--me", "esa",  # New Addition: Switches the motion estimation method to exhaustive search, which is the most CPU-intensive option
                        "--subme", "11",  # Changed from "10" to "11": to set the highest level of subpixel estimation, increasing CPU usage
                        "--psy-rd", "2.0:0",  # Changed from "1.5:0" to "2.0:0": to increase the psychovisual optimization strength, increasing CPU demand
                        "--bframes", "16",  # New Addition: Increases the number of B-frames, enhancing compression efficiency but utilizing more CPU
                        "--b-adapt", "2",  # New Addition: Enables a more complex algorithm for B-frame adaptation, increasing CPU usage
                        "--ref", "16",  # New Addition: Increases the number of reference frames, utilizing more CPU resources for potentially higher quality output
                        "--trellis", "2",  # New Addition: Enables the most detailed trellis quantization method, consuming more CPU resources
                        "--no-fast-pskip",  # New Addition: Disables fast P-skip to force the encoder to evaluate more prediction modes, requiring more CPU resources
                        "--deblock", "-3:-3",  # New Addition: Alters the deblock filter settings for more aggressive deblocking, which is more CPU-intensive
                        "--video-filter", "crop:0,20,0,22/resize:width=1920,height=1040,method=lanczos4",  # No change: Keeps the filter chain for cropping and resizing the video with a high-quality resampling method
                        "--thread-input",  # No change: Maintains threaded input, potentially improving performance by reading input in a separate thread
                        "--output", "encode.mkv",  # No change: Specifies the output file and format
                        "test-1080p.mp4",  # No change: Specifies the input file to be encoded
                        "--aud",  # No change: Continues to insert access unit delimiters for better compatibility with some players and editing systems

                    ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

                    stdout_output, stderr_output = process.communicate()
                
                    stdout_output = stdout_output.strip()
                    if stdout_output:
                        print(stdout_output)  # print the progress dynamically
                        log_file.write(stdout_output + '\n')  # log the progress dynamically

                    stderr_output = stderr_output.strip()
                    if stderr_output:
                        print(stderr_output)  # print any error messages
                        log_file.write(stderr_output + '\n')  # log any error messages
                
                    if process.returncode != 0:
                        print(f"Process ended with return code {process.returncode}")
                        log_file.write(f"Process ended with return code {process.returncode}\n")
                except Exception as e:
                    print(f"An error occurred: {e}")
                    log_file.write(f"An error occurred: {e}\n")

def clean_up(log_filename):
    try:
        with open(log_filename, 'a') as log_file:
            log_file.write(f"Finish: {datetime.now().strftime('%H:%M:%S %Y-%m-%d')}\n\n")
            log_file.write("="*63 + '\n')

        subprocess.run(["ping", "127.0.0.1", "-n", "1", "-w", "1000"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        for pattern in files_to_delete[1:]:
            subprocess.run(["del", pattern], shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        subprocess.run(["move", log_filename, ".."], shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except Exception as e:
        print(f"Failed to clean up: {e}")

def reset():
    try:
        for pattern in files_to_delete:
            try:
                os.remove(pattern)
            except FileNotFoundError:
                pass
    except Exception as e:
        print(f"Failed to reset: {e}")

def save_config(config, filename='config.json'):
    try:
        with open(filename, 'w') as f:
            json.dump(config, f, indent=4)
        print(f"Configuration saved successfully to {filename}")
    except Exception as e:
        print(f"Failed to save config: {e}")

def load_config():
    try:
        with open('config.json', 'r') as file:
            config = json.load(file)
        
        # Verify the necessary keys are in the config
        necessary_keys = ['max_threads', 'half_threads', 'quarter_threads', 'eighth_threads', 'minimal_threads', 'loops_list']
        if all(key in config for key in necessary_keys):
            print("Configuration loaded successfully.")
            return config
        else:
            raise ValueError("Configuration file is missing necessary keys.")
    
    except json.JSONDecodeError:
        print("Failed to load config: Configuration file is not a valid JSON.")
    except FileNotFoundError:
        print("Failed to load config: Configuration file not found.")
    except ValueError as e:
        print(f"Failed to load config: {e}")
    except Exception as e:
        print(f"An unexpected error occurred while loading the config: {e}")
    
    # If we reach here, it means config loading failed. So we delete the possibly corrupt config file to allow the script to create a new one.
    if os.path.exists('config.json'):
        os.remove('config.json')
        print("Invalid configuration file has been deleted.")
    
    return None

def display_thread_values(max_threads, half_threads, quarter_threads, eighth_threads):
    print(f"Maximum Threads = {max_threads}")
    print(f"Half Threads = {half_threads}")
    print(f"Quarter Threads = {quarter_threads}")
    print(f"Eighth Threads = {eighth_threads}")

def setup_log_file(log_prefix, log_extension):
    log_name = get_log_name(log_prefix, log_extension)
    log_filename = f"{log_prefix}{log_name}"
    print(f"Log name = {log_filename}")
    return log_filename

def get_loop_and_thread_configurations():
    prev_config = load_config()
    if prev_config:
        max_threads = prev_config['max_threads']
        half_threads = prev_config['half_threads']
        quarter_threads = prev_config['quarter_threads']
        eighth_threads = prev_config['eighth_threads']
        minimal_threads = prev_config.get('minimal_threads', 2)  # Default to 2 if not found in the config
    else:        
        os.chdir("test")
        display_info()        

        max_threads = get_max_threads()        
        half_threads = max_threads // 2
        quarter_threads = max_threads // 4
        eighth_threads = max_threads // 8  
        minimal_threads = 2  # Set default value for minimal_threads

    # Get loop configurations in all cases, not only in the else block
    loops_config = get_loops_config()
    loops_list = [value for _, value in loops_config]

    # Include loop configuration in the saved configuration
    current_config = {
        'max_threads': max_threads,
        'half_threads': half_threads,
        'quarter_threads': quarter_threads,
        'eighth_threads': eighth_threads,
        'minimal_threads': minimal_threads,  # Save minimal threads here
        'loops_list': loops_list,  # Save loops list here
    }
    save_config(current_config)
    
    threads_list = [max_threads, half_threads, quarter_threads, eighth_threads, minimal_threads]
    return loops_list, threads_list

def main():
    try:
        # Get thread and loop configurations
        loops_list, threads_list = get_loop_and_thread_configurations()
        
        max_threads, half_threads, quarter_threads, eighth_threads = threads_list[:-1]
        
        # Save the current configuration (it seems you are saving it again here, consider if this is necessary as it is already saved in get_loop_and_thread_configurations)
        current_config = {
            'max_threads': max_threads,
            'half_threads': half_threads,
            'quarter_threads': quarter_threads,
            'eighth_threads': eighth_threads,
            'loops_list': loops_list,  # Save loops list here
        }
        save_config(current_config)
        
        display_thread_values(max_threads, half_threads, quarter_threads, eighth_threads)        # Display the thread values
        log_filename = setup_log_file(log_prefix, log_extension)        # Set up the log file
        reset()        # Reset the environment
        write_log_header(log_filename, max_threads, half_threads, quarter_threads, eighth_threads)        # Write the log header
        encode(log_filename, loops_list, threads_list) # Start the encoding process
        clean_up(log_filename)        # Cleanup after the encoding process
        input(f"Hit ENTER to open the directory containing {log_filename} and exit.")        # Prompt the user to open the output directory and then exit the script
        subprocess.run(["explorer.exe", os.path.abspath(os.path.join(".."))])
    except Exception as e:
        print(f"An unexpected error occurred in main: {e}")        # Handle any unexpected errors

if __name__ == "__main__":
    log_header1 = "                     x264-64 Stability test"
    log_header2 = "=" * 63
    log_prefix = ""
    log_extension = "txt"
    encoder_log_prefix = "encoderLoop"
    encoder_log_extension = "log"

    files_to_delete = [
        f"{encoder_log_prefix}*.{encoder_log_extension}",
        "*.stats",
        "*.mbtree",
        "encode.mkv",
        f"{log_prefix}*.{log_extension}",
    ]

    main()

