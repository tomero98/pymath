from typing import List

from PyQt5.QtCore import Qt, pyqtSlot, pyqtSignal
from PyQt5.QtGui import QCursor
from PyQt5.QtWidgets import QVBoxLayout, QWidget, QLabel, QPushButton, QHBoxLayout, QFrame, QGraphicsDropShadowEffect

from ..components import Window
from ..components.topic_setting_dialog import TopicSettingDialog
from ..data_mappers import TopicDataMapper
from ..factories import ButtonFactory, LabelFactory
from ..factories.icon_factory import IconFactory
from ..models import Topic
from ..models.enums import ColorType
from ..models.enums.text_type import TextType


class TopicPage(Window):
    continue_signal = pyqtSignal(Topic)
    back_signal = pyqtSignal()

    def __init__(self):
        self._title = 'Ejercicios sobre funciones'
        super(TopicPage, self).__init__(title=self._title)

        self._topics: List[Topic] = TopicDataMapper.get_topics()
        self._setting_buttons: List[QPushButton] = []
        self._topic_setting_dialog: TopicSettingDialog = None  # noqa

    def draw(self, *args, **kwargs):
        main_window = QWidget()
        layout = QVBoxLayout()

        title_label = LabelFactory.get_label_component(text=self._title, label_type=TextType.TITLE,
                                                       align=Qt.AlignHCenter)
        topic_buttons_layout = self._get_topic_buttons()
        self._setup_layout(layout=layout, title_label=title_label, topic_buttons_layout=topic_buttons_layout)

        main_window.setLayout(layout)
        self.setCentralWidget(main_window)
        self.show()

    @pyqtSlot()
    def _get_topic_buttons(self) -> List[QWidget]:
        topic_buttons_layout = []
        for topic in self._topics:
            layout = self._get_topic_button_widget(topic)
            topic_buttons_layout.append(layout)
        return topic_buttons_layout

    def _get_topic_button_widget(self, topic: Topic) -> QWidget:
        widget = QWidget()
        layout = QHBoxLayout()

        icon = IconFactory.get_icon_widget(image_name='book.png')
        book_button = ButtonFactory.get_button_component(
            title='', function_to_connect=lambda val=topic: self._send_continue_signal(topic=val), icon=icon,
            icon_size=30
        )

        icon = IconFactory.get_icon_widget(image_name='setting.png')
        setting_button = ButtonFactory.get_button_component(
            title='', function_to_connect=lambda val=topic: self._show_settings(topic=val), icon=icon,
            icon_size=45, tooltip=f'Configuración del ejercicio', secondary_button=True
        )
        self._setting_buttons.append(setting_button)

        description_layout = QVBoxLayout()
        title = LabelFactory.get_label_component(text=topic.title, label_type=TextType.SUBTITLE)
        description = LabelFactory.get_label_component(text=topic.description, label_type=TextType.NORMAL_TEXT,
                                                       align=Qt.AlignLeft)
        description_layout.addWidget(title)
        description_layout.addWidget(description, alignment=Qt.AlignLeft)

        layout.addSpacing(10)
        layout.addWidget(book_button, alignment=Qt.AlignLeft)
        layout.addSpacing(15)
        layout.addLayout(description_layout)
        layout.addStretch()
        layout.addWidget(setting_button)
        layout.addSpacing(10)
        widget.setLayout(layout)
        widget.setObjectName('topic-container')
        widget.setToolTip(f'Lección {topic.title}')
        widget.setCursor(QCursor(Qt.PointingHandCursor))
        widget.setStyleSheet("""
            #topic-container {
                border: 2px solid #957FEF;
                border-radius: 20px;
                background: #DEC0F1;
            }
            
            #topic-container::hover {
                border: 5px solid #957FEF;
            }
        """)
        effect = QGraphicsDropShadowEffect()
        effect.setOffset(0, 0)
        effect.setBlurRadius(15)
        widget.setGraphicsEffect(effect)
        widget.setFixedSize(550, 100)
        widget.mouseReleaseEvent = lambda event: self._send_continue_signal(topic=topic)
        return widget

    def _send_continue_signal(self, topic: Topic):
        self.continue_signal.emit(topic)

    def _show_settings(self, topic: Topic):
        if not self._topic_setting_dialog:
            self._topic_setting_dialog = TopicSettingDialog(topic=topic)
            self._topic_setting_dialog.close_signal.connect(self._set_topic_setting_dialog_close)
            self._topic_setting_dialog.draw()

            for button in self._setting_buttons:
                button.setDisabled(True)

    def _set_topic_setting_dialog_close(self):
        if self._topic_setting_dialog:
            self._topic_setting_dialog.close()
            self._topic_setting_dialog = None

        for button in self._setting_buttons:
            button.setDisabled(False)

    @staticmethod
    def _setup_layout(layout: QVBoxLayout, title_label: QLabel, topic_buttons_layout: List[QPushButton]):
        layout.addSpacing(20)
        layout.addWidget(title_label)
        layout.addSpacing(20)
        for topic_button_layout in topic_buttons_layout:
            layout.addWidget(topic_button_layout, alignment=Qt.AlignHCenter)
            layout.addSpacing(35)
        layout.addStretch()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.close_signal.emit()
