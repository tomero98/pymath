from PyQt5.QtWidgets import QPushButton, QSizePolicy


class ButtonFactory:
    @classmethod
    def get_button_component(cls, title: str, function_to_connect=None, is_disable: bool = False,
                             size_policy=(QSizePolicy.Fixed, QSizePolicy.Fixed)) -> QPushButton:
        button = QPushButton(title)
        button.setSizePolicy(*size_policy)
        button.pressed.connect(function_to_connect)
        button.setDisabled(is_disable)
        return button
