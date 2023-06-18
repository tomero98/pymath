import os
from pathlib import Path

from PyQt5 import QtGui
from PyQt5.QtCore import Qt, pyqtSignal, QUrl
from PyQt5.QtGui import QFont
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QSlider, QPushButton, QStatusBar, QHBoxLayout

from src.function.models import StepInfoData
from src.projectConf.factories import ButtonFactory, IconFactory, LabelFactory
from src.projectConf.models.enums import TextType


class VideoDialog(QWidget):
    close_signal = pyqtSignal()

    def __init__(self, step_info_data: StepInfoData):
        super(VideoDialog, self).__init__()

        self._step_info_data: StepInfoData = step_info_data

        self._video_widget: QWidget = None  # noqa
        self._play_button: QPushButton = None  # noqa
        self._media_player: QMediaPlayer = None  # noqa
        self._position_slider: QSlider = None  # noqa
        self._status_bar: QStatusBar = None  # noqa
        self._media_player: QMediaPlayer = None  # noqa

    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        self.close_signal.emit()

    def draw(self):
        self.setObjectName('application')
        self.setStyleSheet("""
            QWidget#application {
                background-color: #EDEDE9;
            }"""
                           )
        self.setWindowTitle('Información del ejercicio')

        layout = QVBoxLayout()
        self._video_widget = QVideoWidget()

        self._media_player = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        self._media_player.setMedia(QMediaContent(QUrl.fromLocalFile(self._get_video_path())))

        icon = IconFactory.get_icon_widget(image_name='play.png')
        self._play_button = ButtonFactory.get_button_component(
            title='', function_to_connect=lambda: self._play(), icon=icon, icon_size=25,
            tooltip='', primary_button=True
        )

        self._position_slider = QSlider(Qt.Horizontal)
        self._position_slider.setRange(0, 0)
        self._position_slider.sliderMoved.connect(self._setPosition)

        self._status_bar = QStatusBar()
        self._status_bar.setFont(QFont("Noto Sans", 7))
        self._status_bar.setFixedHeight(14)

        control_layout = QHBoxLayout()
        control_layout.setContentsMargins(0, 0, 0, 0)
        control_layout.addWidget(self._play_button)
        control_layout.addWidget(self._position_slider)

        layout.addWidget(self._video_widget)
        layout.addLayout(control_layout)
        layout.addWidget(self._status_bar)
        text_widget = self._get_text_widget()
        layout.addWidget(text_widget, alignment=Qt.AlignHCenter)

        self._media_player.setVideoOutput(self._video_widget)
        self._media_player.stateChanged.connect(self._media_state_changed)
        self._media_player.positionChanged.connect(self._position_changed)
        self._media_player.durationChanged.connect(self._duration_hanged)

        self.setLayout(layout)
        self.show()
        self.setMinimumSize(800, 600)

    def _get_video_path(self):
        path = str(
            Path(os.path.dirname(os.path.abspath(__file__))).parent.parent.parent.joinpath(
                f'media/videos/{self._step_info_data.video_name}'
            )
        )
        return str(Path(os.path.dirname(os.path.abspath(__file__))).parent.parent.joinpath(path))

    def _play(self):
        if self._media_player.state() == QMediaPlayer.PlayingState:
            self._media_player.pause()
        else:
            self._media_player.play()

    def _media_state_changed(self, state):
        if self._media_player.state() == QMediaPlayer.PlayingState:
            icon = IconFactory.get_icon_widget(image_name='play.png')
            self._play_button.setIcon(icon)
        else:
            icon = IconFactory.get_icon_widget(image_name='pause.png')
            self._play_button.setIcon(icon)

    def _position_changed(self, position):
        self._position_slider.setValue(position)

    def _duration_hanged(self, duration):
        self._position_slider.setRange(0, duration)

    def _setPosition(self, position):
        self._media_player.setPosition(position)

    def _get_text_widget(self) -> QWidget:
        widget = QWidget()
        layout = QVBoxLayout()
        for indication in self._step_info_data.info_list:
            text = LabelFactory.get_label_component(text=f'* {indication}', label_type=TextType.NORMAL_TEXT,
                                                    align=Qt.AlignLeft)
            layout.addWidget(text, alignment=Qt.AlignLeft)
        widget.setLayout(layout)
        widget.setObjectName('topic-container')
        widget.setStyleSheet("""
            #topic-container {
                border: 4px solid #897B6D;
                border-radius: 20px;
                background: #F5EBE0;
            }
        """)
        widget.setMinimumSize(700, widget.minimumSizeHint().height() * 1.2)
        return widget
