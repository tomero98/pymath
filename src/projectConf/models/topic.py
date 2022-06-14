class Topic:
    def __init__(self, identifier: int, title: str, description: str, topic_parent_id: [id, None]):
        self.id = identifier
        self.title = title
        self.description = description
        self.topic_parent_id = topic_parent_id

    @staticmethod
    def get_topics() -> list:
        pass

    @classmethod
    def create_topic(cls, identifier: int, title: str, description: str, topic_parent_id: [int, None]):
        return cls(identifier=identifier, title=title, description=description, topic_parent_id=topic_parent_id)
