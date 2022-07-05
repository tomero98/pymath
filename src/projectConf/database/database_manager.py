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
            ('Conceptos sobre funciones inversas', 'ConceptInverseExercise', 0, 0, 'Help text', 2),  # 1
            ('Conceptos sobre funciones inversas', 'ConceptInverseExercise', 1, 0, 'Help text', 2),  # 2
            ('Conceptos sobre funciones inversas', 'ConceptInverseExercise', 2, 0, 'Help text', 2),  # 3
            ('Conceptos sobre funciones inversas', 'ConceptInverseExercise', 3, 0, 'Help text', 2),  # 4
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
            # First exercise inverse
            ('x**(1/5)', '[-4, 4]', 1, None),  # 1
            ('x**5', '[-2, 2]', 1, 1),  # 2
            ('-(x**(1/5))', '[-4, 4]', 0, None),  # 3
            ('-x**1/2', '[0, 4]', 0, None),  # 4

            # Second exercise inverse
            ('math.e**x', '[-4, 2]', 1, None),  # 5
            ('math.log(x)', '[0, 3]', 1, 5),  # 6
            ('-math.e**x', '[-4, 2]', 0, None),  # 7
            ('-(x+4)**(1/2)', '[-4, 6]', 0, None),  # 8

            # Third exercise inverse
            ('math.cos(x)', '[-4, 4]', 1, None),  # 9
            ('math.acos(x)', '[-1, 1]', 0, 9),  # 10
            ('math.sin(x)', '[-4, 4]', 1, None),  # 11
            ('-math.cos(x)', '[-4, 4]', 0, None),  # 12

            # Four exercise inverse
            ('x**4', '(0, 2)', 1, None),  # 13
            ('x**(1/4)', '[0, 6)', 0, 13),  # 14
            ('-x**4', '(0, 2)', 0, None),  # 15
            ('-x**3', '(0, 2', 0, None),  # 16



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
            # First exercise
            (1, 1, 1),
            (1, 2, 0),
            (1, 3, 0),
            (1, 4, 0),

            # Second exercise
            (2, 5, 1),
            (2, 6, 0),
            (2, 7, 0),
            (2, 8, 0),

            # Third exercise
            (3, 9, 1),
            (3, 10, 0),
            (3, 11, 0),
            (3, 12, 0),

            # Four exercise
            (4, 13, 1),
            (4, 14, 0),
            (4, 15, 0),
            (4, 16, 0),

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
