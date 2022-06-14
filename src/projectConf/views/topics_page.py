from typing import List

from PyQt5.QtCore import Qt, pyqtSlot, pyqtSignal
from PyQt5.QtWidgets import QVBoxLayout, QWidget, QLabel, QPushButton

from ..components import Window
from ..data_mappers import TopicDataMapper
from ..factories import ButtonFactory, LabelFactory
from ..models import Topic
from ..models.enums.text_type import TextType


class TopicPage(Window):
    continue_signal = pyqtSignal(Topic)

    def __init__(self, topic: Topic = None):
        title = 'Página2' if not topic else 'Página3'
        super(TopicPage, self).__init__(title=title)

        topic_id = topic.id if topic else None
        self._topics: List[Topic] = TopicDataMapper.get_topics(topic_parent_id=topic_id)

    def draw(self, *args, **kwargs):
        main_window = QWidget()
        layout = QVBoxLayout()

        title_label = LabelFactory.get_label_component(text='Temario de repaso', label_type=TextType.TITLE)
        topic_buttons = self._get_topic_buttons()
        self._setup_layout(layout=layout, title_label=title_label, topic_buttons=topic_buttons)

        main_window.setLayout(layout)
        self.setCentralWidget(main_window)
        self.show()

    @pyqtSlot()
    def _get_topic_buttons(self) -> List[QPushButton]:
        topic_buttons = []
        for topic in self._topics:
            topic_button = ButtonFactory.get_button_component(
                title=topic.title, function_to_connect=lambda val=topic: self._send_continue_signal(val)
            )
            topic_buttons.append(topic_button)
        return topic_buttons

    def _send_continue_signal(self, topic: Topic):
        self.continue_signal.emit(topic)

    @staticmethod
    def _setup_layout(layout: QVBoxLayout, title_label: QLabel, topic_buttons: List[QPushButton]):
        layout.setContentsMargins(25, 35, 0, 0)
        layout.addWidget(title_label)
        layout.addSpacing(25)
        for topic_button in topic_buttons:
            layout.addWidget(topic_button)
        layout.addStretch()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.close_signal.emit()
