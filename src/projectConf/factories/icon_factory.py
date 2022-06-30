import os
from pathlib import Path

from PyQt5.QtGui import QIcon


class IconFactory:
    @classmethod
    def get_icon_widget(cls, image_name: str) -> QIcon:
        image_path = cls._get_image_path(image_name=image_name)
        return QIcon(image_path)

    @staticmethod
    def _get_image_path(image_name: str) -> str:
        image_path = str(Path(os.path.dirname(os.path.abspath(__file__))).parent.parent.joinpath(f'media/{image_name}'))
        return image_path
