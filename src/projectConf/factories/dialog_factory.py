from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog, QDialogButtonBox, QVBoxLayout

from .label_factory import LabelFactory
from ..models.enums import TextType


class DialogFactory:
    @classmethod
    def get_dialog_widget(cls, text: str, accepted_fn, rejected_fn, window_title: str = 'Confirmación') -> QDialog:
        dialog_widget = QDialog()
        dialog_widget.setWindowTitle(window_title)

        buttons = QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        button_box = QDialogButtonBox(buttons)
        button_box.accepted.connect(accepted_fn)
        button_box.rejected.connect(rejected_fn)

        dialog_layout = QVBoxLayout()
        message = LabelFactory.get_label_component(text=text, label_type=TextType.NORMAL_TEXT, align=Qt.AlignHCenter)
        dialog_layout.addWidget(message)
        dialog_layout.addSpacing(7)
        dialog_layout.addWidget(button_box)
        dialog_widget.setLayout(dialog_layout)
        return dialog_widget
