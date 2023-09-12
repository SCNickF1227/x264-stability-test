# x264-64 CPU Stability Test Script v3.00 BETA 3

## Overview

This script leverages the x264-64 tool to perform a CPU stability test, simulating different workloads by varying the number of threads involved in the processing. It has been designed to work in a Windows environment using Python 3.11.

This is the spiritual successor to the Overclock.net community batch script [Which Originally appeared in the Haswell Overclocking guide nearly a decade ago!](https://www.overclock.net/threads/haswell-overclocking-guide-with-statistics.1411077/page-737#post-22689780)

Join the conversation of my personal overclocking journey with a 7900X3D
https://forum.level1techs.com/t/one-man-s-adventure-in-ryzen-7900x3d-overclocking/201144
## 🚀 Features

### **Preset Thread Allocation for Stress Testing**

The script performs stress tests using pre-defined thread allocations to emulate different workload conditions. Here are the different scenarios tested:

#### 1. Maximum Threads
- **Loops**: :large_blue_diamond: Configurable, Default 1
- **Threads Used**: `max_threads`, as specified by the user
- **Description**: 
  Utilizes the full number of threads specified by the user, aiming to test the CPU's capacity under heavy multithreaded workloads.

#### 2. Half Threads
- **Loops**: :large_blue_diamond: Configurable, Default 1
- **Threads Used**: `max_threads // 2`
- **Description**:
  Employs half of the specified maximum threads (rounded down) to simulate moderately multithreaded workloads.

#### 3. Quarter Threads
- **Loops**: :large_blue_diamond: Configurable, Default 1
- **Threads Used**: `max_threads // 4`
- **Description**:
  Engages a quarter of the maximum threads (rounded down) for testing under lighter multithreaded conditions.

#### 4. Minimal Threads
- **Loops**: :large_blue_diamond: Configurable, Default 1
- **Threads Used**: 2
- **Description**:
  A minimal setup using 2 threads is engaged to scrutinize the stability under minimal multithreaded conditions.

#### 5. Maximum Threads
- **Loops**: :large_orange_diamond: Not Configurable, Same number of loops as other Maxium Threads.
- **Threads Used**: `max_threads`, as specified by the user
- **Description**: 
  Generate some heat before ending the stability test.

### Script Workflow

Each scenario presents a different level of stress on the CPU, aiming to ensure stability under various potential workloads.

### **Detailed Logging**

Each test iteration logs detailed reports into a specified log file, capturing both standard output and errors during execution to facilitate a comprehensive review post testing.

:red_circle: Now includes better sampling and statistics. 

### **Automatic File Cleanup**

Upon completion of the test, the script automatically removes all temporary files created during the test process, maintaining a clean working environment.

:red_circle: Fixed some bugs relating to improper cleanup

### **Interactive Input**

Users are guided through the setup process with intuitive prompts to specify critical inputs such as maximum thread count and log file naming, ensuring a user-friendly experience.<br>
:large_blue_diamond: Now More Detailed and still easier to use.

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

## :older_man: It may be wise to use a number larger than the maximum thread count for your CPU. 

- :speech_balloon: You may benefit from an increase of 3-4x in maxium thread allocation vs the number of threads available on your system. This is an intentional design decision to allow better scaling, and to allow better variation of load on high-core-count CPUs.  



## Configuration File

To tailor the stability test to specific needs and preferences, a configuration file in JSON format has been introduced in this version. This file allows users to configure various settings including loop and thread counts, enhancing the flexibility and customization of the stress tests.

Here's how it works:

### **Creating and Modifying the Configuration File**
- **Location**: Ensure that the configuration file is located in the root directory of the script.
- **Format**: The configuration file must adhere to a valid JSON format. 
- **Parameters**: Define key parameters such as `max_threads`, `loops`, among others to suit your testing requisites.
- **Error Handling**: The script is designed to gracefully handle errors by notifying the user and automatically deleting incorrectly formatted configuration files, maintaining a seamless user experience.

### **Sample Configuration**
```
{    "max_threads": 72,
    "half_threads": 36,
    "quarter_threads": 18,
    "eighth_threads": 9,
    "loops_list": [
        1,
        1,
        1,
        1,
        1
    ],
    "minimal_threads": 2
}
```
## 🤝 Contribution

Contributions are welcome! Feel free to provide feedback, suggest improvements, or propose new features to enhance the script’s functionality.

## 📄 License

The script is open for use, distribution, and modification under the terms of the GPL v3 license. Check the LICENSE file in the project repository for more details.
