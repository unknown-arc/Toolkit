
import yt_dlp
import os
from PySide6.QtCore import QObject, Signal
  
class fetch_info:

    def fetch_basic_info(self, url: str):
        print("Fetching basic video info...")
        try:
        # """Fetch video info, formats, and subtitles."""
            opts = {"quiet": True,
            "listformats": True,       # still lists formats but faster
            "simulate": True,          # don't download anything
            "noplaylist": True,        # avoid fetching playlist info
            "skip_download": True
            }
             # The core of the process: extract info without downloading
            with yt_dlp.YoutubeDL(opts) as ydl:
                info = ydl.extract_info(url, download=False) 
            video_details = {
                "title": info.get("title"),            
                "thumbnail_url": info.get("thumbnail"),
                "formats": info.get("formats", []),
            } 
            print("✅ Fetched video info successfully.")
            return video_details
        except Exception as e:
            print(f"❌ Error: Could not fetch video info. Reason: {e}")
            return None
    
    def fetch_all_info(url: str):
        ydl_opts = {
            "quiet": True,
        }
        try:
            # The core of the process: extract info without downloading
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                return info
        except yt_dlp.utils.DownloadError as e:
            print(f"❌ Error: Could not process the URL. Reason: {e}")
            return None

class format_categorizer(fetch_info):
    def __init__(self, formats: list):
        self.formats = formats
        self.categories = {
            "Video Only": [],
            "Audio Only": [],
            "Audio + Video": []
        }
        self.categorize_formats()

    def categorize_formats(self):
        """Categorize formats into Video Only, Audio Only, and Audio + Video."""
        for f in self.formats:
            vcodec = f.get('vcodec', 'none')
            acodec = f.get('acodec', 'none')

            if vcodec != "none" and acodec == "none":
                self.categories["Video Only"].append(f)
            elif vcodec == "none" and acodec != "none":
                self.categories["Audio Only"].append(f)
            elif vcodec != "none" and acodec != "none":
                self.categories["Audio + Video"].append(f)

    def get_categories(self):
        return self.categories             

class Download_file_info:
    # return download_file
    pass

class Downloader():     
    def __init__(self, output_path: str = "downloads"):
        self.output_path = output_path
        self.formats = []
        self.subs = {}
        self.categories = {}     
        os.makedirs(self.output_path, exist_ok=True)   

    def basic_download(self, url: str, format_id: str, subtitles: str = None, progress_callback=None):
        """Download video with the selected format and optional subtitles."""
        def hook(d):
            if progress_callback:
                progress_callback(d)
            else:
                if d['status'] == 'downloading':
                    print(f"⬇ {d['_percent_str']} at {d['_speed_str']}")
                elif d['status'] == 'finished':
                    print(f"✅ Download complete: {d['filename']}")

        download_file = {
            "format": format_id,
            "merge_output_format": "mp4",
            "outtmpl": f"{self.output_path}/%(title)s.%(ext)s",
            "progress_hooks": [hook],
        }

        try:
            with yt_dlp.YoutubeDL(download_file) as ydl:
                ydl.download([url])
        except Exception as e:
            print(f"❌ Error during download: {e}")  

    def advanced_download(
        self,
        url: str,
        format_id: str,
        outtmpl: str,
        advanced: bool,
        subtitles: str = None,
        category: str = None,
        extras: dict = {},
        progress_callback=None
    ):
        """Download video with advanced options."""
        def hook(d):
            if progress_callback:
                progress_callback(d)
            else:
                if d['status'] == 'downloading':
                    print(f"⬇ {d['_percent_str']} at {d['_speed_str']}")
                elif d['status'] == 'finished':
                    print(f"✅ Download complete: {d['filename']}")

        ydl_opts = {
            "format": format_id,
            "outtmpl": outtmpl,
            "merge_output_format": "mp4",
            "noplaylist": extras.get("noplaylist", True),
            "progress_hooks": [hook],
        }

        if advanced:
            if extras.get("writethumbnail"):
                ydl_opts["writethumbnail"] = True
            if extras.get("writeinfojson"):
                ydl_opts["writeinfojson"] = True

            if category == "Audio Only" and extras.get("extract_audio", True):
                ydl_opts["postprocessors"] = [{
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": extras.get("audio_format", "mp3"),
                    "preferredquality": extras.get("audio_quality", "192"),
                }]

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
        except Exception as e:
            print(f"❌ Error during download: {e}")     

class DownloadWorker(QObject):
    progress = Signal(int)    # emits percentage
    finished = Signal()       # emits when done

    def __init__(self, downloader: Downloader, url, format_id, filename):
        super().__init__()
        self.downloader = downloader
        self.url = url
        self.format_id = format_id
        self.filename = filename

    def run(self):
        def hook(d):
            if d['status'] == 'downloading':
                total = d.get('total_bytes') or d.get('total_bytes_estimate', 0)
                downloaded = d.get('downloaded_bytes', 0)
                percent = int(downloaded / total * 100) if total else 0
                self.progress.emit(percent)
            elif d['status'] == 'finished':
                self.progress.emit(100)

        try:
            self.downloader.basic_download(self.url, self.format_id, self.filename, hook)
            self.finished.emit()
        except Exception as e:
            print(f"❌ Download error: {e}")
            self.finished.emit()            


  

    