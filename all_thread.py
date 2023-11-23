#-*- coding:utf-8 -*-

import os
import yt_dlp
from PyQt5.QtCore import *

downloads_folder = os.path.expanduser("~")
downloads_folder = os.path.join(downloads_folder, "Downloads")


class DownloadThread(QThread):
    update_progress = pyqtSignal(int)

    def __init__(self, parent, video_url):
        super().__init__()
        self.parent = parent
        self.video_url = video_url
        self.output_path = downloads_folder
        self.stop_requested = False

    def run(self):
        try:
            if self.parent.format == 'mp4':
                options = {
                    'format': 'bestvideo+bestaudio/best',
                    'outtmpl': self.output_path + '/%(title)s.%(ext)s',
                    'progress_hooks': [self._update_progress],
                }
            else:
                options = {
                    'format': 'bestaudio/best',
                    'postprocessors': [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'mp3',
                        'preferredquality': '192',
                    }],
                    'outtmpl': self.output_path + '/%(title)s.%(ext)s',
                    'progress_hooks': [self._update_progress],
                }

            with yt_dlp.YoutubeDL(options) as ydl:
                video_title = ""
                self.parent.video_name = video_title
                ydl.download([self.video_url])
            self.parent.unavailable = False
        except:
            self.parent.unavailable = True

    def _update_progress(self, d):
        try:
            if self.stop_requested:
                return
            if d['status'] == 'finished':
                self.stop_download()
            if d['status'] == 'downloading':
                percent_str = str(d['_percent_str']).replace(" ", "").replace("%", "")
                if float(percent_str) > 0:
                    self.parent.label.setText("Téléchargement {0} en cours ...".format(self.parent.video_name))
                self.update_progress.emit(float(percent_str))
        except:
            self.parent.unavailable = True

    def stop_download(self):
        self.stop_requested = True