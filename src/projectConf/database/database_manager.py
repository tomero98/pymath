import os
import sys

from PyQt5.QtSql import QSqlDatabase, QSqlQuery


class DatabaseManager:
    def setup_database(self):
        database_name = 'project.db'
        database = QSqlDatabase.addDatabase('QSQLITE')
        database.setDatabaseName(database_name)

        is_database_created = os.path.isfile(database_name)

        if not database.open():
            print("Database Error: %s" % database.lastError().databaseText())
            sys.exit(1)

        if not is_database_created:
            self._create_database()

    def _create_database(self):
        self._setup_topic_data()
        self._setup_subtopic_data()
        self._setup_exercise_data()
        self._setup_graph_data()
        self._setup_exercise_graph_data()

    def _setup_topic_data(self):
        self._create_topic_table()
        self._populate_topic_data()

    @staticmethod
    def _create_topic_table():
        sql_query = QSqlQuery()
        sql_query.exec(
            """
            CREATE TABLE topics (
                id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
                title VARCHAR(64) NOT NULL,
                description VARCHAR(128),
                topic_parent_id INT,
                FOREIGN KEY (topic_parent_id) REFERENCES topics(id)
                )
            """
        )

    @staticmethod
    def _populate_topic_data():
        topic_seed = ['Funciones']
        sql_query = QSqlQuery()
        sql_query.prepare(
            """
            INSERT INTO topics (title) VALUES (?)
            """
        )

        for title in topic_seed:
            sql_query.addBindValue(title)
            sql_query.exec()

    def _setup_subtopic_data(self):
        self._populate_subtopic_data()

    @staticmethod
    def _populate_subtopic_data():
        subtopic_seed = [
            ('Funciones inversas', 'Ejercicios sobre inversas', 1),
            ('Dominio y recorrido', 'Ejercicios sobre dominio y recorrido', 1),
            ('Gráficas elementales', 'Ejercicios para reconocer gráficas elementales', 1),
            ('Máximos y mínimos', 'Ejercicios para detectar máximos y mínimos', 1)
        ]
        sql_query = QSqlQuery()
        sql_query.prepare(
            """
            INSERT INTO topics (title, description, topic_parent_id) VALUES (?, ?, ?)
            """
        )

        for title, description, parent_topic_id in subtopic_seed:
            sql_query.addBindValue(title)
            sql_query.addBindValue(description)
            sql_query.addBindValue(parent_topic_id)
            sql_query.exec()

    def _setup_exercise_data(self):
        self._create_exercise_table()
        self._populate_exercise_data()

    @staticmethod
    def _create_exercise_table():
        sql_query = QSqlQuery()
        sql_query.exec(
            """
            CREATE TABLE exercises (
                id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
                title VARCHAR(64) NOT NULL,
                type VARCHAR(64) NOT NULL,
                'order' INT NOT NULL, 
                priority INT NOT NULL, 
                help_text VARCHAR(64), 
                topic_id INT NOT NULL,
                FOREIGN KEY (topic_id) REFERENCES topics(id)
                )
            """
        )

    @staticmethod
    def _populate_exercise_data():
        exercise_seed = [
            ('Conceptos sobre funciones inversas', 'ConceptInverseExercise', 0, 0, 'Help text', 2),
            ('Conceptos sobre dominio y recorrido', 'ConceptDomainExercise', 0, 0, 'Help text', 3),
            ('Conceptos sobre dominio y recorrido', 'ConceptDomainExercise', 1, 1, 'Help text', 3),
            ('Conceptos sobre dominio y recorrido', 'ConceptDomainExercise', 2, 2, 'Help text', 3),
            ('Conceptos sobre funciones inversas', 'ConceptInverseExercise', 1, 1, 'Help text', 2),
            ('Gráficas elementales', 'ElementaryGraphExercise', 0, 0, 'Help text', 4),
            ('Máximos relativos y absoluto', 'MaximumPointsExercise', 0, 0, 'Help text', 5),
            ('Mínimos relativos y absoluto', 'MinimumPointsExercise', 0, 0, 'Help text', 5),
        ]
        sql_query = QSqlQuery()
        sql_query.prepare(
            """
            INSERT INTO exercises (title, type, 'order', priority, help_text, topic_id) VALUES (?, ?, ?, ?, ?, ?)
            """
        )

        for title, exercise_type, exercise_order, priority, help_text, topic_id in exercise_seed:
            sql_query.addBindValue(title)
            sql_query.addBindValue(exercise_type)
            sql_query.addBindValue(exercise_order)
            sql_query.addBindValue(priority)
            sql_query.addBindValue(help_text)
            sql_query.addBindValue(topic_id)
            sql_query.exec()

    def _setup_graph_data(self):
        self._create_graph_table()
        self._populate_graph_data()

    @staticmethod
    def _create_graph_table():
        sql_query = QSqlQuery()
        sql_query.exec(
            """
            CREATE TABLE graphs (
                id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
                expression VARCHAR(64) NOT NULL,
                domain VARCHAR(64),
                is_elementary_graph INT,
                inverse_graph_id INT,
                FOREIGN KEY (inverse_graph_id) REFERENCES graphs(id)
                )
            """
        )

    @staticmethod
    def _populate_graph_data():
        graph_seed = [
            ('math.sqrt(x)', '[0, 5)', 0, None),
            ('x**2', '[0, 5)', 0, 1),
            ('x + 2', '[0, 5)', 0, None),
            ('x - 1', '[0, 5)', 0, None),
            ('x**3', '[-6, 6]', 1, None),
            ('3', '(-3, 2]', 1, None),
            ('math.sin(x)', '[-3, 1)', 1, None),
            ('2', '[2, 8]', 1, None),
            ('(x)**4', '[-3, 3]', 0, None),
            ('x**(1/4)', '[0, 3]', 0, 9),
            ('math.cos(x)', '(-4, 2)', 1, None),
            ('math.tan(x)', '(-4, 4)', 1, None),
            ('math.asin(x)', '(-1, 1)', 1, None),
            ('math.acos(x)', '(-1, 1)', 1, None),
            ('math.atan(x)', '(-3, 4]', 1, None),
            ('(x)**3-4*(x)**2+2*x+2', '(-3, 3]', 0, None),
            ('(x)**3-3*(x)**2', '(-1, 3)', 0, None),
        ]
        sql_query = QSqlQuery()
        sql_query.prepare(
            """
            INSERT INTO graphs (expression, domain, is_elementary_graph, inverse_graph_id) VALUES (?, ?, ?,?)
            """
        )

        for expression, domain, is_elementary_graph, inverse_graph_id in graph_seed:
            sql_query.addBindValue(expression)
            sql_query.addBindValue(domain)
            sql_query.addBindValue(is_elementary_graph)
            sql_query.addBindValue(inverse_graph_id)
            sql_query.exec()

    def _setup_exercise_graph_data(self):
        self._create_exercise_graph_table()
        self._populate_exercise_graph_data()

    @staticmethod
    def _create_exercise_graph_table():
        sql_query = QSqlQuery()
        sql_query.exec(
            """
            CREATE TABLE exercise_graphs (
                id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
                exercise_id INT NOT NULL,
                graph_id INT NOT NULL,
                is_main_graphic INT
                )
            """
        )

    @staticmethod
    def _populate_exercise_graph_data():
        exercise_graph_seed = [
            (1, 1, 1),
            (1, 3, 0),
            (1, 4, 0),
            (2, 5, 1),
            (3, 6, 1),
            (4, 7, 1),
            (4, 8, 1),
            (5, 9, 1),
            (5, 10, 0),
            (6, 7, 1),
            (6, 11, 0),
            (6, 12, 0),
            (6, 13, 0),
            (7, 17, 1),
            (8, 16, 1),
        ]
        sql_query = QSqlQuery()
        sql_query.prepare(
            """
            INSERT INTO exercise_graphs (exercise_id, graph_id, is_main_graphic) VALUES (?, ?, ?)
            """
        )

        for exercise_id, graph_id, is_main_graphic in exercise_graph_seed:
            sql_query.addBindValue(exercise_id)
            sql_query.addBindValue(graph_id)
            sql_query.addBindValue(is_main_graphic)
            sql_query.exec()
