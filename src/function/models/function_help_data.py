from typing import List

from .function import Function


class FunctionHelpData:
    def __init__(self, identifier: int, help_text: str, help_expressions: List[Function]):
        self.identifier = identifier
        self.help_text = help_text
        self.help_expressions = help_expressions
