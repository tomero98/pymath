from typing import List

from PyQt5.QtCore import Qt, pyqtSlot, pyqtSignal
from PyQt5.QtGui import QCursor
from PyQt5.QtWidgets import QVBoxLayout, QWidget, QLabel, QPushButton, QHBoxLayout, QGraphicsDropShadowEffect

from ..components import Window
from ..components.topic_setting_dialog import TopicSettingDialog
from ..components.user_stats_dialog import UserStatsDialog
from ..data_mappers import TopicDataMapper
from ..factories import ButtonFactory, LabelFactory
from ..factories.icon_factory import IconFactory
from ..models import Topic
from ..models.enums.text_type import TextType


class TopicPage(Window):
    continue_signal = pyqtSignal(Topic)
    back_signal = pyqtSignal()

    def __init__(self):
        self._title = 'Conceptos relativos a funciones y sus características'
        super(TopicPage, self).__init__(title=self._title)

        self._topics: List[Topic] = TopicDataMapper.get_topics()
        self._setting_buttons: List[QPushButton] = []
        self._user_button: QPushButton = None  # noqa
        self._topic_setting_dialog: TopicSettingDialog = None  # noqa
        self._topic_buttons: List[QWidget] = []
        self._user_stats_dialog: UserStatsDialog = None  # noqa

    def draw(self, *args, **kwargs):
        main_window = QWidget()
        layout = QVBoxLayout()

        icon = IconFactory.get_icon_widget(image_name='usuario.png')
        self._user_button = ButtonFactory.get_button_component(
            title='', function_to_connect=self._setup_user_stats, icon=icon, icon_size=30, primary_button=True,
            tooltip='Estadísticas de usuario'
        )

        title_label = LabelFactory.get_label_component(text=self._title, label_type=TextType.TITLE,
                                                       align=Qt.AlignHCenter, set_bold=True)
        self._topic_buttons = self._get_topic_buttons()
        self._setup_layout(layout=layout, title_label=title_label)

        main_window.setLayout(layout)
        self.setCentralWidget(main_window)
        self.show()

    def _setup_user_stats(self):
        if not self._user_stats_dialog:
            self._user_stats_dialog = UserStatsDialog()
            self._user_stats_dialog.close_signal.connect(self._close_user_stats_dialog)
            self._user_stats_dialog.draw()

            for button in self._setting_buttons:
                button.setDisabled(True)

            for button in self._topic_buttons:
                button.setDisabled(True)

            self._user_button.setDisabled(True)

    def _close_user_stats_dialog(self):
        if self._user_stats_dialog:
            self._user_stats_dialog.close()
            self._user_stats_dialog = None

        for button in self._setting_buttons:
            button.setDisabled(False)

        for button in self._topic_buttons:
            button.setDisabled(False)

        self._user_button.setDisabled(False)

    @pyqtSlot()
    def _get_topic_buttons(self) -> List[QWidget]:
        topic_buttons = []
        for topic in self._topics:
            layout = self._get_topic_button_widget(topic)
            topic_buttons.append(layout)
        return topic_buttons

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
        title = LabelFactory.get_label_component(text=topic.title, label_type=TextType.SUBTITLE, set_bold=True)
        description_layout.addWidget(title, alignment=Qt.AlignVCenter)

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
                border: 4px solid #897B6D;
                border-radius: 20px;
                background: #F5EBE0;
            }
            
            #topic-container::hover {
                border: 5px solid #897B6D;
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
        if not self._topic_setting_dialog:
            self.continue_signal.emit(topic)

    def _show_settings(self, topic: Topic):
        if not self._topic_setting_dialog:
            self._topic_setting_dialog = TopicSettingDialog(topic=topic)
            self._topic_setting_dialog.close_signal.connect(self._set_topic_setting_dialog_close)
            self._topic_setting_dialog.draw()

            for button in self._setting_buttons:
                button.setDisabled(True)

            for button in self._topic_buttons:
                button.setDisabled(True)

            self._user_button.setDisabled(True)

    def _set_topic_setting_dialog_close(self):
        if self._topic_setting_dialog:
            self._topic_setting_dialog.close()
            self._topic_setting_dialog = None

        for button in self._setting_buttons:
            button.setDisabled(False)

        for button in self._topic_buttons:
            button.setDisabled(False)

        self._user_button.setDisabled(False)

    def _setup_layout(self, layout: QVBoxLayout, title_label: QLabel):
        layout.setContentsMargins(10, 10, 50, 0)
        layout.addWidget(self._user_button, alignment=Qt.AlignLeft)
        layout.addWidget(title_label, alignment=Qt.AlignHCenter)
        layout.addSpacing(30)
        for topic_button_layout in self._topic_buttons:
            layout.addWidget(topic_button_layout, alignment=Qt.AlignHCenter)
            layout.addSpacing(45)
        layout.addStretch()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.close_signal.emit()
