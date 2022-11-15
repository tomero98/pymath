from typing import List

from PyQt5.QtCore import Qt, pyqtSlot, pyqtSignal
from PyQt5.QtWidgets import QVBoxLayout, QWidget, QLabel, QPushButton, QHBoxLayout

from ..components import Window
from ..data_mappers import TopicDataMapper
from ..factories import ButtonFactory, LabelFactory
from ..factories.icon_factory import IconFactory
from ..models import Topic
from ..models.enums.text_type import TextType


class TopicPage(Window):
    continue_signal = pyqtSignal(Topic)
    back_signal = pyqtSignal()

    def __init__(self):
        self._title = 'Funciones'
        self._description = ''
        super(TopicPage, self).__init__(title=self._title)

        self._topics: List[Topic] = TopicDataMapper.get_topics()

    def draw(self, *args, **kwargs):
        main_window = QWidget()
        layout = QVBoxLayout()

        title_label = LabelFactory.get_label_component(text=self._title, label_type=TextType.TITLE,
                                                       align=Qt.AlignHCenter)
        description_label = LabelFactory.get_label_component(text=self._description,
                                                             label_type=TextType.NORMAL_TEXT, align=Qt.AlignHCenter)
        topic_buttons_layout = self._get_topic_buttons()
        self._setup_layout(layout=layout, title_label=title_label, description_label=description_label,
                           topic_buttons_layout=topic_buttons_layout)

        main_window.setLayout(layout)
        self.setCentralWidget(main_window)
        self.show()

    @pyqtSlot()
    def _get_topic_buttons(self) -> List[QPushButton]:
        topic_buttons_layout = []
        for topic in self._topics:
            layout = self._get_topic_button_layout(topic)
            topic_buttons_layout.append(layout)
        return topic_buttons_layout

    def _get_topic_button_layout(self, topic: Topic) -> QHBoxLayout:
        layout = QHBoxLayout()

        icon = IconFactory.get_icon_widget(image_name='book.png')
        button = ButtonFactory.get_button_component(
            title='', function_to_connect=lambda val=topic: self._send_continue_signal(val), icon=icon, icon_size=35,
            tooltip=f'Lección {topic.title}'
        )

        description_layout = QVBoxLayout()
        title_layout = QHBoxLayout()
        blue_point = LabelFactory.get_label_image_component(image_name='blue_point.png', width=12, height=12)
        title = LabelFactory.get_label_component(text=topic.title, label_type=TextType.SUBTITLE)
        title_layout.addWidget(blue_point, alignment=Qt.AlignLeft)
        title_layout.addWidget(title, alignment=Qt.AlignLeft)
        title_layout.addWidget(button, alignment=Qt.AlignBottom)
        title_layout.addStretch()

        description = LabelFactory.get_label_component(text=topic.description, label_type=TextType.NORMAL_TEXT,
                                                       align=Qt.AlignLeft)
        description_layout.addLayout(title_layout)
        description_layout.addWidget(description, alignment=Qt.AlignLeft)

        layout.addSpacing(180)
        layout.addStretch()
        layout.addLayout(description_layout)
        layout.addWidget(button, alignment=Qt.AlignLeft)
        layout.addStretch()

        return layout

    def _send_continue_signal(self, topic: Topic):
        self.continue_signal.emit(topic)

    @staticmethod
    def _setup_layout(layout: QVBoxLayout, title_label: QLabel, description_label: QLabel,
                      topic_buttons_layout: List[QPushButton]):
        layout.setContentsMargins(5, 0, 0, 0)
        layout.addSpacing(10)
        layout.addSpacing(0)
        layout.addWidget(title_label)
        layout.addWidget(description_label)
        layout.addSpacing(20)
        for topic_button_layout in topic_buttons_layout:
            layout.addLayout(topic_button_layout)
        layout.addStretch()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.close_signal.emit()
