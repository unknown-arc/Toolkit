# downloader.py

import yt_dlp

class Downloader:
    def __init__(self, output_path: str = "downloads"):
        self.output_path = output_path
        self.formats = []
        self.subs = {}
        self.categories = {}

    def list_formats(self, url: str):
        """Fetch available formats and subtitles for a video."""
        with yt_dlp.YoutubeDL({"listformats": True}) as ydl:
            info = ydl.extract_info(url, download=False)
            self.formats = info.get("formats", [])
            self.subs = info.get("subtitles", {})
        self.categorize_formats()
        return self.formats, self.subs

    def categorize_formats(self):
        """Categorize formats into Video Only, Audio Only, and Audio + Video."""
        self.categories = {
            "Video Only": [],
            "Audio Only": [],
            "Audio + Video": []
        }
        for f in self.formats:
            vcodec = f.get('vcodec', 'none')
            acodec = f.get('acodec', 'none')

            if vcodec != "none" and acodec == "none":
                self.categories["Video Only"].append(f)
            elif vcodec == "none" and acodec != "none":
                self.categories["Audio Only"].append(f)
            elif vcodec != "none" and acodec != "none":
                self.categories["Audio + Video"].append(f)

    def show_formats(self, category: str):
        """Display formats for the selected category."""
        category_list = self.categories.get(category, [])
        for f in category_list:
            print(f"{f['format_id']:>6} | {f.get('ext',''):<5} | "
                  f"{f.get('resolution',''):<10} | "
                  f"{f.get('filesize','N/A')}")

    def download(self, url: str, format_id: str, subtitles: str = None, progress_callback=None):
        """Download video with the selected format and optional subtitles."""
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
            "merge_output_format": "mp4",
            "outtmpl": f"{self.output_path}/%(title)s.%(ext)s",
            "progress_hooks": [hook],
        }

        if subtitles:
            ydl_opts.update({
                "writesubtitles": True,
                "subtitleslangs": [subtitles],
                "subtitleformat": "srt",
            })

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

if __name__ == "__main__":
    downloader = Downloader()
    url = input("Enter video URL: ")
    downloader.list_formats(url)

    print("\nChoose category:")
    for i, cat in enumerate(downloader.categories.keys(), 1):
        print(f"{i}. {cat}")
    choice = input("Enter number (1/2/3): ").strip()
    category_map = {"1": "Video Only", "2": "Audio Only", "3": "Audio + Video"}
    selected_category = category_map.get(choice, "Audio + Video")

    print(f"\nShowing {selected_category} formats:\n")
    downloader.show_formats(selected_category)

    format_id = input("\nEnter format ID: ").strip()

    subtitle_choice = None
    if downloader.subs:
        print("\nAvailable subtitles:")
        for lang in downloader.subs.keys():
            print(f"   {lang}")
        subtitle_choice = input("\nEnter subtitle language code (or press Enter to skip): ").strip() or None

    downloader.download(url, format_id, subtitles=subtitle_choice)
