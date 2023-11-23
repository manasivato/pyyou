#-*- coding:utf-8 -*-

import sys
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from all_thread import DownloadThread


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Manasivato YouTube Downloader')

        self.resize(500, 500)
        desktop = QDesktopWidget().availableGeometry()
        window_size = self.frameGeometry()
        center_position = desktop.center() - window_size.center()
        self.move(center_position)

        self.init_elements()
        self.format = False
        self.style = """
            QLabel {
                font-size: 14px;
            }
            QLineEdit {
                font-size: 14px;
                padding: 5px;
                border: 1px solid #ccc;
            }
            QComboBox {
                font-size: 14px;
                padding: 5px;
                border: 1px solid #ccc;
            }
            QPushButton {
                font-size: 16px;
                padding: 10px;
                background-color: black;
                color: white;
                border: none;
            }
            QPushButton:hover {
                background-color: #333232;
            }
            QProgressBar {
                border: 2px solid grey;
                border-radius: 5px;
                background: #FFFFFF;
                height: 40px;
                width: 100%;
                text-align: center; /* Center text in the progress bar */
            }
            QProgressBar::chunk {
                text-align: center; /* Center text in the progress indicator */
                margin: 0px; /* Set margin to 0 to hide the text */
            }
            QMainWindow {
                background-color: #FFFFFF;
            }
        """
        self.setStyleSheet(self.style)
        self.setWindowIcon(QIcon('youtube.png'))

        self.show()

    def init_elements(self):

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)

        self.unavailable = False
        self.video_name = ""

        self.loader_movie = QMovie("loader.gif")
        self.loader_movie_label = QLabel('')
        layout.addWidget(self.loader_movie_label)
        self.loader_movie_label.setMovie(self.loader_movie)
        self.loader_movie_label.setAlignment(Qt.AlignCenter)
        self.loader_movie_label.hide()

        self.success_movie = QMovie("success.gif")
        self.success_movie_label = QLabel('')
        layout.addWidget(self.success_movie_label)
        self.success_movie_label.setMovie(self.success_movie)
        self.success_movie_label.setAlignment(Qt.AlignCenter)
        self.success_movie_label.hide()

        self.label = QLabel("")
        self.label.setMaximumWidth(500)
        self.label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.label)

        self.url_input = QLineEdit()
        self.url_input.setMaximumWidth(500)
        self.url_input.setPlaceholderText("Url youtube")
        layout.addWidget(self.url_input)

        self.label_format = QLabel('Choix de format à télécharger')
        self.label_format.setMaximumWidth(500)
        self.label_format.setMidLineWidth(500)
        layout.addWidget(self.label_format)

        self.format_input = QComboBox(self)
        self.format_input.setMaximumWidth(500)
        self.format_input.setMinimumWidth(500)
        self.format_input.addItem('', "")
        self.format_input.addItem('Format Mp4', "mp4")
        self.format_input.addItem('Format Mp3', 'mp3')
        layout.addWidget(self.format_input)

        self.progress_bar = QProgressBar(self)
        self.progress_bar.setMaximumWidth(500)
        self.progress_bar.hide()
        layout.addWidget(self.progress_bar)

        self.download_button = QPushButton('Commencer le téléchargement', self)
        self.download_button.setMaximumWidth(500)
        self.download_button.clicked.connect(self.start_download)
        layout.addWidget(self.download_button)

        layout.setAlignment(Qt.AlignCenter)

        widget_central = QWidget()
        widget_central.setLayout(layout)

        self.setCentralWidget(widget_central)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Return or event.key() == Qt.Key_Enter:
            if self.url_input.isVisible() and self.format_input.isVisible():
                self.download_button.click()

    def start_download(self):
        self.format = self.format_input.currentData()
        video_url = self.url_input.text()

        if video_url == "":
            self.url_input.setStyleSheet("border: 2px solid red;")
            self.label.setStyleSheet("color: red;")
            self.label.setText('Url youtube est obligatoire.')
            if self.format == "":
                self.format_input.setStyleSheet("border: 2px solid red;")
                self.label.setText('Url youtube et choix de format à télécharger sont obligatoires.')
            else:
                self.format_input.setStyleSheet("border: 1px solid #ccc;")
        elif self.format == "":
            self.url_input.setStyleSheet("border: 1px solid #ccc;")
            self.format_input.setStyleSheet("border: 2px solid red;")
            self.label.setStyleSheet("color: red;")
            self.label.setText('Choix de format à télécharger est obligatoire.')
        else:
            self.format_input.setStyleSheet("border: 1px solid #ccc;")
            self.url_input.setStyleSheet("border: 1px solid #ccc;")
            self.label.setStyleSheet("color: black;")
            self.progress_bar.setValue(0)
            self.success_movie.stop()
            self.success_movie_label.hide()
            self.label.setText("Préparation téléchargement ...")
            self.loader_movie.start()
            self.loader_movie_label.show()
            self.progress_bar.show()
            self.url_input.hide()
            self.label_format.hide()
            self.format_input.hide()
            self.download_button.hide()
            self.download_thread = DownloadThread(self, video_url)
            self.download_thread.update_progress.connect(self.update_progress_bar)
            self.download_thread.finished.connect(self.after_finished)
            self.download_thread.start()

    def update_progress_bar(self, progress):
        if progress >= 100:
            if progress == 800:
                self.url_input.setStyleSheet("border: 2px solid red;")
                self.label.setStyleSheet("color: red;")
                self.label.setText('Url youtube invalide.')
            else:
                self.label.setStyleSheet("color: black;")
                self.label.setText("Conversion en mp3 en cours ...")
        self.progress_bar.setValue(progress)

    def after_finished(self):
        self.progress_bar.hide()
        if self.unavailable:
            self.url_input.setStyleSheet("border: 2px solid red;")
            self.label.setStyleSheet("color: red;")
            self.label.setText('Url youtube invalide.')
        else:
            self.label.setStyleSheet("color: black;")
            self.label.setText("Téléchargement terminé.")

        self.loader_movie.stop()
        self.loader_movie_label.hide()
        self.url_input.setText("")
        self.url_input.show()
        self.label_format.show()
        self.format_input.show()
        self.download_button.show()
        self.download_thread.stop_download()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())