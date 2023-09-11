import os
import subprocess
from datetime import datetime
import json
import math
import shutil
import glob
import re

CONFIG_PATH = os.path.join(os.getcwd(), 'config.json')


def find_x264_executable():
    try:
        # Get the directory where the script is located
        script_dir = os.path.dirname(__file__)

        # Construct the full path to the "test" subdirectory
        test_dir = os.path.join(script_dir, 'test')

        # Search for the x264-64.exe file within the "test" subdirectory
        for root, dirs, files in os.walk(test_dir):
            for file in files:
                if file == 'x264-64.exe':
                    return os.path.join(root, file)

        # If the executable is not found, raise an exception
        raise FileNotFoundError("x264-64.exe not found in the 'test' subdirectory.")
    except Exception as e:
        print(f"An error occurred while finding x264-64.exe: {e}")
        return None

# Example usage:
x264_executable_path = find_x264_executable()
if x264_executable_path:
    print(f"x264-64 executable found at: {x264_executable_path}")
else:
    print("x264-64 executable not found.")

def find_test_video():
    try:
        # Get the directory where the script is located
        script_dir = os.path.dirname(os.path.abspath(__file__))

        # Construct the full path to the "test" subdirectory
        test_dir = os.path.join(script_dir, 'test')

        # Search for the test-1080p.mp4 file within the "test" subdirectory
        for root, dirs, files in os.walk(test_dir):
            for file in files:
                if file == 'test-1080p.mp4':
                    return os.path.join(root, file)

        # If the video file is not found, raise an exception
        raise FileNotFoundError("test-1080p.mp4 not found in the 'test' subdirectory.")
    except Exception as e:
        print(f"An error occurred while finding test-1080p.mp4: {e}")
        return None

# Example usage:
test_video_path = find_test_video()
if test_video_path:
    print(f"test-1080p.mp4 found at: {test_video_path}")
else:
    print("test-1080p.mp4 not found.")

