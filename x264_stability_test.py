import os
import subprocess
from datetime import datetime

def display_info():
    try:
        print("="*63)
        print("                  x264-64 Stability test v3.00 BETA")
        print("="*63)
        print()
        subprocess.run(["x264-64", "--version"])
        print()
    except Exception as e:
        print(f"Failed to display info: {e}")

def get_max_threads():
    while True:
        try:
            max_threads = int(input("Enter the maximum number of threads: "))
            if max_threads <= 0:
                raise ValueError("Invalid number. Please enter a valid number.")
            break
        except ValueError as e:
            print(e)
    return max_threads

def get_log_name(log_prefix, log_extension):
    while True:
        timestamp = datetime.now().strftime("%Y%m%d_%H_%M")
        user_input = input("Log name = ").strip()
        log_name = f"{log_prefix}{user_input or 'twister'}_{timestamp}.{log_extension}"
        
        if not os.path.exists(log_name):
            return log_name
        print("File already exists. Please choose a different name.")

            
def write_log_header(log_filename, max_threads, half_threads, quarter_threads):
    try:
        with open(log_filename, 'a') as log_file:
            log_file.write(f"{log_header2}\n{log_header1}\n{log_header2}\n\n")
            subprocess.run(["x264-64", "--version"], stdout=log_file, text=True)
            log_file.write('\n')
            
            log_file.write("==== Configuration =============================================\n\n")
            log_file.write(f"Log name = {log_filename}\n")
            log_file.write(f"Maximum Threads = {max_threads}\n")
            log_file.write(f"Half Threads = {half_threads}\n")
            log_file.write(f"Quarter Threads = {quarter_threads}\n\n")
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
                        "x264-64",
                        "--quiet",  
                        "--preset", "slower",
                        "--crf", "16",
                        "--threads", str(current_thread),
                        "--rc-lookahead", "40",
                        "--aq-strength", "1.5",
                        "--merange", "24",
                        "--subme", "10",
                        "--psy-rd", "1.5:0",
                        "--video-filter", "crop:0,20,0,22/resize:width=1920,height=1040,method=lanczos4",
                        "--thread-input",
                        "--output", "encode.mkv",
                        "test-1080p.mp4",
                        "--aud"
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

def main():
    try:
        os.chdir("test")
        display_info()

        max_threads = get_max_threads()
        half_threads = max_threads // 2
        quarter_threads = max_threads // 4
        print(f"Maximum Threads = {max_threads}")
        print(f"Half Threads = {half_threads}")
        print(f"Quarter Threads = {quarter_threads}")

        log_name = get_log_name(log_prefix, log_extension)
        log_filename = f"{log_prefix}{log_name}"

        print(f"Log name = {log_filename}")

        reset()
        write_log_header(log_filename, max_threads, half_threads, quarter_threads)
        encode(log_filename, [10] * 6 + [20], [max_threads, half_threads, quarter_threads] * 2 + [2])
        clean_up(log_filename)

        input(f"Hit ENTER to open the directory containing {log_filename} and exit.")
        subprocess.run(["explorer.exe", os.path.abspath(os.path.join(".."))])
    except Exception as e:
        print(f"An unexpected error occurred in main: {e}")

if __name__ == "__main__":
    # Constants
    log_header1 = "                     x264-64 Stability test"
    log_header2 = "="*63
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
