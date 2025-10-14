Universal File Converter Pro
https://img.shields.io/badge/Python-3.8%252B-blue
https://img.shields.io/badge/License-MIT-green
https://img.shields.io/badge/Platform-Windows%2520%257C%2520macOS%2520%257C%2520Linux-lightgrey

A powerful, user-friendly file conversion application built with Python that supports images, PDFs, documents, presentations, and audio files with an intuitive GUI interface.

✨ Features
🔄 Supported Conversions
Category	Input Formats	Output Formats
Images	JPG, JPEG, PNG, BMP, GIF, WEBP, TIFF	PNG, JPEG, BMP, GIF, WEBP, PDF, PPTX
PDF	PDF	PNG, JPG, TXT
Documents	DOCX, DOC, TXT	PDF, TXT
Presentations	PPTX, PPT	PDF, PNG
Audio	MP3, WAV, OGG, FLAC, M4A	MP3, WAV, OGG
🚀 Special Features
🖼️ Image to PowerPoint: Convert single or multiple images to professional presentations

📁 Batch Processing: Convert entire folders with one click

🎨 Multiple Layout Options: Various layouts for image to PPT conversion

⚡ Quality Control: Adjustable quality settings for image conversion

📊 Progress Tracking: Real-time conversion progress with detailed logs

🔍 File Information: Detailed file properties and metadata display

🔄 Cross-Platform: Works on Windows, macOS, and Linux

🏁 Quick Start
Prerequisites
Python 3.8 or higher

100MB free disk space

Windows, macOS, or Linux operating system

Installation
Download the Project

bash
# Clone the repository or download the ZIP file
git clone https://github.com/your-username/file-converter-app.git
cd file-converter-app
Install Python Dependencies

bash
pip install -r requirements.txt
Setup FFmpeg (Required for Audio Conversion)

Windows Users:

Download ffmpeg-master-latest-win64-gpl-shared.zip from FFmpeg Official Releases

Extract the contents to file-converter-app/ffmpeg/ folder

Final structure should look like:

text
file-converter-app/
├── ffmpeg/
│   ├── bin/
│   │   ├── ffmpeg.exe
│   │   ├── ffplay.exe
│   │   └── ffprobe.exe
│   ├── doc/
│   └── presets/
├── converter.py
└── requirements.txt
macOS Users:

bash
brew install ffmpeg
Linux Users:

bash
sudo apt update && sudo apt install ffmpeg
Launch the Application

bash
python converter.py
🎮 How to Use
Basic File Conversion
Start the Application

bash
python converter.py
Select Your File

Click "Browse File" for individual files

Click "Browse Folder" for batch processing

Choose Output Format

Select from available conversion options in the dropdown menu

Adjust Settings (Optional)

Quality Slider: 1-100 (for image formats)

PPT Layout: Choose layout style for presentations

Convert

Click "Convert Single File" for individual conversion

Click "Batch Convert" for folder processing

🖼️ Image to PowerPoint Guide
Single Image to Presentation
Select any image file (.jpg, .png, .bmp, etc.)

Choose "PPTX" as output format

Select "Single Image" layout

Click convert - creates a beautiful 1-slide presentation

Multiple Images to Presentation
Select a folder containing images

Choose "PPTX" as output format

Select your preferred layout:

"One per Slide": Each image gets its own dedicated slide

"Grid Layout (2x2)": 4 images arranged in a grid per slide

"Grid Layout (3x3)": 9 images arranged in a grid per slide

Convert - creates a professional multi-slide presentation

📊 Supported PPT Layouts
Layout	Description	Best For
Single Image	One centered image per slide	Professional presentations, portfolios
One per Slide	Each image on separate slide	Photo galleries, image showcases
Grid (2x2)	4 images arranged in 2x2 grid	Comparison slides, product catalogs
Grid (3x3)	9 images arranged in 3x3 grid	Thumbnail overviews, contact sheets
🛠️ Technical Details
Dependencies
The application uses these Python packages:

txt
Pillow==10.0.0          # Advanced image processing
python-docx==1.1.0      # Microsoft Word document handling
PyPDF2==3.0.1           # PDF manipulation and extraction
python-pptx==0.6.21     # PowerPoint presentation creation
pydub==0.25.1           # Audio file processing
reportlab==4.0.4        # PDF document generation
PyMuPDF==1.23.8         # High-performance PDF handling
comtypes==1.1.14        # Windows COM interface
Project Structure
text
file-converter-app/
├── 📄 converter.py          # Main application file
├── 📄 requirements.txt      # Python dependencies
├── 📁 ffmpeg/              # FFmpeg binaries (Windows)
│   └── 📁 bin/
│       ├── ⚙️ ffmpeg.exe
│       ├── ⚙️ ffplay.exe
│       └── ⚙️ ffprobe.exe
├── 📄 README.md            # This documentation
└── 📄 LICENSE              # MIT License file
🐛 Troubleshooting
Common Issues & Solutions
"FFmpeg not found" Warning

text
Couldn't find ffmpeg or avconv - defaulting to ffmpeg, but may not work
Fix: Ensure FFmpeg is properly installed in the ffmpeg/bin/ folder

Missing Dependencies Error

text
ModuleNotFoundError: No module named 'module_name'
Fix: Run pip install -r requirements.txt

Audio Conversion Not Working
Fix: Verify FFmpeg installation and PATH configuration

PPT Conversion Limitations

Current version creates visual representations of slides

For full content extraction, Microsoft PowerPoint is recommended

Permission Errors
Fix: Run as administrator or check file/folder permissions

Dependency Status Icons
The application displays real-time status of features:

✅ Green: Feature available and ready

❌ Red: Feature disabled (missing dependency)

Status shown in application header

🔧 Advanced Usage
Command Line Interface
While primarily GUI-based, you can extend functionality:

python
# Example: Extend for custom conversions
def convert_custom_format(self, input_path, output_path, format):
    # Add your custom conversion logic here
    pass
Adding New Converters
Create converter method in UniversalConverter class

Update supported formats in setup_file_types()

Add conversion routing in convert_file() method

📈 Performance Tips
Batch Processing: Use folder conversion for multiple files

Quality Settings: Lower quality for faster conversion (images)

File Organization: Keep source files in separate folders

Storage Space: Ensure adequate space for output files

🤝 Contributing
We welcome contributions! Here's how you can help:

Report Bugs: Open an issue with detailed description

Suggest Features: Share your ideas for improvements

Code Contributions: Submit pull requests for new features

Documentation: Help improve this README and documentation

Development Setup
bash
# Fork and clone the repository
git clone https://github.com/your-username/file-converter-app.git
cd file-converter-app

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install development dependencies
pip install -r requirements.txt
📄 License
This project is licensed under the MIT License - see the LICENSE file for details.

🙏 Acknowledgments
FFmpeg Team for the powerful multimedia framework

Python Community for the extensive library ecosystem

Contributors who help improve this application

📞 Support & Contact
Having issues? Here's how to get help:

Check Troubleshooting section above

Verify Dependencies are properly installed

Check Application Logs for detailed error messages

Open an Issue on GitHub with:

Error messages

Steps to reproduce

Your operating system and Python version

🎊 Get Started Now!
Ready to convert your files?

bash
# Launch the application and start converting!
python converter.py
Happy Converting! 🎉
