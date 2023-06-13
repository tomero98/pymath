from PyQt5.QtWidgets import QLineEdit


class LineEditFactory:
    @classmethod
    def get_line_edit_component(cls, placeholder_text: str, fixed_height: int = None,
                                font_size: int = None, fixed_width: int = None) -> QLineEdit:
        line_edit = QLineEdit()
        line_edit.setPlaceholderText(placeholder_text)
        if fixed_height:
            line_edit.setFixedHeight(fixed_height)
        if fixed_width:
            line_edit.setFixedWidth(fixed_width)
        if font_size:
            line_edit.setStyleSheet(f'font-size: {font_size}px')
        return line_edit
