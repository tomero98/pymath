from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QVBoxLayout, QLabel, QSizePolicy, QPushButton, QWidget, QHBoxLayout

from ..components import Window


class WelcomePage(Window):
    def __init__(self):
        title = 'Página de inicio'
        super(WelcomePage, self).__init__(title=title)

    def draw(self, *args, **kwargs):
        main_window = QWidget()
        layout = QVBoxLayout()

        title_widget = self._get_title_widget()
        subtitle_widget = self._get_subtitle_widget()
        logo_widget = self._get_logo_widget()
        enter_button = self._get_enter_button()
        self._set_layout(layout=layout, title_widget=title_widget, subtitle_widget=subtitle_widget,
                         logo_widget=logo_widget, enter_button=enter_button)

        main_window.setLayout(layout)
        self.setCentralWidget(main_window)
        self.show()

    @staticmethod
    def _get_title_widget():
        label = QLabel()
        text = 'UVa PyMath'
        font = QFont('Times', 36, QFont.Capitalize)
        font.setUnderline(True)
        align = Qt.AlignHCenter
        label.setText(text)
        label.setFont(font)
        label.setAlignment(align)
        return label

    @staticmethod
    def _get_subtitle_widget():
        label = QLabel()
        text = 'Aplicación de refuerzo para la asignatura de Fundamento de Matemáticas'
        font = QFont('Times', 18, QFont.Capitalize)
        align = Qt.AlignHCenter
        label.setText(text)
        label.setFont(font)
        label.setAlignment(align)
        return label

    @staticmethod
    def _get_logo_widget() -> QLabel:
        pixmap = QPixmap('uva_logo.png')
        logo_widget = QLabel()
        logo_widget.setPixmap(pixmap)
        return logo_widget

    def _get_enter_button(self):
        text = 'Iniciar'
        button = QPushButton(text)
        button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        button.pressed.connect(self.continue_signal)
        return button

    @staticmethod
    def _set_layout(layout: QVBoxLayout, title_widget: QLabel, subtitle_widget: QLabel, logo_widget: QLabel,
                    enter_button: QPushButton):
        layout.setContentsMargins(0, 75, 0, 0)
        layout.setSpacing(0)
        layout.setAlignment(Qt.AlignTop | Qt.AlignHCenter)
        layout.addWidget(title_widget)
        layout.addWidget(subtitle_widget)

        layout.addWidget(logo_widget)
        lay = QHBoxLayout()
        layout.addStretch()
        layout.addLayout(lay)
        lay.addStretch()
        lay.addWidget(enter_button)
        lay.addStretch()
        layout.addStretch()

    def keyPressEvent(self, e):
        if e.key() in (Qt.Key_Return, Qt.Key_Enter):
            self.continue_signal.emit()
        elif e.key() == Qt.Key_Escape:
            self.close_signal.emit()
