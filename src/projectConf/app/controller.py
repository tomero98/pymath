from .py_math_app import PyMathApp
from ..models import Topic
from ..views import WelcomePage, TopicPage
from ...function.views import FunctionExercisePage


class Controller:
    def __init__(self):
        self._app = None
        self._current_view = None

    def run(self):
        self._init_app()
        self._start_app_flow()
        self._execute_app()

    def _init_app(self):
        self._app = PyMathApp(sys_argv=[])

    def _start_app_flow(self):
        self._setup_front_page()

    def _setup_front_page(self):
        front_page = WelcomePage()
        front_page.draw()
        self._current_view = front_page
        self._current_view.continue_signal.connect(self._setup_subtopic_page)
        self._current_view.close_signal.connect(self._close_page)

    def _setup_topic_page(self):
        topic_page = TopicPage()
        topic_page.draw()
        self._current_view = topic_page
        self._current_view.close_signal.connect(self._close_page)
        self._current_view.continue_signal.connect(self._setup_subtopic_page)

    def _setup_subtopic_page(self):
        topic = Topic(identifier=1, title='Funciones', description='Ejercicios sobre funciones', topic_parent_id=None)
        topic_page = TopicPage(topic=topic)
        topic_page.draw()
        self._current_view = topic_page
        self._current_view.close_signal.connect(self._close_page)
        self._current_view.continue_signal.connect(self._setup_exercise_page)
        self._current_view.back_signal.connect(self._setup_topic_page)

    def _setup_exercise_page(self, subtopic: Topic):
        exercise_page = FunctionExercisePage(subtopic=subtopic)
        exercise_page.draw()
        exercise_page.back_signal.connect(self._back_page)
        self._current_view = exercise_page

    def _close_page(self):
        self._current_view.close()

    def _back_page(self):
        self._current_view.close()
        self._setup_subtopic_page()

    def _execute_app(self):
        self._app.exec()
