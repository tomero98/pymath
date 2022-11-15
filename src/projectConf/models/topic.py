class Topic:
    def __init__(self, identifier: int, title: str, description: str):
        self.id = identifier
        self.title = title
        self.description = description

    @classmethod
    def create_topic(cls, identifier: int, title: str, description: str):
        return cls(identifier=identifier, title=title, description=description)
