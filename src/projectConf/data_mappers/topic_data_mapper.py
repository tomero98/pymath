from PyQt5.QtSql import QSqlQuery

from ..models import Topic


class TopicDataMapper:
    @classmethod
    def get_topics(cls, topic_parent_id: [int, None]):
        query = cls._get_topic_query() if not topic_parent_id \
            else cls._get_subtopic_query(topic_parent_id=topic_parent_id)
        result = QSqlQuery()
        result.exec(query)

        topics = []
        while result.next():
            identifier = result.value('id')
            title = result.value('title')
            description = result.value('description')
            topic_parent_id = result.value('topic_parent_id')
            topic = Topic.create_topic(identifier=identifier, title=title, description=description,
                                       topic_parent_id=topic_parent_id)
            topics.append(topic)
        return topics

    @staticmethod
    def _get_topic_query():
        return 'SELECT id, title, description, topic_parent_id FROM topics WHERE topic_parent_id IS NULL'

    @staticmethod
    def _get_subtopic_query(topic_parent_id):
        return f'SELECT id, title, description, topic_parent_id FROM topics WHERE topic_parent_id={topic_parent_id}'
