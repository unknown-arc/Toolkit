🚀 Application Setup Guide
This guide provides detailed, step-by-step instructions to install and configure the Universal File Converter Pro application on your system.

📋 Prerequisites
Before you begin, please ensure your system meets the following requirements:

Operating System: Windows, macOS, or Linux.

Python: Version 3.8 or higher.

Disk Space: At least 100MB of free space for the application and its dependencies.

Git: Required for cloning the repository (optional, you can also download a ZIP).

⚙️ Step-by-Step Installation
Follow these steps carefully to set up the application.

Step 1: Get the Project Files
You can either clone the repository using Git (recommended) or download the source code as a ZIP file.

Option A: Clone with Git
Open your terminal or command prompt and run the following command:

git clone [https://github.com/your-username/file-converter-app.git](https://github.com/your-username/file-converter-app.git)
cd file-converter-app

Option B: Download ZIP

Go to the repository's GitHub page.

Click the green < > Code button and select Download ZIP.

Extract the downloaded file to your desired location and navigate into the file-converter-app directory using your terminal.

Step 2: Install Python Dependencies
The application relies on several Python libraries. Install them all at once by running this command from the project's root directory:

pip install -r requirements.txt

This command reads the requirements.txt file and automatically installs all the necessary packages.

Step 3: Configure FFmpeg (Crucial for Audio Conversion)
FFmpeg is a required third-party tool for handling audio conversions. The setup process varies depending on your operating system.

🖥️ For Windows Users
Download FFmpeg: Go to the FFmpeg for Windows builds page and download the ffmpeg-master-latest-win64-gpl-shared.zip file.

Extract Files: Unzip the downloaded file.

Place in Project: Copy the extracted contents into the ffmpeg/ folder inside the main file-converter-app/ directory.

Your final folder structure must look like this for the application to find it:

file-converter-app/
└── 📁 ffmpeg/
    ├── 📁 bin/
    │   ├── ⚙️ ffmpeg.exe
    │   ├── ⚙️ ffplay.exe
    │   └── ⚙️ ffprobe.exe
    ├── 📁 doc/
    └── 📁 presets/

🍏 For macOS Users
If you have Homebrew installed, simply run this command in your terminal:

brew install ffmpeg

The application will automatically detect the system-wide installation.

🐧 For Linux Users (Debian/Ubuntu)
Use your system's package manager to install FFmpeg:

sudo apt update && sudo apt install ffmpeg

▶️ Launching the Application
Once you have completed the installation steps, you can start the application by running the main Python script from the project's root directory:

python converter.py

✅ Verifying the Setup
After launching, check the application's header for dependency status icons:

✅ Green Icon: The feature is correctly configured and ready to use.

❌ Red Icon: The feature is disabled because a dependency (like FFmpeg) is missing or not found. If you see a red icon for audio conversion, please revisit Step 3.

🐛 Troubleshooting
If you encounter any issues, please refer to the Troubleshooting section in the main README.md file for common problems and their solutions.
