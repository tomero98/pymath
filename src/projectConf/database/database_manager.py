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
        self._setup_exercise_resume()
        self._setup_exercise_settings_data()
        self._setup_step_settings_data()

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
                first_time INT
                )
            """
        )

    @staticmethod
    def _populate_topic_data():
        topic_seed = [
            {'title': 'Funciones inversas', 'description': 'Ejercicios sobre inversas', 'first_time': 1},  # 1
            {'title': 'Dominio y recorrido', 'description': 'Ejercicios sobre dominio y recorrido', 'first_time': 1},
            # 2
            {'title': 'Gráficas elementales', 'description': 'Ejercicios para reconocer gráficas elementales',
             'first_time': 1},  # 3
            {'title': 'Máximos y mínimos', 'description': 'Ejercicios para detectar máximos y mínimos',
             'first_time': 1},  # 4
        ]

        sql_query = QSqlQuery()
        sql_query.prepare(
            """
            INSERT INTO topics (title, description, first_time) VALUES (?, ?, ?)
            """
        )

        for topic in topic_seed:
            sql_query.addBindValue(topic['title'])
            sql_query.addBindValue(topic['description'])
            sql_query.addBindValue(topic['first_time'])
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
        sql_query = QSqlQuery()
        exercise_seed = [
            # Elementary exercises
            {'exercise_type': 'ElementaryGraphExercise', 'domain': None, 'topic_id': 3},  # 1

            # Inverse exercises
            {'exercise_type': 'InverseGraphExercise', 'domain': '-2, 2', 'topic_id': 1},  # 2
            {'exercise_type': 'InverseGraphExercise', 'domain': '-3, 3', 'topic_id': 1},  # 3

            # Domain exercises
            {'exercise_type': 'ConceptDomainExercise', 'domain': None, 'topic_id': 2},  # 4

            # Maximum minimum exercises
            {'exercise_type': 'MaximumMinimumExercise', 'domain': None, 'topic_id': 2},  # 5
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
            {'expression': 'x'},  # 6
            {'expression': 'math.cos(x)'},  # 7
            {'expression': 'math.sin(x)'},  # 8
            {'expression': 'math.tan(x)'},  # 9

            # Inverse graphs
            {'expression': '-x**(1/3)'},  # 10
            {'expression': '-(x)**3 * (-x**2)'},  # 11

            # Domain graphs
            {'expression': 'x'},  # 12
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
            # {'exercise_id': 1, 'graph_id': 1, 'domain': None, 'is_main_graphic': 0},  # 1
            # {'exercise_id': 1, 'graph_id': 2, 'domain': None, 'is_main_graphic': 0},  # 2
            # {'exercise_id': 1, 'graph_id': 3, 'domain': None, 'is_main_graphic': 0},  # 3
            # {'exercise_id': 1, 'graph_id': 4, 'domain': None, 'is_main_graphic': 0},  # 4
            # {'exercise_id': 1, 'graph_id': 5, 'domain': None, 'is_main_graphic': 0},  # 5
            {'exercise_id': 1, 'graph_id': 6, 'domain': None, 'is_main_graphic': 0},  # 6
            {'exercise_id': 1, 'graph_id': 7, 'domain': None, 'is_main_graphic': 0},  # 7
            {'exercise_id': 1, 'graph_id': 8, 'domain': None, 'is_main_graphic': 0},  # 8
            {'exercise_id': 1, 'graph_id': 9, 'domain': None, 'is_main_graphic': 0},  # 9

            # Inverse exercise
            {'exercise_id': 2, 'graph_id': 2, 'domain': None, 'is_main_graphic': True},  # 10
            {'exercise_id': 2, 'graph_id': 10, 'domain': None, 'is_main_graphic': False},  # 11
            {'exercise_id': 2, 'graph_id': 11, 'domain': None, 'is_main_graphic': False},  # 12

            {'exercise_id': 3, 'graph_id': 3, 'domain': None, 'is_main_graphic': True},  # 14

            {'exercise_id': 4, 'graph_id': 12, 'domain': None, 'is_main_graphic': True},  # 15

            {'exercise_id': 5, 'graph_id': 3, 'domain': '(3, 3)', 'is_main_graphic': True},  # 16
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
                step_type VARCHAR(64) NOT NULL,
                response VARCHAR(64) NOT NULL,
                exercise_id INT NOT NULL,
                graph_id INT NOT NULL,
                FOREIGN KEY (exercise_id) REFERENCES exercises(id),
                FOREIGN KEY (graph_id) REFERENCES graphs(id)
                )
            """
        )

    def _setup_exercise_settings_data(self):
        self._create_exercise_settings_table()
        self._populate_exercise_settings_data()

    @staticmethod
    def _create_exercise_settings_table():
        sql_query = QSqlQuery()
        sql_query.exec(
            """
            CREATE TABLE exercise_settings (
                id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
                exercise_type VARCHAR(64) NOT NULL,
                description VARCHAR(128), 
                exercise_num INT NOT NULL,
                is_active INT NOT NULL,
                topic_id INT NOT NULL,
                FOREIGN KEY (topic_id) REFERENCES topics(id)
                )
            """
        )

    @staticmethod
    def _populate_exercise_settings_data():
        exercise_settings_seed = [
            {
                'exercise_type': 'InverseGraphExercise',
                'description': 'Estudio de la función inversa.',
                'exercise_num': 5,
                'is_active': 1,
                'topic_id': 1,
            },
            {
                'exercise_type': 'ConceptDomainExercise',
                'description': 'Estudio del dominio y recorrido de la función.',
                'exercise_num': 5,
                'is_active': 1,
                'topic_id': 2,
            },
            {
                'exercise_type': 'ElementaryGraphExercise',
                'description': 'Estudio de las gráficas elementales.',
                'exercise_num': 5,
                'is_active': 1,
                'topic_id': 3,
            },
            {
                'exercise_type': 'MaximumMinimumExercise',
                'description': 'Estudio de puntos máximos en la función.',
                'exercise_num': 5,
                'is_active': 1,
                'topic_id': 4,
            },
        ]

        sql_query = QSqlQuery()
        sql_query.prepare(
            """
            INSERT INTO exercise_settings (exercise_type, description, exercise_num, is_active, topic_id) VALUES (?, ?, ?, ?, ?)
            """
        )

        for topic in exercise_settings_seed:
            sql_query.addBindValue(topic['exercise_type'])
            sql_query.addBindValue(topic['description'])
            sql_query.addBindValue(topic['exercise_num'])
            sql_query.addBindValue(topic['is_active'])
            sql_query.addBindValue(topic['topic_id'])
            sql_query.exec()

    def _setup_step_settings_data(self):
        self._create_step_settings_table()
        self._populate_step_settings_data()

    @staticmethod
    def _create_step_settings_table():
        sql_query = QSqlQuery()
        sql_query.exec(
            """
            CREATE TABLE step_settings (
                id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
                step_type VARCHAR(64) NOT NULL,
                description VARCHAR(128), 
                is_active INT NOT NULL,
                exercise_setting_id INT NOT NULL,
                FOREIGN KEY (exercise_setting_id) REFERENCES exercise_settings(id)
                )
            """
        )

    @staticmethod
    def _populate_step_settings_data():
        step_settings_seed = [
            {
                'step_type': 'ConceptInverseExercise',
                'description': 'Indicar si la siguiente función tiene inversa.',
                'is_active': 1,
                'exercise_setting_id': 1,
            },
            {
                'step_type': 'SelectionInverseExercise',
                'description': 'Seleccionar la función inversa.',
                'is_active': 1,
                'exercise_setting_id': 1,
            },
            {
                'step_type': 'DelimitedInverseExercise',
                'description': 'Definir el dominio de la función para la cual hay inversa.',
                'is_active': 1,
                'exercise_setting_id': 1,
            },

            {
                'step_type': 'IndicateDomainExercise',
                'description': 'Indicar el dominio de la función.',
                'is_active': 1,
                'exercise_setting_id': 2,
            },
            {
                'step_type': 'IndicateRangeExercise',
                'description': 'Indicar el recorrido de la función.',
                'is_active': 1,
                'exercise_setting_id': 2,
            },

            {
                'step_type': 'IndicateElementaryExercise',
                'description': 'Seleccionar la función elemental correcta.',
                'is_active': 1,
                'exercise_setting_id': 3,
            },
            {
                'step_type': 'IndicateElementaryShiftExercise',
                'description': 'Seleccionar el desplazamiento correcto.',
                'is_active': 1,
                'exercise_setting_id': 3,
            },

            {
                'step_type': 'MaximumMinimumExercise',
                'description': 'Seleccionar máximos y mínimos absolutos y relativos.',
                'is_active': 1,
                'exercise_setting_id': 4,
            }
        ]

        sql_query = QSqlQuery()
        sql_query.prepare(
            """
            INSERT INTO step_settings (step_type, description, is_active, exercise_setting_id) VALUES (?, ?, ?, ?)
            """
        )

        for step_setting in step_settings_seed:
            sql_query.addBindValue(step_setting['step_type'])
            sql_query.addBindValue(step_setting['description'])
            sql_query.addBindValue(step_setting['is_active'])
            sql_query.addBindValue(step_setting['exercise_setting_id'])
            sql_query.exec()
