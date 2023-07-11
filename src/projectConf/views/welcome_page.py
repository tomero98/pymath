from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QVBoxLayout, QLabel, QPushButton, QWidget

from ..components import Window
from ..factories import LabelFactory, ButtonFactory
from ..factories.icon_factory import IconFactory
from ..models.enums.text_type import TextType


class WelcomePage(Window):
    def __init__(self):
        title = 'Inicio'
        super(WelcomePage, self).__init__(title=title)

    def draw(self, *args, **kwargs):
        main_window = QWidget()
        layout = QVBoxLayout()

        title_widget = self._get_title_widget()
        subtitle_widget = self._get_subtitle_widget()
        logo_widget = self._get_logo_widget()
        enter_button = self._get_enter_button()
        footer_layout = self._get_footer_layout()
        self._set_layout(layout=layout, title_widget=title_widget, subtitle_widget=subtitle_widget,
                         logo_widget=logo_widget, enter_button=enter_button, footer_layout=footer_layout)

        main_window.setLayout(layout)
        self.setCentralWidget(main_window)
        self.show()

    @staticmethod
    def _get_title_widget():
        title = LabelFactory.get_label_component(
            text='Desarrollo de recursos de apoyo para el aprendizaje de conceptos básicos relativos a funciones',
            label_type=TextType.TITLE, fixed_width=900, need_word_wrap=True, align=Qt.AlignHCenter
        )
        return title

    @staticmethod
    def _get_subtitle_widget():
        subtitle = LabelFactory.get_label_component(
            text='Aplicación de refuerzo para la asignatura de Fundamento de Matemáticas',
            label_type=TextType.NORMAL_TEXT, align=Qt.AlignHCenter
        )
        return subtitle

    @staticmethod
    def _get_logo_widget() -> QLabel:
        logo_widget = LabelFactory.get_label_image_component(image_name='uva_logo2.png', align=Qt.AlignHCenter,
                                                             width=600, height=600)
        return logo_widget

    def _get_enter_button(self) -> QPushButton:
        icon = IconFactory.get_icon_widget(image_name='power_button2.png')
        button = ButtonFactory.get_button_component(title='', function_to_connect=self.continue_signal, icon=icon,
                                                    icon_size=75, tooltip='Iniciar')
        return button

    @staticmethod
    def _get_footer_layout() -> QVBoxLayout:
        layout = QVBoxLayout()
        student_label = LabelFactory.get_label_component(text='Alumno: Tomás Meroño Madriz.',
                                                         label_type=TextType.SUBTITLE)
        teacher_label = LabelFactory.get_label_component(text='Tutora: María Rosario Abril Raymundo.',
                                                         label_type=TextType.SUBTITLE)
        layout.addWidget(student_label, alignment=Qt.AlignRight)
        layout.addWidget(teacher_label, alignment=Qt.AlignRight)
        return layout

    @staticmethod
    def _set_layout(layout: QVBoxLayout, title_widget: QLabel, subtitle_widget: QLabel, logo_widget: QLabel,
                    enter_button: QPushButton, footer_layout: QVBoxLayout):
        layout.setContentsMargins(0, 70, 0, 0)
        layout.setAlignment(Qt.AlignTop | Qt.AlignHCenter)
        layout.addWidget(title_widget)
        layout.addSpacing(10)
        layout.addWidget(subtitle_widget)
        layout.addSpacing(30)
        layout.addWidget(logo_widget, alignment=Qt.AlignHCenter)
        layout.addSpacing(30)
        layout.addWidget(enter_button, alignment=Qt.AlignHCenter)
        layout.addSpacing(65)
        layout.addLayout(footer_layout)
        layout.addStretch()

    def keyPressEvent(self, e):
        if e.key() in (Qt.Key_Return, Qt.Key_Enter):
            self.continue_signal.emit()
        elif e.key() == Qt.Key_Escape:
            self.close_signal.emit()
