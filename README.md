# x264-64 CPU Stability Test Script v3.00 BETA 2

## Overview

This script leverages the x264-64 tool to perform a CPU stability test, simulating different workloads by varying the number of threads involved in the processing. It has been designed to work in a Windows environment using Python 3.11.

This is the spiritual successor to the Overclock.net community batch script [Which Originally appeared in the Haswell Overclocking guide nearly a decade ago!](https://www.overclock.net/threads/haswell-overclocking-guide-with-statistics.1411077/page-737#post-22689780)

Join the conversation of my personal overclocking journey with a 7900X3D
https://forum.level1techs.com/t/one-man-s-adventure-in-ryzen-7900x3d-overclocking/201144
## 🚀 Features

### **Preset Thread Allocation for Stress Testing**

The script performs stress tests using pre-defined thread allocations to emulate different workload conditions. Here are the different scenarios tested:

#### 1. Maximum Threads
- **Loops**: 10 
- **Threads Used**: `max_threads`, as specified by the user
- **Description**: 
  Utilizes the full number of threads specified by the user, aiming to test the CPU's capacity under heavy multithreaded workloads.

#### 2. Half Threads
- **Loops**: 10
- **Threads Used**: `max_threads // 2`
- **Description**:
  Employs half of the specified maximum threads (rounded down) to simulate moderately multithreaded workloads.

#### 3. Quarter Threads
- **Loops**: 10
- **Threads Used**: `max_threads // 4`
- **Description**:
  Engages a quarter of the maximum threads (rounded down) for testing under lighter multithreaded conditions.

#### 4. Minimal Threads
- **Loops**: 20
- **Threads Used**: 2
- **Description**:
  In the final stage, a minimal setup using 2 threads is engaged to scrutinize the stability under minimal multithreaded conditions.
  
### Script Workflow

Each scenario presents a different level of stress on the CPU, aiming to ensure stability under various potential workloads.

### **Detailed Logging**

Each test iteration logs detailed reports into a specified log file, capturing both standard output and errors during execution to facilitate a comprehensive review post testing.

### **Automatic File Cleanup**

Upon completion of the test, the script automatically removes all temporary files created during the test process, maintaining a clean working environment.

### **Interactive Input**

Users are guided through the setup process with intuitive prompts to specify critical inputs such as maximum thread count and log file naming, ensuring a user-friendly experience.

### **Version Display**

At initiation, the script displays the x264-64 tool version, providing users with a quick reference to the tool’s version in use.

## 🛠 Requirements

- Python 3.x. You can use [My setup Script](https://github.com/SCNickF1227/x264-stability-test/blob/v3.0-BETA-3/test/setup.python.md)
- Windows 10,11
- x264-64 tool ensure it's named `x264-64.exe` and in the `test` directory. It is provide here in the release.
- Test video file (`test-1080p.mp4`) available in the `test` directory. You can use [my download script](https://github.com/SCNickF1227/x264-stability-test/blob/v3.0-BETA-3/test/dl_bbb.py) to get Big Buck Bunny, Royalty Free

## 📥 Installation

1. Ensure Python 3.x is installed on your system. Download it from the [Python official website](https://www.python.org/).
2. Download the latest x264-64 tool and ensure it's named `x264-64.exe` and placed in the `test` directory, adjacent to the script. [VideoLAN x264 Binaries](https://artifacts.videolan.org/x264/)
3. Place a ~2 minute video file named `test-1080p.mp4` in the `test` directory, adjacent to the script.
4. Clone or download the script to your local system.

Ensure your directory structure looks like this:

📂 **x264_stability_test/**<br>
|-- 📝 **README.md** - Your guide to using and contributing to the project.<br>
|-- 🐍 **x264_stability_test.py** - The main script to perform CPU stress tests.<br>
|-- 📁 **test/**<br>
&nbsp;&nbsp;&nbsp;&nbsp;|---- 🎬 **test-1080p.mp4** - Video file used during the testing process.<br>
&nbsp;&nbsp;&nbsp;&nbsp;|---- 🖥️ **x264-64.exe** - Executable necessary to conduct the stability tests.<br>
&nbsp;&nbsp;&nbsp;&nbsp;|---- 📝 **config.json** - Stores configuration between runs.
## 🚀 Usage

To execute the script, run the following command in your command prompt or terminal:

```
python3 x264_stability_test.py

```

## 🤝 Contribution

Contributions are welcome! Feel free to provide feedback, suggest improvements, or propose new features to enhance the script’s functionality.

## 📄 License

The script is open for use, distribution, and modification under the terms of the GPL v3 license. Check the LICENSE file in the project repository for more details.
