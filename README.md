# x264-64 CPU Stability Test Script v3.00 BETA 

## Overview

This script leverages the x264-64 tool to perform a CPU stability test, simulating different workloads by varying the number of threads involved in the processing. It has been designed to work in a Windows environment using Python 3.11.

## 🚀 Features

### **Preset Thread Allocation for Stress Testing**

The script performs stress tests using pre-defined thread allocations to emulate different workload conditions. Here are the different scenarios tested:

- **Maximum Threads**: Utilizes the full number of threads specified by the user, aiming to test the CPU's capacity under heavy multithreaded workloads.
- **Half Threads**: Employs half of the specified maximum threads (rounded down) to simulate moderately multithreaded workloads.
- **Quarter Threads**: Engages a quarter of the maximum threads (rounded down) for testing under lighter multithreaded conditions.
- **Minimal Threads**: In the final stage, a minimal setup using 2 threads is engaged to scrutinize the stability under minimal multithreaded conditions.

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

- Python 3.x
- Windows OS
- x264-64 tool ensure it's named `x264-64.exe` and in the `test` directory
- Test video file (`test-1080p.mp4`) available in the `test` directory

## 📥 Installation

1. Ensure Python 3.x is installed on your system. Download it from the [Python official website](https://www.python.org/).
2. Download the latest x264-64 tool and ensure it's named `x264-64.exe` and in the `test` directory, adjacent to the script. [VideoLAN x264 Binaries] (https://artifacts.videolan.org/x264/)
3. Place a ~2 minute video file named `test-1080p.mp4` in the `test` directory, adjacent to the script.
4. Clone or download the script to your local system.

Ensure your diretory structure looks like this!

📂 x264_stability_test/

├── 📝 README.md - Your guide to using and contributing to the project.

├── 🐍 x264_stability_test.py - The main script to perform CPU stress tests.

└── 📁 test/

  ├── 🎬 test-1080p.mp4 - Video file used during the testing process.

  └── 🖥️ x264-64.exe - Executable necessary to conduct the stability tests.

## 🚀 Usage

To execute the script, run the following command in your command prompt or terminal:

```
python3 x264_stability_test.py

```

## 🤝 Contribution

Contributions are welcome! Feel free to provide feedback, suggest improvements, or propose new features to enhance the script’s functionality.

## 📄 License

The script is open for use, distribution, and modification under the terms of the GPL v3 license. Check the LICENSE file in the project repository for more details.
