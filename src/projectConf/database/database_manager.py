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
            ('Funciones inversas', 'Ejercicios sobre inversas', 1),  # 2
            ('Dominio y recorrido', 'Ejercicios sobre dominio y recorrido', 1),  # 3
            ('Gráficas elementales', 'Ejercicios para reconocer gráficas elementales', 1),  # 4
            ('Máximos y mínimos', 'Ejercicios para detectar máximos y mínimos', 1)  # 5
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
                type VARCHAR(64) NOT NULL,
                'order' INT NOT NULL, 
                domain VARCHAR(64),
                topic_id INT NOT NULL,
                FOREIGN KEY (topic_id) REFERENCES topics(id)
                )
            """
        )

    @staticmethod
    def _populate_exercise_data():
        # Domain example: '5, 5'
        exercise_seed = [
            # Elementary functions exercises
            ('ElementaryGraphExercise', 0, None, 4),  # 1

            # Domain functions exercises
            ('ConceptDomainExercise', 0, None, 3),  # 2
            ('ConceptDomainExercise', 0, None, 3),  # 3
            ('ConceptDomainExercise', 0, None, 3),  # 4
            ('ConceptDomainExercise', 0, None, 3),  # 5
            ('ConceptDomainExercise', 0, None, 3),  # 6
            ('ConceptDomainExercise', 0, None, 3),  # 7

            # # Inverse exercise
            # ('ConceptInverseExercise', 0, '-3, 3', 2),  # 1
            # ('ConceptInverseExercise', 0, '-3, 3', 2),  # 2
            # ('ConceptInverseExercise', 0, None, 2),  # 3
            # ('ConceptInverseExercise', 0, None, 2),  # 4
            # ('ConceptInverseExercise', 0, None, 2),  # 5
            # ('ConceptInverseExercise', 0, None, 2),  # 6
            #
            # # Domain exercise
            # ('ConceptDomainExercise', 0, None, 3),
            # ('ConceptDomainExercise', 1, None, 3),
            # ('ConceptDomainExercise', 2, None, 3),
            # ('ConceptDomainExercise', 3, None, 3),

            # # Maximum functions
            # ('MaximumPointsExercise', 0, None, 5),
            # ('MinimumPointsExercise', 1, None, 5),
            # ('MaximumPointsExercise', 2, None, 5),
            # ('MinimumPointsExercise', 3, None, 5),

        ]
        sql_query = QSqlQuery()
        sql_query.prepare(
            """
            INSERT INTO exercises (type, 'order', domain, topic_id) VALUES (?, ?, ?, ?)
            """
        )

        for exercise_type, exercise_order, domain, topic_id in exercise_seed:
            sql_query.addBindValue(exercise_type)
            sql_query.addBindValue(exercise_order)
            sql_query.addBindValue(domain)
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
                is_elementary_graph INT,
                inverse_graph_id INT,
                FOREIGN KEY (inverse_graph_id) REFERENCES graphs(id)
                )
            """
        )

    @staticmethod
    def _populate_graph_data():
        graph_seed = [
            # Elementary graphs
            ('x**(1/3)', 1, None),  # 1
            ('x**3', 1, None),  # 2
            ('-x**(1/3)', 1, None),  # 3
            ('x**2', 1, None),  # 4
            ('math.e**x', 1, None),  # 5
            ('math.log(x)', 1, None),  # 6
            ('-math.e**x', 1, None),  # 7
            ('0.5**x', 1, None),  # 8
            ('math.cos(x)', 1, None),  # 9
            ('math.acos(x)', 1, None),  # 10
            ('math.sin(x)', 1, None),  # 11
            ('math.asin(x)', 1, None),  # 12
            ('math.log(x - 1)', 1, None),  # 13
            ('(x + 2)**2', 1, None),  # 14
            ('x**2 - 1', 1, None),  # 15
            ('math.sinh(x + 1)', 1, None),  # 16

            # Domain graphs
            ('(x)**4 / 4 - 2 * (x)**3 / 3  - (x)**2 / 2 + 2 * (x) - 5 / 12', 0, None),  # 17
            ('(x + 4) ** 2 - 1', 0, None),  # 18
            ('- x', 0, None),  # 19
            ('((x + 3) * (2 - x))**(1 / 2) - 1', 0, None),  # 20
            ('- abs(x - 2) + 3', 0, None),  # 21
            ('math.log(3 - x)', 0, None),  # 22
            ('math.cosh(x)', 0, None),  # 23
        ]
        sql_query = QSqlQuery()
        sql_query.prepare(
            """
            INSERT INTO graphs (expression, is_elementary_graph, inverse_graph_id) VALUES (?, ?,?)
            """
        )

        for expression, is_elementary_graph, inverse_graph_id in graph_seed:
            sql_query.addBindValue(expression)
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
                is_main_graphic INT,
                domain VARCHAR(64)
                )
            """
        )

    @staticmethod
    def _populate_exercise_graph_data():
        exercise_graph_seed = [
            # Elementary exercise
            (1, 1, 0, None),
            (1, 2, 0, None),
            (1, 3, 0, None),
            (1, 4, 0, None),
            (1, 5, 0, None),
            (1, 6, 0, None),
            (1, 7, 0, None),
            (1, 8, 0, None),
            (1, 9, 0, None),
            (1, 10, 0, None),
            (1, 11, 0, None),
            (1, 12, 0, None),
            (1, 13, 0, None),
            (1, 14, 0, None),
            (1, 15, 0, None),
            (1, 16, 0, None),

            # Domain exercises
            (2, 17, 1, None),
            (3, 18, 1, '[-4, -2]'),
            (3, 19, 1, '(-1, 3]'),
            (4, 20, 1, '[-3, 2]'),
            (5, 21, 1, None),
            (6, 22, 1, None),
            (7, 23, 1, None),
        ]
        sql_query = QSqlQuery()
        sql_query.prepare(
            """
            INSERT INTO exercise_graphs (exercise_id, graph_id, is_main_graphic, domain) VALUES (?, ?, ?, ?)
            """
        )

        for exercise_id, graph_id, is_main_graphic, domain in exercise_graph_seed:
            sql_query.addBindValue(exercise_id)
            sql_query.addBindValue(graph_id)
            sql_query.addBindValue(is_main_graphic)
            sql_query.addBindValue(domain)
            sql_query.exec()
