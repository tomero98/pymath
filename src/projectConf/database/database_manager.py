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
        self._setup_exercise_graph_points_data()
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
            {'title': 'Funciones inversas',
             'description': 'Ejercicios para afianzar el conocimiento sobre las funciones inversas: '
                            'detección de inversas y restricciones de dominio.', 'first_time': 1},  # 1
            {'title': 'Dominio y recorrido',
             'description': 'Ejercicios para interiorizar los conceptos de dominio y recorrido:'
                            ' definir el conjunto inicial y el conjunto final. ', 'first_time': 1},
            # 2
            {'title': 'Funciones elementales',
             'description': 'Ejercicios para reconocer funciones: funciones elementales y'
                            ' desplazamientos sobre ellas.',
             'first_time': 1},  # 3
            {'title': 'Máximos y mínimos',
             'description': 'Ejercicios para la comprensión de puntos máximos y mínimos sobre '
                            'la función.',
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
            {'exercise_type': 'InverseGraphExercise', 'domain': '-3, 3', 'topic_id': 1},  # 2
            {'exercise_type': 'InverseGraphExercise', 'domain': '-3, 3', 'topic_id': 1},  # 3
            {'exercise_type': 'InverseGraphExercise', 'domain': '-3, 3', 'topic_id': 1},  # 4
            {'exercise_type': 'InverseGraphExercise', 'domain': '-3, 3', 'topic_id': 1},  # 5
            {'exercise_type': 'InverseGraphExercise', 'domain': '-3, 3', 'topic_id': 1},  # 6
            {'exercise_type': 'InverseGraphExercise', 'domain': '-3, 3', 'topic_id': 1},  # 7
            {'exercise_type': 'InverseGraphExercise', 'domain': None, 'topic_id': 1},  # 8
            {'exercise_type': 'InverseGraphExercise', 'domain': None, 'topic_id': 1},  # 9
            {'exercise_type': 'InverseGraphExercise', 'domain': '-4, 4', 'topic_id': 1},  # 10
            {'exercise_type': 'InverseGraphExercise', 'domain': '-3, 3', 'topic_id': 1},  # 11
            {'exercise_type': 'InverseGraphExercise', 'domain': '-3, 3', 'topic_id': 1},  # 12
            {'exercise_type': 'InverseGraphExercise', 'domain': '-3, 3', 'topic_id': 1},  # 13
            {'exercise_type': 'InverseGraphExercise', 'domain': None, 'topic_id': 1},  # 14
            {'exercise_type': 'InverseGraphExercise', 'domain': '-3, 3', 'topic_id': 1},  # 15
            {'exercise_type': 'InverseGraphExercise', 'domain': None, 'topic_id': 1},  # 16
            {'exercise_type': 'InverseGraphExercise', 'domain': '-2, 2', 'topic_id': 1},  # 17
            {'exercise_type': 'InverseGraphExercise', 'domain': '-4, 4', 'topic_id': 1},  # 18
            {'exercise_type': 'InverseGraphExercise', 'domain': '-3, 3', 'topic_id': 1},  # 19
            {'exercise_type': 'InverseGraphExercise', 'domain': '-2, 2', 'topic_id': 1},  # 20

            # Domain exercises
            {'exercise_type': 'ConceptDomainExercise', 'domain': '-5, 5', 'topic_id': 2},  # 21

            # Maximum exercises
            {'exercise_type': 'MaximumMinimumExercise', 'domain': '-5, 5', 'topic_id': 4},  # 22

            # Domain exercises
            {'exercise_type': 'ConceptDomainExercise', 'domain': '-4, 4', 'topic_id': 2},  # 23
            {'exercise_type': 'ConceptDomainExercise', 'domain': '-4, 4', 'topic_id': 2},  # 24
            {'exercise_type': 'ConceptDomainExercise', 'domain': '-4, 4', 'topic_id': 2},  # 25
            {'exercise_type': 'ConceptDomainExercise', 'domain': '-5, 5', 'topic_id': 2},  # 26
            {'exercise_type': 'ConceptDomainExercise', 'domain': '-5, 5', 'topic_id': 2},  # 27
            {'exercise_type': 'ConceptDomainExercise', 'domain': '-6, 6', 'topic_id': 2},  # 28
            {'exercise_type': 'ConceptDomainExercise', 'domain': '-6, 6', 'topic_id': 2},  # 29
            {'exercise_type': 'ConceptDomainExercise', 'domain': '-6, 6', 'topic_id': 2},  # 30
            {'exercise_type': 'ConceptDomainExercise', 'domain': '-3, 3', 'topic_id': 2},  # 31
            {'exercise_type': 'ConceptDomainExercise', 'domain': '-5, 5', 'topic_id': 2},  # 32
            {'exercise_type': 'ConceptDomainExercise', 'domain': '-5, 5', 'topic_id': 2},  # 33
            {'exercise_type': 'ConceptDomainExercise', 'domain': '-5, 5', 'topic_id': 2},  # 34
            {'exercise_type': 'ConceptDomainExercise', 'domain': '-5, 5', 'topic_id': 2},  # 35
            {'exercise_type': 'ConceptDomainExercise', 'domain': '-5, 5', 'topic_id': 2},  # 35
            {'exercise_type': 'ConceptDomainExercise', 'domain': '-2, 2', 'topic_id': 2},  # 36
            {'exercise_type': 'ConceptDomainExercise', 'domain': '-5, 5', 'topic_id': 2},  # 37
            {'exercise_type': 'ConceptDomainExercise', 'domain': '-5, 5', 'topic_id': 2},  # 38
            {'exercise_type': 'ConceptDomainExercise', 'domain': '-5, 5', 'topic_id': 2},  # 39
            {'exercise_type': 'ConceptDomainExercise', 'domain': '-5, 5', 'topic_id': 2},  # 40

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
            {'expression': '(x)**2'},  # 1
            {'expression': '(x)**3'},  # 2
            {'expression': '1 / (x)**3'},  # 3
            {'expression': '1 / (x)**2'},  # 4
            {'expression': 'math.sqrt(x)'},  # 5
            {'expression': 'math.sqrt(x**3)'},  # 6
            {'expression': '1 / math.sqrt(x)'},  # 7 need 100 points
            {'expression': '1 / math.sqrt((x)**2)'},  # 8
            {'expression': 'math.e**x'},  # 9
            {'expression': '(1 / math.e) ** x'},  # 10
            {'expression': 'math.cos(x)'},  # 11
            {'expression': 'math.sin(x)'},  # 12
            {'expression': 'math.tan(x)'},  # 13
            {'expression': 'math.cos(x) / math.sin(x)'},  # 14
            {'expression': '1 / math.sin(x)'},  # 15
            {'expression': '1 / math.cos(x)'},  # 16
            {'expression': '(math.e**x - math.e**(-x)) / 2'},  # 17
            {'expression': '(math.e**x + math.e**(-x)) / 2'},  # 18
            {'expression': '(math.e**x - math.e**(-x)) / (math.e**x + math.e**(-x))'},  # 19

            # Inverse graphs
            {'expression': '(-x)**3'},  # 20
            {'expression': '1 / (x)**3'},  # 21

            {'expression': '1 / x'},  # 22
            {'expression': '- 1 / x'},  # 23
            {'expression': '-1 / math.sqrt(x)'},  # 24

            {'expression': '- math.sqrt(x)'},  # 25

            {'expression': 'math.sqrt(-x)'},  # 26
            {'expression': '1 / math.sqrt(-x)'},  # 27
            {'expression': '- math.sqrt(-x)'},  # 28

            {'expression': '(3 * (x)**2) / ((x)**2 + 1)'},  # 29

            {'expression': 'x**2 - abs(x)'},  # 30

            {'expression': '- math.e**x'},  # 31
            {'expression': '-(x)**3'},  # 32

            {'expression': '(1 / 2)**x'},  # 33
            {'expression': '-(1 / 2)**x'},  # 34
            {'expression': '(1 / 2)**(-x)'},  # 35

            {'expression': '- ((3 * (x)**2) / ((x)**2 + 1))'},  # 36

            {'expression': '- ((3 * x) / ((x)**2 + 1))'},  # 37

            {'expression': 'math.log2(x)'},  # 38
            {'expression': '- math.log2(x)'},  # 39

            {'expression': 'math.log10(x)'},  # 40
            {'expression': '-math.log10(x)'},  # 41

            {'expression': '(3 * x) / ((x)**2 + 1)'},  # 42

            {'expression': '((x)**2 +  1) / x'},  # 43

            {'expression': 'math.log10(-x)'},  # 44

            {'expression': '(x)**2 / 4'},  # 45

            {'expression': '-(x)**2 / 2 + 4'},  # 46

            {'expression': '0'},  # 47

            {'expression': '-1'},  # 48

            {'expression': '((x)**2 * ((x)**4 + 7 * (x)**2 - 104)) / 120'},  # 49

            {'expression': 'abs(x)'},  # 50
            {'expression': '(x)**3 - 5 * (x)**2 + 3 * x + 8'},  # 51
            {'expression': 'abs(x+1)'},  # 52

            {'expression': '2 * (x)**2 - 3'},  # 53
            {'expression': '-x ** (3) + 11 * (x) ** 2 - 35 * x + 26'},  # 54
            {'expression': '2 * (x-3) * (x-5)'},  # 55

            {'expression': '-(((x + 4) * ((x) ** 2 + 2 * x + 8)) / (4))'}, #56
            {'expression': '-((3 * (x) ** 2 - 4 * x - 12) / (4))'}, #57

            {'expression': '-(2 * x) / 3'}, #58

            {'expression': '((2 * x**3 - 15 * (x)**2 + 24 * x + 5) / (4))'}, #59
            {'expression': '-9 * x**3 + 16 * (x)**2 - 3'}, #60
            {'expression': '-(((x)**(2) + 4 * x + 6)/(2))'}, #61

            {'expression': '3'}, #62
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
            {'exercise_id': 1, 'graph_id': 1, 'domain': '(-3, 3)', 'is_main_graphic': 0},  # 1
            {'exercise_id': 1, 'graph_id': 2, 'domain': '(-2, 2)', 'is_main_graphic': 0},  # 2
            {'exercise_id': 1, 'graph_id': 3, 'domain': None, 'is_main_graphic': 0},  # 3
            {'exercise_id': 1, 'graph_id': 4, 'domain': None, 'is_main_graphic': 0},  # 4
            {'exercise_id': 1, 'graph_id': 5, 'domain': '(0, +inf)', 'is_main_graphic': 0},  # 5
            {'exercise_id': 1, 'graph_id': 6, 'domain': '(0, +inf)', 'is_main_graphic': 0},  # 6
            {'exercise_id': 1, 'graph_id': 7, 'domain': '(0, +inf)', 'is_main_graphic': 0},  # 7
            {'exercise_id': 1, 'graph_id': 8, 'domain': None, 'is_main_graphic': 0},  # 8
            {'exercise_id': 1, 'graph_id': 9, 'domain': '(-inf, 2)', 'is_main_graphic': 0},  # 9
            {'exercise_id': 1, 'graph_id': 10, 'domain': '(-2, +inf)', 'is_main_graphic': 0},  # 10
            {'exercise_id': 1, 'graph_id': 11, 'domain': None, 'is_main_graphic': 0},  # 11
            {'exercise_id': 1, 'graph_id': 12, 'domain': None, 'is_main_graphic': 0},  # 12
            {'exercise_id': 1, 'graph_id': 13, 'domain': None, 'is_main_graphic': 0},  # 13
            {'exercise_id': 1, 'graph_id': 14, 'domain': None, 'is_main_graphic': 0},  # 14
            {'exercise_id': 1, 'graph_id': 15, 'domain': None, 'is_main_graphic': 0},  # 15
            {'exercise_id': 1, 'graph_id': 16, 'domain': None, 'is_main_graphic': 0},  # 16
            {'exercise_id': 1, 'graph_id': 17, 'domain': '(-3, 3)', 'is_main_graphic': 0},  # 17
            {'exercise_id': 1, 'graph_id': 18, 'domain': '(-3, 3)', 'is_main_graphic': 0},  # 18
            {'exercise_id': 1, 'graph_id': 19, 'domain': None, 'is_main_graphic': 0},  # 19

            # Inverse exercise
            {'exercise_id': 2, 'graph_id': 2, 'domain': None, 'is_main_graphic': 1},  # 20
            {'exercise_id': 2, 'graph_id': 20, 'domain': None, 'is_main_graphic': 0},  # 21
            {'exercise_id': 2, 'graph_id': 21, 'domain': None, 'is_main_graphic': 0},  # 22

            {'exercise_id': 3, 'graph_id': 1, 'domain': None, 'is_main_graphic': 1},  # 23

            {'exercise_id': 4, 'graph_id': 22, 'domain': None, 'is_main_graphic': 1},  # 24
            {'exercise_id': 4, 'graph_id': 23, 'domain': None, 'is_main_graphic': 0},  # 25
            {'exercise_id': 4, 'graph_id': 24, 'domain': None, 'is_main_graphic': 0},  # 26

            {'exercise_id': 5, 'graph_id': 23, 'domain': None, 'is_main_graphic': 1},  # 27
            {'exercise_id': 5, 'graph_id': 22, 'domain': None, 'is_main_graphic': 0},  # 28
            {'exercise_id': 5, 'graph_id': 2, 'domain': None, 'is_main_graphic': 0},  # 29

            {'exercise_id': 6, 'graph_id': 5, 'domain': None, 'is_main_graphic': 1},  # 29
            {'exercise_id': 6, 'graph_id': 2, 'domain': None, 'is_main_graphic': 0},  # 30
            {'exercise_id': 6, 'graph_id': 25, 'domain': None, 'is_main_graphic': 0},  # 31

            {'exercise_id': 7, 'graph_id': 26, 'domain': None, 'is_main_graphic': 1},  # 29
            {'exercise_id': 7, 'graph_id': 27, 'domain': None, 'is_main_graphic': 0},  # 30
            {'exercise_id': 7, 'graph_id': 28, 'domain': None, 'is_main_graphic': 0},  # 31

            {'exercise_id': 8, 'graph_id': 11, 'domain': None, 'is_main_graphic': 1},  # 32

            {'exercise_id': 9, 'graph_id': 18, 'domain': None, 'is_main_graphic': 1},  # 33

            {'exercise_id': 10, 'graph_id': 29, 'domain': None, 'is_main_graphic': 1},  # 33

            {'exercise_id': 11, 'graph_id': 30, 'domain': None, 'is_main_graphic': 1},  # 34

            {'exercise_id': 12, 'graph_id': 9, 'domain': None, 'is_main_graphic': 1},  # 29
            {'exercise_id': 12, 'graph_id': 31, 'domain': None, 'is_main_graphic': 0},  # 30
            {'exercise_id': 12, 'graph_id': 32, 'domain': None, 'is_main_graphic': 0},  # 31

            {'exercise_id': 13, 'graph_id': 33, 'domain': None, 'is_main_graphic': 1},  # 32
            {'exercise_id': 13, 'graph_id': 34, 'domain': None, 'is_main_graphic': 0},  # 33
            {'exercise_id': 13, 'graph_id': 35, 'domain': None, 'is_main_graphic': 0},  # 34

            {'exercise_id': 14, 'graph_id': 36, 'domain': None, 'is_main_graphic': 1},  # 35

            {'exercise_id': 15, 'graph_id': 37, 'domain': None, 'is_main_graphic': 1},  # 36

            {'exercise_id': 16, 'graph_id': 38, 'domain': None, 'is_main_graphic': 1},  # 37
            {'exercise_id': 16, 'graph_id': 39, 'domain': None, 'is_main_graphic': 0},  # 38
            {'exercise_id': 16, 'graph_id': 26, 'domain': None, 'is_main_graphic': 0},  # 39

            {'exercise_id': 17, 'graph_id': 40, 'domain': None, 'is_main_graphic': 1},  # 40
            {'exercise_id': 17, 'graph_id': 41, 'domain': None, 'is_main_graphic': 0},  # 41
            {'exercise_id': 17, 'graph_id': 1, 'domain': None, 'is_main_graphic': 0},  # 42

            {'exercise_id': 18, 'graph_id': 42, 'domain': None, 'is_main_graphic': 1},  # 43

            {'exercise_id': 19, 'graph_id': 43, 'domain': None, 'is_main_graphic': 1},  # 44

            {'exercise_id': 20, 'graph_id': 44, 'domain': None, 'is_main_graphic': 1},  # 45
            {'exercise_id': 20, 'graph_id': 28, 'domain': None, 'is_main_graphic': 0},  # 46
            {'exercise_id': 20, 'graph_id': 9, 'domain': None, 'is_main_graphic': 0},  # 47

            # DomainExercises
            {'exercise_id': 21, 'graph_id': 45, 'domain': '[-4, -2)', 'is_main_graphic': 1},  # 47
            {'exercise_id': 21, 'graph_id': 46, 'domain': '[-2, 0)', 'is_main_graphic': 1},  # 47
            {'exercise_id': 21, 'graph_id': 47, 'domain': '[0, 2]', 'is_main_graphic': 1},  # 47
            {'exercise_id': 21, 'graph_id': 45, 'domain': '(2, +inf)', 'is_main_graphic': 1},  # 47

            # Maximum exercises
            {'exercise_id': 22, 'graph_id': 45, 'domain': '[-4, -2)', 'is_main_graphic': 1},  # 47
            {'exercise_id': 22, 'graph_id': 46, 'domain': '[-2, 0)', 'is_main_graphic': 1},  # 47
            {'exercise_id': 22, 'graph_id': 47, 'domain': '[0, 2]', 'is_main_graphic': 1},  # 47
            {'exercise_id': 22, 'graph_id': 45, 'domain': '(2, +inf)', 'is_main_graphic': 1},  # 47

            # DomainExercises
            {'exercise_id': 23, 'graph_id': 49, 'domain': '[-3, -2)', 'is_main_graphic': 1},  # 47
            {'exercise_id': 23, 'graph_id': 49, 'domain': '(-2, 2)', 'is_main_graphic': 1},  # 47
            {'exercise_id': 23, 'graph_id': 49, 'domain': '(2, +inf)', 'is_main_graphic': 1},  # 47
            {'exercise_id': 24, 'graph_id': 49, 'domain': '(-3, 0]', 'is_main_graphic': 1},  # 47
            {'exercise_id': 24, 'graph_id': 48, 'domain': '(0, +inf)', 'is_main_graphic': 1},  # 47
            {'exercise_id': 25, 'graph_id': 49, 'domain': '(-3, 0]', 'is_main_graphic': 1},  # 47
            {'exercise_id': 25, 'graph_id': 48, 'domain': '(2, +inf)', 'is_main_graphic': 1},  # 47
            {'exercise_id': 26, 'graph_id': 50, 'domain': '(-inf, 2]', 'is_main_graphic': 1},  # 47
            {'exercise_id': 26, 'graph_id': 51, 'domain': '(2, 4]', 'is_main_graphic': 1},  # 47
            {'exercise_id': 27, 'graph_id': 52, 'domain': '(-2, 1]', 'is_main_graphic': 1},  # 47
            {'exercise_id': 27, 'graph_id': 51, 'domain': '(2, 3]', 'is_main_graphic': 1},  # 47
            {'exercise_id': 28, 'graph_id': 53, 'domain': '(-1, 2]', 'is_main_graphic': 1},  # 47
            {'exercise_id': 28, 'graph_id': 54, 'domain': '[4, 5)', 'is_main_graphic': 1},  # 47
            {'exercise_id': 28, 'graph_id': 55, 'domain': '(3, 4)', 'is_main_graphic': 1},  # 47
            {'exercise_id': 29, 'graph_id': 55, 'domain': '[3, 4)', 'is_main_graphic': 1},  # 47
            {'exercise_id': 29, 'graph_id': 54, 'domain': '(4, 5]', 'is_main_graphic': 1},  # 47
            {'exercise_id': 30, 'graph_id': 53, 'domain': '[-2, 2]', 'is_main_graphic': 1},  # 47
            {'exercise_id': 30, 'graph_id': 55, 'domain': '(4, 5)', 'is_main_graphic': 1},  # 47
            {'exercise_id': 31, 'graph_id': 48, 'domain': '(-inf, +inf)', 'is_main_graphic': 1},  # 47
            {'exercise_id': 32, 'graph_id': 56, 'domain': '(-inf, -2)', 'is_main_graphic': 1},  # 47
            {'exercise_id': 32, 'graph_id': 57, 'domain': '(-2, 2)', 'is_main_graphic': 1},  # 47
            {'exercise_id': 33, 'graph_id': 56, 'domain': '(-inf, -4)', 'is_main_graphic': 1},  # 47
            {'exercise_id': 33, 'graph_id': 57, 'domain': '[-2, 4]', 'is_main_graphic': 1},  # 47
            {'exercise_id': 34, 'graph_id': 56, 'domain': '(-inf, -4)', 'is_main_graphic': 1},  # 47
            {'exercise_id': 34, 'graph_id': 57, 'domain': '[-2, 0)', 'is_main_graphic': 1},  # 47
            {'exercise_id': 34, 'graph_id': 58, 'domain': '[0, 3)', 'is_main_graphic': 1},  # 47
            {'exercise_id': 35, 'graph_id': 59, 'domain': '(-inf, +inf)', 'is_main_graphic': 1},  # 47
            {'exercise_id': 36, 'graph_id': 60, 'domain': '(-inf, 1)', 'is_main_graphic': 1},  # 47
            {'exercise_id': 37, 'graph_id': 48, 'domain': '(-inf, 1]', 'is_main_graphic': 1},  # 47
            {'exercise_id': 38, 'graph_id': 61, 'domain': '(-inf, -2)', 'is_main_graphic': 1},  # 47
            {'exercise_id': 38, 'graph_id': 60, 'domain': '[0, 1)', 'is_main_graphic': 1},  # 47
            {'exercise_id': 38, 'graph_id': 59, 'domain': '(1, +inf)', 'is_main_graphic': 1},  # 47
            {'exercise_id': 39, 'graph_id': 61, 'domain': '(-inf, -2]', 'is_main_graphic': 1},  # 47
            {'exercise_id': 39, 'graph_id': 60, 'domain': '(0, 1)', 'is_main_graphic': 1},  # 47
            {'exercise_id': 39, 'graph_id': 59, 'domain': '(1, 3)', 'is_main_graphic': 1},   # 47
            {'exercise_id': 40, 'graph_id': 61, 'domain': '(-inf, -2]', 'is_main_graphic': 1},  # 47
            {'exercise_id': 40, 'graph_id': 60, 'domain': '(0, 1)', 'is_main_graphic': 1},  # 47
            {'exercise_id': 40, 'graph_id': 59, 'domain': '[1, +inf)', 'is_main_graphic': 1},  # 47

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

    def _setup_exercise_graph_points_data(self):
        self._create_exercise_graph_points_table()
        self._populate_exercise_graph_points_data()

    @staticmethod
    def _create_exercise_graph_points_table():
        sql_query = QSqlQuery()
        sql_query.exec(
            """
            CREATE TABLE exercise_graph_points (
                id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
                exercise_id INT NOT NULL,
                x_value INT NOT NULL,
                y_value INT NOT NULL,
                is_included INT,
                FOREIGN KEY (exercise_id) REFERENCES exercises(id)
                )
            """
        )

    @staticmethod
    def _populate_exercise_graph_points_data():
        exercise_graph_point_seed = [
            # Points
            {'exercise_id': 22, 'x_value': 4, 'y_value': 0, 'is_included': 1},  # 1
            {'exercise_id': 22, 'x_value': 4, 'y_value': 4, 'is_included': 0},  # 2
        ]

        sql_query = QSqlQuery()
        sql_query.prepare(
            """
            INSERT INTO exercise_graph_points (exercise_id, x_value, y_value, is_included) VALUES (?, ?, ?, ?)
            """
        )

        for exercise_graph_point in exercise_graph_point_seed:
            sql_query.addBindValue(exercise_graph_point['exercise_id'])
            sql_query.addBindValue(exercise_graph_point['x_value'])
            sql_query.addBindValue(exercise_graph_point['y_value'])
            sql_query.addBindValue(exercise_graph_point['is_included'])
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
