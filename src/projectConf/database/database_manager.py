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
        self._setup_exercise_data()
        self._setup_graph_data()
        self._setup_exercise_graph_data()
        # self._setup_user_data()
        # self._setup_exercise_resume()

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
                description VARCHAR(128)
                )
            """
        )

    @staticmethod
    def _populate_topic_data():
        topic_seed = [
            {'title': 'Funciones inversas', 'description': 'Ejercicios sobre inversas'},  # 1
            {'title': 'Dominio y recorrido', 'description': 'Ejercicios sobre dominio y recorrido'},  # 2
            {'title': 'Gráficas elementales', 'description': 'Ejercicios para reconocer gráficas elementales'},  # 3
            {'title': 'Máximos y mínimos', 'description': 'Ejercicios para detectar máximos y mínimos'},  # 4
        ]

        sql_query = QSqlQuery()
        sql_query.prepare(
            """
            INSERT INTO topics (title, description) VALUES (?, ?)
            """
        )

        for topic in topic_seed:
            sql_query.addBindValue(topic['title'])
            sql_query.addBindValue(topic['description'])
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
                exercise_type VARCHAR(64) NOT NULL,
                domain VARCHAR(64),
                topic_id INT NOT NULL,
                FOREIGN KEY (topic_id) REFERENCES topics(id)
                )
            """
        )

    @staticmethod
    def _populate_exercise_data():
        # Domain example: '5, 5'
        sql_query = QSqlQuery()
        exercise_seed = [
            # Elementary functions exercises
            {'exercise_type': 'ElementaryGraphExercise', 'domain': None, 'topic_id': 3},  # 1

            # Inverse exercise
            {'exercise_type': 'InverseGraphExercise', 'domain': '-2, 2', 'topic_id': 1},  # 2
            {'exercise_type': 'InverseGraphExercise', 'domain': '-3, 3', 'topic_id': 1}  # 3

            # # Domain functions exercises
            # ('ConceptDomainExercise', 0, None, 2),  # 2
            # ('ConceptDomainExercise', 0, None, 2),  # 3
            # ('ConceptDomainExercise', 0, None, 2),  # 4
            # ('ConceptDomainExercise', 0, None, 2),  # 5
            # ('ConceptDomainExercise', 0, None, 2),  # 6
            # ('ConceptDomainExercise', 0, None, 2),  # 7

            # ('ConceptInverseExercise', 0, '-3, 3', 1),  # 1
            # ('ConceptInverseExercise', 0, '-3, 3', 1),  # 2
            # ('ConceptInverseExercise', 0, None, 1),  # 3
            # ('ConceptInverseExercise', 0, None, 1),  # 4
            # ('ConceptInverseExercise', 0, None, 1),  # 5
            # ('ConceptInverseExercise', 0, None, 1),  # 6
            #
            # # Domain exercise
            # ('ConceptDomainExercise', 0, None, 2),
            # ('ConceptDomainExercise', 1, None, 2),
            # ('ConceptDomainExercise', 2, None, 2),
            # ('ConceptDomainExercise', 3, None, 2),

            # # Maximum functions
            # ('MaximumPointsExercise', 0, None, 4),
            # ('MinimumPointsExercise', 1, None, 4),
            # ('MaximumPointsExercise', 2, None, 4),
            # ('MinimumPointsExercise', 3, None, 4),

        ]
        sql_query.prepare(
            """
            INSERT INTO exercises (exercise_type, domain, topic_id) VALUES (?, ?, ?)
            """
        )

        for exercise in exercise_seed:
            sql_query.addBindValue(exercise['exercise_type'])
            sql_query.addBindValue(exercise['domain'])
            sql_query.addBindValue(exercise['topic_id'])
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
                expression VARCHAR(64) NOT NULL
                )
            """
        )

    @staticmethod
    def _populate_graph_data():
        graph_seed = [
            # Elementary graphs
            {'expression': 'x**(1/3)'},  # 1
            {'expression': 'x**3'},  # 2
            {'expression': '(x)**2'},  # 3
            {'expression': '(x)**(1/2)'},  # 4
            {'expression': 'math.e**x'},  # 5
            {'expression': 'math.log(x)'},  # 6
            {'expression': 'math.cos(x)'},  # 7
            {'expression': 'math.sin(x)'},  # 8
            {'expression': 'math.tan(x)'},  # 9

            # Inverse graphs
            {'expression': '-x**(1/3)'},  # 10
            {'expression': '-(x)**3 * (-x**2)'},  # 11

            # Domain graphs
            # ('(x)**4 / 4 - 2 * (x)**3 / 3  - (x)**2 / 2 + 2 * (x) - 5 / 12', 0, None),  # 17
            # ('(x + 4) ** 2 - 1', 0, None),  # 18
            # ('- x', 0, None),  # 19
            # ('((x + 3) * (2 - x))**(1 / 2) - 1', 0, None),  # 20
            # ('- abs(x - 2) + 3', 0, None),  # 21
            # ('math.log(3 - x)', 0, None),  # 22
            # ('math.cosh(x)', 0, None),  # 23

            # Inverse graphs
            # {'expression': 'x**(3)'},  # 17
        ]
        sql_query = QSqlQuery()
        sql_query.prepare(
            """
            INSERT INTO graphs (expression) VALUES (?)
            """
        )

        for graph in graph_seed:
            sql_query.addBindValue(graph['expression'])
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
                domain VARCHAR(64),
                is_main_graphic INT,
                FOREIGN KEY (exercise_id) REFERENCES exercises(id),
                FOREIGN KEY (graph_id) REFERENCES graphs(id)
                )
            """
        )

    @staticmethod
    def _populate_exercise_graph_data():
        exercise_graph_seed = [
            # Elementary exercise
            {'exercise_id': 1, 'graph_id': 1, 'domain': None, 'is_main_graphic': 0},  # 1
            {'exercise_id': 1, 'graph_id': 2, 'domain': None, 'is_main_graphic': 0},  # 2
            {'exercise_id': 1, 'graph_id': 3, 'domain': None, 'is_main_graphic': 0},  # 3
            {'exercise_id': 1, 'graph_id': 4, 'domain': None, 'is_main_graphic': 0},  # 4
            {'exercise_id': 1, 'graph_id': 5, 'domain': None, 'is_main_graphic': 0},  # 5
            {'exercise_id': 1, 'graph_id': 6, 'domain': None, 'is_main_graphic': 0},  # 6
            {'exercise_id': 1, 'graph_id': 7, 'domain': None, 'is_main_graphic': 0},  # 7
            {'exercise_id': 1, 'graph_id': 8, 'domain': None, 'is_main_graphic': 0},  # 8
            {'exercise_id': 1, 'graph_id': 9, 'domain': None, 'is_main_graphic': 0},  # 9

            # Inverse exercise
            {'exercise_id': 2, 'graph_id': 2, 'domain': None, 'is_main_graphic': True},  # 10
            {'exercise_id': 2, 'graph_id': 10, 'domain': None, 'is_main_graphic': False},  # 11
            {'exercise_id': 2, 'graph_id': 11, 'domain': None, 'is_main_graphic': False},  # 12

            {'exercise_id': 3, 'graph_id': 3, 'domain': None, 'is_main_graphic': True},  # 14
        ]
        sql_query = QSqlQuery()
        sql_query.prepare(
            """
            INSERT INTO exercise_graphs (exercise_id, graph_id, domain, is_main_graphic) VALUES (?, ?, ?, ?)
            """
        )

        for exercise_graph in exercise_graph_seed:
            sql_query.addBindValue(exercise_graph['exercise_id'])
            sql_query.addBindValue(exercise_graph['graph_id'])
            sql_query.addBindValue(exercise_graph['domain'])
            sql_query.addBindValue(exercise_graph['is_main_graphic'])
            res = sql_query.exec()

    def _setup_user_data(self):
        self._create_user_table()
        self._populate_user_data()

    @staticmethod
    def _create_user_table():
        sql_query = QSqlQuery()
        sql_query.exec(
            """
            CREATE TABLE users (
                id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
                nickname VARCHAR(64) NOT NULL
                )
            """
        )

    @staticmethod
    def _populate_user_data():
        user_seed = [
            {'nickname': 'Anonymous'},  # 1
        ]

        sql_query = QSqlQuery()
        sql_query.prepare(
            """
            INSERT INTO users (nickname) VALUES (?)
            """
        )

        for user in user_seed:
            sql_query.addBindValue(user['nickname'])
            sql_query.exec()

    def _setup_exercise_resume(self):
        self._create_exercise_resume()

    @staticmethod
    def _create_exercise_resume():
        sql_query = QSqlQuery()
        sql_query.exec(
            """
            CREATE TABLE exercise_resumes (
                id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
                is_correct INT NOT NULL,
                user_id INT NOT NULL,
                step_type VARCHAR(64) NOT NULL,
                exercise_id INT NOT NULL,
                graph_id INT NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users(id),
                FOREIGN KEY (exercise_id) REFERENCES exercises(id),
                FOREIGN KEY (graph_id) REFERENCES graphs(id)
                )
            """
        )
