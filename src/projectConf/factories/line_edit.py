from PyQt5.QtWidgets import QLineEdit


class LineEditFactory:
    @classmethod
    def get_line_edit_component(cls, placeholder_text: str) -> QLineEdit:
        line_edit = QLineEdit()
        line_edit.setPlaceholderText(placeholder_text)
        return line_edit
