# downloader_logic.py

import yt_dlp
import os
import re
from typing import List, Optional, Dict, Any


def safe_filename(name: str) -> str:
    """Sanitize filename by removing illegal characters."""
    return re.sub(r'[\\/*?:"<>|]', "_", name)


class Downloader:
    def __init__(self, output_path: str = "downloads"):
        self.output_path = output_path
        os.makedirs(self.output_path, exist_ok=True)

    def list_formats(self, url: str):
        """Fetch video info, formats, and subtitles."""
        opts = {"listformats": True}
        with yt_dlp.YoutubeDL(opts) as ydl:
            info = ydl.extract_info(url, download=False) 
        formats = info.get("formats", [])
        subs = info.get("subtitles", {})
        return info, formats, subs

    def auto_select_format(self, category: str, quality: str = "best") -> str:
        """Pick best/worst format automatically."""
        if category == "Audio Only":
            return "bestaudio" if quality == "best" else "worstaudio"
        elif category == "Video Only":
            return "bestvideo" if quality == "best" else "worstvideo"
        else:
            return "best" if quality == "best" else "worst"

    def build_opts(
        self,
        format_id: str,
        outtmpl: str,
        advanced: bool,
        subtitles: Optional[str],
        category: Optional[str],
        extras: Dict[str, Any]
    ) -> dict:
        """Build yt-dlp options dictionary."""
        ydl_opts = {
            "format": format_id,
            "outtmpl": outtmpl,
            "merge_output_format": "mp4",
            "noplaylist": extras.get("noplaylist", True),
        }

        if advanced:
            if extras.get("writethumbnail"):
                ydl_opts["writethumbnail"] = True
            if extras.get("writeinfojson"):
                ydl_opts["writeinfojson"] = True

            if category == "Audio Only" and extras.get("extract_audio", True):
                ydl_opts["postprocessors"] = [{
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "mp3",
                    "preferredquality": "192",
                }]

            if subtitles:
                ydl_opts.update({
                    "writesubtitles": True,
                    "subtitleslangs": [subtitles],
                    "subtitleformat": "srt",
                })

        return ydl_opts

    def download_with_hook(self, url: str, ydl_opts: dict, progress_hook):
        """Download with progress hook (to connect with GUI)."""
        if "progress_hooks" in ydl_opts:
            ydl_opts["progress_hooks"].append(progress_hook)
        else:
            ydl_opts["progress_hooks"] = [progress_hook]

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
