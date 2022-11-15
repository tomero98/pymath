from PyQt5.QtSql import QSqlQuery

from ..models import Topic


class TopicDataMapper:
    @classmethod
    def get_topics(cls):
        query = cls._get_topic_query()
        result = QSqlQuery()
        result.exec(query)

        topics = []
        while result.next():
            identifier = result.value('id')
            title = result.value('title')
            description = result.value('description')
            topic = Topic.create_topic(identifier=identifier, title=title, description=description)
            topics.append(topic)
        return topics

    @staticmethod
    def _get_topic_query():
        return 'SELECT id, title, description FROM topics'
