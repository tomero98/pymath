from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QIcon, QCursor
from PyQt5.QtWidgets import QPushButton, QSizePolicy, QGraphicsDropShadowEffect


class ButtonFactory:
    @classmethod
    def get_button_component(cls, title: str, function_to_connect=None, is_disable: bool = False,
                             size_policy=(QSizePolicy.Fixed, QSizePolicy.Fixed), icon: QIcon = None,
                             icon_size: int = None, tooltip: str = '', minimum_width: int = None,
                             minimum_height: int = None, text_size: int = None,
                             secondary_button: bool = False, primary_button: bool = False) -> QPushButton:
        button = QPushButton(title)
        button.setSizePolicy(*size_policy)
        button.pressed.connect(function_to_connect)
        button.setDisabled(is_disable)
        button.setCursor(QCursor(Qt.PointingHandCursor))
        button.setToolTip(tooltip)

        if minimum_width:
            button.setMinimumWidth(minimum_width)

        if minimum_height:
            button.setMinimumHeight(minimum_height)

        if icon:
            button.setLayoutDirection(Qt.RightToLeft)
            button.setIcon(icon)
            button.setIconSize(QSize(icon_size, icon_size))
            button.setStyleSheet('border-radius: 25px')

        if text_size:
            button.setStyleSheet(f'font-size: {text_size}px')

        if secondary_button:
            button.setObjectName('secondary')
            button.setStyleSheet("""
            #secondary {
                background-color: #CBC5F8;
                border: 1px solid #4831FF; 
                border-radius: 10px;
                padding: 3px;
            }
            
            #secondary:hover {
                border: 3px solid #4831FF; 
            }
            """)
            effect = QGraphicsDropShadowEffect()
            effect.setOffset(0, 0)
            effect.setBlurRadius(5)
            button.setGraphicsEffect(effect)

        if primary_button:
            button.setObjectName('primary')
            button.setStyleSheet("""
            #primary {
                background-color: #DEC0F1;
                border: 1px solid #957FEF; 
                border-radius: 10px;
                padding: 3px;
                font-size: 20px;
            }
            
            #primary:hover {
                border: 3px solid #957FEF; 
            }
            """)
            effect = QGraphicsDropShadowEffect()
            effect.setOffset(0, 0)
            effect.setBlurRadius(5)
            button.setGraphicsEffect(effect)
        return button