def display_info(x264_executable_path):
    try:
        print("="*63)        
        print("                  x264-64 Stability test v3.00 BETA 3")        
        print("                  Now more Configurable")
        print("="*63)        
        print()

        if x264_executable_path:
            process = subprocess.Popen(
                [x264_executable_path, "--version"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            stdout_output, stderr_output = process.communicate()
            
            if stdout_output:
                print("STDOUT:", stdout_output.strip())
            if stderr_output:
                print("STDERR:", stderr_output.strip())
        else:
            print("x264-64 executable not found.")
        print()
    except Exception as e:
        print(f"Failed to display info: {e}")


def get_loops_config():    # A list of tuples containing loop configurations
    configs = [
        ("Maximum Threads", 1),       # Configuration for maximum threads
        ("Half Threads", 1),          # Configuration for half threads
        ("Quarter Threads", 1),       # Configuration for quarter threads
        ("Eighth Threads", 1),        # Configuration for eighth threads
        ("Minimal Threads", 1)        # Configuration for minimal threads
    ]
    user_config = []     # An empty list to store user configurations
    print("Please specify the number of loops for each thread count (between 0-50):")
    print("One loops for each should be sufficient to determine stability")
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

        if confirm in ("yes", ""):        # Accept "yes" or an empty string as a confirmation
            return user_config
        elif confirm == "no":        # If the user does not confirm, call the get_loops_config() function to get new configurations
            return get_loops_config()
        else:        # If the user enters an invalid choice, print an error message
            print("Invalid choice. Please enter 'yes' or 'no'.")

      
def get_max_threads():
    while True:
        try:            
            # Automatically detect the number of available threads
            available_threads = os.cpu_count()
            print(f"The system detected {available_threads} available threads.")
            
            # Calculate the recommended number of threads (300% higher than available)
            recommended_threads = int(math.ceil(available_threads * 3))
            
            # Ensure the recommended number of threads is even
            if recommended_threads % 2 != 0:
                recommended_threads += 1

            print("You can enter a number of threads to use for encoding.")
            print(f"It is recommended to enter a value 3x higher than what you have available.")
            
            # Prompt the user to enter the maximum number of threads or press Enter to use recommended
            max_threads_input = input(f"Enter the maximum number of threads (recommended: {recommended_threads}), or press Enter to accept the recommended value: ").strip()
            
            # Check if the input is empty (user pressed Enter)
            if max_threads_input == "":
                max_threads = recommended_threads
            else:
                max_threads = int(max_threads_input)
            
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
        
        x264_executable_path = find_x264_executable()  # Find the x264 executable path
        display_info(x264_executable_path)  # Pass the path as an argument to display_info        

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

  
def write_log_header(log_filename, max_threads, half_threads, quarter_threads, eighth_threads, minimal_threads):
    try:
        with open(log_filename, 'a') as log_file:
            log_file.write(f"{log_header2}\n{log_header1}\n{log_header2}\n\n")
            subprocess.run([x264_executable_path, "--version"], stdout=log_file, text=True)
            log_file.write('\n')
            
            log_file.write("==== Configuration =============================================\n\n")
            log_file.write(f"Log name = {log_filename}\n")
            log_file.write(f"Maximum Threads = {max_threads}\n")
            log_file.write(f"Half Threads = {half_threads}\n")
            log_file.write(f"Quarter Threads = {quarter_threads}\n")
            log_file.write(f"Eighth Threads = {eighth_threads}\n")  # New log entry for eighth threads
            log_file.write(f"Minimal Threads = {minimal_threads}\n\n")  # New log entry for minimal threads
    except Exception as e:
        print(f"Failed to write log header: {e}")

def log_metrics(log_filename, fps_values, kb_s_values, process_success_flag, summary=False):
    # Calculate and log the average fps, kb/s and process success flag
    if fps_values:
        average_fps = sum(fps_values) / len(fps_values)
    else:
        average_fps = 0.0

    if kb_s_values:
        average_kb_s = sum(kb_s_values) / len(kb_s_values)
    else:
        average_kb_s = 0.0

    # Log the metrics in your report
    with open(log_filename, 'a') as log_file:
        if summary:
            log_file.write("\n=== Final Averages ===\n")
        log_file.write(f"Average FPS: {average_fps}\n")
        log_file.write(f"Average kb/s: {average_kb_s}\n")
        log_file.write(f"Process ended successfully: {'Yes' if process_success_flag else 'No'}\n")
    
    # Print the metrics to the console window as well
    if summary:
        print("\n=== Final Averages ===")
    print(f"Average FPS: {average_fps}")
    print(f"Average kb/s: {average_kb_s}")
    print(f"Process ended successfully: {'Yes' if process_success_flag else 'No'}\n")


def encode(log_filename, loops_list, threads_list, x264_executable_path):
    test_video_path = find_test_video()
    if not test_video_path:
        print("'test-1080p.mp4' not found, terminating the encode function.")
        return

    # Validate arguments
    if not isinstance(loops_list, list) or not all(isinstance(i, int) for i in loops_list):
        print("Invalid loops_list argument")
        return

    if not isinstance(threads_list, list) or not all(isinstance(i, int) for i in threads_list):
        print("Invalid threads_list argument")
        return

    # Added variables to store total fps and kb/s values for overall average computation
    total_fps = []
    total_kb_s = []

    for i, (loops, current_thread) in enumerate(zip(loops_list, threads_list)):
        for j in range(loops):
            current_time = datetime.now().strftime('%H:%M:%S')
            print(f"Loop {j + 1} with {current_thread} threads: {current_time}")

            with open(log_filename, 'a') as log_file:
                log_file.write(f"Loop {j + 1} with {current_thread} threads: {current_time}\n")

            # Variables to store fps and kb/s values for this loop
            fps_values = []
            kb_s_values = []

            try:
                process = subprocess.Popen([
                    x264_executable_path,  # Use only the full path of the executable here
                    "--quiet",
                    "--preset", "slower",
                    "--crf", "0",
                    "--threads", str(current_thread),
                    "--rc-lookahead", "72",
                    "--aq-strength", "1.5",
                    "--aq-mode", "3",
                    "--merange", "64",
                    "--me", "esa",
                    "--subme", "11",
                    "--psy-rd", "2.0:0",
                    "--bframes", "16",
                    "--b-adapt", "2",
                    "--ref", "16",
                    "--trellis", "2",
                    "--no-fast-pskip",
                    "--deblock", "-3:-3",
                    "--video-filter", "crop:0,20,0,22/resize:width=1920,height=1040,method=lanczos4",
                    "--thread-input",
                    "--output", "encode.mkv",
                     test_video_path,  # Replaced the hardcoded video file name with the variable
                    "--aud",
                ], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, bufsize=1)

                line_count = 0  
                print_first_line = True  

                while process.poll() is None:  
                    line = process.stdout.readline().strip()  
                    if line:
                        if print_first_line or line_count % 25 == 0:
                            print(line)  
                            print_first_line = False  
                            fps_match = re.search(r'(\d+\.\d+) fps', line)
                            kb_s_match = re.search(r'(\d+\.\d+) kb/s', line)

                            if fps_match:
                                fps_values.append(float(fps_match.group(1)))
                            if kb_s_match:
                                kb_s_values.append(float(kb_s_match.group(1)))
                            with open(log_filename, 'a') as log_file:
                                log_file.write(line + '\n')  
                        line_count += 1  

                stdout_output, stderr_output = process.communicate()

                if stdout_output is not None:
                    stdout_output = stdout_output.strip()
                    if stdout_output:
                        print(stdout_output)
                        with open(log_filename, 'a') as log_file:
                            log_file.write(stdout_output + '\n')

                if stderr_output is not None:
                    stderr_output = stderr_output.strip()
                    if stderr_output:
                        print(stderr_output)
                        with open(log_filename, 'a') as log_file:
                            log_file.write(stderr_output + '\n')
                # After the loop ends, calculate and log the average fps and kb/s for this loop
                avg_fps = sum(fps_values) / len(fps_values) if fps_values else 0
                avg_kb_s = sum(kb_s_values) / len(kb_s_values) if kb_s_values else 0

                with open(log_filename, 'a') as log_file:
                    log_file.write(f"Loop {j + 1} average FPS: {avg_fps}, average KB/S: {avg_kb_s}\n")

                # Add values to total for overall averages
                total_fps.extend(fps_values)
                total_kb_s.extend(kb_s_values)
                if process.returncode != 0:
                    print(f"Process ended with return code {process.returncode}")
                    with open(log_filename, 'a') as log_file:
                        log_file.write(f"Process ended with return code {process.returncode}\n")
                else:
                    print(f"Process ended successfully with return code {process.returncode}.")        
            except Exception as e:
                print(f"An error occurred: {e}")
                with open(log_filename, 'a') as log_file:
                    log_file.write(f"An error occurred: {e}\n")
                     # After all loops are done, calculate and log the overall averages
                overall_avg_fps = sum(total_fps) / len(total_fps) if total_fps else 0
                overall_avg_kb_s = sum(total_kb_s) / len(total_kb_s) if total_kb_s else 0

    with open(log_filename, 'a') as log_file:
        log_file.write(f"Overall average FPS: {overall_avg_fps}, overall average KB/S: {overall_avg_kb_s}\n")

def clean_up(log_filename, files_to_delete):
    try:
        with open(log_filename, 'a') as log_file:
            log_file.write(f"Finish: {datetime.now().strftime('%H:%M:%S %Y-%m-%d')}\n\n")
            log_file.write("="*63 + '\n')

        subprocess.run(["ping", "127.0.0.1", "-n", "1", "-w", "1000"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        files_deleted = []  # Keep track of files that were successfully deleted
        for pattern in files_to_delete[1:]:
            for filename in glob.glob(pattern):
                try:
                    # Check if the file has a JSON extension and skip it
                    if not filename.endswith('.json'):
                        os.remove(filename)
                        files_deleted.append(filename)
                except FileNotFoundError:
                    print(f"File not found: {filename}")

        # Remove files that were successfully deleted from the files_to_delete list
        files_to_delete[1:] = [pattern for pattern in files_to_delete[1:] if not any(filename.startswith(pattern) for filename in files_deleted)]

        try:
            shutil.move(log_filename, "..")
        except FileNotFoundError:
            print(f"File not found: {log_filename}")

    except Exception as e:
        print(f"Failed to clean up: {e}")

def reset(files_to_delete):
    try:
        files_deleted = []  # Keep track of files that were successfully deleted
        for pattern in files_to_delete:
            for filename in glob.glob(pattern):
                try:
                    # Check if the file is 'encode.mkv' and skip it if it's in use
                    if filename == 'encode.mkv':
                        os.remove(filename)
                    else:
                        with open(filename, 'rb') as f:
                            # Check if the file is in use and skip it if it is
                            pass
                        os.remove(filename)
                    files_deleted.append(filename)
                except FileNotFoundError:
                    print(f"File not found: {filename}")
                except Exception as e:
                    if "file in use" in str(e).lower():
                        print(f"Skipping file '{filename}' because it is in use.")
                    else:
                        print(f"Failed to delete file '{filename}': {e}")

        # Remove files that were successfully deleted from the files_to_delete list
        files_to_delete[:] = [pattern for pattern in files_to_delete if not any(filename.startswith(pattern) for filename in files_deleted)]

    except Exception as e:
        print(f"Failed to reset: {e}")

def save_config(config, filename='config.json'):
    try:
        # Get the directory where the script is located
        script_dir = os.path.dirname(__file__)
        
        # Construct the full path to the "test" subdirectory
        test_dir = os.path.join(script_dir, 'test')
        
        # Create the "test" subdirectory if it doesn't exist
        os.makedirs(test_dir, exist_ok=True)
        
        # Construct the full path to the config file in the "test" subdirectory
        config_path = os.path.join(test_dir, filename)

        # Ensure that all necessary keys are present in the config dictionary
        necessary_keys = ['max_threads', 'half_threads', 'quarter_threads', 'eighth_threads', 'minimal_threads', 'loops_list']
        for key in necessary_keys:
            if key not in config:
                raise ValueError(f"Configuration is missing key: {key}")

        with open(config_path, 'w') as f:
            json.dump(config, f, indent=4)
        print(f"Configuration saved successfully to {config_path}")
    except Exception as e:
        print(f"Failed to save config: {e}")


def load_config():
    try:
        # Get the directory where the script is located
        script_dir = os.path.dirname(os.path.abspath(__file__))

        # Construct the full path to the "test" subdirectory
        test_dir = os.path.join(script_dir, 'test')
        
        # Create the "test" subdirectory if it doesn't exist
        os.makedirs(test_dir, exist_ok=True)

        # Construct the full path to config.json in the "test" subdirectory
        config_path = os.path.join(test_dir, 'config.json')
        print(f"Attempting to load configuration from: {config_path}")  # Debug print

        with open(config_path, 'r') as file:
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
    if os.path.exists(config_path):
        os.remove(config_path)
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
        
        x264_executable_path = find_x264_executable()  # Find the x264 executable path
        display_info(x264_executable_path)  # Pass the path as an argument to display_info

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
        # Only save the new configuration if it is different from the previous configuration
        # Or if there was no previous configuration
    if previous_config is not None:
         if previous_config != current_config:
                save_config(current_config)  # Save the configuration only if it has changed
    else:
            save_config(current_config)  # Save the configuration if there was no previous configuration

    threads_list = [max_threads, half_threads, quarter_threads, eighth_threads, max_threads, minimal_threads]
    return loops_list, threads_list


def main():
    try:
        # Find the x264 executable path at the start
        x264_executable_path = find_x264_executable()
        
        # Call display_info at the start with the executable path
        display_info(x264_executable_path)

        # Ask the user if they want to use a previous configuration
        use_previous_config = input("Do you want to use a previous configuration? (yes/no): ").strip().lower()

        # Load the configuration here so that we can display the thread values at the start
        if use_previous_config == "yes" or not use_previous_config:
            previous_config = load_config()
        else:
            previous_config = None

        if previous_config is not None:
            max_threads = previous_config['max_threads']
            half_threads = previous_config['half_threads']
            quarter_threads = previous_config['quarter_threads']
            eighth_threads = previous_config['eighth_threads']
            minimal_threads = previous_config.get('minimal_threads', 2)
        else:
            max_threads = get_max_threads()
            half_threads = max_threads // 2
            quarter_threads = max_threads // 4
            eighth_threads = max_threads // 8
            minimal_threads = 2
        
        # Display the thread values at the start
        display_thread_values(max_threads, half_threads, quarter_threads, eighth_threads)

        if use_previous_config == "yes" or not use_previous_config:
            # Load the previous configuration
            if previous_config is not None:
                # If a previous configuration is loaded, use it to get loop configurations
                loops_list = previous_config['loops_list']
            else:
                # If no previous configuration is loaded, get loop configurations using get_loop_and_thread_configurations()
                loops_list, _ = get_loop_and_thread_configurations()
        else:
            # If the user doesn't want to use a previous configuration, get loop configurations using get_loop_and_thread_configurations()
            loops_list, _ = get_loop_and_thread_configurations()

        # Define threads_list based on the calculated thread counts
        threads_list = [max_threads, half_threads, quarter_threads, eighth_threads, max_threads, minimal_threads]
        # Save the current configuration
        current_config = {
            'max_threads': max_threads,
            'half_threads': half_threads,
            'quarter_threads': quarter_threads,
            'eighth_threads': eighth_threads,
            'loops_list': loops_list,  # Save loops list here
            'minimal_threads': minimal_threads,  # Save minimal_threads
        }
        save_config(current_config)  # Save the configuration before encoding

        # Find the path to the x264-64.exe executable
        if x264_executable_path:
            print(f"x264-64 executable found at: {x264_executable_path}")
        else:
            print("x264-64 executable not found.")

        log_filename = setup_log_file(log_prefix, log_extension)  # Set up the log file
        reset(files_to_delete)  # Pass the files_to_delete list to reset
        write_log_header(log_filename, max_threads, half_threads, quarter_threads, eighth_threads, minimal_threads)  # Write the log header
        encode(log_filename, loops_list, threads_list, x264_executable_path)  # Start the encoding process with the executable path
        clean_up(log_filename, files_to_delete)  # Pass the files_to_delete list to clean_up
        input(f"Hit ENTER to open the directory containing {log_filename} and exit.")  # Prompt the user to open the output directory and then exit the script
        subprocess.run(["explorer.exe", os.path.abspath(os.path.join(".."))])
    
    except Exception as e:
        print(f"An unexpected error occurred in main: {e}")  
        import traceback
        traceback.print_exc()  # Print the full traceback to help with debugging


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
#        f"{log_prefix}*.{log_extension}", # Uncomment to delete log files after each run
    ]

    main()

