from typing import List

from .function import Function
from .help_step import HelpStep


class HelpData:
    def __init__(self, order: int, functions: List[Function], help_steps: List[HelpStep], text: str = ''):
        self.order = order
        self.functions = functions
        self.help_steps = help_steps
        self.text = text
